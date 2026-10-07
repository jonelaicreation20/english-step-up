#!/usr/bin/env python3
"""
English Step-Up server: student accounts, saved progress and a teacher dashboard.

    python server.py                            start the website (http://localhost:5500)
    python server.py --reset-teacher-password   forget the teacher password so a new one can be set

Uses only the Python standard library. All data is stored in data/english-step-up.db (SQLite).
"""

import csv
import hashlib
import hmac
import io
import json
import os
import re
import secrets
import socket
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import db

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(ROOT, "public")

PORT = int(os.environ.get("PORT", "5500"))

# Optional settings, used when the site is online (set these on Render).
# TEACHER_PASSWORD: fixes the teacher password, so nobody else can claim the dashboard.
# CLASS_CODE: a word your students must type to make an account, so strangers cannot.
TEACHER_PASSWORD = os.environ.get("TEACHER_PASSWORD", "").strip()
CLASS_CODE = os.environ.get("CLASS_CODE", "").strip()
LESSON_COUNT = 10
PASS_PERCENT = 70
SESSION_SECONDS = 60 * 24 * 3600  # stay logged in for 60 days
MAX_BODY_BYTES = 64 * 1024

NAME_RE = re.compile(r"^[^\W_][\w .'-]{1,39}$")
PIN_RE = re.compile(r"^\d{4}$")

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
  id          INTEGER PRIMARY KEY,
  name        TEXT NOT NULL,
  name_key    TEXT NOT NULL UNIQUE,
  pin_hash    TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  last_active TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
  token      TEXT PRIMARY KEY,
  student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,  -- NULL for the teacher
  is_teacher INTEGER NOT NULL DEFAULT 0,
  created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS attempts (
  id         INTEGER PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  lesson_id  INTEGER NOT NULL,
  correct    INTEGER NOT NULL,
  total      INTEGER NOT NULL,
  answers    TEXT NOT NULL,  -- JSON list, true = right on the first try
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS completions (
  student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  lesson_id    INTEGER NOT NULL,
  completed_at TEXT NOT NULL,
  PRIMARY KEY (student_id, lesson_id)
);

CREATE TABLE IF NOT EXISTS settings (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS attempts_by_student ON attempts(student_id, lesson_id);
"""


# ---------------------------------------------------------------- helpers

class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def local_time(iso):
    if not iso:
        return ""
    return datetime.fromisoformat(iso).astimezone().strftime("%Y-%m-%d %H:%M")


def connect():
    return db.connect()


def hash_secret(secret, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", secret.encode(), bytes.fromhex(salt), 200_000)
    return f"{salt}${digest.hex()}"


def check_secret(secret, stored):
    salt = stored.split("$", 1)[0]
    return hmac.compare_digest(hash_secret(secret, salt), stored)


def clean_name(value):
    name = " ".join(str(value or "").split())
    if not NAME_RE.match(name):
        raise ApiError(400, "Please type your name using letters (2 to 40 characters).")
    return name


def clean_pin(value):
    pin = str(value or "").strip()
    if not PIN_RE.match(pin):
        raise ApiError(400, "Your PIN must be exactly 4 numbers.")
    return pin


def lesson_id_from(value):
    try:
        lesson_id = int(value)
    except (TypeError, ValueError):
        raise ApiError(400, "Unknown lesson.")
    if not 1 <= lesson_id <= LESSON_COUNT:
        raise ApiError(400, "Unknown lesson.")
    return lesson_id


def percent(correct, total):
    return round(correct * 100 / total) if total else 0


# Slow down people guessing PINs or the teacher password.
_failures = {}
_failures_lock = threading.Lock()
FAIL_LIMIT = 8
FAIL_WINDOW_SECONDS = 600


def check_not_locked(key):
    with _failures_lock:
        recent = [t for t in _failures.get(key, []) if time.time() - t < FAIL_WINDOW_SECONDS]
        _failures[key] = recent
        if len(recent) >= FAIL_LIMIT:
            raise ApiError(429, "Too many wrong tries. Please wait 10 minutes or ask your teacher.")


def record_failure(key):
    with _failures_lock:
        _failures.setdefault(key, []).append(time.time())


def clear_failures(key):
    with _failures_lock:
        _failures.pop(key, None)


# ---------------------------------------------------------------- data access

def create_session(conn, student_id=None, is_teacher=False):
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sessions (token, student_id, is_teacher, created_at) VALUES (?, ?, ?, ?)",
        (token, student_id, 1 if is_teacher else 0, time.time()),
    )
    return token


def find_session(conn, token):
    if not token:
        return None
    return conn.execute(
        "SELECT * FROM sessions WHERE token = ? AND created_at > ?",
        (token, time.time() - SESSION_SECONDS),
    ).fetchone()


def best_scores(rows):
    """Pick the best attempt per lesson from attempt rows."""
    best = {}
    for row in rows:
        current = best.get(row["lesson_id"])
        if current is None or row["correct"] * current["total"] > current["correct"] * row["total"]:
            best[row["lesson_id"]] = {"correct": row["correct"], "total": row["total"]}
    return best


def student_progress(conn, student_id):
    completed = [
        row["lesson_id"]
        for row in conn.execute(
            "SELECT lesson_id FROM completions WHERE student_id = ? ORDER BY lesson_id", (student_id,)
        )
    ]
    rows = conn.execute(
        "SELECT lesson_id, correct, total FROM attempts WHERE student_id = ?", (student_id,)
    ).fetchall()
    return {"completed": completed, "best": {str(k): v for k, v in best_scores(rows).items()}}


def touch_student(conn, student_id):
    conn.execute("UPDATE students SET last_active = ? WHERE id = ?", (now_iso(), student_id))


def get_setting(conn, key):
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else None


def set_setting(conn, key, value):
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )


def class_overview(conn):
    """Everything the teacher dashboard needs in one go."""
    students = {
        row["id"]: {
            "id": row["id"],
            "name": row["name"],
            "createdAt": row["created_at"],
            "lastActive": row["last_active"],
            "completed": [],
            "lessons": {},
        }
        for row in conn.execute("SELECT * FROM students ORDER BY LOWER(name)")
    }

    for row in conn.execute("SELECT * FROM completions ORDER BY lesson_id"):
        if row["student_id"] in students:
            students[row["student_id"]]["completed"].append(row["lesson_id"])

    lesson_stats = {}
    for row in conn.execute("SELECT * FROM attempts ORDER BY created_at"):
        student = students.get(row["student_id"])
        if not student:
            continue

        info = student["lessons"].setdefault(
            str(row["lesson_id"]), {"correct": 0, "total": 0, "percent": -1, "attempts": 0, "lastAt": None}
        )
        info["attempts"] += 1
        info["lastAt"] = row["created_at"]
        row_percent = percent(row["correct"], row["total"])
        if row_percent > info["percent"]:
            info.update(correct=row["correct"], total=row["total"], percent=row_percent)

        stats = lesson_stats.setdefault(str(row["lesson_id"]), {"attempts": 0, "right": [], "seen": []})
        stats["attempts"] += 1
        for i, right in enumerate(json.loads(row["answers"])):
            while len(stats["right"]) <= i:
                stats["right"].append(0)
                stats["seen"].append(0)
            stats["seen"][i] += 1
            stats["right"][i] += 1 if right else 0

    return {"students": list(students.values()), "lessonStats": lesson_stats, "passPercent": PASS_PERCENT}


# ---------------------------------------------------------------- API routes

ROUTES = []


def route(method, pattern, auth=None):
    """auth: None (anyone), "student", "teacher" or "any" (logged in)."""
    def register(fn):
        ROUTES.append((method, re.compile("^" + pattern + "$"), fn, auth))
        return fn
    return register


@route("POST", "/api/signup")
def signup(ctx):
    if CLASS_CODE and not hmac.compare_digest(str(ctx.body.get("classCode") or "").strip().lower(),
                                              CLASS_CODE.lower()):
        raise ApiError(403, "That class code is not right. Ask your teacher for today's class code.")

    name = clean_name(ctx.body.get("name"))
    pin = clean_pin(ctx.body.get("pin"))
    key = name.lower()

    if ctx.conn.execute("SELECT 1 FROM students WHERE name_key = ?", (key,)).fetchone():
        raise ApiError(409, "That name is already used. If it is you, choose \"I've been here before\". "
                            "If not, add your last name or an initial.")

    student_id = ctx.conn.insert(
        "INSERT INTO students (name, name_key, pin_hash, created_at, last_active) VALUES (?, ?, ?, ?, ?)",
        (name, key, hash_secret(pin), now_iso(), now_iso()),
    )
    token = create_session(ctx.conn, student_id=student_id)
    return {"token": token, "student": {"id": student_id, "name": name},
            "progress": student_progress(ctx.conn, student_id)}


@route("POST", "/api/login")
def login(ctx):
    name = clean_name(ctx.body.get("name"))
    pin = clean_pin(ctx.body.get("pin"))
    lock_key = "student:" + name.lower()
    check_not_locked(lock_key)

    row = ctx.conn.execute("SELECT * FROM students WHERE name_key = ?", (name.lower(),)).fetchone()
    if not row or not check_secret(pin, row["pin_hash"]):
        record_failure(lock_key)
        raise ApiError(400, "That name and PIN do not match. Check your spelling and try again.")

    clear_failures(lock_key)
    touch_student(ctx.conn, row["id"])
    token = create_session(ctx.conn, student_id=row["id"])
    return {"token": token, "student": {"id": row["id"], "name": row["name"]},
            "progress": student_progress(ctx.conn, row["id"])}


@route("POST", "/api/logout", auth="any")
def logout(ctx):
    ctx.conn.execute("DELETE FROM sessions WHERE token = ?", (ctx.session["token"],))
    return {"ok": True}


@route("GET", "/api/me", auth="student")
def me(ctx):
    student_id = ctx.session["student_id"]
    row = ctx.conn.execute("SELECT id, name FROM students WHERE id = ?", (student_id,)).fetchone()
    touch_student(ctx.conn, student_id)
    return {"student": {"id": row["id"], "name": row["name"]}, "progress": student_progress(ctx.conn, student_id)}


@route("POST", "/api/attempts", auth="student")
def save_attempt(ctx):
    lesson_id = lesson_id_from(ctx.body.get("lessonId"))
    answers = ctx.body.get("answers")
    if not isinstance(answers, list) or not 1 <= len(answers) <= 50:
        raise ApiError(400, "Missing answers.")
    answers = [bool(a) for a in answers]

    student_id = ctx.session["student_id"]
    ctx.conn.execute(
        "INSERT INTO attempts (student_id, lesson_id, correct, total, answers, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, lesson_id, sum(answers), len(answers), json.dumps(answers), now_iso()),
    )
    touch_student(ctx.conn, student_id)
    return {"progress": student_progress(ctx.conn, student_id)}


@route("POST", "/api/complete", auth="student")
def complete_lesson(ctx):
    lesson_id = lesson_id_from(ctx.body.get("lessonId"))
    student_id = ctx.session["student_id"]

    rows = ctx.conn.execute(
        "SELECT lesson_id, correct, total FROM attempts WHERE student_id = ? AND lesson_id = ?",
        (student_id, lesson_id),
    ).fetchall()
    best = best_scores(rows).get(lesson_id)
    if not best or percent(best["correct"], best["total"]) < PASS_PERCENT:
        raise ApiError(400, f"You need at least {PASS_PERCENT}% in Practice to finish this lesson.")

    ctx.conn.execute(
        "INSERT INTO completions (student_id, lesson_id, completed_at) VALUES (?, ?, ?) "
        "ON CONFLICT DO NOTHING",
        (student_id, lesson_id, now_iso()),
    )
    touch_student(ctx.conn, student_id)
    return {"progress": student_progress(ctx.conn, student_id)}


# ----- teacher

@route("GET", "/api/config")
def site_config(ctx):
    """What the student page needs to know before anyone logs in."""
    return {"requiresClassCode": bool(CLASS_CODE)}


@route("GET", "/api/teacher/status")
def teacher_status(ctx):
    return {"hasPassword": bool(TEACHER_PASSWORD) or get_setting(ctx.conn, "teacher_password") is not None}


def check_new_password(value):
    password = str(value or "")
    if len(password) < 6:
        raise ApiError(400, "The password must have at least 6 characters.")
    return password


@route("POST", "/api/teacher/setup")
def teacher_setup(ctx):
    if TEACHER_PASSWORD:
        raise ApiError(409, "The teacher password is set on the server. Please log in with it.")
    if get_setting(ctx.conn, "teacher_password") is not None:
        raise ApiError(409, "A teacher password already exists. Please log in.")
    password = check_new_password(ctx.body.get("password"))
    set_setting(ctx.conn, "teacher_password", hash_secret(password))
    return {"token": create_session(ctx.conn, is_teacher=True)}


@route("POST", "/api/teacher/login")
def teacher_login(ctx):
    check_not_locked("teacher")
    given = str(ctx.body.get("password") or "")
    stored = get_setting(ctx.conn, "teacher_password")

    if TEACHER_PASSWORD:
        correct = hmac.compare_digest(given, TEACHER_PASSWORD)
    elif stored is None:
        raise ApiError(409, "No teacher password yet. Please create one.")
    else:
        correct = check_secret(given, stored)

    if not correct:
        record_failure("teacher")
        raise ApiError(400, "Wrong password.")
    clear_failures("teacher")
    return {"token": create_session(ctx.conn, is_teacher=True)}


@route("POST", "/api/teacher/password", auth="teacher")
def teacher_change_password(ctx):
    if TEACHER_PASSWORD:
        raise ApiError(400, "This password is set on the server. Change it there (the TEACHER_PASSWORD setting).")
    stored = get_setting(ctx.conn, "teacher_password")
    if not check_secret(str(ctx.body.get("current") or ""), stored):
        raise ApiError(400, "Your current password is not right.")
    set_setting(ctx.conn, "teacher_password", hash_secret(check_new_password(ctx.body.get("new"))))
    ctx.conn.execute("DELETE FROM sessions WHERE is_teacher = 1 AND token != ?", (ctx.session["token"],))
    return {"ok": True}


@route("GET", "/api/teacher/overview", auth="teacher")
def teacher_overview(ctx):
    return class_overview(ctx.conn)


def find_student(conn, student_id):
    row = conn.execute("SELECT * FROM students WHERE id = ?", (int(student_id),)).fetchone()
    if not row:
        raise ApiError(404, "Student not found.")
    return row


@route("GET", r"/api/teacher/students/(\d+)", auth="teacher")
def teacher_student(ctx):
    row = find_student(ctx.conn, ctx.params[0])
    attempts = [
        {
            "lessonId": a["lesson_id"],
            "correct": a["correct"],
            "total": a["total"],
            "answers": json.loads(a["answers"]),
            "createdAt": a["created_at"],
        }
        for a in ctx.conn.execute(
            "SELECT * FROM attempts WHERE student_id = ? ORDER BY created_at DESC, id DESC", (row["id"],)
        )
    ]
    return {
        "student": {"id": row["id"], "name": row["name"], "createdAt": row["created_at"],
                    "lastActive": row["last_active"]},
        "attempts": attempts,
    }


@route("POST", r"/api/teacher/students/(\d+)/pin", auth="teacher")
def teacher_reset_pin(ctx):
    row = find_student(ctx.conn, ctx.params[0])
    pin = clean_pin(ctx.body.get("pin"))
    ctx.conn.execute("UPDATE students SET pin_hash = ? WHERE id = ?", (hash_secret(pin), row["id"]))
    ctx.conn.execute("DELETE FROM sessions WHERE student_id = ?", (row["id"],))
    clear_failures("student:" + row["name_key"])
    return {"ok": True}


@route("DELETE", r"/api/teacher/students/(\d+)", auth="teacher")
def teacher_delete_student(ctx):
    row = find_student(ctx.conn, ctx.params[0])
    ctx.conn.execute("DELETE FROM students WHERE id = ?", (row["id"],))
    return {"ok": True}


@route("GET", "/api/teacher/export", auth="teacher")
def teacher_export(ctx):
    kind = (ctx.query.get("type") or ["summary"])[0]
    out = io.StringIO()
    writer = csv.writer(out)
    stamp = datetime.now().strftime("%Y-%m-%d")

    if kind == "attempts":
        max_questions = ctx.conn.execute("SELECT COALESCE(MAX(total), 0) AS n FROM attempts").fetchone()["n"]
        writer.writerow(["Student", "Lesson", "Date", "Correct", "Questions", "Score %", "Passed"]
                        + [f"Q{i + 1}" for i in range(max_questions)])
        rows = ctx.conn.execute(
            "SELECT s.name, a.* FROM attempts a JOIN students s ON s.id = a.student_id "
            "ORDER BY LOWER(s.name), a.lesson_id, a.created_at"
        )
        for row in rows:
            answers = json.loads(row["answers"])
            score = percent(row["correct"], row["total"])
            writer.writerow([row["name"], row["lesson_id"], local_time(row["created_at"]), row["correct"],
                             row["total"], score, "Yes" if score >= PASS_PERCENT else "No"]
                            + ["Right" if a else "Wrong" for a in answers])
        filename = f"english-step-up-all-attempts-{stamp}.csv"
    else:
        overview = class_overview(ctx.conn)
        writer.writerow(["Student", "Lessons completed", "Completed lessons", "Average best score %",
                         "Joined", "Last active"]
                        + [f"Lesson {i} best %" for i in range(1, LESSON_COUNT + 1)])
        for s in overview["students"]:
            scores = [s["lessons"][k]["percent"] for k in s["lessons"]]
            writer.writerow([
                s["name"],
                len(s["completed"]),
                ", ".join(str(n) for n in s["completed"]),
                round(sum(scores) / len(scores)) if scores else "",
                local_time(s["createdAt"]),
                local_time(s["lastActive"]),
            ] + [s["lessons"].get(str(i), {}).get("percent", "") for i in range(1, LESSON_COUNT + 1)])
        filename = f"english-step-up-class-summary-{stamp}.csv"

    # The BOM makes Excel read the file as UTF-8 so names with accents look right.
    return ("text/csv; charset=utf-8", filename, ("﻿" + out.getvalue()).encode("utf-8"))


# ---------------------------------------------------------------- HTTP handler

class Context:
    def __init__(self, conn, body, query, params, session):
        self.conn = conn
        self.body = body
        self.query = query
        self.params = params
        self.session = session


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".json": "application/json",
        ".svg": "image/svg+xml",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "/api/" in (self.path or "") or (len(args) > 1 and str(args[1]).startswith(("4", "5"))):
            super().log_message(fmt, *args)

    def do_GET(self):
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            return self.handle_api("GET")
        if path in ("/teacher", "/teacher/"):
            self.path = "/teacher.html"
        return super().do_GET()

    def do_POST(self):
        self.handle_api("POST")

    def do_DELETE(self):
        self.handle_api("DELETE")

    def send_body(self, status, content_type, body, filename=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, data):
        self.send_body(status, "application/json; charset=utf-8", json.dumps(data).encode("utf-8"))

    def read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY_BYTES:
            raise ApiError(413, "Request too large.")
        if not length:
            return {}
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise ApiError(400, "Invalid request.")
        if not isinstance(data, dict):
            raise ApiError(400, "Invalid request.")
        return data

    def handle_api(self, method):
        parsed = urlparse(self.path)
        conn = None
        try:
            for route_method, pattern, fn, auth in ROUTES:
                match = pattern.match(parsed.path)
                if not match or route_method != method:
                    continue

                body = self.read_body() if method == "POST" else {}
                conn = connect()

                header = self.headers.get("Authorization", "")
                token = header[7:].strip() if header.startswith("Bearer ") else ""
                session = find_session(conn, token)

                if auth and not session:
                    raise ApiError(401, "Please log in again.")
                if auth == "student" and not session["student_id"]:
                    raise ApiError(401, "Please log in as a student.")
                if auth == "teacher" and not session["is_teacher"]:
                    raise ApiError(401, "Please log in as the teacher.")

                result = fn(Context(conn, body, parse_qs(parsed.query), match.groups(), session))
                conn.commit()

                if isinstance(result, tuple):
                    content_type, filename, data = result
                    return self.send_body(200, content_type, data, filename)
                return self.send_json(200, result)

            raise ApiError(404, "Not found.")
        except ApiError as err:
            if conn:
                conn.rollback()
            self.send_json(err.status, {"error": err.message})
        except Exception as err:  # keep the server running whatever happens
            if conn:
                conn.rollback()
            self.log_error("Unexpected error: %r", err)
            self.send_json(500, {"error": "Something went wrong on the server. Please try again."})
        finally:
            if conn:
                conn.close()


# ---------------------------------------------------------------- start

def lan_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
    except OSError:
        return None


def main():
    db.init(SCHEMA)

    if "--reset-teacher-password" in sys.argv:
        conn = connect()
        conn.execute("DELETE FROM settings WHERE key = 'teacher_password'")
        conn.execute("DELETE FROM sessions WHERE is_teacher = 1")
        conn.commit()
        conn.close()
        print("Teacher password removed. Open the teacher page to create a new one.")
        return

    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    lan = lan_address()

    print("\n  English Step-Up is running!\n")
    print(f"  Students (this computer):  http://localhost:{PORT}")
    if lan:
        print(f"  Students (same Wi-Fi):     http://{lan}:{PORT}")
    print(f"  Teacher dashboard:         http://localhost:{PORT}/teacher")
    print(f"\n  Saving data in: {db.describe()}")
    if CLASS_CODE:
        print("  Students need the class code to make an account.")
    if TEACHER_PASSWORD:
        print("  Teacher password comes from the TEACHER_PASSWORD setting.")
    print("\n  Keep this window open. Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()

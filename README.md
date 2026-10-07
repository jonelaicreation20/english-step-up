# English Step-Up

A friendly English learning website for young learners (Grade 3 foundations → Grade 7 readiness).
Works on computers and phones.

- **10 foundation lessons**: Learn → Examples → Practice → Review
- **Read aloud** with a clear female voice (uses the browser's built-in voices; best in Microsoft Edge)
- **Student accounts** with name + 4-digit PIN, saved progress and stars
- **Teacher dashboard** with every student's scores, the hardest questions, PIN reset, and **Download for Excel** (CSV)

## Run it

Needs [Python 3](https://www.python.org/downloads/) — no other installs.

Double-click **`START WEBSITE.bat`** (Windows), or run:

```
python server.py
```

| Page | Address |
| --- | --- |
| Students | http://localhost:5500 |
| Teacher dashboard | http://localhost:5500/teacher |

Students on the same Wi-Fi can use the computer's network address shown in the server window.
The first time you open the teacher dashboard, you create the teacher password.

Forgot the teacher password? Run `python server.py --reset-teacher-password`.

## Files

| Path | What it is |
| --- | --- |
| `public/lessons.js` | Lesson content (explanations, examples, questions) |
| `public/index.html` | Student website |
| `public/teacher.html` | Teacher dashboard |
| `server.py` | Server: accounts, saved scores, Excel export |
| `data/` | Student database — created when the server runs, **not** uploaded to GitHub. Back it up. |

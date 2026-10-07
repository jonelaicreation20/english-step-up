@echo off
title English Step-Up
cd /d "%~dp0"
start "" http://localhost:5500
python server.py
pause

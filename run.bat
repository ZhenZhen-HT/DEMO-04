@echo off
setlocal

echo [1/3] Kiem tra moi truong ao (venv)...
if not exist venv (
    echo [+] Dang tao venv moi...
    python -m venv venv
)

echo [2/3] Kich hoat moi truong va cai dat thu vien...
call venv\Scripts\activate
pip install -q -r requirements.txt

echo [3/3] Dang chuan bi khoi chay...

:: Kiem tra neu nguoi dung muon chay test
if "%1"=="test" (
    echo [!] Dang chay Unit Tests...
    python -m unittest test_app.py
    goto :end
)

:: Chay ung dung bang Flask CLI
echo ===============================================
echo Ung dung dang san sang tai: http://127.0.0.1:5001
echo Bam Ctrl+C de dung ung dung.
echo ===============================================
flask run --host=0.0.0.0

:end
pause
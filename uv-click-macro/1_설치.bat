@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 필요한 프로그램을 설치합니다 (처음 한 번만)...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo [오류] 파이썬이 설치되어 있지 않은 것 같습니다.
  echo https://www.python.org 에서 설치할 때 "Add python.exe to PATH" 를 꼭 체크하세요.
  pause
  exit /b 1
)
echo.
echo 설치 완료! 이제 "2_실행.bat" 을 더블클릭하세요.
pause

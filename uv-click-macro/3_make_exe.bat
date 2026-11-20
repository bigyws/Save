@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo exe 파일을 만듭니다 (파이썬 없는 PC에 복사해서 쓰기용)...
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name UV-Click-Macro --icon assets\icon.ico --add-data "assets;assets" macro_app.py
echo.
echo 완료: dist\UV-Click-Macro.exe
pause

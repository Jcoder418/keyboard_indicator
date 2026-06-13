@echo off
REM Se placer dans le dossier du script (important!)
cd /d "%~dp0"

echo [1/3] Installation des dependances...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/3] Generation de l'icone...
python generate_icon.py

echo.
echo [3/3] Compilation PyInstaller...
python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name "KeyIndicator" ^
  --icon "assets\icon.ico" ^
  main.py

echo.
echo Termine !
echo Le fichier EXE se trouve dans : %~dp0dist\KeyIndicator.exe
echo.
pause
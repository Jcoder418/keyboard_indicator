# 🟢 KeyIndicator — Keyboard Indicator Lights in the Windows 11 Taskbar
 
A small utility for your **ASUS VivoBook** (or any PC without physical LED indicators).  
Displays **3 colored dots** in the taskbar reflecting the state of:
 
| Dot | Key | Green = ON | Gray = OFF | Yellow = blinking |
|-----|-----|------------|------------|-------------------|
| 🟢 | Num Lock | ● | ○ | ✦ |
| 🟢 | Caps Lock | ● | ○ | ✦ |
| 🟢 | Scroll Lock | ● | ○ | ✦ |
 
---
 
## 📁 Project Structure
 
```
keyboard_indicator/
│
├── main.py                 ← Main application (tray icon + monitoring)
├── generate_icon.py        ← Generates assets/icon.ico (run once)
├── install_autostart.py    ← Adds/removes from Windows startup
├── build.bat               ← Compiles into a standalone .exe (PyInstaller)
├── requirements.txt        ← Python dependencies
│
└── assets/
    └── icon.ico            ← Auto-generated icon
```
 
---
 
## 🚀 Quick Installation
 
### 1 — Prerequisites
 
- Windows 10 / 11
- Python 3.10 or higher → https://python.org/downloads
- Check **"Add Python to PATH"** during installation
### 2 — Install dependencies
 
```bat
pip install -r requirements.txt
```
 
### 3 — Generate the icon
 
```bat
python generate_icon.py
```
 
### 4 — Run directly (without compiling)
 
```bat
pythonw main.py
```
 
> `pythonw` avoids showing a black console window.
 
---
 
## 🔨 Compile to a Standalone .exe
 
```bat
build.bat
```
 
The file `dist\KeyIndicator.exe` is created.  
Double-click → the icon appears in the taskbar.
 
---
 
## 🔁 Auto-start with Windows
 
```bat
REM Enable auto-start
python install_autostart.py
 
REM Disable
python install_autostart.py --remove
```
 
---
 
## 🎨 Color Legend
 
| Color | Meaning |
|-------|---------|
| 🟢 Green | Key **active** (LED would be on) |
| ⚫ Gray | Key **inactive** |
| 🟡 Yellow | Key **rapidly blinking** |
 
---
 
## 🖱️ Context Menu (right-click on the icon)
 
- Shows the current state of all 3 keys
- **Quit** button to close the application
---
 
## ⚙️ Customization
 
Edit the colors in `main.py`:
 
```python
COLOR_ON    = (80, 220, 120)   # Green  → active key
COLOR_OFF   = (55,  55,  60)   # Gray   → inactive key
COLOR_BLINK = (255, 200,  40)  # Yellow → blinking
COLOR_BG    = (22,  22,  26)   # Icon background
```
 
---
 
## 📦 Dependencies
 
| Package | Role |
|---------|------|
| `pystray` | System tray icon |
| `Pillow` | Drawing colored dots (dynamic icon) |
| `pywin32` | Reading Windows key states |
 
---
 
*Tested on Windows 11*

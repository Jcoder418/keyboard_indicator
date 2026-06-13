"""
install_autostart.py
--------------------
Ajoute KeyIndicator au démarrage automatique de Windows
via la clé de registre HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
"""

import sys
import os
import winreg

APP_NAME = "KeyIndicator"
KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def install():
    exe_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "dist", "KeyIndicator.exe")
    )
    if not os.path.isfile(exe_path):
        print(f"[ERREUR] EXE introuvable : {exe_path}")
        print("Lancez d'abord build.bat pour compiler le programme.")
        return

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, KEY_PATH, 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)

    print(f"[OK] KeyIndicator ajouté au démarrage Windows.")
    print(f"     Chemin enregistré : {exe_path}")


def uninstall():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, KEY_PATH, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, APP_NAME)
        print("[OK] KeyIndicator retiré du démarrage Windows.")
    except FileNotFoundError:
        print("[INFO] Entrée introuvable dans le registre (déjà supprimée ?).")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        uninstall()
    else:
        install()

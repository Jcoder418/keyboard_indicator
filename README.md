# 🟢 KeyIndicator — Voyants clavier dans la barre des tâches Windows 11

Petit utilitaire pour votre **ASUS VivoBook** (ou tout PC sans voyants LED physiques).  
Affiche **3 points colorés** dans la barre des tâches qui reflètent l'état de :

| Point | Touche          | Vert = ON | Gris = OFF | Jaune = clignotement |
|-------|-----------------|-----------|------------|----------------------|
| 🟢    | Verr. Num (Num Lock)  | ● | ○ | ✦ |
| 🟢    | Verr. Maj (Caps Lock) | ● | ○ | ✦ |
| 🟢    | Défilement (Scroll Lock) | ● | ○ | ✦ |

---

## 📁 Structure du projet

```
keyboard_indicator/
│
├── main.py                 ← Application principale (tray icon + surveillance)
├── generate_icon.py        ← Génère assets/icon.ico (à lancer 1 fois)
├── install_autostart.py    ← Ajoute/retire du démarrage Windows
├── build.bat               ← Compile en .exe autonome (PyInstaller)
├── requirements.txt        ← Dépendances Python
│
└── assets/
    └── icon.ico            ← Icône générée automatiquement
```

---

## 🚀 Installation rapide

### 1 — Prérequis
- Windows 10 / 11
- Python 3.10 ou supérieur → https://python.org/downloads
- Cocher **"Add Python to PATH"** lors de l'installation

### 2 — Installer les dépendances
```bat
pip install -r requirements.txt
```

### 3 — Générer l'icône
```bat
python generate_icon.py
```

### 4 — Lancer directement (sans compiler)
```bat
pythonw main.py
```
> `pythonw` évite d'afficher une fenêtre console noire.

---

## 🔨 Compiler en .exe autonome

```bat
build.bat
```
Le fichier `dist\KeyIndicator.exe` est créé.  
Double-clic → l'icône apparaît dans la barre des tâches.

---

## 🔁 Démarrage automatique avec Windows

```bat
REM Activer le démarrage auto
python install_autostart.py

REM Désactiver
python install_autostart.py --remove
```

---

## 🎨 Légende des couleurs

| Couleur  | Signification                        |
|----------|--------------------------------------|
| 🟢 Vert  | Touche **active** (LED serait allumée) |
| ⚫ Gris  | Touche **inactive**                  |
| 🟡 Jaune | Touche en **clignotement** rapide    |

---

## 🖱️ Menu contextuel (clic droit sur l'icône)

- Affiche l'état actuel des 3 touches
- Bouton **Quitter** pour fermer l'application

---

## ⚙️ Personnalisation

Modifiez les couleurs dans `main.py` :

```python
COLOR_ON    = (80, 220, 120)   # Vert  → touche active
COLOR_OFF   = (55,  55,  60)   # Gris  → touche inactive  
COLOR_BLINK = (255, 200,  40)  # Jaune → clignotement
COLOR_BG    = (22,  22,  26)   # Fond de l'icône
```

---

## 📦 Dépendances

| Paquet     | Rôle                                      |
|------------|-------------------------------------------|
| `pystray`  | Icône dans la barre des tâches système    |
| `Pillow`   | Dessin des points colorés (icône dynamique)|
| `pywin32`  | Lecture de l'état des touches Windows     |

---

*Testé sur Windows 11 — ASUS VivoBook 15 / 17*

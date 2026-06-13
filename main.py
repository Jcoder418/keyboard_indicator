"""
KeyIndicator - Indicateur de touches clavier pour barre des tâches Windows 11
Surveille: Verr. Num / Verr. Maj / Défilement
"""

import sys
import threading
import ctypes
import time
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

# ── Constantes Windows ──────────────────────────────────────────────────────
VK_NUMLOCK    = 0x90
VK_CAPITAL    = 0x14
VK_SCROLL     = 0x91

# ── Couleurs ─────────────────────────────────────────────────────────────────
COLOR_ON      = (80, 220, 120)   # vert vif  → touche active
COLOR_OFF     = (55,  55,  60)   # gris foncé → touche inactive
COLOR_BLINK   = (255, 200,  40)  # jaune      → clignotement détecté
COLOR_BG      = (22,  22,  26)   # fond icône

# ── Lecture état LED clavier ──────────────────────────────────────────────────
def get_key_state(vk_code: int) -> bool:
    """Retourne True si la touche toggle est active (LED allumée)."""
    return bool(ctypes.WinDLL("user32").GetKeyState(vk_code) & 0x0001)


# ── Dessin de l'icône ─────────────────────────────────────────────────────────
def make_icon(num: bool, caps: bool, scroll: bool,
              num_blink=False, caps_blink=False, scroll_blink=False) -> Image.Image:
    """
    Génère une image 64×64 avec 3 points circulaires colorés.
    Disposition:  [NUM]  [CAPS]  [SCR]
    """
    size = 64
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fond arrondi
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=14, fill=COLOR_BG)

    dots = [
        (num,    num_blink),
        (caps,   caps_blink),
        (scroll, scroll_blink),
    ]

    r      = 8      # rayon du disque
    y_c    = size // 2
    xs     = [14, 32, 50]   # centres X des 3 points

    for (state, blink), x in zip(dots, xs):
        if blink:
            color = COLOR_BLINK
        elif state:
            color = COLOR_ON
        else:
            color = COLOR_OFF

        # Halo léger si actif
        if state or blink:
            halo_color = (*color[:3], 60)
            draw.ellipse([x-r-3, y_c-r-3, x+r+3, y_c+r+3], fill=halo_color)

        draw.ellipse([x-r, y_c-r, x+r, y_c+r], fill=color)

    return img


# ── Application principale ────────────────────────────────────────────────────
class KeyIndicatorApp:
    def __init__(self):
        self.running      = True
        self._blink_state = {"num": False, "caps": False, "scroll": False}
        self._prev_state  = {"num": None,  "caps": None,  "scroll": None}

        # Icône de départ
        img = make_icon(False, False, False)
        menu = pystray.Menu(
            item("🔢 Verr. Num",   self._dummy, enabled=False),
            item("🔠 Verr. Maj",   self._dummy, enabled=False),
            item("↕  Défilement",  self._dummy, enabled=False),
            pystray.Menu.SEPARATOR,
            item("Quitter",        self._quit),
        )

        self.tray = pystray.Icon(
            name   = "KeyIndicator",
            icon   = img,
            title  = "KeyIndicator",
            menu   = menu,
        )

    # ── Callbacks ──────────────────────────────────────────────────────────────
    def _dummy(self, icon, item): pass

    def _quit(self, icon, item):
        self.running = False
        icon.stop()

    # ── Boucle de surveillance ─────────────────────────────────────────────────
    def _monitor(self):
        POLL_MS      = 80          # intervalle d'interrogation (ms)
        BLINK_TICKS  = 6           # nombre de ticks pour considérer un "clignotement"
        blink_cnt    = {"num": 0, "caps": 0, "scroll": 0}

        while self.running:
            num    = get_key_state(VK_NUMLOCK)
            caps   = get_key_state(VK_CAPITAL)
            scroll = get_key_state(VK_SCROLL)

            keys   = {"num": num, "caps": caps, "scroll": scroll}

            # Détection changement rapide → clignotement
            for k, val in keys.items():
                if self._prev_state[k] is not None and val != self._prev_state[k]:
                    blink_cnt[k] += 1
                else:
                    blink_cnt[k] = max(0, blink_cnt[k] - 1)

                self._blink_state[k] = blink_cnt[k] >= BLINK_TICKS
                self._prev_state[k]  = val

            # Mise à jour icône + tooltip
            icon_img = make_icon(
                num,    caps,    scroll,
                self._blink_state["num"],
                self._blink_state["caps"],
                self._blink_state["scroll"],
            )

            tooltip = (
                f"Verr. Num  : {'ON ●' if num    else 'OFF ○'}\n"
                f"Verr. Maj  : {'ON ●' if caps   else 'OFF ○'}\n"
                f"Défilement : {'ON ●' if scroll else 'OFF ○'}"
            )

            self.tray.icon  = icon_img
            self.tray.title = tooltip

            time.sleep(POLL_MS / 1000)

    # ── Lancement ──────────────────────────────────────────────────────────────
    def run(self):
        t = threading.Thread(target=self._monitor, daemon=True)
        t.start()
        self.tray.run()


# ── Point d'entrée ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Masquer la console Windows si lancé en .pyw
    try:
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0
        )
    except Exception:
        pass

    app = KeyIndicatorApp()
    app.run()

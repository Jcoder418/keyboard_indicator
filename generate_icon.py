"""
generate_icon.py
----------------
Génère le fichier assets/icon.ico utilisé par PyInstaller.
Lancez ce script UNE FOIS avant build.bat.
"""

import os
from PIL import Image, ImageDraw

COLOR_ON  = (80, 220, 120)
COLOR_OFF = (55,  55,  60)
COLOR_BG  = (22,  22,  26)


def draw_icon(size: int) -> Image.Image:
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fond arrondi
    r_corner = max(4, size // 6)
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=r_corner, fill=COLOR_BG)

    # 3 points
    r    = max(3, size // 8)
    y_c  = size // 2
    step = size // 4
    xs   = [step, size // 2, size - step]
    colors = [COLOR_ON, COLOR_OFF, COLOR_OFF]   # Num ON par défaut

    for x, col in zip(xs, colors):
        draw.ellipse([x-r, y_c-r, x+r, y_c+r], fill=col)

    return img


def main():
    os.makedirs("assets", exist_ok=True)
    sizes  = [16, 24, 32, 48, 64, 128, 256]
    images = [draw_icon(s) for s in sizes]
    images[0].save(
        "assets/icon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:],
    )
    print("[OK] assets/icon.ico généré avec succès.")


if __name__ == "__main__":
    main()

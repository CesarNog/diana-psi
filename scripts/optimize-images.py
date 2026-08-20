#!/usr/bin/env python3
"""Regenera as variantes responsivas (WebP + JPEG) de assets/logo.png e
assets/foto.png usados no site. Rode este script sempre que substituir um
desses dois arquivos originais por uma nova versão.

Uso:
    pip install pillow
    python3 scripts/optimize-images.py
"""
from pathlib import Path
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / "assets"

JOBS = [
    # (arquivo de origem, nome base, larguras geradas em px)
    ("logo.png", "logo", [600, 1200]),
    ("foto.png", "foto", [350, 700]),
]


def build_og_image():
    """Recria assets/og-image.jpg (1200x630) a partir do logo atual."""
    logo_path = ASSETS / "logo.png"
    if not logo_path.exists():
        return
    logo = Image.open(logo_path).convert("RGB")
    bg_color = logo.getpixel((5, 5))  # combina com o fundo do próprio logo
    canvas = Image.new("RGB", (1200, 630), bg_color)
    target_h = 480
    w0, h0 = logo.size
    target_w = round(w0 * target_h / h0)
    logo_resized = logo.resize((target_w, target_h), Image.LANCZOS)
    x = (1200 - target_w) // 2
    y = (630 - target_h) // 2
    canvas.paste(logo_resized, (x, y))
    canvas.save(ASSETS / "og-image.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    print("og-image.jpg: 1200x630")


def main():
    for src_name, base, widths in JOBS:
        src = ASSETS / src_name
        if not src.exists():
            print(f"aviso: {src} não encontrado, pulando")
            continue
        im = Image.open(src).convert("RGB")
        w0, h0 = im.size
        for w in widths:
            h = round(h0 * w / w0)
            resized = im.resize((w, h), Image.LANCZOS)
            resized.save(ASSETS / f"{base}-{w}.webp", "WEBP", quality=82, method=6)
            resized.save(ASSETS / f"{base}-{w}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
            print(f"{base}-{w}: {w}x{h}")
    build_og_image()


if __name__ == "__main__":
    main()

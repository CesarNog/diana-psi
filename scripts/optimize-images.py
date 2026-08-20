#!/usr/bin/env python3
"""Regenera as variantes responsivas (WebP + JPEG) de assets/logo.png e
assets/foto.png usados no site, e a imagem de compartilhamento (OG).

Rode este script sempre que substituir um desses dois arquivos originais
por uma nova versão.

Uso:
    pip install pillow
    python3 scripts/optimize-images.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"

# Recortes do retrato original (assets/foto.png, 832x1248), definidos à mão
# para enquadrar bem o rosto (hero) e o corpo inteiro (seção Sobre).
FOTO_HERO_BOX = (56, 0, 776, 900)   # rosto + tronco, proporção 4:5
FOTO_ABOUT_BOX = (60, 0, 772, 1248)  # corpo inteiro, enquadramento mais justo

JOBS = [
    # (arquivo de origem ou None p/ usar crop, nome base, larguras, crop)
    ("logo.png", "logo", [600, 1200], None),
    ("foto.png", "foto-hero", [480, 720, 960], FOTO_HERO_BOX),
    ("foto.png", "foto-about", [400, 700], FOTO_ABOUT_BOX),
]


def build_og_image():
    """Recria assets/og-image.jpg (1200x630): logo + nome/título/CRP à
    esquerda, retrato à direita com transição suave — na paleta e
    tipografia originais da marca. Usado nas prévias de compartilhamento
    (WhatsApp/redes sociais)."""
    foto_path = ASSETS / "foto.png"
    logo_path = ASSETS / "logo.png"
    if not foto_path.exists() or not logo_path.exists():
        return
    W, H = 1200, 630
    BG = (248, 245, 241)
    canvas = Image.new("RGB", (W, H), BG)

    # faixa lateral com o retrato, com transição suave (feather) para o fundo
    portrait = Image.open(foto_path).convert("RGB").crop(FOTO_HERO_BOX)
    port_h = H
    port_w = round(portrait.width * port_h / portrait.height)
    portrait = portrait.resize((port_w, port_h), Image.LANCZOS).convert("RGBA")

    feather = 160
    alpha = Image.new("L", (port_w, port_h), 255)
    adraw = ImageDraw.Draw(alpha)
    for i in range(feather):
        a = round(255 * (i / feather))
        adraw.line([(i, 0), (i, port_h)], fill=a)
    portrait.putalpha(alpha)
    canvas.paste(portrait, (W - port_w, 0), portrait)

    draw = ImageDraw.Draw(canvas)

    try:
        f_name = ImageFont.truetype(str(FONTS / "CormorantGaramond-600.ttf"), 66)
        f_role = ImageFont.truetype(str(FONTS / "Quicksand-600.ttf"), 24)
        f_meta = ImageFont.truetype(str(FONTS / "Quicksand-500.ttf"), 20)
    except OSError:
        f_name = f_role = f_meta = ImageFont.load_default()

    ink = "#6B5170"
    ink_soft = "#7D6482"
    rose_deep = "#A34A6D"
    x = 76

    # bloco de texto centralizado verticalmente, com o logo acima do nome
    logo = Image.open(logo_path).convert("RGBA")
    logo_w = 132
    logo_h = round(logo.height * logo_w / logo.width)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    block_h = logo_h + 22 + 74 + 8 + 8 + 40 + 30 + 24
    y = (H - block_h) // 2

    canvas.paste(logo, (x - 8, y), logo)
    y += logo_h + 22
    draw.text((x, y), "Diana Nogueira", font=f_name, fill=ink)
    y += 74
    draw.line([(x + 2, y), (x + 46, y)], fill=rose_deep, width=3)
    y += 8
    draw.text((x, y), "Psicóloga Clínica", font=f_role, fill=rose_deep)
    y += 40
    draw.text((x, y), "CRP 06/234614 · Atendimento online", font=f_meta, fill=ink_soft)
    y += 30
    draw.text((x, y), "Adultos e idosos · Psicoterapia Comportamental Contextual", font=f_meta, fill=ink_soft)

    canvas.save(ASSETS / "og-image.jpg", "JPEG", quality=92, optimize=True, progressive=True)
    print("og-image.jpg: 1200x630")


def main():
    for src_name, base, widths, crop in JOBS:
        src = ASSETS / src_name
        if not src.exists():
            print(f"aviso: {src} não encontrado, pulando")
            continue
        im = Image.open(src).convert("RGB")
        if crop:
            im = im.crop(crop)
        w0, h0 = im.size
        for w in widths:
            h = round(h0 * w / w0)
            resized = im.resize((w, h), Image.LANCZOS)
            resized.save(ASSETS / f"{base}-{w}.webp", "WEBP", quality=88, method=6)
            resized.save(ASSETS / f"{base}-{w}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
            print(f"{base}-{w}: {w}x{h}")
    build_og_image()


if __name__ == "__main__":
    main()

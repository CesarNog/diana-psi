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
    """Recria assets/og-image.jpg (1200x630): retrato + nome/título/CRP,
    na paleta e tipografia da marca — usado nas prévias de compartilhamento."""
    foto_path = ASSETS / "foto.png"
    if not foto_path.exists():
        return
    W, H = 1200, 630
    canvas = Image.new("RGB", (W, H), "#FAF7F4")
    draw = ImageDraw.Draw(canvas)

    # faixa lateral com o retrato (crop do hero, ajustado à altura do card)
    portrait = Image.open(foto_path).convert("RGB").crop(FOTO_HERO_BOX)
    port_h = H
    port_w = round(portrait.width * port_h / portrait.height)
    portrait = portrait.resize((port_w, port_h), Image.LANCZOS)
    canvas.paste(portrait, (W - port_w, 0))

    # véu para o texto não colidir com a borda da foto
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(veil)
    vdraw.rectangle([W - port_w - 40, 0, W - port_w + 120, H], fill=(250, 247, 244, 255))
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), veil).convert("RGB"), (0, 0))

    try:
        f_name = ImageFont.truetype(str(FONTS / "Fraunces-600.ttf"), 58)
        f_role = ImageFont.truetype(str(FONTS / "Inter-500.ttf"), 24)
        f_meta = ImageFont.truetype(str(FONTS / "Inter-400.ttf"), 21)
    except OSError:
        f_name = f_role = f_meta = ImageFont.load_default()

    ink = "#2E2430"
    ink_soft = "#5B4E5D"
    rose_deep = "#8C3A5B"
    x = 72
    y = 210
    draw.text((x, y), "Diana Nogueira", font=f_name, fill=ink)
    y += 76
    draw.text((x, y), "Psicóloga Clínica", font=f_role, fill=rose_deep)
    y += 34
    draw.text((x, y), "CRP 06/234614 · Atendimento online", font=f_meta, fill=ink_soft)
    y += 32
    draw.text((x, y), "Adultos e idosos · Psicoterapia Comportamental Contextual", font=f_meta, fill=ink_soft)

    canvas.save(ASSETS / "og-image.jpg", "JPEG", quality=90, optimize=True, progressive=True)
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

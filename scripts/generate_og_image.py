#!/usr/bin/env python3
"""
Generate a 1200x630 social preview ("OG") card for a Bayanihan Wire issue.

Usage:
    python3 generate_og_image.py \
        --date "Tuesday, August 4, 2026" \
        --headline "Eala's Historic Crown & Six Dispatches of Bayanihan Spirit" \
        --count 6 \
        --out ../assets/img/og-2026-08-04.png

Requires Pillow (pip install pillow). Fonts are bundled in ./fonts/ next to
this script — do not point it at system fonts, since those won't exist on
whatever machine runs this next.
"""
import argparse
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# ---- brand tokens (keep in sync with template.html) ----
PAPER = (239, 230, 211)
INK = (32, 43, 34)
INK_SOFT = (75, 84, 73)
GOLD = (215, 154, 50)
GOLD_DEEP = (185, 121, 31)
RED = (165, 51, 42)

W, H = 1200, 630


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def draw_seal(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(248, 242, 228), outline=GOLD_DEEP, width=3)
    import math
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = cx + (r * 0.55) * math.cos(rad)
        y1 = cy + (r * 0.55) * math.sin(rad)
        x2 = cx + (r * 0.92) * math.cos(rad)
        y2 = cy + (r * 0.92) * math.sin(rad)
        draw.line([x1, y1, x2, y2], fill=GOLD, width=5)
    inner_r = r * 0.34
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=RED, outline=(75, 107, 79), width=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help='e.g. "Tuesday, August 4, 2026"')
    ap.add_argument("--headline", required=True, help="Lead headline for the issue")
    ap.add_argument("--count", type=int, default=0, help="Number of dispatches in this issue")
    ap.add_argument("--out", required=True, help="Output PNG path")
    args = ap.parse_args()

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # soft corner tints (simple flat approximation of the site's radial glows)
    overlay = Image.new("RGB", (W, H), PAPER)
    odraw = ImageDraw.Draw(overlay)
    odraw.ellipse([-200, -250, 500, 350], fill=(226, 197, 145))
    odraw.ellipse([800, 380, 1500, 900], fill=(196, 209, 197))
    img = Image.blend(img, overlay, 0.18)
    draw = ImageDraw.Draw(img)

    # seal
    draw_seal(draw, W // 2, 118, 58)

    # eyebrow
    eyebrow_font = load_font("JetBrainsMono-Bold.ttf", 20)
    eyebrow = "G O O D   N E W S   F R O M   T H E   I S L A N D S"
    bbox = draw.textbbox((0, 0), eyebrow, font=eyebrow_font)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 205), eyebrow, font=eyebrow_font, fill=RED)

    # masthead title
    title_font = load_font("YoungSerif-Regular.ttf", 64)
    title = "The Bayanihan Wire"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 240), title, font=title_font, fill=INK)

    # gold rule
    rule_y = 335
    draw.rectangle([W / 2 - 70, rule_y, W / 2 + 70, rule_y + 4], fill=GOLD)

    # headline (wrapped, centered)
    headline_font = load_font("IBMPlexSerif-Bold.ttf", 36)
    wrapped = textwrap.wrap(args.headline, width=38)[:3]
    y = 370
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=headline_font)
        draw.text(((W - (bbox[2] - bbox[0])) / 2, y), line, font=headline_font, fill=INK)
        y += 48

    # dateline + dispatch count
    meta_font = load_font("JetBrainsMono-Regular.ttf", 22)
    meta = args.date.upper()
    if args.count:
        meta += f"   ·   {args.count} DISPATCHES"
    bbox = draw.textbbox((0, 0), meta, font=meta_font)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, H - 80), meta, font=meta_font, fill=INK_SOFT)

    img.save(args.out, "PNG")
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()

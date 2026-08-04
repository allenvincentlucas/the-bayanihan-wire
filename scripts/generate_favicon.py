#!/usr/bin/env python3
"""
Generate the Bayanihan Wire favicon set from the sun-ray seal mark.

Usage:
    cd scripts
    python3 generate_favicon.py --out ../assets/favicon

Produces:
    favicon.ico            (16, 32, 48 px, multi-size)
    favicon-16x16.png
    favicon-32x32.png
    favicon-192x192.png    (Android/PWA)
    apple-touch-icon.png   (180x180, iOS)
    favicon.svg            (scalable, modern browsers)
"""
import argparse
import math
import os
from PIL import Image, ImageDraw

PAPER = (248, 242, 228, 255)
GOLD = (215, 154, 50, 255)
GOLD_DEEP = (185, 121, 31, 255)
RED = (165, 51, 42, 255)
GREEN = (75, 107, 79, 255)


def draw_seal(size):
    """Draw the seal at high resolution; downscale for crisp small icons."""
    S = size * 4  # supersample factor
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = S / 2
    r = S * 0.47

    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPER, outline=GOLD_DEEP, width=max(2, int(S * 0.02)))

    ray_w = max(2, int(S * 0.045))
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = cx + (r * 0.5) * math.cos(rad)
        y1 = cy + (r * 0.5) * math.sin(rad)
        x2 = cx + (r * 0.9) * math.cos(rad)
        y2 = cy + (r * 0.9) * math.sin(rad)
        draw.line([x1, y1, x2, y2], fill=GOLD, width=ray_w)

    inner_r = r * 0.4
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
                 fill=RED, outline=GREEN, width=max(1, int(S * 0.012)))

    return img.resize((size, size), Image.LANCZOS)


SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="47" fill="#F8F2E4" stroke="#B9791F" stroke-width="3"/>
  <g stroke="#D79A32" stroke-width="5" stroke-linecap="round">
    <line x1="50" y1="8" x2="50" y2="24"/>
    <line x1="50" y1="76" x2="50" y2="92"/>
    <line x1="8" y1="50" x2="24" y2="50"/>
    <line x1="76" y1="50" x2="92" y2="50"/>
    <line x1="19" y1="19" x2="30" y2="30"/>
    <line x1="70" y1="70" x2="81" y2="81"/>
    <line x1="81" y1="19" x2="70" y2="30"/>
    <line x1="30" y1="70" x2="19" y2="81"/>
  </g>
  <circle cx="50" cy="50" r="18" fill="#A5332A" stroke="#4B6B4F" stroke-width="2"/>
</svg>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output directory for favicon files")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    icon16 = draw_seal(16)
    icon32 = draw_seal(32)
    icon48 = draw_seal(48)
    icon192 = draw_seal(192)
    icon180 = draw_seal(180)

    icon16.save(os.path.join(args.out, "favicon-16x16.png"))
    icon32.save(os.path.join(args.out, "favicon-32x32.png"))
    icon192.save(os.path.join(args.out, "favicon-192x192.png"))
    icon180.save(os.path.join(args.out, "apple-touch-icon.png"))

    icon48.save(os.path.join(args.out, "favicon.ico"), format="ICO",
                sizes=[(16, 16), (32, 32), (48, 48)])

    with open(os.path.join(args.out, "favicon.svg"), "w") as f:
        f.write(SVG_TEMPLATE)

    print("Favicon set written to", args.out)


if __name__ == "__main__":
    main()

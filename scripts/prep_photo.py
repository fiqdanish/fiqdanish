"""
Prepare a portrait photo for clean ASCII conversion:
  1. convert to grayscale
  2. boost local contrast so a flatly-lit face gains highlights/shadows
  3. push near-white background pixels to pure white so they read as blank
     in the ascii ramp

Works best with photos that already have a plain, light background (e.g. an
ID photo). Output: source-prepped.png, consumed by make_ascii_svg.py.

    python scripts/prep_photo.py <input.jpg> [output.png]
"""
import os
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

BG_FLOOR = 235  # pixels this bright or brighter get pushed to pure white

im = Image.open(INP).convert("L")

# local contrast via a simple unsharp-mask-style boost + autocontrast
im = ImageOps.autocontrast(im, cutoff=1)
im = ImageEnhance.Contrast(im).enhance(1.15)
im = ImageEnhance.Brightness(im).enhance(1.02)

arr = np.array(im).astype(np.float32)
arr = np.where(arr >= BG_FLOOR, 255.0, arr)
out = np.clip(arr, 0, 255).astype(np.uint8)

Image.fromarray(out, mode="L").save(OUT)
print("wrote", OUT, out.shape)

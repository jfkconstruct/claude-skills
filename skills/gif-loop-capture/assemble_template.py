"""Assemble captured frames into an animated webp (gif-loop-capture skill)."""
import sys
from pathlib import Path
from PIL import Image

FRAMES_DIR = Path(__file__).parent / "frames"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "loop.webp"
TARGET = (720, 540)
DURATION_MS = 140
QUALITY = 68


def cover(im, tw, th):
    w, h = im.size
    scale = max(tw / w, th / h)
    im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    left, top = (im.width - tw) // 2, (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


frames = [cover(Image.open(p).convert("RGB"), *TARGET)
          for p in sorted(FRAMES_DIR.glob("frame_*.png"))]
frames[0].save(OUT, save_all=True, append_images=frames[1:],
               duration=DURATION_MS, loop=0, quality=QUALITY, method=4)

check = Image.open(OUT)
kb = OUT.stat().st_size / 1024
print(f"{OUT} {kb:.1f} KB animated={check.is_animated} n_frames={check.n_frames} size={check.size}")
assert check.is_animated and check.size == TARGET
if kb > 2000:
    print("OVER 2000 KB: re-save with ~24 frames and quality=60")

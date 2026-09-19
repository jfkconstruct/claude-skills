"""Frame-burst capture template (gif-loop-capture skill).

Per-target knobs: URL, SELECTOR, how-to-reach-motion block, N_FRAMES, INTERVAL_MS.
Setup: pip install playwright pillow; python -m playwright install chromium.
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

WORKDIR = Path(__file__).parent
FRAMES_DIR = WORKDIR / "frames"
FRAMES_DIR.mkdir(exist_ok=True)
for old in FRAMES_DIR.glob("frame_*.png"):
    old.unlink()  # a shorter recapture must not inherit stale frames

URL = "http://127.0.0.1:8091/TARGET.html"  # served with: python -m http.server 8091 --bind 127.0.0.1
SELECTOR = "canvas"          # the game surface; fall back to clipped page.screenshot
N_FRAMES = 32
INTERVAL_MS = 140

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 960, "height": 720})
    # State injection (optional): runs BEFORE any page script.
    # context.add_init_script("localStorage.setItem('game.save.v1', JSON.stringify({...}))")
    page = context.new_page()
    page.goto(URL, wait_until="load")
    page.evaluate("document.fonts.ready.then(()=>{})")
    page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
    page.wait_for_timeout(900)  # settle: no loading flash in frame 1

    surface = page.locator(SELECTOR)

    # --- reach visible motion here: clicks/keys/JS, per target ---
    # surface.click(position={"x": 480, "y": 360})
    page.wait_for_timeout(1400)  # let motion establish before the burst

    for i in range(N_FRAMES):
        surface.screenshot(path=str(FRAMES_DIR / f"frame_{i:03d}.png"))
        # keep driving inputs here if the action must span the burst
        page.wait_for_timeout(INTERVAL_MS)

    browser.close()

print(f"Captured {N_FRAMES} frames to {FRAMES_DIR}")

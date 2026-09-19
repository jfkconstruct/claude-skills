---
name: gif-loop-capture
description: Capture HTML loops and animated sequences as optimized GIF and video for social sharing.
---

---
name: gif-loop-capture
description: Turn any local HTML game/app/animation into an animated-webp gameplay loop (playwright frame-burst -> PIL assemble), with parallel fan-out across many targets, state-injection for hard-to-reach screens, and the reduced-motion wire-in pattern. Use when the user asks for gameplay gifs/loops, animated tiles, or "capture X in motion".
---

# Gameplay loop capture (animated webp)

First shipped: evidence rung 2, 2026-07-31 (site commit `b7b62b8`, 5 games). Templates in this directory: `capture_template.py`, `assemble_template.py`.

## Pipeline

1. **Serve the target dir once, shared:** `python -m http.server 8091 --bind 127.0.0.1` from the app root, background. One read-only server for all agents; never one per agent.
2. **Fan out one forge (sonnet) per target**, isolated workdir each, all writing to ONE shared `out/` dir with UNIQUE per-target filenames (`<slug>-loop.webp`). Forge prompt must include: URL + source file path, how to reach visible motion (or "read the game and find it"), the capture/assemble specs below, and the <=20-line return contract.
3. **Capture spec** (see `capture_template.py`): headless chromium, viewport 960x720, wait load + `document.fonts.ready` + 2 rAF + settle so frame 1 has no loading flash. 28-36 frames of the canvas/game element spaced ~140ms. Drive inputs DURING the burst so motion spans frames.
4. **Assemble spec** (see `assemble_template.py`): PIL, RGB, cover-crop+resize to exactly 720x540, `save_all=True, duration=140, loop=0, quality=68, method=4`. Re-save at ~24f/q60 only if >2000 KB. Observed sizes: 54-780 KB per 32-frame loop.
5. **Orchestrator verify, never skip:** (a) PIL reopen each: `is_animated`, `n_frames`, `size==(720,540)`; (b) md5 across all outputs, identical hashes = workdir collision; (c) frame-diff first/mid/last nonzero = real motion; (d) build a first/mid/last contact sheet PNG and EYEBALL it (probe-invisible defects are a recurring class).

## Reaching hard game states

- **Save-inject** beats playing the game: `add_init_script` sets the game's localStorage save key BEFORE page scripts run; read the game's `loadGame()` for required fields. Worked twice on Emberfall (minimal v2 save spawns at the vale).
- Pre-seed flags the same way to skip tutorials/demos (Math Facts: `demoSeen:true`).
- Calling the game's own JS (`load(4)`) to jump levels is fine; the RENDERED result must be genuine gameplay.
- Real pointer/key events over test hooks for the visible action itself.

## Wire-in (site tiles)

Static webp stays as `src` (first paint + no-JS + reduced-motion fallback); add `data-loop="<slug>-loop.webp"`; one IntersectionObserver script (rootMargin 200px) gated on `matchMedia('(prefers-reduced-motion: no-preference)')` preloads via `new Image()` then swaps `src`. Worked copy: `a portfolio site lab example` bottom script.

## Known gotchas

- NEW filenames on every recapture; the user's browser caches images past a css cache-bust (bit us twice: stale styles.css 07-31, stale emberfall webp).
- Probing lazy swap at narrow widths: off-screen tiles legitimately DON'T swap until scrolled near; scroll to the LAST tile before counting, or the probe fails on correct behavior.
- `img.decode()` on a `loading="lazy"` image that never started loading NEVER settles (probe hung silently, 07-31): scroll-sweep the page to trigger lazy loads first, and always `Promise.race` the decode-wait against a timeout.
- Bigger display target = bigger RASTER, same composition: `zoom: 1.5` on the rig stage re-renders the approved layout at a larger glyph raster (real sharpness, unlike upscaling the asset) with zero layout edits; capture viewport must fit the ZOOMED dims ( band, 07-31).
- Animated-webp write support: Pillow >=11 always has it; `features.check('webp_anim')` warns Unknown, ignore it.
- libwebp merges pixel-identical consecutive frames; n_frames < captured count is not a bug if source PNGs md5-match.
- Long readable holds: design the rig so holds are EXACTLY static (all eases saturated, counters stopped), then dedupe at capture: merge identical frames (`im.tobytes()` compare) and pass `duration=` a per-frame LIST; a 116-frame 16.2s cycle shipped as 54 frames / 274 KB with timing intact (applied-demo capture.py, 07-31).
- Verifying per-frame durations on readback: PIL fills `info["duration"]` on `load()`, not on `seek()`; seek-then-read reports 0 and looks like the durations were dropped when they were not.


## Posting to LinkedIn

LinkedIn accepts mp4 (as video) or gif/png/jpg (as image), never webp. Keep the webp for the page and convert a copy with ffmpeg for the post. A 1080x1350 portrait frame reads best in the feed; hide buttons, kbd hints, and captions before the burst so the loop shows the work, not the chrome.

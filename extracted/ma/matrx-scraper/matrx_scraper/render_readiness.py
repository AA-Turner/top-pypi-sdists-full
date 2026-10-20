"""Know when a page has actually painted before it is photographed.

A slow site commits its document long before its content shows. Capturing at
DOMContentLoaded (or right after `commit`) yields a nearly white frame — and a
screenshot taken that way is evidence of nothing. Two defenses, both bounded
and neither ever raising:

1. ``wait_until_painted`` — wait for ``load`` and a short ``networkidle``, then
   poll the page until real, visible content is inside the first viewport and
   stable (text actually shown — not opacity-0 entrance animations — and every
   in-viewport image decoded).
2. ``png_looks_blank`` — after the shot, judge the pixels. A blank frame is
   re-shot after a short wait by the caller.

Both only ever add time while a page is genuinely not ready; a ready page
passes through each in one cheap probe.
"""

from __future__ import annotations

import asyncio
import io
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)

# How long past `commit` we will wait for a page to paint before shooting what
# we have. A hard ceiling: a never-ready page must not hold a pool slot.
RENDER_READY_MAX_MS = 15_000
LOAD_WAIT_MS = 10_000
NETWORK_IDLE_WAIT_MS = 4_000
PROBE_INTERVAL_MS = 500
# Enough visible words in the first viewport to call it "content", not chrome.
MIN_VISIBLE_CHARS = 60

BLANK_RETRIES = 2
BLANK_RETRY_WAIT_MS = 4_000
# Share of (downscaled) pixels within BLANK_TOLERANCE of the dominant color at
# or above which the frame is judged blank.
BLANK_DOMINANT_SHARE = 0.985
BLANK_TOLERANCE = 6
# Fallback when Pillow is absent: compressed bytes per pixel. A blank 1366x768
# frame compresses to a few KB; a rendered page is tens to hundreds of KB.
BLANK_BYTES_PER_PIXEL = 0.004

# Visible = painted: not display:none, not visibility:hidden, not opacity ~0
# (WordPress/Elementor entrance animations start there), inside the viewport.
PAINT_PROBE_JS = """() => {
  const vh = window.innerHeight || 768;
  const vw = window.innerWidth || 1366;
  const inView = (el) => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < vh && r.right > 0 && r.left < vw;
  };
  const shown = (el) => {
    try {
      return el.checkVisibility({ opacityProperty: true, visibilityProperty: true }) && inView(el);
    } catch (_) {
      const cs = getComputedStyle(el);
      return cs.display !== "none" && cs.visibility !== "hidden" && Number(cs.opacity) > 0.05 && inView(el);
    }
  };
  let chars = 0;
  if (document.body) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    let scanned = 0;
    while ((node = walker.nextNode()) && scanned < 4000) {
      scanned += 1;
      const text = node.nodeValue ? node.nodeValue.trim() : "";
      if (!text) continue;
      const parent = node.parentElement;
      if (!parent || ["SCRIPT", "STYLE", "NOSCRIPT"].includes(parent.tagName)) continue;
      if (shown(parent)) chars += text.length;
    }
  }
  let pendingImages = 0;
  let paintedMedia = 0;
  for (const el of document.querySelectorAll("img, video, canvas, svg")) {
    if (!shown(el)) continue;
    if (el.tagName === "IMG") {
      if (el.complete && el.naturalWidth > 0) paintedMedia += 1;
      else if (!el.complete) pendingImages += 1;
    } else {
      paintedMedia += 1;
    }
  }
  return { chars, pendingImages, paintedMedia, readyState: document.readyState };
}"""


async def wait_until_painted(
    page: Any,
    *,
    max_ms: int = RENDER_READY_MAX_MS,
    min_chars: int = MIN_VISIBLE_CHARS,
) -> dict[str, Any]:
    """Wait (bounded) until the first viewport shows stable, real content.

    Never raises: a page that cannot be probed, or never gets ready, returns a
    report saying so and the caller shoots what is there. The report is for
    logs and tests.
    """
    started = time.monotonic()
    deadline = started + max_ms / 1000.0

    def remaining_ms() -> int:
        return max(0, int((deadline - time.monotonic()) * 1000))

    for state, wait_ms in (("load", LOAD_WAIT_MS), ("networkidle", NETWORK_IDLE_WAIT_MS)):
        budget = min(wait_ms, remaining_ms())
        if budget <= 0:
            break
        try:
            await page.wait_for_load_state(state, timeout=budget)
        except asyncio.CancelledError:
            raise
        except Exception:
            # Slow third parties keep networkidle from ever arriving; the
            # content probe below is what decides readiness.
            logger.debug("page did not reach %s within %dms", state, budget)

    last: dict[str, Any] = {}
    stable_polls = 0
    previous_chars = -1
    ready = False
    while True:
        try:
            last = await asyncio.wait_for(
                page.evaluate(PAINT_PROBE_JS), timeout=max(1.0, min(5.0, remaining_ms() / 1000))
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 — a probe failure must not fail the capture
            logger.info("paint probe failed: %s: %s", type(exc).__name__, exc)
            break
        if not isinstance(last, dict):
            last = {}
            break  # a page that cannot be probed is shot as it stands
        chars = int(last.get("chars", 0))
        has_content = chars >= min_chars or int(last.get("paintedMedia", 0)) >= 2
        settled = int(last.get("pendingImages", 0)) == 0 and chars == previous_chars
        stable_polls = stable_polls + 1 if (has_content and settled) else 0
        previous_chars = chars
        if stable_polls >= 2:
            ready = True
            break
        if remaining_ms() <= PROBE_INTERVAL_MS:
            break
        await asyncio.sleep(PROBE_INTERVAL_MS / 1000.0)

    report = {
        "ready": ready,
        "waited_ms": int((time.monotonic() - started) * 1000),
        "visible_chars": int(last.get("chars", 0)) if last else 0,
        "pending_images": int(last.get("pendingImages", 0)) if last else 0,
    }
    if not ready:
        logger.warning(
            "page was not painted after %dms (visible_chars=%s pending_images=%s); "
            "capturing what is shown",
            report["waited_ms"],
            report["visible_chars"],
            report["pending_images"],
        )
    return report


def png_looks_blank(png: bytes, width: int, height: int) -> bool:
    """True when a screenshot is (nearly) a single flat color.

    Pillow gives the real answer (dominant-colour share of a downscaled frame).
    Without it, fall back to how well the PNG compressed — a flat frame is tiny.
    """
    try:
        from PIL import Image  # noqa: PLC0415 — optional dependency
    except ImportError:
        return len(png) < width * height * BLANK_BYTES_PER_PIXEL
    try:
        with Image.open(io.BytesIO(png)) as image:
            small = image.convert("L").resize((96, 54))
            getter = getattr(small, "get_flattened_data", None) or small.getdata
            pixels = list(getter())
    except Exception:  # noqa: BLE001 — an undecodable frame is not judged blank
        return False
    counts: dict[int, int] = {}
    for value in pixels:
        counts[value] = counts.get(value, 0) + 1
    best = 0
    for centre in counts:
        near = sum(n for v, n in counts.items() if abs(v - centre) <= BLANK_TOLERANCE)
        best = max(best, near)
    return best / len(pixels) >= BLANK_DOMINANT_SHARE

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
   re-shot by the caller after ``coax_render`` (network idle, a scroll pass to
   wake lazy content) and an escalating wait (``BLANK_RETRY_WAITS_MS``).
3. ``blank_flag_metadata`` — at persist time, a frame that is STILL blank is
   stored with ``metadata.blank = true`` so no reader ever picks it as a hero
   over a good capture, and never silently.

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

# One escalating wait per blank re-shot: a JS-heavy site that has not painted
# after the first gets a longer second chance. len() is the retry count.
BLANK_RETRY_WAITS_MS: tuple[int, ...] = (3_000, 8_000)
BLANK_RETRIES = len(BLANK_RETRY_WAITS_MS)
# Bounded effort per re-shot spent coaxing the page: the same network-idle wait as the
# first shot, then a scroll pass pausing half a probe interval per step.
COAX_SCROLL_STEPS = 6
# Seconds a caller must budget for one kind's blank retries (waits + coax + shot).
BLANK_RETRY_BUDGET_S = sum(BLANK_RETRY_WAITS_MS) / 1000.0 + BLANK_RETRIES * (
    NETWORK_IDLE_WAIT_MS / 1000.0 + COAX_SCROLL_STEPS * (PROBE_INTERVAL_MS // 2) / 1000.0 + 20.0
)
# Share of (downscaled) pixels within BLANK_TOLERANCE of the dominant color at
# or above which the frame is judged blank.
BLANK_DOMINANT_SHARE = 0.985
BLANK_TOLERANCE = 6
# A frame whose grey-level standard deviation is at or below this is one flat
# field (or a barely-visible gradient) even when no single color dominates.
BLANK_MAX_STDDEV = 3.0
BLANK_SAMPLE_SIZE = (96, 54)
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


def blank_measure(png: bytes) -> dict[str, float] | None:
    """Dominant-color share and grey stddev of a downscaled frame; None without Pillow or on a bad frame."""
    try:
        from PIL import Image  # noqa: PLC0415 — optional dependency
    except ImportError:
        return None
    try:
        with Image.open(io.BytesIO(png)) as image:
            small = image.convert("L").resize(BLANK_SAMPLE_SIZE)
            getter = getattr(small, "get_flattened_data", None) or small.getdata
            pixels = list(getter())
    except Exception:  # noqa: BLE001 — an undecodable frame is not judged
        return None
    if not pixels:
        return None
    counts: dict[int, int] = {}
    for value in pixels:
        counts[value] = counts.get(value, 0) + 1
    best = 0
    for centre in counts:
        near = sum(n for v, n in counts.items() if abs(v - centre) <= BLANK_TOLERANCE)
        best = max(best, near)
    mean = sum(pixels) / len(pixels)
    stddev = (sum((v - mean) ** 2 for v in pixels) / len(pixels)) ** 0.5
    return {
        "dominant_share": round(best / len(pixels), 4),
        "stddev": round(stddev, 2),
        "mean": round(mean, 1),
    }


def png_looks_blank(png: bytes, width: int, height: int) -> bool:
    """True when a screenshot is (nearly) a single flat color.

    Pillow gives the real answer (dominant-color share and pixel spread of a
    downscaled frame). Without it, fall back to how well the PNG compressed —
    a flat frame is tiny.
    """
    try:
        import PIL  # noqa: F401, PLC0415 — optional dependency
    except ImportError:
        return len(png) < width * height * BLANK_BYTES_PER_PIXEL
    measure = blank_measure(png)
    if measure is None:
        return False
    return measure["dominant_share"] >= BLANK_DOMINANT_SHARE or measure["stddev"] <= BLANK_MAX_STDDEV


def blank_flag_metadata(png: bytes, width: int | None, height: int | None) -> dict[str, Any]:
    """Screenshot-row metadata for a frame that is still blank after every retry; {} for a real frame.

    ``blank: true`` is the one flag every hero reader skips; ``blank_measure``
    says why. Logged loudly — a stored blank is never silent.
    """
    if not png_looks_blank(png, width or 1366, height or 768):
        return {}
    measure = blank_measure(png)
    logger.warning("storing a screenshot that is still blank after retries: %s", measure)
    flag: dict[str, Any] = {"blank": True}
    if measure is not None:
        flag["blank_measure"] = measure
    return flag


_SCROLL_PASS_JS = """async ([steps, pauseMs]) => {
  const h = Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0);
  for (let i = 1; i <= steps; i++) {
    window.scrollTo(0, Math.round((h * i) / steps));
    await new Promise((r) => setTimeout(r, pauseMs));
  }
  window.scrollTo(0, 0);
  return h;
}"""


async def coax_render(page: Any, *, preserve_scroll: bool = False) -> None:
    """Give a frame that came out blank its best chance to paint. Bounded, never raises.

    Waits for network idle, then (unless the caller owns the scroll position)
    scrolls through the page once and back to the top so lazy and
    intersection-triggered content mounts.
    """
    try:
        await page.wait_for_load_state("networkidle", timeout=NETWORK_IDLE_WAIT_MS)
    except asyncio.CancelledError:
        raise
    except Exception:  # noqa: BLE001 — chatty third parties never go idle
        logger.debug("blank retry: page did not reach networkidle within %dms", NETWORK_IDLE_WAIT_MS)
    if preserve_scroll:
        return
    try:
        await asyncio.wait_for(
            page.evaluate(_SCROLL_PASS_JS, [COAX_SCROLL_STEPS, PROBE_INTERVAL_MS // 2]),
            timeout=COAX_SCROLL_STEPS * (PROBE_INTERVAL_MS // 2) / 1000.0 + 5.0,
        )
    except asyncio.CancelledError:
        raise
    except Exception as exc:  # noqa: BLE001 — the re-shot still happens
        logger.debug("blank retry scroll pass skipped: %s", exc)

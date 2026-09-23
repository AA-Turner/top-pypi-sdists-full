"""Human-shaped input for a real, persistent Chrome (CB-013).

A site watching pointer and key events can tell a Playwright ``page.click`` from a
person instantly: the pointer teleports to the exact centre of the element, the
button goes down and up in the same millisecond, and ``page.fill`` writes a whole
string without a single keystroke. This module is the ONE place that turns the
agent's intent ("click this", "type that", "scroll down") into the event stream a
person produces:

* the pointer travels from where it last was along a curved path with a natural
  speed profile (slow-fast-slow), lands at a random point inside the target —
  never the exact centre — pauses, presses, pauses, releases;
* text arrives one keystroke at a time with a per-key delay drawn from a
  log-normal distribution, longer after spaces and punctuation, and with the odd
  short "thinking" pause;
* scrolling is wheel notches of a plausible size with short gaps, not a single
  ``window.scrollBy``.

It never changes WHAT happens — only how the input events are shaped — so the
callers in ``actions.py`` keep their results, guards and error mapping unchanged.
Everything here degrades LOUDLY: when a target has no box to aim at (detached,
zero-size), the caller falls back to the plain Playwright action and the fallback
is logged at WARNING with the selector, so a run that stops looking human is
visible in the worker log rather than silently regressing.

Timings are deliberately conservative (a fast, confident user), because the agent
issues many actions per task and a slow typist would make every task slow. The
knobs below are module constants; the control plane's ``LaunchPolicy.humanize_input``
turns the whole behaviour on or off per run.
"""

from __future__ import annotations

import asyncio
import logging
import math
import random
import weakref
from typing import Any

from matrx_scraper.ai_browser.readiness import element_readiness

logger = logging.getLogger(__name__)

# ── timing constants (seconds) ──────────────────────────────────────────────
KEY_DELAY_MEDIAN = 0.085  # log-normal median between keystrokes
KEY_DELAY_SIGMA = 0.45  # log-normal spread
KEY_DELAY_MIN = 0.025
KEY_DELAY_MAX = 0.55
WORD_BREAK_EXTRA = (0.06, 0.22)  # extra pause after space / punctuation
THINK_PAUSE_PROBABILITY = 0.04  # occasional longer pause mid-text
THINK_PAUSE = (0.25, 0.7)
HOVER_DWELL = (0.04, 0.14)  # pointer rests on the target before pressing
PRESS_HOLD = (0.05, 0.13)  # mouse button held down
MOVE_MIN_DURATION = 0.18
MOVE_MAX_DURATION = 0.75
MOVE_STEP_PX = 9.0  # one pointer sample roughly every N px of path
WHEEL_NOTCH = (80, 160)  # pixels per wheel notch
WHEEL_GAP = (0.02, 0.07)  # gap between notches

_rng = random.SystemRandom()

# Last known pointer position per page. A new page starts wherever a real cursor
# would plausibly rest: somewhere in the upper-left quadrant, never (0, 0).
_pointer: weakref.WeakKeyDictionary[Any, tuple[float, float]] = weakref.WeakKeyDictionary()


def _uniform(bounds: tuple[float, float]) -> float:
    lo, hi = bounds
    return _rng.uniform(lo, hi)


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def key_delay(prev_char: str | None) -> float:
    """Seconds to wait BEFORE the next keystroke. Pure so a test can bound it."""
    d = _rng.lognormvariate(math.log(KEY_DELAY_MEDIAN), KEY_DELAY_SIGMA)
    d = _clamp(d, KEY_DELAY_MIN, KEY_DELAY_MAX)
    if prev_char is not None and (prev_char.isspace() or prev_char in ".,;:!?"):
        d += _uniform(WORD_BREAK_EXTRA)
    if _rng.random() < THINK_PAUSE_PROBABILITY:
        d += _uniform(THINK_PAUSE)
    return d


def ease_in_out(t: float) -> float:
    """Smoothstep speed profile: slow start, fast middle, slow settle."""
    return t * t * (3.0 - 2.0 * t)


def bezier_path(
    start: tuple[float, float], end: tuple[float, float], *, steps: int | None = None
) -> list[tuple[float, float]]:
    """Pointer samples from ``start`` to ``end`` along a cubic Bézier curve.

    The two control points sit off the straight line by a random fraction of the
    distance, so no two moves share a path and none is a straight line. The last
    sample is exactly ``end``. Pure geometry; timing is applied by the caller.
    """
    (x0, y0), (x3, y3) = start, end
    dx, dy = x3 - x0, y3 - y0
    dist = math.hypot(dx, dy)
    if steps is None:
        steps = int(_clamp(dist / MOVE_STEP_PX, 10, 80))
    if dist < 1.0:
        return [end]
    # Perpendicular unit vector for the bow of the curve.
    px, py = -dy / dist, dx / dist
    bow1 = _rng.uniform(-0.28, 0.28) * dist
    bow2 = _rng.uniform(-0.28, 0.28) * dist
    c1 = (
        x0 + dx * _rng.uniform(0.2, 0.4) + px * bow1,
        y0 + dy * _rng.uniform(0.2, 0.4) + py * bow1,
    )
    c2 = (
        x0 + dx * _rng.uniform(0.6, 0.8) + px * bow2,
        y0 + dy * _rng.uniform(0.6, 0.8) + py * bow2,
    )
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = ease_in_out(i / steps)
        u = 1.0 - t
        x = u**3 * x0 + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * x3
        y = u**3 * y0 + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * y3
        # Sub-pixel hand tremor, fading out as the pointer settles.
        if i < steps:
            jitter = 0.8 * (1.0 - t)
            x += _rng.uniform(-jitter, jitter)
            y += _rng.uniform(-jitter, jitter)
        pts.append((x, y))
    pts[-1] = end
    return pts


def move_duration(dist: float) -> float:
    """Seconds a pointer move of ``dist`` px takes — a Fitts-like curve, bounded."""
    if dist < 1.0:
        return 0.0
    d = 0.12 + 0.09 * math.log2(1.0 + dist / 40.0) + _rng.uniform(-0.03, 0.05)
    return _clamp(d, MOVE_MIN_DURATION, MOVE_MAX_DURATION)


def aim_point(box: dict[str, float]) -> tuple[float, float]:
    """A landing point inside ``box``, biased to the middle, never the exact centre
    and never within the outer 12% (where a real click risks the edge)."""
    w, h = max(box["width"], 1.0), max(box["height"], 1.0)
    mx, my = w * 0.12, h * 0.12
    x = _rng.gauss(w / 2.0, w / 6.0)
    y = _rng.gauss(h / 2.0, h / 6.0)
    x = _clamp(x, mx, w - mx)
    y = _clamp(y, my, h - my)
    return box["x"] + x, box["y"] + y


class HumanInput:
    """Drives one Playwright ``Page`` with human-shaped events."""

    def __init__(self, page: Any) -> None:
        self.page = page

    # ── pointer ──────────────────────────────────────────────────────────

    def _where(self) -> tuple[float, float]:
        pos = _pointer.get(self.page)
        if pos is None:
            vp = self.page.viewport_size or {"width": 1280, "height": 800}
            pos = (
                _rng.uniform(vp["width"] * 0.15, vp["width"] * 0.45),
                _rng.uniform(vp["height"] * 0.15, vp["height"] * 0.45),
            )
            _pointer[self.page] = pos
        return pos

    async def move_to(self, x: float, y: float) -> None:
        start = self._where()
        path = bezier_path(start, (x, y))
        total = move_duration(math.hypot(x - start[0], y - start[1]))
        gap = total / max(len(path), 1)
        for px, py in path:
            await self.page.mouse.move(px, py)
            if gap > 0:
                await asyncio.sleep(gap)
        _pointer[self.page] = (x, y)

    async def _target_box(self, selector: str, timeout_ms: int) -> dict[str, float] | None:
        """The aim-able box for ``selector``, or None with a WARNING saying why.

        Readiness is NOT decided here — it comes from the one shared definition
        in ``readiness.py``, which is also what ``actions.get_element`` reports.
        Returning None (rather than raising) is what makes the documented
        degrade-loudly contract real: the caller falls back to the plain
        Playwright action. A ``wait_for`` TIMEOUT used to escape this function,
        propagate out of ``HumanInput.type_text`` and be swallowed by the blanket
        ``except Exception`` in ``actions.type_text`` — so on the COMMONEST
        failure the promised fallback never ran and the promised WARNING was
        never logged.
        """
        verdict = await element_readiness(self.page, selector, timeout_ms=timeout_ms)
        if verdict.usable and verdict.box is not None:
            return verdict.box
        logger.warning(
            "humanize: %r is not aim-able (%s); falling back to the plain Playwright action",
            selector,
            verdict.reason,
        )
        return None

    async def click(self, selector: str, *, timeout_ms: int) -> bool:
        """Move, dwell, press, release on ``selector``. Returns False (after a
        WARNING) when the target offers no box, so the caller can fall back."""
        box = await self._target_box(selector, timeout_ms)
        if box is None:
            logger.warning(
                "humanize: %r has no bounding box; falling back to a plain click", selector
            )
            return False
        x, y = aim_point(box)
        await self.move_to(x, y)
        await asyncio.sleep(_uniform(HOVER_DWELL))
        await self.page.mouse.down()
        await asyncio.sleep(_uniform(PRESS_HOLD))
        await self.page.mouse.up()
        return True

    # ── keyboard ─────────────────────────────────────────────────────────

    async def type_text(
        self, selector: str, text: str, *, clear_first: bool, timeout_ms: int
    ) -> bool:
        """Click into ``selector`` like a person, optionally select-all + delete,
        then type ``text`` one key at a time. Returns False (after a WARNING)
        when the field offers no box, so the caller can fall back."""
        if not await self.click(selector, timeout_ms=timeout_ms):
            return False
        await asyncio.sleep(_uniform((0.08, 0.2)))
        if clear_first:
            await self.page.keyboard.press("ControlOrMeta+a")
            await asyncio.sleep(_uniform((0.04, 0.1)))
            await self.page.keyboard.press("Backspace")
            await asyncio.sleep(_uniform((0.06, 0.16)))
        prev: str | None = None
        for ch in text:
            await asyncio.sleep(key_delay(prev))
            if ch == "\n":
                await self.page.keyboard.press("Enter")
            else:
                await self.page.keyboard.type(ch)
            prev = ch
        return True

    async def press_enter(self) -> None:
        await asyncio.sleep(_uniform((0.12, 0.35)))
        await self.page.keyboard.press("Enter")

    # ── wheel ────────────────────────────────────────────────────────────

    async def scroll_by(self, delta_y: float, *, over_selector: str | None = None) -> None:
        """Wheel ``delta_y`` px (negative = up) in notches, pointer resting over
        the scrolled region so the wheel lands on the right scroller."""
        if over_selector:
            box = await self._target_box(over_selector, 5_000)
            if box is not None:
                x, y = aim_point(box)
                await self.move_to(x, y)
        else:
            x0, y0 = self._where()
            vp = self.page.viewport_size or {"width": 1280, "height": 800}
            # A hand scrolling rests the pointer somewhere in the page body.
            x, y = (
                _clamp(x0 + _rng.uniform(-40, 40), 40, vp["width"] - 40),
                _clamp(y0 + _rng.uniform(-30, 30), 80, vp["height"] - 40),
            )
            await self.move_to(x, y)
        remaining = float(delta_y)
        sign = 1.0 if remaining >= 0 else -1.0
        while abs(remaining) >= 1.0:
            notch = min(abs(remaining), _uniform(WHEEL_NOTCH))
            await self.page.mouse.wheel(0, sign * notch)
            remaining -= sign * notch
            await asyncio.sleep(_uniform(WHEEL_GAP))

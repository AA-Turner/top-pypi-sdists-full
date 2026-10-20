"""Inline-HTML inspection — render a caller-supplied document, run a caller-supplied
measurement script in the page, and return the result per (width, theme) capture.

Why this exists: `inspect_url` can only look at a public URL. A generated diagram or
component has no URL yet, and the question "does it render legibly" is answered by
measuring the live DOM (text boxes, overlaps, clipping), not by reading its source.

Contract (see `matrx_scraper/FEATURE.md` § Inline inspection):

* `html` is a full document, or anything else (a bare `<svg>`, a fragment) which is
  wrapped in a minimal document with a zero-margin body.
* `measure_script` is JavaScript text evaluated in the page after load + settle.
  Two forms, chosen by whether the text parses as ONE EXPRESSION:
  an expression (`document.querySelectorAll('text').length`) is evaluated and awaited;
  anything else is the body of an async function and MUST `return` its result.
  The result is serialised with `JSON.stringify` inside the page; `undefined`,
  circular values and thrown errors all become `error` text on THAT capture.
* One capture per width x theme. A script failure never aborts the other captures and
  is never an empty `measurements`: failure => `measurements is None` and `error` set.
* The page cannot reach non-public hosts (`install_egress_guard`), exactly like
  `inspect_url`.
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Any

from matrx_scraper.ai_browser.url_guard import install_egress_guard
from matrx_scraper.parser.knobs import parser_knob
from matrx_scraper.screenshot_dimensions import png_dimensions

logger = logging.getLogger(__name__)

INLINE_MAX_HTML_CHARS = 2_000_000
INLINE_MAX_SCRIPT_CHARS = 500_000
INLINE_MAX_WIDTHS = 6
INLINE_MIN_WIDTH = 240
INLINE_MAX_WIDTH = 3840
INLINE_VIEWPORT_HEIGHT = 900
INLINE_THEMES = ("light", "dark")
# The largest result a script may hand back; bounds the wire response.
INLINE_MAX_MEASUREMENT_CHARS = 5_000_000


def _inline_limit(key: str, mirror: float) -> float:
    """Read the live knowledge.scraper knob, retaining its seeded standalone value."""
    return float(parser_knob(f"inline_inspect.{key}", mirror))


class InlineInspectTimeout(Exception):
    """The whole inline inspection exceeded its hard budget — retryable."""


@dataclass
class InlineCapture:
    width: int
    theme: str
    viewport_height: int
    measurements: Any = None
    error: str | None = None
    console_errors: list[str] = field(default_factory=list)
    screenshot_png: bytes | None = None
    screenshot_width: int = 0
    screenshot_height: int = 0
    screenshot_error: str | None = None


def wrap_html(html: str) -> str:
    """A full document is used as given; anything else is wrapped in a minimal one."""
    head = html.lstrip()[:512].lower()
    if head.startswith("<!doctype") or "<html" in head:
        return html
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<style>html,body{margin:0;padding:0}</style></head><body>"
        f"{html}</body></html>"
    )


# Runs in the page. Receives the script text; returns {ok, json} or {ok:false, error}.
_RUN_SCRIPT_JS = r"""async (src) => {
  const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
  let run;
  try {
    // One expression? Then it is evaluated and awaited. Otherwise a function body.
    try { run = new AsyncFunction('return (\n' + src + '\n)'); }
    catch (_) { run = new AsyncFunction(src); }
  } catch (e) {
    return {ok: false, error: 'measure_script does not parse: ' + (e && e.message ? e.message : String(e))};
  }
  let value;
  try { value = await run(); }
  catch (e) {
    return {ok: false, error: 'measure_script threw: ' + (e && e.stack ? e.stack : (e && e.message) || String(e))};
  }
  if (value === undefined) {
    return {ok: false, error: 'measure_script returned undefined (a function-body script must `return` its result)'};
  }
  let text;
  try { text = JSON.stringify(value); }
  catch (e) { return {ok: false, error: 'measure_script result is not JSON-serialisable: ' + e.message}; }
  if (text === undefined) {
    return {ok: false, error: 'measure_script result is not JSON-serialisable (got a function or symbol)'};
  }
  return {ok: true, json: text};
}"""


async def _capture_one(
    context: Any,
    *,
    document: str,
    measure_script: str | None,
    width: int,
    theme: str,
    screenshot: bool,
) -> InlineCapture:
    capture = InlineCapture(width=width, theme=theme, viewport_height=INLINE_VIEWPORT_HEIGHT)
    page = await context.new_page()
    try:
        load_timeout_ms = int(_inline_limit("load_timeout_ms", 15_000))
        settle_seconds = _inline_limit("settle_seconds", 0.4)
        script_timeout_ms = int(_inline_limit("script_timeout_ms", 15_000))
        screenshot_timeout_ms = int(_inline_limit("screenshot_timeout_ms", 15_000))
        await page.set_viewport_size({"width": width, "height": INLINE_VIEWPORT_HEIGHT})
        page.on("console", lambda msg: capture.console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: capture.console_errors.append(f"Uncaught: {exc}"))
        try:
            await page.set_content(document, wait_until="load", timeout=load_timeout_ms)
            await asyncio.sleep(settle_seconds)
        except Exception as exc:  # noqa: BLE001 — reported on the capture, never silent
            capture.error = f"page did not load: {type(exc).__name__}: {exc}"
            return capture

        if measure_script is not None:
            try:
                outcome = await asyncio.wait_for(
                    page.evaluate(_RUN_SCRIPT_JS, measure_script),
                    timeout=script_timeout_ms / 1000,
                )
            except TimeoutError:
                capture.error = f"measure_script did not finish within {script_timeout_ms} ms"
            except Exception as exc:  # noqa: BLE001
                capture.error = f"measure_script could not run: {type(exc).__name__}: {exc}"
            else:
                if not outcome.get("ok"):
                    capture.error = str(outcome.get("error") or "measure_script failed")
                elif len(outcome["json"]) > INLINE_MAX_MEASUREMENT_CHARS:
                    capture.error = (
                        f"measure_script result is {len(outcome['json'])} chars; "
                        f"the limit is {INLINE_MAX_MEASUREMENT_CHARS}"
                    )
                else:
                    capture.measurements = json.loads(outcome["json"])

        if screenshot:
            try:
                png = await page.screenshot(
                    full_page=True,
                    type="png",
                    timeout=screenshot_timeout_ms,
                    animations="disabled",
                    caret="hide",
                )
                capture.screenshot_png = png
                capture.screenshot_width, capture.screenshot_height = png_dimensions(png)
            except Exception as exc:  # noqa: BLE001 — missing evidence is reported
                capture.screenshot_error = f"{type(exc).__name__}: {exc}"
    finally:
        await page.close()
    return capture


async def run_inline_inspection(
    pool: Any,
    html: str,
    *,
    measure_script: str | None,
    widths: list[int],
    themes: list[str],
    screenshot: bool = True,
    hard_budget_seconds: float | None = None,
) -> list[InlineCapture]:
    """One capture per width x theme, ordered themes-major then widths."""
    for theme in themes:
        if theme not in INLINE_THEMES:
            raise ValueError(f"theme must be one of {INLINE_THEMES}, got {theme!r}")
    for width in widths:
        if not INLINE_MIN_WIDTH <= width <= INLINE_MAX_WIDTH:
            raise ValueError(f"width {width} outside {INLINE_MIN_WIDTH}..{INLINE_MAX_WIDTH}")
    document = wrap_html(html)
    captures: list[InlineCapture] = []

    async def _run() -> None:
        browser = await pool.acquire(timeout=30.0)
        try:
            for theme in themes:
                context = await browser.new_context(
                    viewport={"width": widths[0], "height": INLINE_VIEWPORT_HEIGHT},
                    color_scheme=theme,
                    device_scale_factor=1.0,
                    is_mobile=False,
                    has_touch=False,
                )
                await install_egress_guard(context)
                try:
                    for width in widths:
                        captures.append(
                            await _capture_one(
                                context,
                                document=document,
                                measure_script=measure_script,
                                width=width,
                                theme=theme,
                                screenshot=screenshot,
                            )
                        )
                finally:
                    await context.close()
        finally:
            pool.release(browser)

    if hard_budget_seconds is None:
        hard_budget_seconds = _inline_limit("hard_budget_seconds", 90.0)
    try:
        await asyncio.wait_for(_run(), timeout=hard_budget_seconds)
    except TimeoutError as exc:
        raise InlineInspectTimeout(
            f"Timed out inspecting inline html (budget {hard_budget_seconds}s)."
        ) from exc
    return captures

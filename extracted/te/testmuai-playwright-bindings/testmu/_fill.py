"""``testmu.fill``: the whole text-entry sequence a generated fill step runs.

1. Click the field to focus it (best-effort: a click a covering element or a
   non-clickable field refuses must not fail the step, the fill below does).
2. ``Locator.fill`` with the value coerced by ``as_text`` (a ``var()`` value
   can be a number).
3. Press ``End`` (best-effort). ``fill()`` fires only ``input``, no
   keydown/keyup, so a page that reacts from ``onkeyup`` (a form enabling a
   control once the field has text) would never see the typing. A caret-only
   key fires real key events without changing the value.

``timeout`` and ``reprobe`` go to every call, so with ``reprobe`` no part of
the sequence acts on the recorded (stale) locator: each verb re-locates the
field by the step's current description through the installed heal patch.

With ``delay`` (milliseconds), steps 2 and 3 become real typing, for fields that
react to keystrokes and ignore a ``fill``: clear with ``fill("")`` (a key-driven
widget refuses that, so it gets select-all instead), then ``press_sequentially``. Playwright's timeout covers the whole typing call, so
the typing timeout grows with the text: the ``timeout`` (or 5s) plus
``len(text) * delay``.

Shared (not per mode). ``as_text`` comes from the active mode's package. TS
twin: ``src/fill.ts``.
"""
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from testmu import _router

# The best-effort focus click and End press give up quickly: the fill itself
# carries the real wait and the real error.
_BEST_EFFORT_TIMEOUT_MS = 2000
_DELAY_BASE_TIMEOUT_MS = 5000


async def fill(locator, value, *, timeout=None, reprobe=False, delay=0):
    opts = {}
    if timeout is not None:
        opts["timeout"] = timeout
    if reprobe:
        opts["reprobe"] = True
    try:
        await locator.click(**{"timeout": _BEST_EFFORT_TIMEOUT_MS, **opts})
    except Exception:  # noqa: BLE001
        pass
    text = _router.impl().as_text(value)
    if delay:
        try:
            await locator.fill("", **opts)
        except PlaywrightTimeoutError:
            raise
        except Exception:  # noqa: BLE001
            await locator.press("ControlOrMeta+a", **opts)
        base = timeout if timeout is not None else _DELAY_BASE_TIMEOUT_MS
        typing_opts = {**opts, "delay": delay, "timeout": base + len(text) * delay}
        await locator.press_sequentially(text, **typing_opts)
        return
    await locator.fill(text, **opts)
    try:
        await locator.press("End", **{**opts, "timeout": _BEST_EFFORT_TIMEOUT_MS})
    except Exception:  # noqa: BLE001
        pass

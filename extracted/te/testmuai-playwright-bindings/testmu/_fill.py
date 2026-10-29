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

Shared (not per mode). ``as_text`` comes from the active mode's package. TS
twin: ``src/fill.ts``.
"""
from testmu import _router

# The best-effort focus click and End press give up quickly: the fill itself
# carries the real wait and the real error.
_BEST_EFFORT_TIMEOUT_MS = 2000


async def fill(locator, value, *, timeout=None, reprobe=False):
    opts = {}
    if timeout is not None:
        opts["timeout"] = timeout
    if reprobe:
        opts["reprobe"] = True
    try:
        await locator.click(**{"timeout": _BEST_EFFORT_TIMEOUT_MS, **opts})
    except Exception:  # noqa: BLE001
        pass
    await locator.fill(_router.impl().as_text(value), **opts)
    try:
        await locator.press("End", **{**opts, "timeout": _BEST_EFFORT_TIMEOUT_MS})
    except Exception:  # noqa: BLE001
        pass

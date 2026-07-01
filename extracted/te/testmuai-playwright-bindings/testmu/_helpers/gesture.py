"""Click-gesture helpers for Playwright (V3 click_modifier port).

Async Playwright port of the V2 source ``_validate_click_modifier``
/ ``_do_multi_click`` (spec §5.5/§5.6). Two surfaces:

- ``validate_click_modifier(click_modifier)`` — Layer-2 runtime validation +
  normalization of a resolved ``click_modifier`` dict. Mutates in place:
  coerces ``duration``→float / ``frequency``→int, clears the dict for
  ``frequency == 1`` (caller falls through to a plain click), raises
  ``ValueError`` on out-of-bounds. Bounds are identical to V2.
- ``multi_click(locator, *, frequency, gap=0.1)`` — the only ``multi_click``
  case needing a binding change: ``frequency > 2``. ``frequency == 2`` is a
  native ``dblclick`` (emitted directly by the code generator) and ``right_click`` is a native
  ``click(button='right')`` — neither reaches this module. Validates, then runs
  ``multi_click_loop`` (N × ``click()`` spaced by ``asyncio.sleep(gap)``).

The +0.1s long-press buffer lives in ``_action_specs._long_press_runner`` (not
here): long_press dispatches through the verb spec / heal cascade, multi_click
loops on the locator directly.
"""
from __future__ import annotations

import asyncio
import logging

from testmu._vars import var

_log = logging.getLogger("testmu")


def validate_click_modifier(click_modifier):
    """Validate + normalize a resolved click_modifier dict in place.

    Parity with V2 source ``_validate_click_modifier`` (identical bounds):
      - ``long_press``: ``duration`` coerced to float, must be 0.1..30.
      - ``multi_click``: ``frequency`` a whole number 2..20 (bool rejected;
        float must be integral; str parsed). ``frequency == 1`` clears the dict
        (caller does a plain click).
      - ``right_click``: no ``duration``/``frequency`` keys permitted.

    Raises ``ValueError`` on any out-of-bounds / non-numeric value, or on a
    missing required scalar (``long_press`` without ``duration`` /
    ``multi_click`` without ``frequency`` — the code generator never legitimately emits one).
    """
    if not click_modifier:
        return
    kind = click_modifier.get("kind")
    if kind == "long_press":
        raw = click_modifier.get("duration")
        if raw is None:
            # the code generator never legitimately emits a scalar-less gesture; raise loudly
            # instead of silently skipping (3-surface parity with sel-py/sel-java).
            raise ValueError("Long press requires a 'duration' scalar (0.1..30 seconds).")
        try:
            duration = float(raw)
        except (TypeError, ValueError):
            duration = None
        if duration is None or not 0.1 <= duration <= 30:
            raise ValueError(
                f"Long press duration must be a number between 0.1 and 30 seconds, got: {raw!r}."
            )
        click_modifier["duration"] = duration
    elif kind == "multi_click":
        raw = click_modifier.get("frequency")
        if raw is None:
            raise ValueError("Multi-click requires a 'frequency' scalar (whole number 2..20).")
        frequency = None
        try:
            if isinstance(raw, bool):
                pass
            elif isinstance(raw, int):
                frequency = raw
            elif isinstance(raw, float) and raw.is_integer():
                frequency = int(raw)
            elif isinstance(raw, str):
                f = float(raw)
                if f.is_integer():
                    frequency = int(f)
        except (TypeError, ValueError):
            frequency = None
        if frequency == 1:
            # frequency=1 → plain click; empty dict signals the caller to tap once.
            click_modifier.clear()
            return
        if frequency is None or not 2 <= frequency <= 20:
            raise ValueError(
                f"Multi-click frequency must be a whole number between 2 and 20, got: {raw!r}."
            )
        click_modifier["frequency"] = frequency
    elif kind == "right_click":
        if "duration" in click_modifier or "frequency" in click_modifier:
            raise ValueError("click_modifier(right_click): no additional fields allowed")


def resolve_click_modifier_variables(click_modifier):
    """Resolve data-driven gesture params against the binding variable store.

    Export-path mirror of selenium-python ``resolve_click_modifier_variables``
    (plan Task 25). A data-driven long_press/multi_click carries the raw
    ``{{var}}``/``${param}`` text under ``click_modifier['variables']``
    ({'frequency'|'duration': template}); the scalar field holds a Layer-1
    placeholder. Resolve each template via ``testmu._vars.var`` — the V3 export
    resolver, whose store is populated by the generated ``set_var`` calls and
    which is type-preserving (``var('{{n}}')`` returns the stored int/float) —
    write the result back onto ``frequency``/``duration``, and drop the carrier
    so the downstream validator/runner sees a plain resolved dict. Mutates in
    place and returns the dict. Call this BEFORE ``validate_click_modifier`` in
    the gesture dispatch. Mirrors V2 source ``_handle_click_modifier``.
    """
    if not isinstance(click_modifier, dict):
        return click_modifier
    variables = click_modifier.get("variables")
    if isinstance(variables, dict) and variables:
        for field, template in variables.items():
            resolved = var(template)
            if field == "frequency":
                click_modifier["frequency"] = resolved
            elif field == "duration":
                click_modifier["duration"] = resolved
        click_modifier.pop("variables", None)
    return click_modifier


async def multi_click_loop(locator, frequency, gap):
    """Click ``locator`` ``frequency`` times, sleeping ``gap`` seconds between
    clicks (no trailing sleep). Parity with V2 ``_do_multi_click`` freq>2 loop."""
    for i in range(frequency):
        await locator.click()
        if i < frequency - 1:
            await asyncio.sleep(gap)


def _is_selectorless(locator) -> bool:
    """True when ``locator`` is a selectorless ``VisionLocator`` (heal-by-
    description) rather than a concrete Playwright Locator. Lazy import keeps
    ``_helpers.gesture`` free of a module-level cycle (``_vision_locator``
    imports this module)."""
    from testmu._vision_locator import VisionLocator
    return isinstance(locator, VisionLocator)


async def multi_click(locator, *, frequency, gap=0.1, variables=None):
    """Public V3 multi_click entry (freq>2). Resolves templates, validates, loops.

    ``locator`` is a ``VisionLocator`` (selectorless, emitted as
    ``testmu.locator(page, description=...)``) or a real Playwright Locator —
    both expose an awaitable ``click()``. ``gap`` defaults to 0.1s (V3
    multi_click never carries a duration). ``variables`` carries a data-driven
    ``{'frequency': '<template>'}`` map (the code generator templated emit); when present it is
    resolved via ``resolve_click_modifier_variables`` BEFORE validation, so a
    ``${count}``/``{{count}}`` frequency drives the loop count. ``frequency == 1``
    degrades to a single click (defensive; the code generator only emits this helper for freq>2).

    Selectorless freq>2 resolves the target ONCE through the heal engine and
    clicks that single resolved Locator/coordinate N times (V2 parity), instead
    of re-running the full heal/vision cascade on every click.
    """
    cm = {"kind": "multi_click", "frequency": frequency}
    if variables:
        cm["variables"] = variables
        resolve_click_modifier_variables(cm)
    validate_click_modifier(cm)
    if not cm:  # frequency == 1 cleared the dict → plain click
        await locator.click()
        return
    freq = cm["frequency"]
    if freq == 2:
        # freq==2 → native dblclick DOM event (text-selection semantics, RFC
        # §4.2.6), not two discrete single clicks. The code generator emits dblclick() natively
        # for a literal 2, but a templated frequency resolving to 2 reaches this
        # helper — keep 3-surface parity with sel-py do_multi_click / sel-java
        # gestureClick, which both special-case freq==2. For a VisionLocator,
        # .dblclick() already runs a single heal cascade — no resolve-once concern.
        _log.info("    [multi_click] frequency=2 -> native dblclick")
        await locator.dblclick()
        return
    if _is_selectorless(locator):
        # Resolve the selectorless target ONCE via the engine; the
        # MULTI_CLICK_SPEC runner clicks that single resolved Locator/coordinate
        # `freq` times (one heal cascade, not `freq` of them).
        from testmu._action_engine import _run_verb
        from testmu._action_specs import MULTI_CLICK_SPEC
        _log.info("    [multi_click] selectorless frequency=%s gap=%ss -> resolve once", freq, gap)
        await _run_verb(
            locator._page, None, MULTI_CLICK_SPEC,
            description=locator._description, verb_name="multi_click",
            frequency=freq, gap=gap,
        )
        return
    _log.info("    [multi_click] frequency=%s gap=%ss", freq, gap)
    await multi_click_loop(locator, freq, gap)


async def long_press(locator, *, duration, variables=None):
    """Public V3 long_press entry for a SELECTOR-bound (DOM) Playwright Locator.

    Sibling of ``multi_click`` (top-level function taking a locator), so the
    selector-bound code-generator emit can reuse a binding entrypoint the way it does for
    multi_click. The selectorless path uses the ``VisionLocator.long_press``
    METHOD — which a real Playwright Locator does NOT have — so a selector-bound
    long_press must call ``testmu.long_press(<locator>, duration=...)`` instead.

    ``variables`` carries a data-driven ``{'duration': '<template>'}`` map; when
    present it is resolved via ``resolve_click_modifier_variables`` BEFORE
    validation. Bounds are validated (0.1..30s); the +0.1s hold buffer is applied
    by the shared ``_long_press_runner`` (hover → mouse.down → hold → mouse.up).

    A ``VisionLocator`` passed here is delegated to its own heal-routed method
    (single resolve), keeping the entrypoint correct for both locator shapes.
    """
    if _is_selectorless(locator):
        return await locator.long_press(duration=duration, variables=variables)
    cm = {"kind": "long_press", "duration": duration}
    if variables:
        cm["variables"] = variables
        resolve_click_modifier_variables(cm)
    validate_click_modifier(cm)
    from testmu._action_specs import _long_press_runner
    _log.info("    [long_press] selector-bound duration=%ss", cm["duration"])
    return await _long_press_runner(locator, duration=cm["duration"])


__all__ = [
    "validate_click_modifier",
    "resolve_click_modifier_variables",
    "multi_click",
    "multi_click_loop",
    "long_press",
]

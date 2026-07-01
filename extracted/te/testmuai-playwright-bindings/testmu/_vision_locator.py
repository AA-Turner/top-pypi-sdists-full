"""VisionLocator — the vision-agent empty-selector entry point.

When codegen has no selector to build a Playwright Locator from (vision-agent
op), it emits ``await testmu.locator(page, description=...).<verb>(...)``.
Each verb method dispatches straight to the heal cascade — there's no
"original locator" to try first because there's no selector.

When codegen has a selector (V3 press-key element-targeting), it emits:
    ``await testmu.locator(page, SEL_NNN, description=...).<verb>(...)``.
The selector is a list of ``{'selector': str, 'isXPath': bool}`` dicts (same
shape as drag_drop). A non-empty list means "try this selector first, heal on
timeout"; an empty list means "heal-by-description immediately" (cascade with
locator=None). The discriminator is ``is not None``, not truthiness — an empty
list is a valid selector value.

Replaces the previous ``testmu.heal_action(page, desc, method)`` design
which only worked for coordinate-healable verbs and forced codegen into
contortions for clear/fill/type/etc.
"""
from __future__ import annotations

import logging
from typing import Optional

from testmu._action_engine import _run_verb
from testmu._action_specs import _VERB_SPECS, _resolve_file_input_dom
from testmu._helpers.gesture import resolve_click_modifier_variables, validate_click_modifier

_log = logging.getLogger(__name__)


def _build_locator_from_selector_list(page, selector_list: list):
    """Build a Playwright Locator from the first entry in a selector list.

    Mirrors drag._build_locator: xpath selectors get the ``xpath=`` engine
    prefix; CSS selectors pass through unchanged so Playwright's default
    engine handles them.

    Args:
        page: Playwright Page (or frame scope).
        selector_list: Non-empty list of ``{'selector': str, 'isXPath': bool}`` dicts.

    Returns:
        A Playwright Locator built from ``selector_list[0]``.
    """
    sel = selector_list[0]
    raw = sel.get("selector", "")
    if sel.get("isXPath"):
        return page.locator(f"xpath={raw}")
    return page.locator(raw)


class VisionLocator:
    """Thin async wrapper. Terminal actions only (no chaining like .first(),
    .nth(), .locator() — by design for v0.3.0; add later if the code generator needs them).
    """

    __slots__ = ("_page", "_description", "_selector")

    def __init__(self, page, selector: Optional[list] = None, *, description: str):
        self._page = page
        self._description = description
        # None = no selector (current description-only path); [] = heal-by-description
        # immediately; [{...}] = try this selector first, heal on timeout.
        self._selector = selector

    def __repr__(self) -> str:
        return f"VisionLocator(description={self._description!r})"

    # -------------------------------------------------------------------
    # Pointer verbs
    # -------------------------------------------------------------------

    async def click(self, **kwargs):
        return await _run_verb(
            self._page, None, _VERB_SPECS["click"],
            description=self._description, verb_name="click", **kwargs,
        )

    async def dblclick(self, **kwargs):
        return await _run_verb(
            self._page, None, _VERB_SPECS["dblclick"],
            description=self._description, verb_name="dblclick", **kwargs,
        )

    async def hover(self, **kwargs):
        return await _run_verb(
            self._page, None, _VERB_SPECS["hover"],
            description=self._description, verb_name="hover", **kwargs,
        )

    async def long_press(self, *, duration, variables=None, **kwargs):
        """V3 long-press gesture (hover → mouse.down → hold → mouse.up).

        ``variables`` carries a data-driven ``{'duration': '<template>'}`` map
        (the code generator templated emit); when present it is resolved via
        ``resolve_click_modifier_variables`` against the binding variable store
        BEFORE validation, so a ``{{holdTime}}``/``${holdTime}`` duration drives
        the hold. Validates ``duration`` against the V2 bounds (0.1..30s) before
        dispatch; the +0.1s hold buffer is applied in the LONG_PRESS_SPEC runner.
        Routes through the heal cascade like every other VisionLocator verb
        (locator=None → resolve-by-description → run on the fresh locator, or a
        COORDINATE-tier fallback via the coord runner — the resolved scalar is
        forwarded to either tier).
        """
        cm = {"kind": "long_press", "duration": duration}
        if variables:
            cm["variables"] = variables
            resolve_click_modifier_variables(cm)
        validate_click_modifier(cm)
        return await _run_verb(
            self._page, None, _VERB_SPECS["long_press"],
            description=self._description, verb_name="long_press",
            duration=cm["duration"], **kwargs,
        )

    # -------------------------------------------------------------------
    # Text-input verbs
    # -------------------------------------------------------------------

    async def clear(self, **kwargs):
        return await _run_verb(
            self._page, None, _VERB_SPECS["clear"],
            description=self._description, verb_name="clear", **kwargs,
        )

    async def fill(self, value, **kwargs):
        return await _run_verb(
            self._page, None, _VERB_SPECS["fill"], value,
            description=self._description, verb_name="fill", **kwargs,
        )

    async def type(self, text, **kwargs):
        return await _run_verb(
            self._page, None, _VERB_SPECS["type"], text,
            description=self._description, verb_name="type", **kwargs,
        )

    async def press(self, key, **kwargs):
        # Selector-bearing path (V3 press-key element-targeting).
        # Discriminator is ``is not None``, NOT truthiness — [] is a valid
        # heal-by-description selector that must also go through _run_verb.
        if self._selector is not None:
            if self._selector:
                # Non-empty: build a PW Locator and try it first; the engine
                # heals on timeout via the cascade. Mirrors how _heal_patch.py
                # routes selector-bearing verbs (locator is not None → try first).
                pw_locator = _build_locator_from_selector_list(self._page, self._selector)
            else:
                # Empty list: no selector to try; go straight to cascade.
                pw_locator = None
            return await _run_verb(
                self._page, pw_locator, _VERB_SPECS["press"], key,
                description=self._description, verb_name="press", **kwargs,
            )
        # No selector at all: current description-only / global-press path.
        return await _run_verb(
            self._page, None, _VERB_SPECS["press"], key,
            description=self._description, verb_name="press", **kwargs,
        )

    # -------------------------------------------------------------------
    # File upload + scroll
    # -------------------------------------------------------------------

    async def set_input_files(self, files, **kwargs):
        # V2 handle_upload parity (mirrors selenium-python _resolve_file_input_dom):
        # a selectorless vision upload resolves the <input type=file> via pure DOM
        # first (light + open shadow) because the DESKTOP_LOCATE/VISION_QUERY heal
        # can't anchor on a hidden file input (commonly display:none behind a styled
        # trigger). First-match like Selenium; a miss/failure falls through to the
        # heal cascade unchanged. Multi-input pages take the first input (V2 parity).
        element = await _resolve_file_input_dom(self._page)
        if element is not None:
            try:
                await element.set_input_files(files)
                return
            except Exception:
                _log.info(
                    "    [upload] DOM-first set_input_files failed; falling back to heal",
                    exc_info=True,
                )
        return await _run_verb(
            self._page, None, _VERB_SPECS["set_input_files"], files,
            description=self._description, verb_name="set_input_files", **kwargs,
        )

    async def scroll_into_view_if_needed(self, **kwargs):
        return await _run_verb(
            self._page, None, _VERB_SPECS["scroll_into_view_if_needed"],
            description=self._description,
            verb_name="scroll_into_view_if_needed",
            **kwargs,
        )


def locator(page, selector: Optional[list] = None, *, description: str) -> VisionLocator:
    """Factory for VisionLocator. Codegen-facing entry point.

    Two call shapes::

        # Description-only (vision-agent / no selector):
        await testmu.locator(page, description='Submit button').click()

        # Selector-bearing (V3 press-key element-targeting and future verbs):
        SEL_001 = [{"selector": "//button", "isXPath": True}]
        await testmu.locator(page, SEL_001, description='Submit button').press('Enter')

    ``selector`` is a list of ``{'selector': str, 'isXPath': bool}`` dicts. A
    non-empty list routes press (and future selector-bearing verbs) through the
    heal cascade with a PW Locator built from the first entry. An empty list
    routes directly to the cascade (heal-by-description). ``None`` (default)
    keeps the existing description-only path.
    """
    return VisionLocator(page, selector, description=description)


__all__ = ["VisionLocator", "locator"]

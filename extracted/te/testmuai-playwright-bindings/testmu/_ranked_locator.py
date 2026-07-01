"""Ranked-selector resolution + wrong-element heal for the Playwright runtime.

When codegen has multiple ranked candidate selectors for one element it emits::

    await testmu.resolve_ranked_locator(
        page, [page.locator("#a"), page.locator("#b")], description="email field"
    )

This module owns that resolution so the generated test body stays thin (a single
call) instead of carrying a ~95-line helper preamble inlined into *every* file —
keeping parity with the rest of the binding, where the generated code imports
runtime helpers (``testmu.step``, ``testmu.locator``, ...) rather than inlining
them.

Behaviour:
  * Tries each Playwright Locator in rank order and returns the first whose
    ``count() > 0`` — Selenium's sequential-try semantics rather than
    Playwright's ``.or_().first`` union (which picks by DOM order, not rank).
  * V3 (a ``description`` is provided):
      - a ranked MATCH is wrapped in ``_HealingLocator`` so an action that raises
        a Playwright error (e.g. the matched element is a wrong, non-input
        container) falls through to the description-based vision heal instead of
        hard-failing.
      - on exhaustion (no selector matches) returns ``locator(page,
        description=description)`` — a VisionLocator that heals on the awaited
        action.
  * V4 (``description`` omitted): returns the bare locator, or raises
    ``TimeoutError`` on exhaustion.
"""
from __future__ import annotations

from playwright.async_api import Error as _PlaywrightError

from testmu._vision_locator import locator


class _HealingLocator:
    """Wrap a ranked-selector MATCH so an action that fails because the matched
    element is the wrong one (e.g. ``Locator.fill`` on a non-input container that
    a structural selector happened to match) falls through to description-based
    vision heal instead of raising an unrecoverable Playwright error.

    Parity with the Selenium binding's recoverable-exception heal cascade, in the
    correct direction — genuine recovery via the existing ``VisionLocator``, not a
    silent swallow. Only used on the V3 path (a description is present); V4
    callers receive the bare locator. All non-action attributes (count, nth,
    locator, first, ...) pass through unchanged, so the wrapper is a drop-in for
    the raw Locator.
    """

    # Async action methods that can raise on a wrong / non-actionable element
    # and for which a description-based vision retry is meaningful.
    _HEAL_ACTIONS = frozenset((
        "click", "dblclick", "fill", "type", "press", "press_sequentially",
        "check", "uncheck", "set_checked", "select_option", "set_input_files",
        "hover", "tap", "clear", "focus", "drag_to",
    ))

    def __init__(self, page, loc, description):
        self._page = page
        self._loc = loc
        self._description = description

    def __getattr__(self, name):
        # Guard the private slots: they are real instance attributes, so they
        # never reach __getattr__ in normal flow — raising here prevents an
        # infinite recursion through self._loc if one is ever missing.
        if name.startswith("_"):
            raise AttributeError(name)
        attr = getattr(self._loc, name)
        if name not in self._HEAL_ACTIONS or not self._description:
            return attr

        async def _healed(*args, **kwargs):
            # Unwrap any wrapped locator arguments (e.g. drag_to(target)) so
            # Playwright's Locator type-check on the argument still passes.
            args = tuple(a._loc if isinstance(a, _HealingLocator) else a for a in args)
            kwargs = {k: (v._loc if isinstance(v, _HealingLocator) else v)
                      for k, v in kwargs.items()}
            try:
                return await attr(*args, **kwargs)
            except _PlaywrightError:
                # A genuine Playwright error on the matched element — heal via
                # the description. Non-Playwright exceptions propagate untouched.
                _vision = locator(self._page, description=self._description)
                # VisionLocator implements only a subset of _HEAL_ACTIONS; for a
                # verb it lacks, surface the ORIGINAL Playwright error rather than
                # masking it with an AttributeError from getattr.
                if not hasattr(_vision, name):
                    raise
                return await getattr(_vision, name)(*args, **kwargs)

        return _healed


async def resolve_ranked_locator(page, locators, description=""):
    """Return the first locator in *locators* that matches at least one element.

    See the module docstring for the V3 (heal-wrapped) vs V4 (bare) semantics.
    """
    for _loc in locators:
        if await _loc.count() > 0:
            if description:
                return _HealingLocator(page, _loc, description)
            return _loc
    if description:
        return locator(page, description=description)
    raise TimeoutError("ranked locator resolution exhausted — no selector matched")

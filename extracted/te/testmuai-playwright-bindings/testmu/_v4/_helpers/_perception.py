"""One perception backend per page: how this binding sees and acts on a page.

Chromium speaks CDP; Firefox does not, so it gets the portable
aria-snapshot backend. ``perception_for(page)`` picks the backend ONCE from the
page's engine (``testmu._aria_perception.engine_of`` — the only engine reader),
and every helper calls the backend's methods instead of branching on the
engine itself. Each method delegates to the engine-specific function that
lives next to the code it replaces (``_x_cdp`` / ``_x_portable``).

A backend is an async context manager: work that spans several calls (flat
DOM, then an element snapshot, then a locator for it) shares one CDP session,
detached on exit. The portable backend holds no session.

New engine-dependent behaviour goes here as a method on both backends —
``tests/shared/test_boundaries.py`` fails on engine checks anywhere else.
"""
from __future__ import annotations

from typing import Any

from testmu._aria_perception import engine_of


class CdpPerception:
    """Chromium: the CDP implementations, unchanged."""

    engine = "chromium"
    select_all_key = "Control+a"

    def __init__(self, page):
        self.page = page
        self._cdp = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()

    async def close(self) -> None:
        """Detach the CDP session this backend opened (if any)."""
        if self._cdp is not None:
            cdp, self._cdp = self._cdp, None
            await cdp.detach()

    async def _session(self):
        if self._cdp is None:
            self._cdp = await self.page.context.new_cdp_session(self.page)
        return self._cdp

    # -- capture --------------------------------------------------------
    async def capture_forest(self, **kwargs):
        from testmu._v4._helpers.ax_tree._frame_capture import _capture_frame_forest_cdp
        return await _capture_frame_forest_cdp(self.page, **kwargs)

    async def structured_dom(self):
        from testmu._v4._helpers._dom_structured import _capture_structured_dom_cdp
        return await _capture_structured_dom_cdp(self.page)

    async def flat_dom(self) -> list[dict[str, Any]]:
        from testmu._v4._helpers._dom_capture import _capture_flat_dom_cdp
        return await _capture_flat_dom_cdp(await self._session())

    async def flat_a11y(self, viewport_only: bool = True, logger=None) -> list:
        from testmu._v4._helpers.a11y_flatten import _get_flat_a11y_tree_cdp
        return await _get_flat_a11y_tree_cdp(self.page, viewport_only=viewport_only, logger=logger)

    async def screenshot_b64(self, *, full_page: bool = False) -> str:
        from testmu._v4._helpers import vision
        capture = vision._capture_full_page_screenshot_b64_cdp if full_page else vision._capture_screenshot_b64_cdp
        return await capture(self.page)

    async def before_screenshot(self) -> None:
        return None

    # -- elements -------------------------------------------------------
    async def element_snapshot(self, node_id: int) -> dict[str, Any]:
        from testmu._v4._helpers._dom_capture import get_element_snapshot
        return await get_element_snapshot(await self._session(), node_id)

    async def enrich_locator(self, element: dict[str, Any]) -> dict[str, Any] | None:
        from testmu._v4._helpers._locator_enrichment import enrich_element_locator
        return await enrich_element_locator(await self._session(), element, page=self.page)

    async def heal_target(self, entry: dict, forest, *, want_option_index: bool) -> dict[str, Any] | None:
        from testmu._v4._helpers.autoheal_ax import _heal_target_cdp
        return await _heal_target_cdp(self.page, entry, forest, want_option_index=want_option_index)

    # -- capabilities ---------------------------------------------------
    def ensure_sse_supported(self) -> None:
        return None

    async def unsupported_vitals(self) -> list[str]:
        return []


class AriaPerception:
    """Firefox: Playwright's aria snapshot and ``aria-ref`` locators.
    Element ids are portable handles (``testmu._aria_perception._refs``)."""

    select_all_key = "ControlOrMeta+a"  # the platform's select-all (Meta on macOS)

    def __init__(self, page, engine: str):
        self.page = page
        self.engine = engine

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()

    async def close(self) -> None:
        return None

    # -- capture --------------------------------------------------------
    async def capture_forest(self, *, viewport_width: float = 1280, viewport_height: float = 800):
        from testmu._v4._helpers.aria_perception import capture_frame_forest_portable
        forest = await capture_frame_forest_portable(
            self.page, viewport_width=viewport_width, viewport_height=viewport_height,
        )
        if forest.error:
            raise RuntimeError(forest.error)  # as a failed CDP main-tree capture
        return forest

    async def structured_dom(self):
        from testmu._v4._helpers._dom_structured import _capture_structured_dom_portable
        return await _capture_structured_dom_portable(self.page)

    async def flat_dom(self) -> list[dict[str, Any]]:
        from testmu._v4._helpers._dom_capture import build_flat_dom_from_ax_tree
        from testmu._v4._helpers.aria_perception import capture_tree_portable
        return build_flat_dom_from_ax_tree(await capture_tree_portable(self.page))

    async def flat_a11y(self, viewport_only: bool = True, logger=None) -> list:
        from testmu._v4._helpers.a11y_flatten import _get_flat_a11y_tree_non_cdp
        return await _get_flat_a11y_tree_non_cdp(self.page, viewport_only=viewport_only, logger=logger)

    async def screenshot_b64(self, *, full_page: bool = False) -> str:
        from testmu._aria_perception import screenshot_png_b64
        await self.before_screenshot()
        return await screenshot_png_b64(self.page, full_page=full_page)

    async def before_screenshot(self) -> None:
        if self.engine == "firefox":
            from testmu._aria_perception import nudge_fonts
            await nudge_fonts(self.page)

    # -- elements -------------------------------------------------------
    async def element_snapshot(self, node_id: int) -> dict[str, Any]:
        from testmu._v4._helpers._dom_capture import get_element_snapshot_portable
        return await get_element_snapshot_portable(self.page, node_id)

    async def enrich_locator(self, element: dict[str, Any]) -> dict[str, Any] | None:
        from testmu._v4._helpers._locator_enrichment import _enrich_portable
        return await _enrich_portable(self.page, element)

    async def heal_target(self, entry: dict, forest, *, want_option_index: bool) -> dict[str, Any] | None:
        from testmu._v4._helpers.autoheal_ax import _heal_target_portable
        return await _heal_target_portable(self.page, entry, want_option_index=want_option_index)

    # -- capabilities ---------------------------------------------------
    def ensure_sse_supported(self) -> None:
        from testmu._errors import TestmuConfigError
        raise TestmuConfigError(
            f"SSE capture is not supported on {self.engine} yet (Chromium-only)."
        )

    async def unsupported_vitals(self) -> list[str]:
        from testmu._v4._helpers.devtools_performance import _unsupported_vitals_portable
        return await _unsupported_vitals_portable(self.page)


class _CdpOnlyPerception(CdpPerception):
    """WebKit: no portable backend yet, so the Chromium code paths, as before
    this module existed. SSE still fails clearly, and the locate a11y tree
    still comes from the grid aria-snap bundle."""

    def __init__(self, page, engine: str):
        super().__init__(page)
        self.engine = engine

    async def flat_a11y(self, viewport_only: bool = True, logger=None) -> list:
        from testmu._v4._helpers.a11y_flatten import _get_flat_a11y_tree_via_js
        return await _get_flat_a11y_tree_via_js(self.page, viewport_only=viewport_only, logger=logger)

    def ensure_sse_supported(self) -> None:
        from testmu._errors import TestmuConfigError
        raise TestmuConfigError(
            f"SSE capture is not supported on {self.engine} yet (Chromium-only)."
        )


_BACKENDS = {
    "chromium": CdpPerception,
    "firefox": lambda page: AriaPerception(page, "firefox"),
    "webkit": lambda page: _CdpOnlyPerception(page, "webkit"),
}


def perception_for(page) -> CdpPerception | AriaPerception:
    """The backend for ``page``'s engine (see the module doc)."""
    return _BACKENDS[engine_of(page)](page)

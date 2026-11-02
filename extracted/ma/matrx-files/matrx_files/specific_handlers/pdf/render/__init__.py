"""PDF page render helpers — page → PNG, with optional overlays."""

from .overlay import (
    OverlayBbox,
    OverlaySpec,
    RenderedPage,
    render_page_with_overlay,
    render_page_with_overlay_async,
)


__all__ = [
    "OverlayBbox",
    "OverlaySpec",
    "RenderedPage",
    "render_page_with_overlay",
    "render_page_with_overlay_async",
]

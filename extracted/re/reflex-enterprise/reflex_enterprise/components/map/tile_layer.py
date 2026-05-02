"""TileLayer component for leaflet."""

from __future__ import annotations

import reflex as rx

from reflex_enterprise.components.map.base import BaseLeafletComponent


class TileLayer(BaseLeafletComponent):
    """TileLayer component for leaflet."""

    tag = "TileLayer"

    # URL template for tile layer
    url: rx.Var[str]

    # The opacity of the tile layer (0.0 - 1.0)
    opacity: rx.Var[float]

    # The map pane where the tile layer will be added
    pane: rx.Var[str]

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        """Create a TileLayer component."""
        # props["class_name"] = "dark:map-tiles" # noqa: ERA001
        return super().create(*children, **props)

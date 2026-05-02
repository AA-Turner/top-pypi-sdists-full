"""Map module for Reflex Enterprise."""

from __future__ import annotations

from reflex.components.component import ComponentNamespace

from .base import MapAPI
from .controls import (
    AttributionControl,
    LayersControl,
    LayersControlBaseLayer,  # noqa: F401
    LayersControlOverlay,  # noqa: F401
    ScaleControl,
    ZoomControl,
)
from .map_container import MapContainer
from .marker import Marker
from .popup import Popup
from .tile_layer import TileLayer
from .tooltip import Tooltip
from .types import (
    LatLng,
    LatLngBounds,
    LocateOptions,
    ZoomEvent,
    ZoomLevelsChangeEvent,
    latlng,
    latlng_bounds,
    locate_options,
)
from .vectors import (
    Circle,
    CircleMarker,
    PathOptions,
    Polygon,
    Polyline,
    Rectangle,
    SVGOverlay,
    path_options,
)


class MapNamespace(ComponentNamespace):
    """Namespace for map components."""

    __call__ = staticmethod(MapContainer.create)

    # Controls
    zoom_control = staticmethod(ZoomControl.create)
    attribution_control = staticmethod(AttributionControl.create)
    scale_control = staticmethod(ScaleControl.create)
    layers_control = staticmethod(LayersControl.create)
    # layers_control_base_layer = staticmethod(LayersControlBaseLayer.create)
    # layers_control_overlay = staticmethod(LayersControlOverlay.create)

    # Basic layers
    tile_layer = staticmethod(TileLayer.create)
    marker = staticmethod(Marker.create)
    popup = staticmethod(Popup.create)
    tooltip = staticmethod(Tooltip.create)

    # Vector layers
    circle = staticmethod(Circle.create)
    circle_marker = staticmethod(CircleMarker.create)
    polyline = staticmethod(Polyline.create)
    polygon = staticmethod(Polygon.create)
    rectangle = staticmethod(Rectangle.create)
    svg_overlay = staticmethod(SVGOverlay.create)

    # Events and types
    ZoomEvent: type[ZoomEvent] = ZoomEvent
    ZoomLevelsChangeEvent: type[ZoomLevelsChangeEvent] = ZoomLevelsChangeEvent
    LatLng: type[LatLng] = LatLng
    LatLngBounds: type[LatLngBounds] = LatLngBounds
    LocateOptions: type[LocateOptions] = LocateOptions
    PathOptions: type[PathOptions] = PathOptions

    # Helper functions
    latlng = staticmethod(latlng)
    latlng_bounds = staticmethod(latlng_bounds)
    locate_options = staticmethod(locate_options)
    path_options = staticmethod(path_options)
    api = staticmethod(MapAPI.create)


map = MapNamespace()

__all__ = ["map"]

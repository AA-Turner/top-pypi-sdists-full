"""Control components for leaflet maps."""

from typing import Literal

from reflex.vars.base import Var

from .base import BaseLeafletComponent


class PositionControl(BaseLeafletComponent):
    """Position Mixin for Control components."""

    # The position of the control (topleft, topright, bottomleft, bottomright)
    position: Var[Literal["topleft", "topright", "bottomleft", "bottomright"]]


class ZoomControl(PositionControl):
    """ZoomControl component for leaflet."""

    tag = "ZoomControl"


class AttributionControl(PositionControl):
    """Attribution control for leaflet maps."""

    tag = "AttributionControl"


class LayersControl(PositionControl):
    """Layers control for leaflet maps.

    This component allows users to switch between different base layers and toggle overlays.
    """

    tag = "LayersControl"

    # Whether the control should be collapsed (true) or expanded (false)
    collapsed: Var[bool]


class LayersControlBaseLayer(BaseLeafletComponent):
    """Base layer option for the LayersControl.

    This component should be used as a child of LayersControl.
    """

    tag = "LayersControl.BaseLayer"

    # Display name for the layer in the control
    name: Var[str]

    # Whether the layer should be selected by default
    checked: Var[bool]


class LayersControlOverlay(BaseLeafletComponent):
    """Overlay layer option for the LayersControl.

    This component should be used as a child of LayersControl.
    """

    tag = "LayersControl.Overlay"

    # Display name for the layer in the control
    name: Var[str]

    # Whether the overlay should be visible by default
    checked: Var[bool]


class ScaleControl(PositionControl):
    """Scale control for leaflet maps.

    Displays a scale indicator showing the distance in metric/imperial units.
    """

    tag = "ScaleControl"

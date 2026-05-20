"""Marker component for displaying a marker on a map."""

from reflex.vars.base import Var

from .base import InteractiveLeafletLayer
from .types import LatLng, MouseEvent  # noqa: F401


class Marker(InteractiveLeafletLayer):
    """Marker component for displaying a marker on a map."""

    tag = "Marker"

    # The position of the marker
    position: Var[LatLng]

    # Whether the marker is draggable or not
    draggable: Var[bool]

    # The z-index offset of the marker
    z_index_offset: Var[int]

    # The opacity of the marker (0-1)
    opacity: Var[float]

    # The attribution text for the marker
    attribution: Var[str]

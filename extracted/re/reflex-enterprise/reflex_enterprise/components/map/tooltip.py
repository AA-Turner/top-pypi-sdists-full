"""Tooltip component for displaying information on a map."""

from __future__ import annotations

from reflex.vars.base import Var

from .base import BaseLeafletComponent
from .types import LatLng


class Tooltip(BaseLeafletComponent):
    """Tooltip component for displaying information on a map."""

    tag = "Tooltip"

    # The map pane where the tooltip element will be added.
    pane: Var[str]

    # The position where the tooltip will be shown, as a LatLng object.
    position: Var[LatLng]

    # String to be shown in the attribution control for this tooltip.
    attribution: Var[str]

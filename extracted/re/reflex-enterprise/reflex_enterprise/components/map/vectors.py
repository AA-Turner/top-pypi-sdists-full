"""Vector layer components for Leaflet maps."""

from __future__ import annotations

from typing import Dict, List, TypedDict

from reflex.vars.base import Var

from .base import BaseLeafletComponent
from .types import LatLng, LatLngBounds


class PathOptions(TypedDict, total=False):
    """Options for styling vector paths."""

    stroke: bool  # Whether to draw stroke along the path
    color: str  # Stroke color
    weight: int  # Stroke width in pixels
    opacity: float  # Stroke opacity
    lineCap: str  # Shape of stroke ends ('butt', 'round' or 'square')
    lineJoin: str  # Shape of stroke corners ('miter', 'round' or 'bevel')
    dashArray: str  # String defining dash pattern (e.g. '5, 10')
    dashOffset: str  # Distance into the dash pattern to start
    fill: bool  # Whether to fill the path with color
    fillColor: str  # Fill color
    fillOpacity: float  # Fill opacity
    fillRule: str  # Fill rule ('nonzero' or 'evenodd')
    className: str  # Custom CSS class name


def path_options(
    *,
    stroke: bool | None = None,
    color: str | None = None,
    weight: int | None = None,
    opacity: float | None = None,
    line_cap: str | None = None,  # 'butt', 'round' or 'square'
    line_join: str | None = None,  # 'miter', 'round' or 'bevel'
    dash_array: str | None = None,
    dash_offset: str | None = None,
    fill: bool | None = None,
    fill_color: str | None = None,
    fill_opacity: float | None = None,
    fill_rule: str | None = None,  # 'nonzero' or 'evenodd'
    class_name: str | None = None,
) -> PathOptions:
    """Create a PathOptions dictionary with styling options for vector paths.

    Args:
        stroke: Whether to draw stroke along the path
        color: Stroke color
        weight: Stroke width in pixels
        opacity: Stroke opacity
        line_cap: Shape of stroke ends ('butt', 'round' or 'square')
        line_join: Shape of stroke corners ('miter', 'round' or 'bevel')
        dash_array: String defining dash pattern (e.g. '5, 10')
        dash_offset: Distance into the dash pattern to start
        fill: Whether to fill the path with color
        fill_color: Fill color
        fill_opacity: Fill opacity
        fill_rule: Fill rule ('nonzero' or 'evenodd')
        class_name: Custom CSS class name

    Returns:
        A dictionary with path styling options
    """
    options = {}

    if stroke is not None:
        options["stroke"] = stroke
    if color is not None:
        options["color"] = color
    if weight is not None:
        options["weight"] = weight
    if opacity is not None:
        options["opacity"] = opacity
    if line_cap is not None:
        options["lineCap"] = line_cap
    if line_join is not None:
        options["lineJoin"] = line_join
    if dash_array is not None:
        options["dashArray"] = dash_array
    if dash_offset is not None:
        options["dashOffset"] = dash_offset
    if fill is not None:
        options["fill"] = fill
    if fill_color is not None:
        options["fillColor"] = fill_color
    if fill_opacity is not None:
        options["fillOpacity"] = fill_opacity
    if fill_rule is not None:
        options["fillRule"] = fill_rule
    if class_name is not None:
        options["className"] = class_name

    return options  # type: ignore[return-value]


class Circle(BaseLeafletComponent):
    """Circle component for displaying a circle on a map."""

    tag = "Circle"

    # The center of the circle
    center: Var[LatLng]

    # The radius of the circle in meters
    radius: Var[float]

    # Styling options for the circle
    path_options: Var[PathOptions]

    # The attribution text
    attribution: Var[str]

    # The map pane where the circle will be added
    pane: Var[str]


class CircleMarker(BaseLeafletComponent):
    """CircleMarker component for displaying a small circle marker on a map.

    Unlike Circle, CircleMarker uses screen pixels for its radius, not meters.
    """

    tag = "CircleMarker"

    # The center of the circle marker
    center: Var[LatLng]

    # The radius of the circle marker in pixels
    radius: Var[float]

    # Styling options for the circle marker
    path_options: Var[PathOptions]

    # The attribution text
    attribution: Var[str]

    # The map pane where the circle marker will be added
    pane: Var[str]


class Polyline(BaseLeafletComponent):
    """Polyline component for displaying a line on a map."""

    tag = "Polyline"

    # Array of points making up the polyline
    positions: Var[List[LatLng]]

    # Styling options for the polyline
    path_options: Var[PathOptions]

    # The attribution text
    attribution: Var[str]

    # The map pane where the polyline will be added
    pane: Var[str]


class Polygon(BaseLeafletComponent):
    """Polygon component for displaying a filled polygon on a map."""

    tag = "Polygon"

    # Array of points making up the polygon
    positions: Var[List[LatLng]]

    # Styling options for the polygon
    path_options: Var[PathOptions]

    # The attribution text
    attribution: Var[str]

    # The map pane where the polygon will be added
    pane: Var[str]


class Rectangle(BaseLeafletComponent):
    """Rectangle component for displaying a rectangle on a map."""

    tag = "Rectangle"

    # The bounds of the rectangle
    bounds: Var[LatLngBounds]

    # Styling options for the rectangle
    path_options: Var[PathOptions]

    # The attribution text
    attribution: Var[str]

    # The map pane where the rectangle will be added
    pane: Var[str]


class SVGOverlay(BaseLeafletComponent):
    """SVGOverlay component for displaying custom SVG on a map."""

    tag = "SVGOverlay"

    # The bounds where the SVG will be drawn
    bounds: Var[LatLngBounds]

    # SVG attributes
    attributes: Var[Dict[str, str]]

    # The attribution text
    attribution: Var[str]

    # The map pane where the SVG overlay will be added
    pane: Var[str]

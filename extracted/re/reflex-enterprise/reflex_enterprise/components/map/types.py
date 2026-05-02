"""Type definitions for map (Leaflet) components."""

from __future__ import annotations

from typing import TypedDict


class Point(TypedDict):
    """Point for the map."""

    x: float
    y: float


class LatLng(TypedDict):
    """LatLng for the map."""

    lat: float
    lng: float


def latlng(lat: float, lng: float, nround: int | bool = False) -> LatLng:
    """Create a LatLng dictionary.

    Args:
        lat: The latitude
        lng: The longitude
        nround: Number of decimal places to round to. If False, no rounding is done.

    Returns:
        A dictionary with lat and lng keys
    """
    if not nround:
        return {"lat": lat, "lng": lng}
    else:
        return {
            "lat": round(lat, nround),
            "lng": round(lng, nround),
        }


class LatLngBounds(list):
    """LatLngBounds for the map, representing a rectangular area.

    In Leaflet, bounds are typically represented as an array of two points:
    [[southwest_lat, southwest_lng], [northeast_lat, northeast_lng]]
    """

    def __init__(self, southwest: list, northeast: list):
        """Initialize the bounds with southwest and northeast corners.

        Args:
            southwest: A list containing [lat, lng] for the southwest corner
            northeast: A list containing [lat, lng] for the northeast corner
        """
        super().__init__([southwest, northeast])


def latlng_bounds(
    corner1_lat: float, corner1_lng: float, corner2_lat: float, corner2_lng: float
) -> LatLngBounds:
    """Create a LatLngBounds list for Leaflet rectangle bounds.

    Args:
        corner1_lat: The latitude of the first corner (southwest)
        corner1_lng: The longitude of the first corner (southwest)
        corner2_lat: The latitude of the second corner (northeast)
        corner2_lng: The longitude of the second corner (northeast)

    Returns:
        A LatLngBounds object with southwest and northeast corners
    """
    southwest = [corner1_lat, corner1_lng]
    northeast = [corner2_lat, corner2_lng]
    return LatLngBounds(southwest, northeast)


class EventTarget(TypedDict):
    """Event target for the map."""

    zoom: int
    last_center: LatLng


class MoveEvent(TypedDict):
    """MoveEvent for the map."""

    type: str
    target: EventTarget
    last_center: LatLng


class ZoomEvent(TypedDict):
    """ZoomEvent for the map."""

    type: str
    target: EventTarget


class ZoomLevelsChangeEvent(TypedDict):
    """ZoomLevelsChangeEvent for the map when min/max zoom constraints change."""

    type: str
    target: EventTarget
    min_zoom: int
    max_zoom: int


class MouseEvent(TypedDict):
    """MouseEvent for the map."""

    type: str
    latlng: LatLng
    container_point: Point
    layer_point: Point
    target: EventTarget


class LocationEvent(TypedDict):
    """LocationEvent for the map when geolocation succeeds."""

    type: str
    latlng: LatLng
    accuracy: float
    altitude: float
    altitude_accuracy: float
    heading: float
    speed: float
    timestamp: int


class ErrorEvent(TypedDict):
    """ErrorEvent for the map when an error occurs."""

    type: str
    message: str
    code: int


class LayerEvent(TypedDict):
    """LayerEvent for the map when a layer is added/removed."""

    type: str
    layer: dict


class PopupEvent(TypedDict):
    """PopupEvent for the map when a popup is opened/closed."""

    type: str
    popup: dict


class TooltipEvent(TypedDict):
    """TooltipEvent for the map when a tooltip is opened/closed."""

    type: str
    tooltip: dict


class ResizeEvent(TypedDict):
    """ResizeEvent for the map when it's resized."""

    type: str
    old_size: Point
    new_size: Point


class LocateOptions(TypedDict):
    """Options for the locate method of the Leaflet map.

    See: https://leafletjs.com/reference.html#locate-options
    """

    # If true, starts continuous watching of location changes using W3C watchPosition method
    watch: bool

    # If true, automatically sets the map view to the user location with respect to detection accuracy
    setView: bool

    # The maximum zoom for automatic view setting when using `setView` option
    maxZoom: float

    # Number of milliseconds to wait for a response from geolocation before firing a locationerror event
    timeout: int

    # Maximum age in milliseconds of a possible cached position that is acceptable to return
    maximumAge: int

    # If true and supported by the browser, uses W3C compass readings to get a more precise heading value
    enableHighAccuracy: bool


def locate_options(
    *,
    watch: bool | None = None,
    set_view: bool | None = None,
    max_zoom: float | None = None,
    timeout: int | None = None,
    maximum_age: int | None = None,
    enable_high_accuracy: bool | None = None,
) -> LocateOptions:
    """Create a LocateOptions dictionary with the specified options.

    Args:
        watch: If true, starts continuous watching of location changes
        set_view: If true, automatically sets the map view to the user location
        max_zoom: The maximum zoom for automatic view setting
        timeout: Number of milliseconds to wait for a response before error
        maximum_age: Maximum age of a cached position that is acceptable
        show_marker: If true, creates a marker at the user's location
        emulate_watch_position: If true, emulates watchPosition native method
        enable_high_accuracy: If true, tries to get a more precise location
        circle_style: Style for the accuracy circle
        marker_style: Style for the position marker
        marker_options: Custom options for the location marker
        position: Position of the control on the map

    Returns:
        A LocateOptions dictionary with the specified options
    """
    options: LocateOptions = {}  # type: ignore [assignment]

    if watch is not None:
        options["watch"] = watch
    if set_view is not None:
        options["setView"] = set_view
    if max_zoom is not None:
        options["maxZoom"] = max_zoom
    if timeout is not None:
        options["timeout"] = timeout
    if maximum_age is not None:
        options["maximumAge"] = maximum_age
    if enable_high_accuracy is not None:
        options["enableHighAccuracy"] = enable_high_accuracy

    return options

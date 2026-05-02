"""Event handlers for map (Leaflet) components."""

from __future__ import annotations

from reflex.vars.base import Var
from reflex.vars.object import ObjectVar

from reflex_enterprise.components.map.types import (
    ErrorEvent,
    LatLng,
    LayerEvent,
    LocationEvent,
    MouseEvent,
    MoveEvent,
    Point,
    PopupEvent,
    ResizeEvent,
    TooltipEvent,
    ZoomEvent,
    ZoomLevelsChangeEvent,
)


def move_event_spec(event: ObjectVar[dict]) -> tuple[Var[MoveEvent]]:
    """Format the move event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "target": {"zoom": event["target"].to(dict)["_zoom"]},
                "last_center": event["target"].to(dict)["_lastCenter"],
            }
        ).to(MoveEvent),
    )


def zoom_event_spec(event: ObjectVar[dict]) -> tuple[Var[ZoomEvent]]:
    """Format the zoom event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "target": {"zoom": event["target"].to(dict)["_zoom"]},
            }
        ).to(ZoomEvent),
    )


def mouse_event_spec(event: ObjectVar[dict]) -> tuple[Var[MouseEvent]]:
    """Format the mouse event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "latlng": event["latlng"].to(dict),
                "target": {"zoom": event["target"].to(dict)["_zoom"]},
                "container_point": event["containerPoint"].to(Point),
                "layer_point": event["layerPoint"].to(Point),
            }
        ).to(MouseEvent),
    )


def locationfound_event_spec(event: ObjectVar[dict]) -> tuple[Var[LatLng]]:
    """Format the location found event for the map."""
    return (
        Var.create(
            event["latlng"].to(dict),
        ).to(LatLng),
    )


def location_event_spec(event: ObjectVar[dict]) -> tuple[Var[LocationEvent]]:
    """Format the location event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "latlng": event["latlng"].to(dict),
                "accuracy": event["accuracy"],
                "altitude": event.get("altitude", 0),
                "altitude_accuracy": event.get("altitudeAccuracy", 0),
                "heading": event.get("heading", 0),
                "speed": event.get("speed", 0),
                "timestamp": event.get("timestamp", 0),
            }
        ).to(LocationEvent),
    )


def error_event_spec(event: ObjectVar[dict]) -> tuple[Var[ErrorEvent]]:
    """Format the error event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "message": event["message"],
                "code": event["code"],
            }
        ).to(ErrorEvent),
    )


def layer_event_spec(event: ObjectVar[dict]) -> tuple[Var[LayerEvent]]:
    """Format the layer event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "layer": event["layer"].to(dict),
            }
        ).to(LayerEvent),
    )


def popup_event_spec(event: ObjectVar[dict]) -> tuple[Var[PopupEvent]]:
    """Format the popup event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "popup": event["popup"].to(dict),
            }
        ).to(PopupEvent),
    )


def tooltip_event_spec(event: ObjectVar[dict]) -> tuple[Var[TooltipEvent]]:
    """Format the tooltip event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "tooltip": event["tooltip"].to(dict),
            }
        ).to(TooltipEvent),
    )


def resize_event_spec(event: ObjectVar[dict]) -> tuple[Var[ResizeEvent]]:
    """Format the resize event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "old_size": event["oldSize"].to(Point),
                "new_size": event["newSize"].to(Point),
            }
        ).to(ResizeEvent),
    )


def zoom_levels_change_event_spec(
    event: ObjectVar[dict],
) -> tuple[Var[ZoomLevelsChangeEvent]]:
    """Format the zoom levels change event for the map."""
    return (
        Var.create(
            {
                "type": event["type"],
                "target": {"zoom": event["target"].to(dict)["_zoom"]},
                "min_zoom": event["target"].to(dict)["_layersMinZoom"],
                "max_zoom": event["target"].to(dict)["_layersMaxZoom"],
            }
        ).to(ZoomLevelsChangeEvent),
    )

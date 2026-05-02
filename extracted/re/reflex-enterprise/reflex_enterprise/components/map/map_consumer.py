"""Map consumer component for event handling in leaflet."""

from __future__ import annotations

import reflex as rx
from reflex.vars.base import Var

from reflex_enterprise.components.map.base import LazyBaseLeafletComponent
from reflex_enterprise.components.map.events import (
    error_event_spec,
    layer_event_spec,
    locationfound_event_spec,
    mouse_event_spec,
    move_event_spec,
    popup_event_spec,
    resize_event_spec,
    tooltip_event_spec,
    zoom_event_spec,
    zoom_levels_change_event_spec,
)

# Force this imports for the pyi file
from .types import (  # noqa: F401
    ErrorEvent,
    LatLng,
    LayerEvent,
    MouseEvent,
    MoveEvent,
    PopupEvent,
    ResizeEvent,
    TooltipEvent,
    ZoomEvent,
    ZoomLevelsChangeEvent,
)


class MapConsumer(LazyBaseLeafletComponent):
    """MapConsumer for events."""

    tag = "MapConsumer"

    map_ref: Var[str]

    # Map movement events
    on_move: rx.EventHandler[move_event_spec]
    on_move_start: rx.EventHandler[move_event_spec]
    on_move_end: rx.EventHandler[move_event_spec]

    # Mouse events
    on_click: rx.EventHandler[mouse_event_spec]
    on_dblclick: rx.EventHandler[mouse_event_spec]
    on_mousedown: rx.EventHandler[mouse_event_spec]
    on_mouseup: rx.EventHandler[mouse_event_spec]
    on_mouseover: rx.EventHandler[mouse_event_spec]
    on_mouseout: rx.EventHandler[mouse_event_spec]
    on_mousemove: rx.EventHandler[mouse_event_spec]
    on_contextmenu: rx.EventHandler[mouse_event_spec]

    # Zoom events
    on_zoom: rx.EventHandler[zoom_event_spec]
    on_zoom_start: rx.EventHandler[zoom_event_spec]
    on_zoom_end: rx.EventHandler[zoom_event_spec]
    on_zoom_levels_change: rx.EventHandler[zoom_levels_change_event_spec]

    # Location events
    on_locationfound: rx.EventHandler[locationfound_event_spec]
    on_locationerror: rx.EventHandler[error_event_spec]

    # UI events
    on_resize: rx.EventHandler[resize_event_spec]
    on_load: rx.EventHandler[rx.event.passthrough_event_spec(str)]
    on_unload: rx.EventHandler[rx.event.passthrough_event_spec(str)]
    on_viewreset: rx.EventHandler[rx.event.passthrough_event_spec(str)]

    # Layer events
    on_layeradd: rx.EventHandler[layer_event_spec]
    on_layerremove: rx.EventHandler[layer_event_spec]

    # Popup/tooltip events
    on_popupopen: rx.EventHandler[popup_event_spec]
    on_popupclose: rx.EventHandler[popup_event_spec]
    on_tooltipopen: rx.EventHandler[tooltip_event_spec]
    on_tooltipclose: rx.EventHandler[tooltip_event_spec]

    # A dictionary to hold all event handlers
    events_handler: Var[dict]

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        """Create a MapConsumer.

        This method maps Python-style event handlers (on_move) to
        the Leaflet-style event names (move).
        """
        _mapping = {
            # Map state change events
            "on_move": "move",
            "on_move_start": "movestart",
            "on_move_end": "moveend",
            "on_zoom": "zoom",
            "on_zoom_start": "zoomstart",
            "on_zoom_end": "zoomend",
            "on_zoom_levels_change": "zoomlevelschange",
            "on_resize": "resize",
            "on_load": "load",
            "on_unload": "unload",
            "on_viewreset": "viewreset",
            # Pointer events
            "on_click": "click",
            "on_dblclick": "dblclick",
            "on_mousedown": "mousedown",
            "on_mouseup": "mouseup",
            "on_mouseover": "mouseover",
            "on_mouseout": "mouseout",
            "on_mousemove": "mousemove",
            "on_contextmenu": "contextmenu",
            # Location events
            "on_locationfound": "locationfound",
            "on_locationerror": "locationerror",
            # Layer events
            "on_layeradd": "layeradd",
            "on_layerremove": "layerremove",
            # Popup/tooltip events
            "on_popupopen": "popupopen",
            "on_popupclose": "popupclose",
            "on_tooltipopen": "tooltipopen",
            "on_tooltipclose": "tooltipclose",
        }

        # Call create for a temporary object that formats the events_triggers
        _consumer = super().create(*children, **props)

        props["events_handler"] = {}
        to_remove = []
        for evt in _consumer.event_triggers:
            if evt in _mapping:
                props["events_handler"][_mapping[evt]] = _consumer.event_triggers[evt]
                to_remove.append(evt)

        for rem in to_remove:
            props.pop(rem)

        return super().create(*children, **props)

    def add_hooks(self) -> list[Var]:
        """Add hooks for leaflet components."""
        hooks = []
        return hooks

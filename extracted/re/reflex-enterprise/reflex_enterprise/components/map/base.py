"""Base class for map (leaflet) components."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

import reflex as rx
from reflex import ImportVar, constants
from reflex.event import EventSpec
from reflex.vars.base import Var, VarData
from reflex.vars.object import ObjectVar

from reflex_enterprise.components.component import NoSSRComponentEnterprise
from reflex_enterprise.components.map.events import mouse_event_spec
from reflex_enterprise.vars import JSAPIVar

# Force this import for the pyi file
from .types import MouseEvent  # noqa: F401

PACKAGE_NAME = "react-leaflet"
PACKAGE_VERSION = "5.0.0"

path = rx.asset("MapLazyComponents.jsx", shared=True)
public_path = path.importable_path

refs_var_data = VarData(
    imports={f"$/{constants.Dirs.STATE_PATH}": [ImportVar(tag="refs")]}
)
refs = Var(
    _js_expr="refs",
    _var_data=refs_var_data,
).to(
    ObjectVar,
    Mapping[str, str],
)


class MapAPIVar(JSAPIVar):
    """Wrapper for the Leaflet Map API object as represented in JS."""


@dataclass
class MapAPI:
    """Map API for leaflet components."""

    ref: str

    @classmethod
    def create(cls, ref: str) -> MapAPI:
        """Create a new MapAPI instance."""
        return cls(ref=ref)

    @property
    def _api(self) -> MapAPIVar:
        return MapAPIVar(
            f"refs['{self.ref}']",
            _var_data=refs_var_data,
        )

    def __getattr__(self, name: str) -> Callable[..., EventSpec]:
        """Get the attribute of the map API."""

        def _call_api(*args, **kwargs):
            """Call the API function with the given arguments."""
            return rx.event.run_script(
                getattr(self._api, name)(*args),
                **kwargs,
            )

        return _call_api


class BaseLeafletComponent(NoSSRComponentEnterprise):
    """Base class for leaflet."""

    library = f"{PACKAGE_NAME}@{PACKAGE_VERSION}"

    lib_dependencies: list[str] = [f"{PACKAGE_NAME}@{PACKAGE_VERSION}", "leaflet@1.9.4"]

    def add_imports(self):
        """Add imports for leaflet components."""
        return {
            "": "leaflet/dist/leaflet.css",
        }


class InteractiveLeafletLayer(BaseLeafletComponent):
    """Leaflet layer that wires layer mouse events into react-leaflet's eventHandlers prop."""

    on_click: rx.EventHandler[mouse_event_spec]
    on_dblclick: rx.EventHandler[mouse_event_spec]
    on_mousedown: rx.EventHandler[mouse_event_spec]
    on_mouseup: rx.EventHandler[mouse_event_spec]
    on_mouseover: rx.EventHandler[mouse_event_spec]
    on_mouseout: rx.EventHandler[mouse_event_spec]
    on_contextmenu: rx.EventHandler[mouse_event_spec]

    event_handlers: Var[dict]

    _LAYER_EVENT_MAPPING = {
        "on_click": "click",
        "on_dblclick": "dblclick",
        "on_mousedown": "mousedown",
        "on_mouseup": "mouseup",
        "on_mouseover": "mouseover",
        "on_mouseout": "mouseout",
        "on_contextmenu": "contextmenu",
    }

    @classmethod
    def create(cls, *children, **props):
        """Translate on_<event> props into a single eventHandlers dict that react-leaflet understands."""
        _instance = super().create(*children, **props)
        handlers = {}
        to_remove = []
        for evt in _instance.event_triggers:
            if evt in cls._LAYER_EVENT_MAPPING:
                handlers[cls._LAYER_EVENT_MAPPING[evt]] = _instance.event_triggers[evt]
                to_remove.append(evt)
        if not handlers:
            return _instance
        for rem in to_remove:
            props.pop(rem, None)
        props["event_handlers"] = handlers
        return super().create(*children, **props)


class LazyBaseLeafletComponent(BaseLeafletComponent):
    """Lazy load leaflet components."""

    library = public_path

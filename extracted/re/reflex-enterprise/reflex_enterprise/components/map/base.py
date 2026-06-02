"""Base class for map (leaflet) components."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

import reflex as rx
from reflex import ImportVar, constants
from reflex.event import EventChain, EventSpec, EventType, no_args_event_spec
from reflex.vars.base import Var, VarData
from reflex.vars.object import ObjectVar

from reflex_enterprise.components.component import NoSSRComponentEnterprise
from reflex_enterprise.components.map.events import (
    LAYER_EVENT_ARGS_SPECS,
    LayerEventName,
    mouse_event_spec,
)
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

    # Mapping of leaflet event name to the EventChain that handles it.
    event_handlers: Var[dict[LayerEventName, EventChain]]

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
    def create(
        cls,
        *children,
        event_handlers: Var[dict[LayerEventName, EventChain | EventType]] | None = None,
        **props,
    ):
        """Wire layer events into react-leaflet's `eventHandlers` prop.

        The `on_<event>` triggers and any values passed in the `event_handlers`
        mapping are normalized into `EventChain` instances so they render as the
        JS functions leaflet invokes. The args_spec for each event comes from the
        matching `on_<event>` `EventHandler` annotation, or from
        `LAYER_EVENT_ARGS_SPECS` for events without an alias, so handlers receive
        the correct typed event however they are wired.

        Args:
            *children: The children of the component.
            event_handlers: Mapping of leaflet event name to an `EventChain` or a
                raw `EventType` (a handler, list of handlers, or lambda). Merged
                with any `on_<event>` triggers and normalized to `EventChain`.
            **props: The props of the component.

        Returns:
            The component instance.

        Raises:
            ValueError: If an event is supplied via both its `on_<event>` trigger
                and `event_handlers`, or if a Var `event_handlers` mapping is
                combined with `on_<event>` triggers (which cannot be merged).
        """
        # args_spec per event: from the on_<event> annotation for aliased events,
        # otherwise from the shared leaflet event -> args_spec mapping.
        event_triggers = cls.get_event_triggers()
        args_spec_by_name = {
            **LAYER_EVENT_ARGS_SPECS,
            **{
                leaflet_name: event_triggers.get(trigger_name, no_args_event_spec)
                for trigger_name, leaflet_name in cls._LAYER_EVENT_MAPPING.items()
            },
        }

        # Pull any on_<event> triggers out of props, keyed by leaflet event name.
        mapped_triggers = {
            leaflet_name: props.pop(trigger_name)
            for trigger_name, leaflet_name in cls._LAYER_EVENT_MAPPING.items()
            if trigger_name in props
        }

        if isinstance(event_handlers, Var):
            # A Var mapping can't be introspected, so on_<event> triggers can't be
            # merged into it; otherwise pass it through untouched.
            if mapped_triggers:
                msg = (
                    "Cannot combine a Var `event_handlers` mapping with "
                    "`on_<event>` triggers; pass all handlers through one or the "
                    "other."
                )
                raise ValueError(msg)
            props["event_handlers"] = event_handlers
        else:
            # Merge the explicit mapping (copied) with the on_<event> triggers,
            # then normalize every value to a validated EventChain so it renders
            # as a function leaflet can invoke.
            handlers = dict(event_handlers or {})
            for leaflet_name, value in mapped_triggers.items():
                if leaflet_name in handlers:
                    msg = (
                        f"Event `{leaflet_name}` is set both via its `on_<event>` "
                        "trigger and `event_handlers`; specify it in only one place."
                    )
                    raise ValueError(msg)
                handlers[leaflet_name] = value
            if handlers:
                props["event_handlers"] = {
                    leaflet_name: EventChain.create(
                        value=value,
                        args_spec=args_spec_by_name.get(
                            leaflet_name, no_args_event_spec
                        ),
                    )
                    for leaflet_name, value in handlers.items()
                }

        return super().create(*children, **props)


class LazyBaseLeafletComponent(BaseLeafletComponent):
    """Lazy load leaflet components."""

    library = public_path

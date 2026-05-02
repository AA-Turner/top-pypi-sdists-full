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
from reflex_enterprise.vars import JSAPIVar

PACKAGE_NAME = "react-leaflet"
PACKAGE_VERSION = "5.0.0"

path = rx.asset("MapLazyComponents.jsx", shared=True)
try:
    public_path = path.importable_path
except AttributeError:
    # Fallback for < 0.9.0
    public_path = "$/public" + path

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


class LazyBaseLeafletComponent(BaseLeafletComponent):
    """Lazy load leaflet components."""

    library = public_path

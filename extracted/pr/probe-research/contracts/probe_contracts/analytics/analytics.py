"""EventCatalog and SurfaceCatalog: the one list of product-analytics events (events.json) and of
the product surfaces every event carries (surfaces.json), each beside it and checked on load.

Codegen draws each runtime's `Event` and `ProductSurface` enums from them; nothing reads the JSON
at run time.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from ..compat import StrEnum

#: The catalog this package ships.
CATALOG_PATH = Path(__file__).with_name("events.json")
#: The surface list this package ships.
SURFACE_CATALOG_PATH = Path(__file__).with_name("surfaces.json")

_KEY = re.compile(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*")
_SURFACE_VALUE = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*")


class Runtime(StrEnum):
    """Who sends an event. `plugin` is the hooks, which keep their own constants (no generated enum)."""

    SERVER = "server"
    AGENT = "agent"
    PLUGIN = "plugin"
    DASHBOARD = "dashboard"


@dataclass(frozen=True)
class CatalogEvent:
    """One event: its enum key (UPPER_SNAKE), wire name, who sends it and a one-line why."""

    key: str
    name: str
    runtimes: tuple[Runtime, ...]
    doc: str = ""


@dataclass(frozen=True)
class CatalogGroup:
    """A titled run of related events, drawn as a comment block in each generated enum."""

    title: str
    events: tuple[CatalogEvent, ...]
    doc: str = ""


class CatalogError(ValueError):
    """events.json or surfaces.json breaks a catalog rule (named in the message)."""


@dataclass(frozen=True)
class EventCatalog:
    about: str
    groups: tuple[CatalogGroup, ...]

    @classmethod
    def load(cls, path: Path = CATALOG_PATH) -> EventCatalog:
        """Read and check a catalog: unique keys and names, UPPER_SNAKE keys, known runtimes."""
        data = json.loads(path.read_text(encoding="utf-8"))
        groups = tuple(
            CatalogGroup(
                title=group["title"],
                doc=group.get("doc", ""),
                events=tuple(
                    CatalogEvent(
                        key=event["key"],
                        name=event["name"],
                        runtimes=tuple(Runtime(r) for r in event["runtimes"]),
                        doc=event.get("doc", ""),
                    )
                    for event in group["events"]
                ),
            )
            for group in data["groups"]
        )
        catalog = cls(about=data["about"], groups=groups)
        catalog.check()
        return catalog

    @property
    def events(self) -> tuple[CatalogEvent, ...]:
        return tuple(event for group in self.groups for event in group.events)

    def check(self) -> None:
        """Raise CatalogError on the first broken rule. A name is unique in the whole catalog; a key
        only within a runtime (the server's `onboarding.completed` and the browser's
        `onboarding_completed` are both ONBOARDING_COMPLETED in their own enum)."""
        keys: set[tuple[Runtime, str]] = set()
        names: set[str] = set()
        for event in self.events:
            if not _KEY.fullmatch(event.key):
                raise CatalogError(f"{event.name}: key {event.key!r} is not UPPER_SNAKE")
            if event.name in names:
                raise CatalogError(f"name {event.name!r} is used twice")
            if not event.runtimes or len(set(event.runtimes)) != len(event.runtimes):
                raise CatalogError(f"{event.key}: runtimes must be a non-empty list without repeats")
            for runtime in event.runtimes:
                if (runtime, event.key) in keys:
                    raise CatalogError(f"{runtime} key {event.key} is used twice")
                keys.add((runtime, event.key))
            names.add(event.name)

    def get_groups(self, runtime: Runtime) -> tuple[CatalogGroup, ...]:
        """The groups with an event `runtime` sends, holding only those events, in catalog order."""
        kept = []
        for group in self.groups:
            events = tuple(e for e in group.events if runtime in e.runtimes)
            if events:
                kept.append(CatalogGroup(title=group.title, events=events, doc=group.doc))
        return tuple(kept)

    def get_names(self, runtime: Runtime) -> list[str]:
        """Every wire name `runtime` sends, in catalog order."""
        return [event.name for group in self.get_groups(runtime) for event in group.events]


@dataclass(frozen=True)
class CatalogSurface:
    """One product surface: its enum key (UPPER_SNAKE), wire value (lower_snake) and who stamps it."""

    key: str
    value: str
    doc: str


@dataclass(frozen=True)
class SurfaceCatalog:
    """The closed list of `surface` values: which program an event came through."""

    about: str
    surfaces: tuple[CatalogSurface, ...]

    @classmethod
    def load(cls, path: Path = SURFACE_CATALOG_PATH) -> SurfaceCatalog:
        """Read and check the list: unique UPPER_SNAKE keys, unique lower_snake values, each documented."""
        data = json.loads(path.read_text(encoding="utf-8"))
        surfaces = tuple(
            CatalogSurface(key=surface["key"], value=surface["value"], doc=surface.get("doc", ""))
            for surface in data["surfaces"]
        )
        catalog = cls(about=data["about"], surfaces=surfaces)
        catalog.check()
        return catalog

    def check(self) -> None:
        """Raise CatalogError on the first broken rule."""
        if not self.surfaces:
            raise CatalogError("surfaces.json lists no surface")
        keys: set[str] = set()
        values: set[str] = set()
        for surface in self.surfaces:
            if not _KEY.fullmatch(surface.key):
                raise CatalogError(f"{surface.value}: key {surface.key!r} is not UPPER_SNAKE")
            if not _SURFACE_VALUE.fullmatch(surface.value):
                raise CatalogError(f"{surface.key}: value {surface.value!r} is not lower_snake")
            if not surface.doc.strip():
                raise CatalogError(f"{surface.key}: says nothing about who stamps it (doc)")
            if surface.key in keys:
                raise CatalogError(f"key {surface.key} is used twice")
            if surface.value in values:
                raise CatalogError(f"value {surface.value!r} is used twice")
            keys.add(surface.key)
            values.add(surface.value)

    def get_values(self) -> list[str]:
        """Every wire value, in list order."""
        return [surface.value for surface in self.surfaces]

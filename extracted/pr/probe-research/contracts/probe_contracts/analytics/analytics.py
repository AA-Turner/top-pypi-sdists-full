"""EventCatalog: the one list of product-analytics events (events.json beside it), checked on load.

Codegen draws each runtime's `Event` enum from it; nothing reads the JSON at run time.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from ..compat import StrEnum

#: The catalog this package ships.
CATALOG_PATH = Path(__file__).with_name("events.json")

_KEY = re.compile(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*")


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
    """events.json breaks a catalog rule (named in the message)."""


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

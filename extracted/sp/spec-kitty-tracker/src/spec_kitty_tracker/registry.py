from __future__ import annotations

from importlib.metadata import entry_points
from typing import Iterable

from spec_kitty_tracker.errors import ConnectorConfigError
from spec_kitty_tracker.protocols import TaskTrackerConnector


class ConnectorRegistry:
    def __init__(self) -> None:
        self._connectors: dict[str, TaskTrackerConnector] = {}

    def register(self, connector: TaskTrackerConnector) -> None:
        name = connector.name.strip().lower()
        if not name:
            raise ConnectorConfigError("Connector name must not be empty")
        self._connectors[name] = connector

    def unregister(self, name: str) -> None:
        self._connectors.pop(name.lower(), None)

    def get(self, name: str) -> TaskTrackerConnector:
        key = name.lower()
        if key not in self._connectors:
            raise ConnectorConfigError(f"Connector not registered: {name}")
        return self._connectors[key]

    def list_names(self) -> list[str]:
        return sorted(self._connectors.keys())

    def connectors(self) -> Iterable[TaskTrackerConnector]:
        return self._connectors.values()

    def load_entrypoints(self, group: str = "spec_kitty_tracker.connectors") -> None:
        for ep in entry_points(group=group):
            obj = ep.load()
            connector = obj() if callable(obj) else obj
            self.register(connector)

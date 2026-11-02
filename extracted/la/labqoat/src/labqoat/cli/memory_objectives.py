"""Replace one ranking objective while keeping the project's others."""

from __future__ import annotations

import json
from collections.abc import Mapping

from typing import TYPE_CHECKING

from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class MemoryObjectives:
    """Merge a set or removal into the project's current objective list."""

    @staticmethod
    def current(client: ManagementClient, project: str) -> JsonValue:
        """Read the project's objectives; a project nothing was written to yet has none."""
        try:
            return client.get("/api/v1/projects/{name}", {"name": project})["objectives"]
        except ApiError as error:
            if error.status != 404:
                raise
            return []

    @staticmethod
    def update(current: object, values: Mapping[str, object], remove: bool) -> JsonDocument:
        """Drop the named metric, then append its new definition unless removing."""
        metric = str(values["metric"])
        objectives: list[JsonValue] = [
            item for item in JsonDocument.expect_list(current) if JsonDocument.expect_dict(item)["metric"] != metric
        ]
        if remove:
            return JsonDocument({"objectives": objectives})
        require = MemoryObjectives.require(values.get("require") or ())
        objectives.append({"metric": metric, "direction": str(values["direction"]), "require": require})
        return JsonDocument({"objectives": objectives})

    @staticmethod
    def require(pairs: object) -> dict[str, JsonValue]:
        """Parse KEY=VALUE setup filters; JSON numbers and booleans keep their type."""
        if not isinstance(pairs, tuple):
            raise ValueError("Requirements must be repeated KEY=VALUE options.")
        parsed: dict[str, JsonValue] = {}
        for pair in pairs:
            key, separator, raw = str(pair).partition("=")
            if not separator or not key:
                raise ValueError("Requirements must be KEY=VALUE.")
            parsed[key] = MemoryObjectives.value(raw)
        return parsed

    @staticmethod
    def value(raw: str) -> JsonValue:
        """Decode true, false and numbers; keep everything else as text."""
        try:
            decoded = json.loads(raw)
        except ValueError:
            return raw
        return decoded if isinstance(decoded, (bool, int, float)) else raw

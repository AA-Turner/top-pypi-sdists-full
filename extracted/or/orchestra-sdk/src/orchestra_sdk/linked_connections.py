"""
Reads the credentials of a Task's linked connections, which Orchestra exports as environment
variables named `<INTEGRATION>__<CONNECTION_ID>__<FIELD>`.
"""

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

from orchestra_sdk.errors import LinkedConnectionNotFoundError

_NAME_PART_RE = re.compile(r"[^a-zA-Z0-9]+")
_DELIMITER = "__"


def _normalise(value: str) -> str:
    """Mirrors how Orchestra builds each part of the variable name."""
    return _NAME_PART_RE.sub("_", value).strip("_").upper()


def _decode(value: str) -> Any:
    # Orchestra serialises only dict and list fields as JSON. Other values stay strings, so an
    # account ID "12345" or a flag "true" isn't turned into a number or a bool.
    if value.startswith(("{", "[")):
        try:
            return json.loads(value)
        except ValueError:
            pass
    return value


@dataclass(frozen=True)
class LinkedConnection:
    integration: str
    connection_id: str
    # Kept out of the repr so printing or logging a connection doesn't leak its secrets.
    fields: dict[str, Any] = field(repr=False)

    def __getitem__(self, field: str) -> Any:
        """Look up a field by name, case-insensitively, e.g. `connection["snowflake_password"]`."""
        return self.fields[_normalise(field)]

    def get(self, field: str, default: Any = None) -> Any:
        return self.fields.get(_normalise(field), default)


def list_linked_connections() -> list[LinkedConnection]:
    fields_by_connection: dict[tuple[str, str], dict[str, Any]] = {}
    for name, value in os.environ.items():
        parts = name.split(_DELIMITER)
        if len(parts) != 3 or not all(parts) or any(part != _normalise(part) for part in parts):
            continue
        integration, connection_id, field = parts
        fields_by_connection.setdefault((integration, connection_id), {})[field] = _decode(value)

    return [
        LinkedConnection(integration=integration, connection_id=connection_id, fields=fields)
        for (integration, connection_id), fields in sorted(fields_by_connection.items())
    ]


def get_linked_connection(integration: str, connection_id: str | None = None) -> LinkedConnection:
    integration = _normalise(integration)
    candidates = [
        connection
        for connection in list_linked_connections()
        if connection.integration == integration
        and (connection_id is None or connection.connection_id == _normalise(connection_id))
    ]

    if len(candidates) == 1:
        return candidates[0]

    if connection_id is not None:
        raise LinkedConnectionNotFoundError(
            f"{integration} connection '{connection_id}' is not linked to this Task, or its "
            "credentials could not be loaded."
        )
    if not candidates:
        raise LinkedConnectionNotFoundError(
            f"No {integration} connection is linked to this Task, or its credentials could not be "
            "loaded."
        )
    connection_ids = ", ".join(connection.connection_id for connection in candidates)
    raise LinkedConnectionNotFoundError(
        f"Several {integration} connections are linked to this Task ({connection_ids}). "
        "Pass connection_id to choose one."
    )

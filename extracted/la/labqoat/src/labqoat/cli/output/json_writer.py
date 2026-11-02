"""Machine-readable JSON output on stdout."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, IO

if TYPE_CHECKING:
    from labqoat.json_document import JsonValue


class JsonWriter:
    """Stable JSON documents for scripting."""

    def __init__(self, stream: IO[str] | None = None, pretty: bool | None = None) -> None:
        """Select the output stream, defaulting to stdout."""
        self._stream = stream if stream is not None else sys.stdout
        self._pretty = JsonWriter.current_pretty() if pretty is None and stream is None else bool(pretty)

    def write(self, document: JsonValue) -> None:
        """Write one JSON document with a trailing newline."""
        indent = 2 if self._pretty else None
        separators = None if self._pretty else (",", ":")
        self._stream.write(json.dumps(document, indent=indent, separators=separators, sort_keys=True) + "\n")
        self._stream.flush()

    @staticmethod
    def current_pretty() -> bool:
        """Read the root invocation's selected output mode when available."""
        import click

        context = click.get_current_context(silent=True)
        if context is None:
            return False
        invocation = context.find_root().obj
        return bool(getattr(invocation, "output_mode", "json") == "pretty")

    def write_dict(self, document: dict[str, JsonValue]) -> None:
        """Write a generic JSON object."""
        self.write(document)

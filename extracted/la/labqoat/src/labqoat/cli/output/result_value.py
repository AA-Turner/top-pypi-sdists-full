"""A run's returned value, shown to a person or handed to a pipe."""

import json
import sys
from typing import IO

from labqoat.cli.output.json_writer import JsonWriter
from labqoat.cli.output.output_style import OutputStyle
from labqoat.cli.output.pretty_writer import PrettyWriter
from labqoat.cli.output.resource_view import ResourceView
from labqoat.json_document import JsonValue


class ResultValue:
    """Text stays text; rows become a table and structure is indented for people, compact JSON for pipes."""

    def __init__(self, stream: IO[str] | None = None) -> None:
        """Write to standard output unless a destination is supplied."""
        self._stream = stream if stream is not None else sys.stdout

    def write(self, data: JsonValue) -> None:
        """Render one decoded result; nothing is printed for an absent value."""
        if data is None:
            return
        if isinstance(data, str):
            self._stream.write(data + "\n")
        elif OutputStyle.current(self._stream) == "compact":
            JsonWriter(self._stream, pretty=False).write(data)
        elif self.rows(data):
            PrettyWriter(self._stream).table_only(ResourceView.of(data, "result"))
        elif isinstance(data, list) and not any(isinstance(item, (dict, list)) for item in data):
            self._stream.write(json.dumps(data) + "\n")
        else:
            self.indented(data)
        self._stream.flush()

    def indented(self, data: JsonValue) -> None:
        """Structured values keep every field, one per line, with syntax color."""
        from rich.console import Console
        from rich.json import JSON

        Console(file=self._stream, highlight=False).print(JSON.from_data(data, indent=2))

    @staticmethod
    def rows(data: JsonValue) -> bool:
        """A non-empty list of flat objects reads best as a table."""
        if not isinstance(data, list) or not data:
            return False
        return all(
            isinstance(row, dict) and not any(isinstance(value, (dict, list)) for value in row.values()) for row in data
        )

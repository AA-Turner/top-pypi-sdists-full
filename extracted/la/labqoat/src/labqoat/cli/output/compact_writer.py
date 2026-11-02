"""Tab-separated rows and ``key: value`` facts for agents, pipes and logs."""

from typing import IO

from labqoat.cli.output.field_text import FieldText
from labqoat.cli.output.resource_view import ResourceView


class CompactWriter:
    """Spend one short line per row or fact, with exact identifiers and no decoration."""

    def __init__(self, stream: IO[str]) -> None:
        """Retain the destination; nothing here depends on a terminal."""
        self._stream = stream

    def write(self, view: ResourceView) -> None:
        """Rows under one header line, then the facts that surround them."""
        lines: list[str] = []
        if view.rows is not None:
            lines.append("\t".join(column.header.lower().replace(" ", "_") for column in view.columns))
            lines.extend(
                "\t".join(FieldText.compact(column.value(row), column.kind) for column in view.columns)
                for row in view.rows
            )
        lines.extend(f"{fact.header}: {FieldText.compact(fact.value(view.record), fact.kind)}" for fact in view.facts)
        self._stream.write("\n".join(lines) + "\n")
        self._stream.flush()

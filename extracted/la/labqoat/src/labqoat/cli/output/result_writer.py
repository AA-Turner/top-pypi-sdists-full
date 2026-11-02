"""Resource output honoring the invocation's human or JSON presentation mode."""

import click

from labqoat.cli.output.compact_writer import CompactWriter
from labqoat.cli.output.field_selection import FieldSelection
from labqoat.cli.output.json_writer import JsonWriter
from labqoat.cli.output.output_style import OutputStyle
from labqoat.cli.output.pretty_writer import PrettyWriter
from labqoat.cli.output.resource_view import ResourceView
from labqoat.json_document import JsonValue


class ResultWriter(JsonWriter):
    """Keep JSON encoding centralized while people get designed output and pipes get compact text."""

    def write(self, document: JsonValue) -> None:
        """Render a resource in the explicitly selected invocation mode."""
        context = click.get_current_context(silent=True)
        invocation = context.find_root().obj if context is not None else None
        selected = context.find_root().meta.get(FieldSelection.KEY) if context is not None else None
        if selected:
            document = FieldSelection(str(selected)).apply(document)
        if getattr(invocation, "output_mode", "json") != "human" or context is None:
            super().write(document)
            return
        view = ResourceView.of(document, self.command(context))
        if OutputStyle.current(self._stream) == "pretty":
            PrettyWriter(self._stream, color=context.find_root().color is not False).write(view)
        else:
            CompactWriter(self._stream).write(view)

    @staticmethod
    def command(context: click.Context) -> str:
        """The invoked command below the program name, such as ``run list``."""
        names: list[str] = []
        current: click.Context | None = context
        while current is not None and current.parent is not None:
            names.append(str(current.info_name))
            current = current.parent
        return " ".join(reversed(names))

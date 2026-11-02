"""Dict and queue values as the command line reads and shows them."""

import base64
import json

import click

from labqoat.json_document import JsonDocument, JsonValue


class StoredValue:
    """Read a value as JSON, or as plain text when asked; show bytes as base64 so output stays JSON."""

    @staticmethod
    def parse(text: str, as_text: bool) -> object:
        """The value a command-line argument stands for."""
        if as_text:
            return text
        try:
            return json.loads(text)
        except ValueError as error:
            raise click.BadParameter(
                f"{text!r} is not JSON; quote text as '\"{text}\"' or pass --text to store it as written"
            ) from error

    @staticmethod
    def show(value: object) -> JsonValue:
        """A stored value as JSON output: the value itself, or ``{"base64": ...}`` for bytes."""
        if isinstance(value, bytes):
            return {"base64": base64.b64encode(value).decode("ascii")}
        return JsonDocument.expect_value(value)

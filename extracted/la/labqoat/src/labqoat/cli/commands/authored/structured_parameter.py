"""A dataclass, list or mapping parameter given on the command line as JSON."""

import json
from dataclasses import dataclass, fields, is_dataclass
from pathlib import Path
from typing import cast, get_args, get_origin

import click

from labqoat.argument_codec import encode_result
from labqoat.cli.commands.authored.asset_selectors import AssetSelectors
from labqoat.client import Client
from labqoat.compute.value_codec import ValueCodec
from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class SelectedAssets:
    """A structured argument that names assets by ID or digest, parsed and waiting for the catalog."""

    document: JsonValue


class StructuredParameter(click.ParamType[object]):
    """Read JSON text, or ``@path`` to a JSON file, and rebuild the declared Python value from it.

    The value is decoded exactly as a Python caller's argument would be, so dataclasses come back with their
    nested artifacts, datasets and checkpoints as typed inputs the platform authorizes. A run's result printed
    by ``lab --json run result`` can be passed on as it is.
    """

    name = "json"

    def __init__(self, annotation: object) -> None:
        """Bind the declared type; raises TypeError when the type has no transport."""
        self.annotation = annotation
        self.codec = ValueCodec(cast("type[object]", annotation))
        self.codec.schema()

    def convert(self, value: object, param: click.Parameter | None, ctx: click.Context | None) -> object:
        """Parse and decode, naming what was wrong when the text does not fit the type.

        An asset ID or ``sha256:`` digest where the type declares an Artifact needs the catalog, so such a document
        waits, as parsed, for ``resolve``.
        """
        if not isinstance(value, str):
            return value
        document = self.parse(value, param, ctx)
        if AssetSelectors.selectors(self.annotation, document):
            return SelectedAssets(document)
        try:
            return self.codec.decode(document)
        except (TypeError, ValueError) as error:
            self.fail(f"does not match {self.describe()}: {error}", param, ctx)

    def resolve(self, client: Client, value: object) -> object:
        """Look up the assets a parsed document names, then decode it like any other."""
        if not isinstance(value, SelectedAssets):
            return value
        document = AssetSelectors.replace(
            self.annotation, value.document, lambda selector: encode_result(client.assets.resolve(selector))
        )
        return self.codec.decode(document)

    def parse(self, value: str, param: click.Parameter | None, ctx: click.Context | None) -> JsonValue:
        """The JSON document in the text, or in the file ``@path`` names."""
        try:
            text = Path(value[1:]).read_text(encoding="utf-8") if value.startswith("@") else value
        except OSError as error:
            self.fail(f"cannot read {value[1:]!r}: {error.strerror}", param, ctx)
        try:
            return cast("JsonValue", json.loads(text))
        except ValueError as error:
            self.fail(f"not JSON for {self.describe()}: {error}", param, ctx)

    def describe(self) -> str:
        """The declared type as a reader recognizes it."""
        return getattr(self.annotation, "__name__", None) or str(self.annotation).replace("typing.", "")

    def help(self) -> str:
        """Option help naming the JSON shape: a dataclass lists its fields, a list its element."""
        return f"JSON or @file.json: {StructuredParameter.shape(self.annotation)}"

    @staticmethod
    def shape(annotation: object) -> str:
        """A short picture of the JSON a type takes."""
        if is_dataclass(annotation):
            names = [field.name for field in fields(annotation)]
            return "{" + ", ".join(names[:8]) + (", ..." if len(names) > 8 else "") + "}"
        arguments = get_args(annotation)
        if get_origin(annotation) in (list, tuple) and arguments:
            return f"[{StructuredParameter.shape(arguments[0])}, ...]"
        if get_origin(annotation) is dict and len(arguments) == 2:
            return "{name: " + StructuredParameter.shape(arguments[1]) + "}"
        return getattr(annotation, "__name__", str(annotation)).replace("typing.", "")

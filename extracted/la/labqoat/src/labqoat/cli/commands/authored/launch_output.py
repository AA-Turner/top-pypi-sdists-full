"""Human results and schema-bound machine receipts for authored launches."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.json_writer import JsonWriter
from labqoat.cli.output.result_value import ResultValue
from labqoat.compute.value_codec import ValueCodec
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.runs.run_handle import RunHandle
from labqoat.schemas.schema_document import SchemaDocument


class LaunchOutput:
    """Keep logs separate from a single result or durable-acceptance receipt."""

    @staticmethod
    def value(value: object, value_type: type[object], handle: RunHandle[object] | None = None) -> None:
        """Render plain authored values by default and typed envelopes in explicit JSON modes."""
        codec = ValueCodec(value_type)
        data = codec.encode(value)
        if ContextAccessor.current().output_mode == "human":
            ResultValue().write(data)
            return
        JsonWriter().write(
            {
                "kind": "local_entrypoint" if handle is None else "run",
                "run": None if handle is None else LaunchOutput.receipt(handle),
                "value": {"schema_digest": SchemaDocument.capture(codec.schema()).digest, "data": data},
            }
        )

    @staticmethod
    def accepted(handle: RunHandle[object]) -> None:
        """Print a reusable identity immediately after durable acceptance."""
        if ContextAccessor.current().output_mode == "human":
            click.echo(handle.id)
        else:
            JsonWriter().write({"kind": "run", "run": LaunchOutput.receipt(handle), "value": None})

    receipt_fields = ("id", "name", "project", "status", "state", "child_operation_key", "inserted_at", "links")

    @classmethod
    def receipt(cls, handle: RunHandle[object]) -> dict[str, JsonValue]:
        """What a caller of a launch needs: identity, place and state; `lab run get` keeps the whole record."""
        run = handle.client.get(handle.id).to_dict()
        return {name: JsonDocument.expect_value(run[name]) for name in cls.receipt_fields if run.get(name) is not None}

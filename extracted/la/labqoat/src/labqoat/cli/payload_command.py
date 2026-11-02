"""Strict Click leaf backed by one explicit JSON mutation."""

from __future__ import annotations

import json
from collections.abc import Sequence
from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.mutation_spec import MutationSpec
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.cli.mutation_key import MutationKey

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class PayloadCommand(StrictCommand):
    """Convert validated CLI values into an explicit JSON request."""

    def __init__(
        self,
        name: str,
        spec: MutationSpec,
        params: Sequence[click.Parameter],
        help_text: str,
    ) -> None:
        """Store mutation metadata while constructing the Click command."""
        super().__init__(name, params=[*params, MutationKey.option()], help=help_text)
        self._spec = spec

    def invoke(self, ctx: click.Context) -> object:
        """Validate relationships, submit JSON, and render the response."""
        values = {name: value for name, value in ctx.params.items() if value is not None}
        supplied_key = values.pop("key", None)
        self.validate_exclusive(values, ctx)
        query = self.query(values)
        try:
            payload = self.payload(values)
        except (TypeError, ValueError) as error:
            ErrorReporter.report_usage(str(error))
        client = ContextAccessor.current().management()
        try:
            query["operation_key"] = MutationKey.resolve(supplied_key)
            self.render_response(client, client.post(self._spec.path, query, payload))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    def render_response(self, _client: ManagementClient, response: JsonDocument) -> None:
        """Render a completed mutation; lifecycle commands may override this."""
        ResultWriter().write_dict(response)

    def query(self, values: dict[str, object]) -> dict[str, object]:
        """Move selected values into the query with explicit renaming."""
        renames = self._spec.query_renames or {}
        query = {renames.get(name, name): values.pop(name) for name in self._spec.query_names if name in values}
        query.update(self._spec.fixed_query or {})
        return query

    def payload(self, values: dict[str, object]) -> JsonDocument:
        """Rename, decode, and supplement request fields."""
        document: dict[str, JsonValue] = {}
        renames = self._spec.renames or {}
        for name, value in values.items():
            target = renames.get(name, name)
            if name in self._spec.json_names:
                document[target] = JsonDocument.expect_value(json.loads(str(value)))
            else:
                document[target] = JsonDocument.expect_value(value)
        document.update(self._spec.fixed or {})
        return JsonDocument(document)

    def validate_exclusive(self, values: dict[str, object], ctx: click.Context) -> None:
        """Enforce zero-or-one or exactly-one related option selection."""
        if not self._spec.exclusive:
            return
        selected = [name for name in self._spec.exclusive if values.get(name) not in {None, False}]
        expected = 1 if self._spec.exclusive_required else 0
        if len(selected) > 1 or (self._spec.exclusive_required and len(selected) != expected):
            names = ", ".join(f"--{name.replace('_', '-')}" for name in self._spec.exclusive)
            qualifier = "exactly one of" if self._spec.exclusive_required else "at most one of"
            raise click.UsageError(f"Use {qualifier}: {names}.", ctx)

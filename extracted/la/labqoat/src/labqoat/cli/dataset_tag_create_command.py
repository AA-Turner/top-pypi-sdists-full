"""Immutable dataset tag creation from any revision reference."""

from __future__ import annotations


import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument
from labqoat.cli.mutation_key import MutationKey


class DatasetTagCreateCommand(StrictCommand):
    """Resolve a revision's repository before creating its immutable tag."""

    def __init__(self, params: list[click.Parameter]) -> None:
        """Construct the strict tag creation command."""
        super().__init__(
            "create", params=[*params, MutationKey.option()], help="Attach an immutable tag to a dataset revision."
        )

    def invoke(self, ctx: click.Context) -> object:
        """Resolve revision ownership, create the tag, and render it."""
        client = ContextAccessor.current().management()
        try:
            revision = client.get("/api/v1/dataset-revisions/item", {"ref": ctx.params["revision_ref"]})
            repository = client.get("/api/v1/dataset-repositories/item", {"ref": revision["repository_id"]})
            payload = JsonDocument(
                {
                    "repository_ref": repository["name"],
                    "revision_ref": revision["id"],
                    "tag": ctx.params["tag_name"],
                }
            )
            result = client.post(
                "/api/v1/dataset-tags", {"operation_key": MutationKey.resolve(ctx.params["key"])}, payload
            )
            ResultWriter().write_dict(result)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

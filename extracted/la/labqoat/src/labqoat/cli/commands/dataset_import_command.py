"""Submit public Hugging Face source selections through the same typed API as SDK users."""

from __future__ import annotations

from contextlib import closing
from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.cli.mutation_key import MutationKey
from labqoat.cli.observation_deadline import ObservationDeadline

if TYPE_CHECKING:
    from labqoat._generated.hugging_face_source import HuggingFaceSource
    from labqoat._generated.dataset_import import DatasetImport
    from labqoat.datasets_client import DatasetsClient
    from labqoat.json_document import JsonDocument


class DatasetImportCommand(StrictCommand):
    """Expose source discovery, immutable admission and optional event-backed waiting."""

    def __init__(self) -> None:
        """Declare explicit destination and data-only source options."""
        super().__init__(
            "import-hf",
            help="Import a public Hugging Face dataset through the API.",
            params=[
                click.Argument(["repository"]),
                click.Option(["--name"], help="Destination dataset name."),
                click.Option(["--revision"], help="Source branch or commit; resolved to an immutable commit."),
                click.Option(["--config", "configuration"], default="default"),
                click.Option(["--split", "splits"], multiple=True, default=["train"]),
                click.Option(["--column", "columns"], multiple=True, help="Select/rename source=target; repeatable."),
                click.Option(["--tag"]),
                click.Option(
                    ["--key", "--idempotency-key", "idempotency_key"], help="Retry-safe import operation key."
                ),
                ObservationDeadline.option(),
                click.Option(["--preview"], is_flag=True, help="Preview ten rows without publishing."),
                click.Option(["--wait"], is_flag=True, help="Wait for the imported revision to be ready."),
            ],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Use CLI-scoped credentials and leave data movement to the backend."""
        from labqoat._generated.new_dataset_import import NewDatasetImport

        try:
            source = self._source(ctx)
            if not ctx.params["preview"] and not ctx.params["name"]:
                raise ValueError("--name is required when importing")
            with closing(ContextAccessor.current().datasets()) as client:
                if ctx.params["preview"]:
                    result = client.preview_hugging_face(source).to_dict()
                else:
                    request = NewDatasetImport(dataset=ctx.params["name"], source=source, tag=ctx.params["tag"])
                    record = client.import_hugging_face(
                        request, idempotency_key=MutationKey.resolve(ctx.params["idempotency_key"])
                    )
                    result = self._observe(client, record, bool(ctx.params["wait"]))
            ResultWriter().write_dict(result)
        except (KeyError, TypeError, ValueError) as error:
            ErrorReporter.report_usage(str(error))
        except Exception as error:
            ErrorReporter.report(error)
        return None

    @staticmethod
    def _observe(client: DatasetsClient, record: DatasetImport, wait: bool) -> JsonDocument:
        """Start the observation deadline only after durable import acceptance."""
        with ObservationDeadline.current(record.id).watching():
            return client.wait_import(record.id).to_dict() if wait else record.to_dict()

    @staticmethod
    def _source(ctx: click.Context) -> HuggingFaceSource:
        """Reject ambiguous column mappings before making requests."""
        from labqoat._generated.hugging_face_source import HuggingFaceSource
        from labqoat.json_document import JsonDocument

        columns = JsonDocument()
        for value in ctx.params["columns"]:
            source, separator, target = value.partition("=")
            if not separator or not source or not target or source in columns or target in columns.values():
                raise ValueError("Each --column must be a unique source=target mapping")
            columns[source] = target
        return HuggingFaceSource(
            repository=ctx.params["repository"],
            revision=ctx.params["revision"],
            configuration=ctx.params["configuration"],
            splits=list(ctx.params["splits"]),
            columns=columns or None,
        )

"""Verified cache-backed dataset view construction."""

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.dataset_selection import DatasetSelection
from labqoat.cli.dataset_workspace import DatasetWorkspace
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class DatasetMaterializeCommand(StrictCommand):
    """Download and verify one immutable revision into a managed local view."""

    def __init__(self, name: str, params: list[click.Parameter], help_text: str) -> None:
        """Store whether the view uses cache links or standalone files."""
        super().__init__(name, params=params, help=help_text)

    def invoke(self, ctx: click.Context) -> object:
        """Resolve the manifest and build its safe local view."""
        from labqoat.storage.cache_settings import CacheSettings

        management = ContextAccessor.current().management()
        assets = ContextAccessor.current().assets()
        try:
            workspace = DatasetWorkspace.discover()
            selector = str(ctx.params["dataset"])
            files = self._files(management, workspace, selector)
            selected = DatasetSelection.select(files, ctx.params["include"])
            result = workspace.materialize(
                selector, selected, assets.download_to, str(self.name), CacheSettings.local()
            )
            ResultWriter().write_dict(result)
        except (OSError, TypeError, ValueError) as error:
            ErrorReporter.report_generic(str(error))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            assets.close()
            management.close()
        return None

    @staticmethod
    def _files(client: ManagementClient, workspace: DatasetWorkspace, selector: str) -> list[JsonDocument]:
        """Verify captured revision identities before projecting materialized parts into view descriptors."""
        from labqoat.dataset_access.revision_files import RevisionFiles
        from labqoat.workflows.dataset_resolver import DatasetResolver

        pin = DatasetResolver(client).resolve(workspace.reference(selector))
        document = client.get("/api/v1/dataset-revisions/files", {"ref": str(pin.revision_id)})
        revision = RevisionFiles.capture(document, pin)
        return [
            JsonDocument(
                {
                    "path": item.path,
                    "asset_id": str(item.asset.id),
                    "sha256": str(item.asset.blob_sha256),
                    "byte_size": item.asset.byte_size,
                    "media_type": item.asset.media_type,
                }
            )
            for item in revision.manifest.files
        ]

"""Workflows sub-manager (reached via ``istari.systems.workflows``).

Create, get, list, archive, and restore workflow log entries, and upload
workflow output files. All methods take ``system_id`` as the first positional
argument (child-collection pattern).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from istari_digital_client.sdk._base import Page
from istari_digital_client.sdk._common._capabilities import _SupportsRead
from istari_digital_client.sdk._common.workflow_types import WorkflowLogEntry, WorkflowOutput
from istari_digital_client.sdk._generated.v3.models.token_create_dto import TokenCreateDto
from istari_digital_client.sdk._generated.v3.models.workflow_log_entry_create_dto import (
    WorkflowLogEntryCreateDto,
)
from istari_digital_client.sdk._generated.v3.models.workflow_output_create_dto import (
    WorkflowOutputCreateDto,
)
from istari_digital_client.sdk._generated.v3.models.workflow_output_file_dto import WorkflowOutputFileDto

_log = logging.getLogger(__name__)


class Workflows(_SupportsRead):
    """Manage workflow log entries and their output files for a system.

    Reached via ``istari.systems.workflows``. All methods take ``system_id``
    as the first positional argument.

    Sub-managers: none (workflows are a leaf collection).

    Usage::

        # 1. Upload a result file as a workflow output
        output = istari.systems.workflows.create_output(
            system_id, "/path/to/results.csv", description="run results"
        )

        # 2. Log the workflow run, attaching the output
        entry = istari.systems.workflows.create(
            system_id,
            title="Simulation Run #42",
            status="SUCCESS",
            branch_id=branch.id,
            output_ids=[output.id],
        )

        # 3. Fetch the full entry with embedded readable outputs
        detail = istari.systems.workflows.get(system_id, entry.id)
        for out in detail.outputs:
            data = out.read_bytes()
    """

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _bind_entry(self, dto: Any, system_id: str) -> WorkflowLogEntry:
        entry = WorkflowLogEntry._bind(dto, mgr=self)
        return entry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create(
        self,
        system_id: str,
        *,
        title: str | None = None,
        status: str = "UNSPECIFIED",
        workflow_type: str = "external",
        configuration_id: str | None = None,
        branch_id: str | None = None,
        branchless: bool = False,
        output_ids: list[str] | None = None,
    ) -> WorkflowLogEntry:
        """Create a new workflow log entry for a system.

        Mutates: true

        ``title`` is a human-readable name for the run. ``status`` is the
        final outcome: "SUCCESS" | "FAILED" | "UNSPECIFIED" | "RUNNING" |
        "CANCELED" (defaults to "UNSPECIFIED"). ``workflow_type`` identifies the
        kind of workflow (defaults to "external").

        Pass ``branch_id`` to link the entry to a specific branch, or set
        ``branchless=True`` for runs with no branch or configuration provenance
        (in which case ``branch_id`` and ``configuration_id`` must be omitted).
        Pass ``output_ids`` to attach previously created WorkflowOutput records
        by UUID.

        Returns a WorkflowLogEntry with fields: id, system_id, title (str |
        None), status (str: "SUCCESS" | "FAILED" | "UNSPECIFIED" | "RUNNING" |
        "CANCELED"), workflow_type (str: "external" | ...), configuration_id
        (str | None), branch_id (str | None), branch_name (str | None),
        branchless (bool), file_count (int), total_file_size (int, bytes),
        archived (bool), created (datetime), created_by_id (str).
        Object methods: archive(), restore(). The outputs list is empty even if
        output_ids were supplied — call get() to retrieve the entry with outputs
        populated.

        Raises NotFoundError if system_id does not exist.
        Raises PermissionDeniedError if the caller cannot access the system.
        """
        dto = self._call(
            self._engine.v3_api.create_workflow_log_entry,
            system_id,
            WorkflowLogEntryCreateDto(
                title=title,
                status=status,
                workflow_type=workflow_type,
                configuration_id=configuration_id,
                branch_id=branch_id,
                branchless=branchless,
                workflow_output_ids=output_ids,
            ),
        )
        return self._bind_entry(dto, system_id)

    def get(self, system_id: str, entry_id: str) -> WorkflowLogEntry:
        """Fetch a workflow log entry by UUID, including its output files.

        Returns a WorkflowLogEntry with fields: id, system_id, title (str |
        None), status (str: "SUCCESS" | "FAILED" | "UNSPECIFIED" | "RUNNING" |
        "CANCELED"), workflow_type (str: "external" | ...), configuration_id
        (str | None), branch_id (str | None), branch_name (str | None),
        branchless (bool), file_count (int), total_file_size (int, bytes),
        archived (bool), created (datetime), created_by_id (str).
        Object methods: archive(), restore(). The outputs list is populated with
        bound WorkflowOutput objects whose content is immediately readable via
        read_bytes(), read_text(), or read_json().

        Raises NotFoundError if the entry does not exist.
        Raises PermissionDeniedError if the caller cannot access the system.
        """
        dto = self._call(
            self._engine.v3_api.get_workflow_log_entry,
            system_id,
            entry_id,
        )
        bound_outputs = [
            WorkflowOutput._bind(o, mgr=self) for o in (dto.workflow_outputs or [])
        ]
        entry = self._bind_entry(dto, system_id)
        # `dto` is a WorkflowLogEntryDetailDto, but WorkflowLogEntry subclasses the
        # LIST DTO (no `workflow_outputs` field). After the in-place reclass the
        # detail-only value would linger as an orphan __dict__ entry: dropped by
        # model_dump, inconsistent with model_fields, and double-stored against
        # `_outputs` (duplicated on deepcopy/pickle). Drop it — outputs are exposed
        # via the `.outputs` property (backed by `_outputs`), not serialized.
        entry.__dict__.pop("workflow_outputs", None)
        fields_set = getattr(entry, "__pydantic_fields_set__", None)
        if fields_set is not None:
            fields_set.discard("workflow_outputs")
        object.__setattr__(entry, "_outputs", bound_outputs)
        return entry

    def list(
        self,
        system_id: str,
        *,
        size: int | None = None,
        cursor: str | None = None,
        branch_id: list[str] | None = None,
        title: list[str] | None = None,
        status: list[str] | None = None,
        archive_status: str | None = None,
    ) -> Page[WorkflowLogEntry]:
        """List workflow log entries for a system and return an auto-paging sequence.

        Aliases: logs log history

        Iterating the returned Page automatically fetches subsequent pages. All
        filter parameters are optional. ``branch_id``, ``title``, and ``status``
        accept lists of values treated as OR filters; prefix a value with "!" to
        negate it. ``archive_status`` accepts "active" (default) | "archived" |
        "all".

        Returns an auto-paging sequence of WorkflowLogEntry objects (see field
        list on get()). Entries returned here do not have their outputs list
        populated — call get(system_id, entry.id) to retrieve a single entry
        with its outputs.

        Raises NotFoundError if system_id does not exist.
        Raises PermissionDeniedError if the caller cannot access the system.
        """

        def fetch(cur: str | None) -> Any:
            return self._call(
                self._engine.v3_api.list_workflow_log_entries,
                system_id,
                cursor=cur,
                size=size,
                branch_id=branch_id,
                title=title,
                status=status,
                archive_status=archive_status,
            )

        return self._paginate(fetch, lambda d: self._bind_entry(d, system_id))

    def archive(self, system_id: str, entry_id: str) -> None:
        """Archive a workflow log entry by its UUID.

        Mutates: true

        Archived entries are excluded from default list() results; pass
        archive_status="archived" to retrieve them. The entry can be restored
        with restore(). Alternatively, call archive() on the WorkflowLogEntry
        object directly.

        Raises NotFoundError if the entry does not exist.
        Raises PermissionDeniedError if the caller cannot access the system.
        """
        self._call(
            self._engine.v3_api.archive_workflow_log_entry,
            system_id,
            entry_id,
        )

    def restore(self, system_id: str, entry_id: str) -> WorkflowLogEntry:
        """Restore an archived workflow log entry and return the refreshed entry.

        Mutates: true

        Returns a freshly bound WorkflowLogEntry with updated state (see field
        list on get()). The outputs list is empty on the returned entry — call
        get() afterward if you need the entry with outputs populated.
        Alternatively, call restore() on the WorkflowLogEntry object directly
        (note: the object method returns None; call get() afterward if you need
        the updated object).

        Raises NotFoundError if the entry does not exist.
        Raises PermissionDeniedError if the caller cannot access the system.
        """
        dto = self._call(
            self._engine.v3_api.restore_workflow_log_entry,
            system_id,
            entry_id,
        )
        return self._bind_entry(dto, system_id)

    def create_output(
        self,
        system_id: str,
        path: str | Path,
        *,
        description: str | None = None,
        display_name: str | None = None,
        external_identifier: str | None = None,
    ) -> WorkflowOutput:
        """Upload a file and register it as a workflow output.

        Mutates: true

        Uploads the file at ``path`` to storage, then registers it as a
        workflow output scoped to ``system_id``. ``description``,
        ``display_name``, and ``external_identifier`` are optional metadata
        forwarded to both the storage upload and the registry.

        Returns a WorkflowOutput with fields: id, file_revision_id,
        name (str | None), extension (str | None), size (int | None, bytes),
        mime (str | None), display_name (str | None), external_identifier (str |
        None), description (str | None), content_token,
        created (datetime), created_by_id (str). Readable: call read_bytes(),
        read_text(), or read_json() to fetch content. Pass
        the returned .id to create() via output_ids to attach it to a log entry.

        Raises NotFoundError if system_id does not exist.
        Raises PermissionDeniedError if the caller cannot access the system.
        Raises FileNotFoundError if the local file at path does not exist.
        """
        rev = self._engine.storage.upload(
            path,
            description=description,
            display_name=display_name,
            external_identifier=external_identifier,
        )
        try:
            dto = self._call(
                self._engine.v3_api.create_workflow_output,
                system_id,
                WorkflowOutputCreateDto(
                    name=rev.name,
                    extension=rev.extension,
                    size=rev.size,
                    mime=rev.mime,
                    description=rev.description,
                    display_name=rev.display_name,
                    external_identifier=rev.external_identifier,
                    content_token=TokenCreateDto(
                        sha=rev.content_token.sha, salt=rev.content_token.salt
                    ),
                    properties_token=TokenCreateDto(
                        sha=rev.properties_token.sha, salt=rev.properties_token.salt
                    ),
                ),
            )
        except Exception:
            _log.warning(
                "create_workflow_output failed after storage upload succeeded; "
                "blobs with sha=%s may be orphaned in storage",
                rev.content_token.sha,
            )
            raise
        # create_workflow_output returns WorkflowOutputDto (has extra system_id).
        # Construct a WorkflowOutputFileDto from shared fields so _bind works cleanly.
        # Use dict comprehension to automatically include new fields from schema updates.
        output_file_dto = WorkflowOutputFileDto.model_construct(
            **{
                k: v
                for k, v in dto.__dict__.items()
                if k in WorkflowOutputFileDto.model_fields
            }
        )
        return WorkflowOutput._bind(output_file_dto, mgr=self)

    # ------------------------------------------------------------------
    # Archivable hooks
    # ------------------------------------------------------------------

    def _archive(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(
            self._engine.v3_api.archive_workflow_log_entry,
            obj.system_id,
            obj.id,
        )

    def _restore(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(
            self._engine.v3_api.restore_workflow_log_entry,
            obj.system_id,
            obj.id,
        )

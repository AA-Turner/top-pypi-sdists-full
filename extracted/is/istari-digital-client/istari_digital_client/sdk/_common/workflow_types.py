"""Rich workflow domain types: WorkflowLogEntry and WorkflowOutput.

A rich type subclasses its pure generated v3 DTO and mixes in capabilities.
All DTO fields are inherited; the mixins add behavior bound to the manager
that produced the object (via ClientHaving._bind).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field, StrictStr

from istari_digital_client.sdk._base import Archivable, ClientHaving, Readable
from istari_digital_client.sdk._generated.v3.models.workflow_log_entry_dto import WorkflowLogEntryDto
from istari_digital_client.sdk._generated.v3.models.workflow_output_file_dto import WorkflowOutputFileDto

if TYPE_CHECKING:
    from istari_digital_client.sdk._common.workflows import Workflows


class WorkflowOutput(WorkflowOutputFileDto, ClientHaving, Readable):
    """A workflow output file attached to a WorkflowLogEntry.

    Fields: id, file_revision_id, name (str | None), extension (str |
    None), size (int | None, bytes), mime (str | None), display_name (str |
    None), external_identifier (str | None), description (str | None),
    content_token, created (datetime), created_by_id (str).

    Readable: call read_bytes(), read_text(), read_json(), or
    read_json() to fetch content from storage.

    Produced by Workflows.create_output() and populated in the outputs list
    of a WorkflowLogEntry returned by Workflows.get(). Not populated on entries
    returned by Workflows.list(), Workflows.create(), or Workflows.restore().
    """

    #: See :class:`Resource.file_id` — kept off the facade data model (excluded from
    #: dumps/JSON and repr) while still populated by the generated DTO.
    file_id: StrictStr = Field(exclude=True, repr=False)

    if TYPE_CHECKING:
        _mgr: Workflows  # narrows from _Manager


class WorkflowLogEntry(WorkflowLogEntryDto, ClientHaving, Archivable):
    """A workflow run — a logged simulation / analysis run record for a system.

    Aliases: workflow run simulation analysis execution


    Fields: id, system_id, title (str | None), status (str: "SUCCESS" |
    "FAILED" | "UNSPECIFIED" | "RUNNING" | "CANCELED"), workflow_type (str:
    "external" | ...), configuration_id (str | None), branch_id (str | None),
    branch_name (str | None), branchless (bool), file_count (int),
    total_file_size (int, bytes), archived (bool), created (datetime),
    created_by_id (str).

    Object methods: archive(), restore().

    The outputs property returns attached WorkflowOutput objects. It is
    populated only when the entry is returned by Workflows.get(); it is empty
    for entries from Workflows.list(), Workflows.create(), or
    Workflows.restore().
    """

    if TYPE_CHECKING:
        _mgr: Workflows  # narrows from _Manager

    @property
    def outputs(self) -> list[WorkflowOutput]:
        """Workflow output files attached to this entry.

        Populated only when the entry is returned by Workflows.get(). Empty
        for entries from Workflows.list(), Workflows.create(), or
        Workflows.restore(). Each item is a WorkflowOutput (Readable).
        """
        return getattr(self, "_outputs", [])


__all__ = ["WorkflowLogEntry", "WorkflowOutput"]

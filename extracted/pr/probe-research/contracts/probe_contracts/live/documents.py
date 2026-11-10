"""The `data` of `notes.changed` and `summary.changed` (rl-next W54): an entity's notes or summary page has a new
version. The text stays on the notes and overview routes."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from ..compat import StrEnum


class DocumentEntity(StrEnum):
    """Whose document changed. The team note belongs to the team (a team event: no refs)."""

    PROJECT = "project"
    EXPERIMENT = "experiment"
    RUN = "run"
    TEAM = "team"


class DocumentChangedData(BaseModel):
    """`notes.changed` / `summary.changed`: the document's new version."""

    entity: DocumentEntity
    #: None for the team note.
    entity_id: UUID | None = None
    version: int = Field(ge=0)

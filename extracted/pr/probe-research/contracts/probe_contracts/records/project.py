"""Project: where research is filed, what it is for, and who may read and write it."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import AliasChoices, Field

from ..compat import StrEnum
from .records import Record


class ProjectKind(StrEnum):
    """What a project is FOR. Presentation + generation steering only."""

    TRAINING = "training"
    EVALUATION = "evaluation"
    RESEARCH = "research"
    GENERAL = "general"
    #: 0231. Structural, not intent: a leaf answering one question, held by 3 CHECKs (DESIGN.md). `kind`
    #: never changes into or out of it, so reclassifying is create-and-move, never a PATCH.
    EXPERIMENT = "experiment"


class Project(Record):
    """A project as every surface reads it (the list row's fields)."""

    id: UUID
    customer_id: str
    # Nullable on the READ path only: rows written before 0019 may carry none.
    workspace_id: UUID | None
    slug: str
    # A plain `str` over a nullable column (0095): an unnamed project reads as its slug.
    name: str
    description: str | None = None
    # Server-stamped creator (0081); NULL on pre-0081 rows, which read as "unknown".
    created_by: str | None = None
    # The parent an older client reads, projected from `part_of` links (projects are flat).
    parent_project_id: UUID | None = None
    # 0401: the projects this one is PART OF, oldest first. None = not computed.
    part_of: list[UUID] | None = None
    # 0149: a `ProjectKind` value, as a plain str on purpose: rows are DB-CHECK-guaranteed, and an
    # enum-validated read would 500 a rolling deploy once a new member widens the CHECK first.
    kind: str = "general"
    # 0219, derived from `write_setting` since 0224; kept for older readers.
    access_mode: str = "inherit"
    # 0221. The two named settings that replace access_mode.
    read_setting: str = "inherit"
    write_setting: str = "inherit"
    # 0219. Whether THIS CALLER may edit it. None = not computed, never false.
    writable: bool | None = None
    # 0219. The node the access rule comes from (the column is `governing_node_id`).
    governed_by: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("governed_by", "governing_node_id"),
    )
    tags: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    # 0118. DERIVED from the `[README](repo url)` embed in the project document.
    repo: str | None = None
    # 0134. Attached code sources (active + suggested + missing). None = not computed.
    code_source_count: int | None = None
    # 0159. Everyone with a row on this project or beneath it. None = not computed
    # (and always None for service tokens), never "no contributors".
    contributor_user_ids: list[UUID] | None = None
    created_at: datetime
    updated_at: datetime

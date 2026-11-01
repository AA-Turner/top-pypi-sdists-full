"""Artifact: a file a run, experiment, project, paper or shared folder holds, and its upload state."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field

from ..compat import StrEnum
from .records import Record


class ArtifactStatus(StrEnum):
    """Upload lifecycle state of an artifact row (single source of truth for the
    string values; the DB CHECK ``artifacts_status_check`` mirrors this set).

    PENDING  -- presigned, blob not yet confirmed in R2.
    COMPLETE -- blob confirmed (client /confirm, the R2-event puller, or a reaper
                revive). Only COMPLETE rows count for have/need dedup.
    FAILED   -- terminally abandoned/failed upload (0030): kept for audit + an
                alertable signal. Comes back to COMPLETE only via an explicit
                client re-presign (which restages it to pending), NOT auto-revived
                from a shared content-addressed blob event. Never written by
                pre-0030 code.
    """

    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"


class AnchorLevel(StrEnum):
    """The three re-fileable artifact anchors (a Shared or paper file never moves
    here). Ordered run < experiment < project so `move`
    can tell a promote (derive the target up the chain) from a demote (target_id
    required, and validated to sit inside the current subtree) from a LATERAL move
    (same rank, a different sibling id)."""

    RUN = "run"
    EXPERIMENT = "experiment"
    PROJECT = "project"


class Artifact(Record):
    """A file as every surface reads it."""

    id: UUID
    customer_id: str
    project_id: UUID | None = None
    experiment_id: UUID | None = None
    run_id: UUID | None = None
    #: Always null since the workspace anchor's retirement (2026-10-17); kept so old clients parse.
    workspace_id: UUID | None = None
    shared_folder_id: UUID | None = None
    #: 0184. The paper this file belongs to, when a paper is its anchor.
    paper_id: UUID | None = None
    span_id: UUID | None = None
    step_index: int | None = None
    # Below-run coordinate key (0059); NULL when registered without coords.
    dims_hash: str | None = None
    kind: str
    name: str
    # Dirname of `name`, derived by the database (0029); '' for a root-level file.
    path: str = ""
    uri: str | None = None
    content_hash: str | None = None
    content_type: str | None = None
    size_bytes: int | None = None
    is_reference: bool
    meta: dict = Field(default_factory=dict)
    status: str = ArtifactStatus.COMPLETE
    #: Detector labels the credential gate found, never a matched value.
    #: None = nobody looked (NOT clean); [] = inspected, nothing found.
    credential_findings: list[str] | None = None
    #: Spans REPLACED before hashing; non-zero means these bytes are not the original.
    redacted_spans: int | None = None
    redacted_at: datetime | None = None
    created_at: datetime
    # Which anchor level a row came from; set only by the run inheritance listing.
    source_level: str | None = None

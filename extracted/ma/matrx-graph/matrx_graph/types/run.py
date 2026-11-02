from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.types.primitives import RunStatus


class Run(BaseModel):
    """Metadata for a single execution of a workflow.

    A Run is identified by `run_id` and optionally threads multiple checkpoints
    under the same `thread_id` (for conversational or multi-invocation graphs).
    Subgraph calls produce child Runs with `parent_run_id` set.

    The row is updated on status transitions; the append-only timeline lives
    in the checkpoint log.
    """

    model_config = ConfigDict(frozen=False)

    run_id: str
    thread_id: str
    parent_run_id: str | None = None
    definition_id: str
    definition_version_id: str
    status: RunStatus = RunStatus.PENDING
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None
    user_id: str = ""
    organization_id: str | None = None
    project_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

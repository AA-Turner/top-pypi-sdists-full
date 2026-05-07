from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Union

from typing_extensions import Self

from chalk.client import ChalkError

if TYPE_CHECKING:
    from pydantic import BaseModel
else:
    try:
        from pydantic.v1 import BaseModel
    except ImportError:
        from pydantic import BaseModel


class BatchProgress(BaseModel):
    total: int = 0
    computed: int = 0
    failed: int = 0
    start: Optional[datetime]
    end: Optional[datetime]
    total_duration_s: float = 0.0

    @classmethod
    def empty(cls) -> "BatchProgress":
        return BatchProgress(
            start=None,
            end=None,
            total=0,
            computed=0,
            failed=0,
            total_duration_s=0.0,
        )

    def __add__(self, other: BatchProgress) -> Self:
        if not isinstance(other, BatchProgress):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise NotImplementedError(
                f"Can only add ProgressReport to ProgressReport. Received '{type(other).__name__}'"
            )

        return type(self)(
            total=self.total + other.total,
            computed=self.computed + other.computed,
            failed=self.failed + other.failed,
            start=(
                self.start
                if other.start is None
                else (other.start if self.start is None else min(self.start, other.start))
            ),
            total_duration_s=self.total_duration_s + other.total_duration_s,
            end=None,
        )


class BatchProgressSum(BaseModel):
    total: int = 0
    computed: int = 0
    failed: int = 0
    total_duration_s: float = 0.0

    @classmethod
    def from_progresses(cls, *args: Union[BatchProgress, Iterable[BatchProgress]]) -> "BatchProgressSum":
        summed = BatchProgressSum()
        for arg in args:
            if not isinstance(arg, BatchProgress):
                for a in arg:
                    summed += a
            else:
                summed += arg

        return summed

    def __add__(self, other: BatchProgress) -> Self:
        if not isinstance(other, BatchProgress):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise NotImplementedError(f"Can only add BatchProgress to BatchProgress. Received '{type(other).__name__}'")

        return type(self)(
            total=self.total + other.total,
            computed=self.computed + other.computed,
            failed=self.failed + other.failed,
            total_duration_s=self.total_duration_s + other.total_duration_s,
        )


class BatchOpKind(str, Enum):
    OFFLINE_QUERY = "OFFLINE_QUERY"
    RECOMPUTE = "RECOMPUTE"
    CRON = "CRON"
    AGGREGATION_BACKFILL = "AGGREGATION_BACKFILL"


class BatchOpStatus(str, Enum):
    INIT = "INIT"
    COMPUTE_STARTED = "COMPUTE_STARTED"
    COMPUTE_ENDED = "COMPUTE_ENDED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ChunkReport(BaseModel):
    # doesn't have its own status.
    # resolver encapsulates the
    # status of the chunk.
    progress: BatchProgress
    generated_at: datetime


class BatchResolverReport(BaseModel):
    resolver_fqn: str
    status: BatchOpStatus
    chunks: List[ChunkReport]
    progress: BatchProgress
    generated_at: datetime
    error: Optional[ChalkError]
    all_errors: Optional[List[ChalkError]] = None


class BatchReport(BaseModel):
    operation_id: str
    operation_kind: BatchOpKind
    status: BatchOpStatus
    resolvers: List[BatchResolverReport]
    progress: BatchProgress
    environment_id: str
    team_id: str
    deployment_id: str
    error: Optional[ChalkError]
    generated_at: datetime
    all_errors: Optional[List[ChalkError]] = None
    operation_metadata: Optional[Dict[str, str]] = None
    computer_id: Optional[int] = None


class BatchReportResponse(BaseModel):
    report: Optional[BatchReport]
    error: Optional[ChalkError] = None


class InitiateOfflineQueryResponse(BaseModel):
    revision_id: uuid.UUID


class Heartbeat(BaseModel):
    operation_id: str
    operation_kind: BatchOpKind
    project_id: str
    environment_id: str
    team_id: str
    deployment_id: str
    generated_at: datetime
    computer_id: int
    shard_id: int

import datetime
import os
from typing import Generic, Literal, Optional, TypeVar

from abstra_internals.entities.execution_context import (
    ClientContext,
    FormExecutionMock,
    HookExecutionMock,
    ScriptExecutionMock,
)
from abstra_internals.utils.serializable import Serializable

T = TypeVar("T", bound=ClientContext)
ExecutionStatus = Literal["running", "failed", "finished", "abandoned"]


class Execution(Serializable, Generic[T]):
    id: str
    stage_id: str
    status: ExecutionStatus
    pid: int
    worker_id: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    context: T

    @classmethod
    def create(
        cls,
        *,
        id: str,
        stage_id: str,
        context: T,
        worker_id: str,
        pid: Optional[int] = None,
    ) -> "Execution[T]":
        return cls(
            stage_id=stage_id,
            context=context,
            status="running",
            id=id,
            # Timezone-aware UTC: stored verbatim into the timestamptz column on
            # the DB path (a naive local time would be misinterpreted in the PG
            # session TZ). The file path is unaffected — to_utc_iso_string is a
            # no-op shift on an already-aware value.
            created_at=datetime.datetime.now(datetime.timezone.utc),
            worker_id=worker_id,
            pid=pid or os.getpid(),
            updated_at=None,
        )

    def teardown_tests(self):
        self.context.mock_execution.test_pending_tasks = []
        if isinstance(self.context.mock_execution, HookExecutionMock):
            self.context.mock_execution.test_request = None
        elif isinstance(self.context.mock_execution, FormExecutionMock):
            self.context.mock_execution.test_answers = []
        elif isinstance(self.context.mock_execution, ScriptExecutionMock):
            self.context.mock_execution.test_trigger_task = None

    def set_status(self, status: ExecutionStatus) -> None:
        if status == "running":
            raise ValueError("Cannot set status to running")

        self.status = status
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)

    @property
    def short_id(self) -> str:
        return self.id[:8]

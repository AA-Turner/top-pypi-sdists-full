"""WorkflowStateSink — NATS streaming sink for activity effect handlers.

Wraps the Workflows API task() context manager. Opens with the initial TaskState;
each update() call passes the new TaskState to set_state(), which internally
computes JSON patches (via make_json_patch) and publishes them to NATS.

Satisfies the StateSink protocol.
"""

from types import TracebackType
from typing import Any

import structlog
from mistralai.workflows import task as workflow_task  # type: ignore[reportMissingImports]

from mistralai.vibe.sdk.agent.execution.compaction import COMPACTION_STREAM_NAME
from mistralai.vibe.sdk.agent.execution.loop import (
    HistoryScope,
    StateSink,
)
from mistralai.vibe.sdk.execution_record.state import MessageEntry, TaskState
from mistralai.vibe.sdk.providers.completion.tokens import latest_compaction_sentinel_index

logger = structlog.get_logger()

# Default stream namespace for activity state streams (one per LLM turn).
LLM_STREAM_NAME = "llm"


class WorkflowStateSink(StateSink):
    """StateSink backed by a Workflows API task() CM.

    Opens with the full TaskState so the SDK can compute JSON patches
    between successive states. Each update() publishes the new state via
    set_state(); the SDK diffs internally and emits JSONPatchPayload events.
    """

    def __init__(
        self,
        task_id: str,
        initial_state: TaskState | None = None,
        *,
        scope: HistoryScope | None = None,
        stream_name: str = LLM_STREAM_NAME,
        stream_sequence: int | None = None,
    ) -> None:
        self._task_id = task_id
        self._initial_state = initial_state
        self._scope = scope
        self._stream_name = stream_name
        self._stream_sequence = (
            stream_sequence
            if stream_sequence is not None
            else self._derive_stream_sequence(stream_name, initial_state)
        )
        self._ctx: Any = None
        self._t: Any = None

    @property
    def scope(self) -> HistoryScope | None:
        return self._scope

    @staticmethod
    def _derive_turn(state: TaskState | None) -> int:
        """Derive LLM turn counter from state history for unique NATS task IDs."""
        if state is None:
            return 0
        return sum(
            1
            for e in state.history
            if isinstance(e, MessageEntry) and e.payload.role == "assistant"
        )

    @staticmethod
    def _derive_stream_sequence(stream_name: str, state: TaskState | None) -> int:
        """Derive the state stream sequence for a stream namespace."""
        if state is None:
            return 0
        match stream_name:
            case _ if stream_name == COMPACTION_STREAM_NAME:
                index = latest_compaction_sentinel_index(state)
                return index if index >= 0 else 0
            case _:
                return WorkflowStateSink._derive_turn(state)

    async def __aenter__(self) -> "WorkflowStateSink":
        task_id_key = f"{self._task_id}/{self._stream_name}/{self._stream_sequence}"
        initial = self._initial_state.model_dump() if self._initial_state else {}
        logger.info("sink.open", sink_key=task_id_key)
        self._ctx = workflow_task("state_stream", state=initial, id=task_id_key)
        self._t = await self._ctx.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        logger.info("sink.close", has_error=exc_type is not None)
        if self._ctx is not None:
            await self._ctx.__aexit__(exc_type, exc_val, exc_tb)

    async def update(self, new_state: TaskState) -> None:
        """Publish new TaskState via set_state(). SDK computes patches internally.

        NATS publishing errors are swallowed — observability failures must
        never crash the workflow. A dropped update means a missed token in
        the live UI; correctness is unaffected (the durable control lane
        carries the final result).
        """
        if self._t is not None:
            try:
                await self._t.set_state(new_state.model_dump())
            except Exception:
                logger.warning("sink.update_failed", exc_info=True)

    def scoped(self, history_scope: HistoryScope) -> "WorkflowStateSink":
        return WorkflowStateSink(
            self._task_id,
            self._initial_state,
            scope=history_scope,
            stream_name=self._stream_name,
            stream_sequence=self._stream_sequence,
        )

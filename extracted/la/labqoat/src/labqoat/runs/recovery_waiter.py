"""Push-based recovery waiting with bounded reconnects and authoritative captured-cycle reconciliation."""

from contextlib import closing
from time import sleep

from labqoat._generated.recovery_operation import RecoveryOperation
from labqoat.errors.api_error import ApiError
from labqoat.errors.recovery_failed_error import RecoveryFailedError
from labqoat.errors.transport_error import TransportError
from labqoat.reconnect_budget import ReconnectBudget
from labqoat.runs.recovery_handle import RecoveryHandle
from labqoat.runs.run_event_cursor import RunEventCursor


class RecoveryWaiter:
    """Ignore old terminal Run snapshots and stop only when this operation or its admitted cycle terminates."""

    def __init__(self, handle: RecoveryHandle, max_reconnects: int) -> None:
        """Bind finite reconnect authority without mutating the original acceptance receipt."""
        if max_reconnects < 0:
            raise ValueError("max_reconnects must be nonnegative")
        self._handle = handle
        self._max_reconnects = max_reconnects
        self._cursor: str | None = None

    def run(self) -> RecoveryOperation:
        """Reconcile at stream boundaries; ordinary progress is driven exclusively by pushed events."""
        budget = ReconnectBudget(self._max_reconnects)
        while True:
            budget.opened()
            try:
                current = self._handle.refresh()
                if self._terminal(current):
                    return current
                self._follow()
                completed = self._handle.refresh()
                if self._terminal(completed):
                    return completed
            except TransportError:
                pass
            except ApiError as error:
                self._recover(error)
            if budget.exhausted():
                raise TransportError("Recovery event stream reconnect limit exceeded.")
            sleep(budget.delay())

    def _follow(self) -> None:
        """Release streams at completion and validate every replay position before storing it."""
        handle = self._handle
        with closing(handle.client.events(handle.accepted.run_id, handle.id, self._cursor)) as events:
            for event in events:
                self._cursor = RunEventCursor.position(handle.accepted.run_id, event)
                if event.event == "run.complete":
                    self._cursor = None
                    return

    def _recover(self, error: ApiError) -> None:
        """Reset an expired cursor but never retry deterministic admission or execution failures."""
        if error.status == 422 and self._cursor is not None:
            self._cursor = None
        elif error.status not in (502, 503, 504):
            raise error

    @staticmethod
    def _terminal(operation: RecoveryOperation) -> bool:
        """Return success only for the admitted cycle's immutable completed outcome."""
        if operation.phase in ("failed", "cancelled"):
            raise RecoveryFailedError(operation)
        if operation.execution_outcome in ("failed", "cancelled", "completed_with_errors"):
            raise RecoveryFailedError(operation)
        if operation.phase == "admitted":
            if operation.execution_outcome not in (None, "completed"):
                raise ApiError("Unknown recovery execution outcome")
            return operation.execution_outcome == "completed"
        if operation.phase not in ("accepted", "waiting_cleanup", "validating", "waiting_admission"):
            raise ApiError("Unknown recovery admission phase")
        return False

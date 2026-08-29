from contextvars import ContextVar

import temporalio.workflow

# 3MB soft limit under gRPC's 4MB RespondWorkflowTaskCompleted cap. The 1MB headroom
# absorbs gRPC framing, Temporal metadata, protobuf field headers, and the gap between
# the JSON size estimate and the encoded payload size.
DEFAULT_CHILD_START_BUDGET_BYTES = 3 * 1024 * 1024


def charge_for(
    size: int,
    max_charge: int = DEFAULT_CHILD_START_BUDGET_BYTES,
) -> int:
    return min(size, max_charge)


class ChildStartBudget:
    """Bounds the bytes of child-start commands issued but not yet confirmed by the server.

    Because confirmations only arrive in a later activation, this also bounds the bytes of
    child-start commands in any single workflow task completion — keeping the
    RespondWorkflowTaskCompleted message under gRPC's cap during a parallel fan-out.

    acquire(charge) blocks until the charged wire cost fits; release(charge) is called once
    the child's start is confirmed (i.e. start_child_workflow returned, which is the workflow
    task boundary for that command). Callers must pass the same value to both — compute it
    once via charge_for() at the call site.

    Replay-safe: wait_condition is Temporal's deterministic blocking primitive and the limit
    is a constant. The ``while`` is required because wait_condition holds no lock: after
    draining the ready list the instance checks every predicate in one pass, so two waiters
    can both see room and both be scheduled; the first to run takes the room and the second
    must re-check. The loop also keeps the common path synchronous — when there is room,
    acquire returns without suspending.

    Scaling ceiling: every release() re-evaluates all blocked waiters' predicates in one
    pass (O(n) per release). Fine for tens of children; a fan-out in the thousands would
    wake every waiter per release. Upgrade path: a FIFO queue of (size, future) pairs so
    only the head waiter is notified per release.
    """

    def __init__(self, limit_bytes: int = DEFAULT_CHILD_START_BUDGET_BYTES) -> None:
        self._limit = limit_bytes
        self._in_flight = 0

    async def acquire(self, charge: int) -> None:
        # A charge above the limit is a configuration error and would otherwise block forever.
        if charge > self._limit:
            raise RuntimeError(
                f"Child-start charge ({charge} bytes) exceeds the per-task budget ({self._limit} bytes). "
                "The budget limit must be at least the maximum child-start charge."
            )
        while self._in_flight + charge > self._limit:
            # Bind charge as a default arg so a future refactor mutating `charge` after this
            # lambda is created can't silently change the predicate.
            bound_charge = charge

            def _has_room(c: int = bound_charge) -> bool:
                return self._in_flight + c <= self._limit

            await temporalio.workflow.wait_condition(_has_room)
        self._in_flight += charge

    def release(self, charge: int) -> None:
        # A double-release or mismatched charge would drive _in_flight negative and silently
        # over-permit every future acquire. Assert loud during testing.
        assert self._in_flight >= charge, f"release({charge}) underflows in_flight={self._in_flight}"
        self._in_flight -= charge


# Per-run budget gate. Set in the interceptor's execute_workflow so the same instance is
# visible to signal/update handlers that start children within the run.
child_start_budget_var: ContextVar[ChildStartBudget | None] = ContextVar("child_start_budget", default=None)

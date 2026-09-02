"""matrx-ai persistence — call-site bridge to ``matrx_orm.Session``.

**Status (Phase G, May 2026):** The legacy WriteCoordinator and its
hand-rolled coalesce / DAG / flush / fallback / InFlightRegistry have
been removed. The canonical primitives live in
:mod:`matrx_orm.session` (``Session``, ``WatchedLifecycleRegistry``,
the sweeper). This module is now a thin call-site bridge that hosts
the cx_-specific table registry and the per-request Coordinator façade.

What still lives here:

* :class:`Coordinator` (and its back-compat alias ``WriteCoordinator``)
  — the per-request façade that the streaming lane finalizer flushes on
  every exit path. Internally wraps ``matrx_orm.Session``.
* :func:`get_coordinator` / queue helpers — call-site API. New code
  prefers ``async with Session():`` directly; the helpers stay for the
  large number of legacy call sites that haven't migrated yet.
* :func:`standalone_coordinator` — isolated synchronous ownership for
  scheduled/background writes to Coordinator-owned cx_ tables.
* :func:`replay_pending` + ``ReplayReport`` — recovery for
  ``system_write_failure`` rows.
* :func:`register_table` / :func:`get_persistence_model` — the cx_
  table-name → Model class registry consumed by the queue helpers.

What moved to matrx-orm:

* Coalescing → :mod:`matrx_orm.session.coalesce`
* FK-inferred DAG → :mod:`matrx_orm.session.dag`
* Transactional flush → :mod:`matrx_orm.session.flush`
* Fresh-connection fallback → :mod:`matrx_orm.session.fallback`
* Watchdog (predicates, sweeper) → :mod:`matrx_orm.session.lifecycle`
  (registered from ``aidream/db/watchdog_configs.py``)

See ``docs/persistence/SESSION_ARCHITECTURE.md`` for the canonical
reference.
"""

from matrx_ai.persistence.coordinator import (
    Coordinator,
    CoordinatorPhase,
    FlushReason,
    FlushReport,
    OpType,
    PersistenceBarrierError,
    WriteCoordinator,  # back-compat alias for Coordinator
)
from matrx_ai.persistence.queue_helpers import (
    get_coordinator,
    queue_agent_memory_create,
    queue_agent_memory_delete,
    queue_agent_memory_update,
    queue_conversation_create,
    queue_conversation_update,
    queue_message_create,
    queue_message_update,
    queue_om_event_create,
    queue_om_memory_create,
    queue_om_memory_update,
    queue_request_create,
    queue_request_snapshot_create,
    queue_request_update,
    queue_tool_call_create,
    queue_tool_call_update,
    queue_tool_trace_create,
    queue_user_request_create,
    queue_user_request_update,
    standalone_coordinator,
)
from matrx_ai.persistence.registry import (
    get_model as get_persistence_model,
)
from matrx_ai.persistence.registry import (
    is_registered,
    register_table,
)
from matrx_ai.persistence.replay import (
    RECOVERABLE_RETRY_ERRORS,
    ReplayReport,
    replay_pending,
    run_auto_replay_loop,
)

__all__ = [
    "Coordinator",
    "CoordinatorPhase",
    "FlushReason",
    "FlushReport",
    "OpType",
    "PersistenceBarrierError",
    "RECOVERABLE_RETRY_ERRORS",
    "ReplayReport",
    "WriteCoordinator",
    "get_coordinator",
    "queue_agent_memory_create",
    "queue_agent_memory_delete",
    "queue_agent_memory_update",
    "get_persistence_model",
    "is_registered",
    "queue_conversation_create",
    "queue_conversation_update",
    "queue_message_create",
    "queue_message_update",
    "queue_om_memory_create",
    "queue_om_memory_update",
    "queue_om_event_create",
    "queue_request_create",
    "queue_request_snapshot_create",
    "queue_request_update",
    "queue_tool_call_create",
    "queue_tool_call_update",
    "queue_tool_trace_create",
    "queue_user_request_create",
    "queue_user_request_update",
    "register_table",
    "replay_pending",
    "run_auto_replay_loop",
    "standalone_coordinator",
]

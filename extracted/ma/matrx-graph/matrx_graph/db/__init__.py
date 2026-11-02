"""Database integration for matrx-graph.

Two layers:

1. **DI registry** (`_registry`) — holds references to matrx-orm-generated
   models and managers. The host app populates it via `configure_db()` at
   startup; matrx-graph code resolves them by name via `get_instance(...)`.
   This mirrors `matrx_ai.db._registry` exactly.

2. **Raw asyncpg pool access** (`pool`) — thin wrapper around matrx-orm's
   AsyncDatabaseManager for code (like PostgresCheckpointer) that wants to run
   hand-rolled SQL without going through the generated managers. Works
   whether or not `configure_db()` has been called, as long as matrx-orm
   has a database registered.

Migration files live in `db/migrations/`. Apply via your usual flow before
running the app.
"""

from __future__ import annotations

from matrx_graph.db._registry import (
    DBNotConfiguredError,
    configure_db,
    get_base,
    get_extra,
    get_instance,
    get_model,
    is_configured,
    reset_for_tests,
    try_get_instance,
    try_get_model,
)
from matrx_graph.db.definition_store import DefinitionRow, DefinitionStore
from matrx_graph.db.event_store import EventStore
from matrx_graph.db.node_data_slot_store import (
    MAX_SLOT_VALUE_BYTES,
    VALID_SLOTS,
    NodeDataSlotRow,
    NodeDataSlotStore,
    SlotValueTooLargeError,
)
from matrx_graph.db.pool import acquire, get_db_config_name, set_db_config_name
from matrx_graph.db.run_store import (
    RunStore,
    configure_run_origin,
    configure_run_settings,
    configure_run_settled,
    configure_run_waiting,
)
from matrx_graph.db.standalone import (
    build_standalone_models,
    configure_standalone_db,
)
from matrx_graph.db.trigger_event_store import (
    TriggerEventRow,
    TriggerEventStore,
    build_event_inputs,
    event_row_actor,
    event_run_metadata,
    store_change_of,
)
from matrx_graph.db.trigger_store import (
    EventSourceSpec,
    StoreEventSource,
    TableEventSource,
    TriggerKind,
    TriggerRow,
    TriggerStore,
    event_source_json,
    validate_event_source,
)
from matrx_graph.db.wf_manager import WfManagers, wf

__all__ = [
    "MAX_SLOT_VALUE_BYTES",
    "VALID_SLOTS",
    "DBNotConfiguredError",
    "DefinitionRow",
    "DefinitionStore",
    "EventStore",
    "NodeDataSlotRow",
    "NodeDataSlotStore",
    "RunStore",
    "configure_run_origin",
    "configure_run_settings",
    "configure_run_settled",
    "configure_run_waiting",
    "SlotValueTooLargeError",
    "EventSourceSpec",
    "StoreEventSource",
    "TableEventSource",
    "event_source_json",
    "validate_event_source",
    "TriggerEventRow",
    "TriggerEventStore",
    "TriggerKind",
    "TriggerRow",
    "TriggerStore",
    "build_event_inputs",
    "event_row_actor",
    "event_run_metadata",
    "store_change_of",
    "WfManagers",
    "acquire",
    "configure_db",
    "configure_standalone_db",
    "get_base",
    "get_db_config_name",
    "get_extra",
    "get_instance",
    "get_model",
    "is_configured",
    "build_standalone_models",
    "reset_for_tests",
    "set_db_config_name",
    "try_get_instance",
    "try_get_model",
    "wf",
]

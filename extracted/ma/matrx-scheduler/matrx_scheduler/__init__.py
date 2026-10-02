"""
matrx-scheduler — server-side execution engine for the sch_* scheduling spine.

Public API:
    configure(...)          — wire host-supplied dependencies (call at startup)
    start_scanner()         — spawn the background scanner asyncio task
    stop_scanner()          — graceful shutdown
    status()                — current scanner health (last tick, queue depth, etc.)
    validate_cron(...)      — server-authoritative cron expression validator
    next_n_fires(...)       — preview a cron expression's next N fires
    compute_next_due_at(...) — compute the next fire time for any trigger config

HTTP API (optional, requires matrx-connect + fastapi):
    matrx_scheduler.api.include_routers(app, prefix="/scheduler")

Models (Pydantic):
    SchTask, SchAgentTask, SchTrigger, SchRun
    HydratedTask, AgentRunInput, AgentRunResult
"""

from __future__ import annotations

from ._ext import configure, configure_db, get_db_model, has_ext, is_configured
from .cron_helpers import (
    fire_count_in_window,
    next_n_fires,
    validate_cron,
)
from .continuation import MAX_CONTINUATIONS_PER_FIRE
from .backlog import BacklogRearmOutcome, BacklogRearmRequest, finalize_and_rearm_backlog
from .lease import RUN_PROGRESS_AT_KEY, NoLease, RunLease, current_run_lease
from .models import (
    RUN_CONTINUATION_KEY,
    RUN_INTERRUPTED_STATUS,
    RUN_STOPPED_EARLY_KEY,
    RUN_UNITS_DONE_KEY,
    AgentRunInput,
    AgentRunResult,
    BacklogRearmResult,
    AuthMode,
    HydratedTask,
    RunStatus,
    SchAgentTask,
    SchRun,
    SchTask,
    SchTrigger,
    ToolRunInput,
    TriggerType,
)


__version__ = "0.3.0"
from .next_due import compute_next_due_at
from .scanner import (
    ScannerStatus,
    is_running,
    start_scanner,
    status,
    stop_scanner,
)


__all__ = [
    # configuration
    "configure",
    "configure_db",
    "get_db_model",
    "is_configured",
    "has_ext",
    # opt-in durable backlog continuation
    "BacklogRearmRequest",
    "BacklogRearmOutcome",
    "finalize_and_rearm_backlog",
    # scanner
    "start_scanner",
    "stop_scanner",
    "status",
    "is_running",
    "ScannerStatus",
    # cron helpers
    "validate_cron",
    "next_n_fires",
    "fire_count_in_window",
    "compute_next_due_at",
    # the run lease every handler inherits
    "RunLease",
    "NoLease",
    "current_run_lease",
    "RUN_PROGRESS_AT_KEY",
    # the continuation every interrupted run inherits
    "MAX_CONTINUATIONS_PER_FIRE",
    "RUN_CONTINUATION_KEY",
    "RUN_INTERRUPTED_STATUS",
    # models
    "SchTask",
    "SchAgentTask",
    "SchTrigger",
    "SchRun",
    "HydratedTask",
    "AgentRunInput",
    "AgentRunResult",
    "BacklogRearmResult",
    "RUN_UNITS_DONE_KEY",
    "RUN_STOPPED_EARLY_KEY",
    "ToolRunInput",
    "TriggerType",
    "RunStatus",
    "AuthMode",
    # version
    "__version__",
]

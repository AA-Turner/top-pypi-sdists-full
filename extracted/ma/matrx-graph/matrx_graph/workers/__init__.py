"""Distributed workflow execution — queue + worker runner.

Phase 5 scaffolding. The queue + runner are complete and testable against
a real Postgres; concrete app wiring (AppContext factory, Scheduler
instantiation per job) lives in aidream's worker entry point.

Architecture::

    POST /workflows/:id/runs  ─┐
                               ├─▶ if inline_budget < N:   run inline
                               │                           (unchanged behavior)
                               └─▶ else:                   enqueue job
                                                          → wf_run row (pending)
                                                          → wf_job row
                                   worker process:
                                     claim_one()          (FOR UPDATE SKIP LOCKED)
                                     → build AppContext (null emitter OK)
                                     → load Definition   (DefinitionStore)
                                     → compile + run     (Scheduler)
                                     → update wf_run
                                     → complete(job_id)  (retained audit row)

Failure modes:
- Worker crash mid-job: visibility_timeout expires, another worker picks it up.
- Retryable job failure with a nonterminal run: bounded exponential backoff with jitter.
- Terminal/exhausted failure: retained dead-letter state; operators inspect.

Schema: see packages/matrx-graph/matrx_graph/db/migrations/0100_baseline_post_reorg.sql
"""

from matrx_graph.workers.cron_watcher import CronWatcher, FireTrigger
from matrx_graph.workers.event_watcher import EventWatcher, FireEvent
from matrx_graph.workers.queue import (
    FailureClass,
    FailureDisposition,
    Job,
    JobHandedBack,
    claim_one,
    classify_failure,
    complete,
    discard_for_run,
    enqueue,
    enqueue_claimed,
    defer_for_capability,
    fail,
    hand_back,
    release,
    retry_delay_seconds,
)
from matrx_graph.workers.capability import (
    JobNeedsCapability,
    missing_node_types,
    required_node_types,
    stamp_runs_awaiting_capability,
    worker_capabilities,
)
from matrx_graph.workers.runner import (
    AppContextFactory,
    JobRunner,
    WorkerRunner,
    active_runner,
    run_single_job,
)

__all__ = [
    "AppContextFactory",
    "CronWatcher",
    "EventWatcher",
    "FireEvent",
    "FireTrigger",
    "FailureClass",
    "FailureDisposition",
    "Job",
    "JobHandedBack",
    "JobNeedsCapability",
    "JobRunner",
    "WorkerRunner",
    "active_runner",
    "claim_one",
    "classify_failure",
    "complete",
    "discard_for_run",
    "enqueue",
    "enqueue_claimed",
    "defer_for_capability",
    "fail",
    "hand_back",
    "missing_node_types",
    "required_node_types",
    "stamp_runs_awaiting_capability",
    "worker_capabilities",
    "release",
    "retry_delay_seconds",
    "run_single_job",
]

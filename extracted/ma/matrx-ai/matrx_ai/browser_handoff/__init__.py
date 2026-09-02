"""Cloud Browser human-handoff park/resume — the WS-6 deliverable.

Executable form of contracts S5 (handoff ↔ runtime park/resume) and S6 (tool
surface / typed outcomes) in
``common-docs/projects/persistent-cloud-browser/``.

A handoff is a client-delegated tool call whose "client" is a human at a Cloud
Browser panel. This package adds the human-episode lifecycle on top of the
platform's EXISTING delegated path + the ``matrx-runtime`` spine — and nothing
else: no waiter, no lease table, no resume endpoint family, no new abandonment
constant, no second CAS over the pending-call ledger.

Public surface:
  * models: the wire shapes crossing the seams + the ``HandoffSource`` protocol
    the Browser Manager (or the test ``FakeHandoffSource``) implements;
  * seam: ``set_handoff_ledger`` / ``get_handoff_ledger`` — the injected durable
    pending-call operations (no fallback);
  * coordinator: ``BrowserHandoffCoordinator`` (park + resume) and
    ``Reconciler`` (restart-safe re-drive);
  * outcomes: the additive S6 tool payloads a producer builds;
  * handle: the D-3 stable agent-facing handle.
"""

from __future__ import annotations

from matrx_ai.browser_handoff.coordinator import (
    BrowserHandoffCoordinator,
    ParkReceipt,
    ReconcileAction,
    ReconcileActionKind,
    Reconciler,
    ResumeReceipt,
    resolution_key,
)
from matrx_ai.browser_handoff.handle import (
    AgentBrowserHandle,
    RunResolver,
    resolve_current_run,
    stable_handle_for,
)
from matrx_ai.browser_handoff.models import (
    CHECKPOINT_KIND,
    SUSPEND_REASON,
    BrowserHandoffToolOutput,
    ControllerKind,
    HandoffOpenRequest,
    HandoffReason,
    HandoffRecord,
    HandoffResolution,
    HandoffResolutionKind,
    HandoffResolutionReceipt,
    HandoffSource,
    HandoffState,
    HandoffTicket,
    PageFacts,
    PageInventory,
    ParkOutcome,
    WorkerQuiesced,
)
from matrx_ai.browser_handoff.outcomes import (
    NEW_ERROR_TYPES,
    human_required_output,
    new_error,
    ok_identity,
    page_inventory_payload,
    reopened_for_handoff_output,
)
from matrx_ai.browser_handoff.seam import (
    HandoffLedger,
    HandoffLedgerUnavailable,
    get_handoff_ledger,
    has_handoff_ledger,
    set_handoff_ledger,
)

__all__ = [
    # coordinator
    "BrowserHandoffCoordinator",
    "Reconciler",
    "ParkReceipt",
    "ResumeReceipt",
    "ReconcileAction",
    "ReconcileActionKind",
    "resolution_key",
    # models
    "HandoffOpenRequest",
    "HandoffTicket",
    "HandoffRecord",
    "HandoffResolution",
    "HandoffResolutionKind",
    "HandoffResolutionReceipt",
    "HandoffSource",
    "HandoffReason",
    "HandoffState",
    "ControllerKind",
    "WorkerQuiesced",
    "PageFacts",
    "PageInventory",
    "ParkOutcome",
    "BrowserHandoffToolOutput",
    "CHECKPOINT_KIND",
    "SUSPEND_REASON",
    # seam
    "HandoffLedger",
    "HandoffLedgerUnavailable",
    "set_handoff_ledger",
    "get_handoff_ledger",
    "has_handoff_ledger",
    # outcomes
    "new_error",
    "NEW_ERROR_TYPES",
    "ok_identity",
    "human_required_output",
    "reopened_for_handoff_output",
    "page_inventory_payload",
    # handle (D-3)
    "AgentBrowserHandle",
    "RunResolver",
    "stable_handle_for",
    "resolve_current_run",
]

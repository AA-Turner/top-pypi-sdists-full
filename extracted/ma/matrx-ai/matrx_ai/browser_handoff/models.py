"""Wire models for the Cloud Browser human-handoff park/resume protocol.

These are the shapes that cross the seam between the Browser Manager
(``matrx-scraper``, out of this package), the ``browser_*`` tools (this
package), and the runtime spine (``matrx-runtime``). They are the executable
form of contracts S5 (handoff ↔ runtime) and S6 (tool surface / typed
outcomes) in ``common-docs/projects/persistent-cloud-browser/``.

The load-bearing decision (S5 §0): a handoff is NOT a new suspension mechanism
— it is a client-delegated tool call whose "client" is a human. These models
carry only the human-episode lifecycle on top of the existing delegated path;
they never re-implement a waiter, a lease table, an abandonment constant, or a
second compare-and-swap over the pending-call ledger.

Pydantic v2, ``extra="forbid"`` unless a shape is explicitly open.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field


# --------------------------------------------------------------------------
# Reasons (S5 §5.1 / S6 §5.2)
# --------------------------------------------------------------------------
# 🚨 OWNERSHIP: S1 §2.8 (browser.handoff.reason) is the single definition and
# the ONE owner of this vocabulary; S2 §12.3, S5, and S6 all reproduce these
# literals verbatim and point here. The pre-freeze OPEN(reason-enum ownership
# sync) is resolved (2026-08-18): the earlier S6-flavoured spellings
# (`credential_missing`, `account_selection`, `sensitive_action_approval_required`,
# `unsafe_to_interpret`) were divergent and are gone. The tool still passes the
# caller's reason string through UNTOUCHED; this enum types our own producers.
class HandoffReason(StrEnum):
    CREDENTIALS_MISSING = "credentials_missing"
    CREDENTIALS_REJECTED = "credentials_rejected"
    MFA_REQUIRED = "mfa_required"
    TOTP_UNAVAILABLE = "totp_unavailable"
    PUSH_APPROVAL_REQUIRED = "push_approval_required"
    WEBAUTHN_REQUIRED = "webauthn_required"
    CAPTCHA_REQUIRED = "captcha_required"
    PROVIDER_CONSENT_REQUIRED = "provider_consent_required"
    ACCOUNT_SELECTION_REQUIRED = "account_selection_required"
    SENSITIVE_ACTION_APPROVAL = "sensitive_action_approval"
    PAYMENT_APPROVAL = "payment_approval"
    DESTRUCTIVE_CHANGE_APPROVAL = "destructive_change_approval"
    UNRECOGNIZED_PAGE = "unrecognized_page"
    SESSION_REVOKED_BY_PROVIDER = "session_revoked_by_provider"
    AGENT_REQUESTED = "agent_requested"
    USER_REQUESTED = "user_requested"  # human clicked "Take control", no agent trigger
    OPERATOR_REQUESTED = "operator_requested"


# --------------------------------------------------------------------------
# Controller / lifecycle string sets (S5 §1) — pinned for all three repos.
# --------------------------------------------------------------------------
ControllerKind = Literal[
    "agent_control",
    "handoff_requested",
    "human_control",
    "resume_pending",
    "stopped",
]

HandoffState = Literal[
    "requested",
    "claimed",
    "returning",
    "returned",
    "cancelled",
    "expired",
    "superseded",
]

# Checkpoint discriminator — invariant 5 (S5 §9): every browser park writes a
# checkpoint whose kind is exactly this string.
CHECKPOINT_KIND = "browser_handoff"

# The parked runtime status is WAITING_INPUT, never PAUSED (S5 §9 invariant 6).
# aidream additionally labels the suspend reason on its orchestrator via
# ``suspended_awaiting_human_browser`` (S5 P5, OPEN(status-string ratification));
# that label is an aidream integration concern and is carried in the checkpoint
# ``reason`` field, not invented here.
SUSPEND_REASON = "suspended_awaiting_human_browser"


# --------------------------------------------------------------------------
# Safe facts (S5 §5.4) — content-free page/account metadata the model may see.
# --------------------------------------------------------------------------
class PageFacts(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page_id: str
    origin: str  # scheme://host[:port]
    url: str | None = None  # redaction-policy filtered; None when policy strips it
    title: str | None = None
    is_active: bool = False
    is_popup: bool = False
    has_open_dialog: bool = False


class PageInventory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_count: int
    pages: list[PageFacts]
    active_page_id: str | None = None
    open_dialogs: int = 0
    pending_downloads: int = 0
    sanitized_description: str = ""
    captured_at: datetime
    # NOT a URL — a Matrx file id, never returned to the model (S5 §5.4 note).
    boundary_artifact_id: str | None = None

    def stripped_for_model(self) -> PageInventory:
        """The inventory the model receives: boundary_artifact_id removed so no
        capture reference reaches a model (S6 §6)."""
        return self.model_copy(update={"boundary_artifact_id": None})


# --------------------------------------------------------------------------
# P1: worker → Browser Manager (S5 §5.3). Referenced by WS-2; reproduced so the
# park sequence can type its input.
# --------------------------------------------------------------------------
class WorkerQuiesced(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    controller_revision: int  # the revision the worker is now fenced at
    queue_drained: bool  # MUST be True; False is a PARK REFUSAL, never a park
    in_flight_aborted: bool = False
    boundary_artifact_id: str | None = None
    inventory: PageInventory
    quiesced_at: datetime


# --------------------------------------------------------------------------
# tool → Browser Manager (S5 §5.2)
# --------------------------------------------------------------------------
class HandoffOpenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    profile_id: str
    reason: HandoffReason
    safe_instructions: str  # shown to the human; content-free
    requested_by_execution_id: str
    requested_by_user_id: str
    # None ⇒ non-conversation flavor (no auto-resume, S5 §0.2 / §7).
    conversation_id: str | None = None
    pending_call_id: str
    expected_controller_revision: int
    account_binding_id: str | None = None


class HandoffTicket(BaseModel):
    """Browser Manager → tool: the receipt of P2 (row + controller transition)."""

    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    run_id: str
    resolution_key: str  # f"{handoff_id}:{pending_call_id}" — S5 §4.4
    controller_revision: int  # revision AFTER the handoff_requested transition
    state: HandoffState = "requested"
    expires_at: datetime | None = None
    reconnect_deadline: datetime | None = None


class HandoffRecord(BaseModel):
    """The durable human-episode row, as the panel / reconciler read it."""

    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    run_id: str
    profile_id: str
    reason: HandoffReason
    state: HandoffState
    resolution_key: str
    pending_call_id: str
    pending_execution_id: str
    conversation_id: str | None = None
    controller_revision: int
    outcome_label: str | None = None
    requested_at: datetime
    expires_at: datetime | None = None
    reconnect_deadline: datetime | None = None
    returning_at: datetime | None = None
    returned_at: datetime | None = None
    tool_resolved_at: datetime | None = None
    resume_dispatched_at: datetime | None = None
    claimed_by_user_id: str | None = None
    returned_by_user_id: str | None = None
    boundary_artifact_id: str | None = None


# --------------------------------------------------------------------------
# Browser Manager → resolver seam (S5 §5.5)
# --------------------------------------------------------------------------
class HandoffResolutionKind(StrEnum):
    COMPLETED = "completed"  # human returned control
    CANCELLED = "cancelled"  # human / authorized actor cancelled
    EXPIRED = "expired"  # nobody claimed / nobody returned in the window
    REOPENED = "reopened"  # live run was gone; state restored from checkpoint


class HandoffResolution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    resolution_key: str  # f"{handoff_id}:{pending_call_id}" — S5 §4.4
    kind: HandoffResolutionKind
    run_id: str
    profile_id: str
    pending_call_id: str
    conversation_id: str | None = None
    execution_id: str
    controller_revision: int  # the NEW agent fencing token (R3)
    outcome_label: str | None = None  # human's hint (a HINT, never proof)
    inventory: PageInventory | None = None
    resolved_by_user_id: str | None = None
    resolved_at: datetime


class HandoffResolutionReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resolved: bool  # this call won the tool-completion CAS
    already_resolved: bool = False  # a prior call won it (idempotent success)
    not_found: bool = False  # unknown call — a real defect; alarm
    continuation_needed: bool = False  # from resolve_client_tool_results
    user_request_id: str | None = None


# --------------------------------------------------------------------------
# What the model finally receives (S5 §5.7). The literal-True field is the rule
# "the label is a hint, never proof" made structural — it survives every prompt
# rewrite.
# --------------------------------------------------------------------------
class BrowserHandoffToolOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal[
        "human_handoff_completed",
        "human_handoff_cancelled",
        "human_handoff_expired",
        "human_handoff_reopened",
    ]
    handoff_id: str
    session_id: str  # S6 compatibility handle mapped to run_id
    run_id: str
    profile_id: str
    reason: HandoffReason
    human_outcome_label: str | None = None
    human_outcome_is_unverified: Literal[True] = True
    page_inventory: PageInventory  # boundary_artifact_id stripped
    next_step_hint: str = (
        "Verify the signed-in / completed state on the page yourself before "
        "continuing. The human's outcome label is a hint, not proof."
    )


# --------------------------------------------------------------------------
# Seam protocols (S5 §8, §5.6)
# --------------------------------------------------------------------------
@runtime_checkable
class HandoffSource(Protocol):
    """The Browser Manager client the park/resume protocol drives. The real
    implementation lives in ``matrx-scraper``; ``FakeHandoffSource`` (tests)
    implements the identical protocol so the production code under test is
    unchanged (S5 §8)."""

    async def open_handoff(self, req: HandoffOpenRequest) -> HandoffTicket: ...
    async def get_handoff(self, handoff_id: str) -> HandoffRecord: ...
    async def get_handoff_or_none(self, handoff_id: str | None) -> HandoffRecord | None: ...
    async def claim(self, handoff_id: str, *, user_id: str) -> HandoffRecord: ...
    async def return_control(
        self, handoff_id: str, *, user_id: str, outcome_label: str | None
    ) -> HandoffResolution: ...
    async def cancel(
        self, handoff_id: str, *, user_id: str
    ) -> HandoffResolution: ...
    # Reconciler-facing operations (Browser Manager; a killed process re-drives
    # every sequence through these from durable rows alone).
    async def resolution_for(self, handoff_id: str) -> HandoffResolution: ...
    async def expire(self, handoff_id: str) -> HandoffResolution: ...
    async def mark_resume_dispatched(self, handoff_id: str) -> None: ...
    async def mark_tool_resolved(self, handoff_id: str) -> None: ...


class ParkOutcome(StrEnum):
    PARKED = "parked"
    REFUSED = "refused"  # queue not drained — no row, no delegate, no park (S5 §8 #10)

"""S2 worker-protocol Pydantic models — the wire contract, verbatim.

Every model is ``extra="forbid"`` with no bare ``Any`` (the one necessarily-open
field, ``EvalJsResult.value``, lives in ``commands.py`` and carries the
``api-any-ok`` waiver in ``actions.py``). Op-specific SUCCESS fields on a response
carry defaults so a typed refusal (``ok=False`` + ``error``) is still constructible
of the correct response type — the envelope is always complete, the success payload
is only meaningful when ``ok`` is True.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_scraper.cloud_browser.worker.commands import (
    BrowserCommand,
    BrowserCommandResult,
)
from matrx_scraper.cloud_browser.worker.errors import WorkerError

# ── Constants (S2 §5, §7.2, §10.2) — declared once here for the worker layer ──
INLINE_CAPTURE_CAP = 2 * 1024 * 1024  # 2 MiB
PAGE_INVENTORY_CAP = 50
REPLAY_CACHE_SIZE = 64
EVENT_BUFFER_CAP = 256

# ── Controller & handoff enums (S2 §10.1, §12.3) ──
ControllerStateName = Literal[
    "provisioning",
    "agent_control",
    "handoff_requested",
    "human_control",
    "resume_pending",
    "stopping",
    "stopped",
    "failed",
]

# Aligned to S1 §2.8 (`browser.handoff.reason`), the ONE owner of this
# vocabulary (2026-08-18). S2 §12.3 reproduces the identical set; the worker
# emits from it verbatim. The pre-freeze spellings (`captcha_or_anti_bot`,
# `webauthn_or_passkey`, `push_or_number_match`, `provider_consent`,
# `account_selection`, `page_not_interpretable`) were divergent and are gone.
HandoffReason = Literal[
    "credentials_missing",
    "credentials_rejected",
    "mfa_required",
    "totp_unavailable",
    "push_approval_required",
    "webauthn_required",
    "captcha_required",
    "provider_consent_required",
    "account_selection_required",
    "sensitive_action_approval",
    "payment_approval",
    "destructive_change_approval",
    "unrecognized_page",
    "session_revoked_by_provider",
    "agent_requested",
    "user_requested",
    "operator_requested",
]

CaptureReason = Literal[
    "run_start",
    "run_stop",
    "pre_navigation",
    "post_navigation",
    "pre_consequential_action",
    "post_consequential_action",
    "error",
    "timeout",
    "human_boundary_handoff_requested",
    "human_boundary_claim",
    "human_boundary_return",
    "human_boundary_resume",
    "post_login_verified",
    "operator",
]

# The four human-boundary reasons admitted during human_control (S2 §11.2).
HUMAN_BOUNDARY_REASONS: frozenset[str] = frozenset(
    {
        "human_boundary_handoff_requested",
        "human_boundary_claim",
        "human_boundary_return",
        "human_boundary_resume",
    }
)


# ── Common envelope (S2 §3) ──


class WorkerCallEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    profile_id: str
    fencing_token: str
    fencing_revision: int = Field(ge=1)
    sequence: int | None = None
    idempotency_key: str | None = None
    issued_at: datetime
    deadline_ms: int = 60_000


class ControllerState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    state: ControllerStateName
    controller_kind: Literal["agent", "human", "none"]
    controller_ref: str | None
    fencing_revision: int
    handoff_id: str | None
    since: datetime
    human_input_enabled: bool


class WorkerReplyEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: bool
    error: WorkerError | None = None
    run_id: str
    profile_id: str
    worker_id: str
    controller: ControllerState
    fencing_revision: int
    sequence_applied: int | None = None
    replayed: bool = False
    queue_depth: int
    queue_state: Literal["open", "draining", "closed"]
    run_mode: Literal["handoff_capable", "automation_only"]
    worker_health: Literal[
        "starting", "healthy", "degraded", "browser_crashed", "stopping", "stopped"
    ]
    chromium_version: str
    worker_version: str
    observed_at: datetime


# ── Page inventory (S2 §10.2 / §10.3) ──


class PageRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page_id: str
    opener_page_id: str | None
    kind: Literal["page", "popup", "pdf_viewer"]
    is_active: bool
    is_closed: bool
    safe_url: str | None
    origin: str | None
    title: str | None
    opened_at: datetime
    closed_at: datetime | None
    opened_by: Literal["agent", "human", "page", "unknown"]
    last_focused_at: datetime | None
    load_state: Literal["loading", "loaded", "crashed"]


class DialogRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dialog_id: str
    page_id: str
    type: Literal["alert", "confirm", "prompt", "beforeunload"]
    opened_at: datetime
    message_present: bool
    message: str | None = None
    default_value_present: bool
    handled: bool


class DownloadRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    download_id: str
    page_id: str
    suggested_filename: str
    state: Literal["pending", "completed", "failed", "cancelled"]
    byte_count: int | None
    content_hash: str | None
    started_at: datetime
    completed_at: datetime | None
    uploaded: bool
    failure_code: str | None


class FileChooserRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chooser_id: str
    page_id: str
    is_multiple: bool
    opened_at: datetime


class PermissionPromptRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_id: str
    page_id: str
    permission: Literal[
        "geolocation", "notifications", "camera", "microphone", "clipboard", "midi", "other"
    ]
    opened_at: datetime


class PageInventory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    revision: int
    active_page_id: str | None
    pages: list[PageRecord] = Field(default_factory=list)
    dialogs: list[DialogRecord] = Field(default_factory=list)
    downloads: list[DownloadRecord] = Field(default_factory=list)
    file_choosers: list[FileChooserRecord] = Field(default_factory=list)
    permission_prompts: list[PermissionPromptRecord] = Field(default_factory=list)
    captured_at: datetime
    truncated: bool = False
    total_page_count: int = 0


class HumanEpisodeSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    claimed_at: datetime
    returned_at: datetime | None
    navigation_count: int
    pages_opened: int
    pages_closed: int
    dialogs_opened: int
    downloads_started: int
    pointer_activity_buckets: int
    keyboard_activity_buckets: int
    origins_visited: list[str] = Field(default_factory=list)


class HumanRequiredSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: HandoffReason
    detected_by: Literal["adapter", "heuristic", "tool"]
    safe_origin: str
    safe_instructions: str | None = None
    page_id: str
    detected_at: datetime
    adapter_version: str | None = None


class ActionEventFacts(BaseModel):
    model_config = ConfigDict(extra="forbid")

    actor: Literal["agent", "human", "system"]
    action_kind: str
    target_description: str | None = None
    safe_url: str | None = None
    origin_host: str | None = None
    started_at: datetime
    ended_at: datetime
    duration_ms: int
    result_class: Literal[
        "ok", "not_found", "timeout", "navigation", "browser", "validation", "blocked", "conflict"
    ]
    error_code: str | None = None
    capture_suppressed_reason: str | None = None
    chromium_version: str
    worker_version: str
    adapter_version: str | None = None


# ── bootstrap (S2 §5.1) ──


class CheckpointRestore(BaseModel):
    """Ephemeral material needed to restore one encrypted profile archive."""

    model_config = ConfigDict(extra="forbid")

    download_url: str
    headers: dict[str, str] = Field(default_factory=dict)
    expires_at: datetime
    dek_plaintext_b64: str
    nonce_b64: str
    ciphertext_hash: str
    plaintext_hash: str


class ProfileMount(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_data_dir: str
    source: Literal["active_volume", "restored_checkpoint"]
    checkpoint_id: str | None = None
    expected_content_hash: str | None = None
    profile_format_version: int
    expected_chromium_version: str | None = None
    restore: CheckpointRestore | None = None


class DisplayConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["xvfb"]
    width: int
    height: int
    color_depth: int = 24
    dpi: int = 96


class LaunchPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_mode: Literal["handoff_capable", "automation_only"]
    reopened_for_handoff: bool = False
    reopened_controller_state: (
        Literal["agent_control", "handoff_requested", "human_control", "resume_pending"] | None
    ) = None
    reopened_handoff_id: str | None = None
    reopened_human_input_enabled: bool = False
    viewport: dict[str, int] | None = None
    user_agent: str | None = None
    locale: str | None = None
    timezone_id: str | None = None
    proxy: str | None = None
    allow_eval_js: bool = False
    allow_downloads: bool = True
    trace_enabled: bool = False
    video_enabled: bool = False
    idle_stop_after_ms: int = 600_000
    handoff_idle_keepalive_ms: int = 1_800_000


class BootstrapRequest(WorkerCallEnvelope):
    mount: ProfileMount
    policy: LaunchPolicy
    activation_key: str
    initial_fencing_token: str
    sequence_base: int
    callback_url: str
    callback_token: str
    display: DisplayConfig | None = None


class BootstrapResponse(WorkerReplyEnvelope):
    accepted: bool
    host_lock_acquired: bool
    display_ref: str | None = None
    page_inventory: PageInventory | None = None
    volatile_state_preserved: bool = False
    egress_guard_installed: bool = False


# ── heartbeat (S2 §5.2) ──


class HeartbeatRequest(WorkerCallEnvelope):
    lease_expires_at: datetime
    rotate_callback_token: bool = False
    access_still_valid: bool


class HeartbeatResponse(WorkerReplyEnvelope):
    lease_acknowledged: bool = False
    callback_token: str | None = None
    idle_ms: int = 0
    last_sequence_applied: int | None = None
    page_count: int = 0
    pending_events: int = 0
    checkpoint_recommended: bool = False


# ── command (S2 §5.3) ──


class CommandRequest(WorkerCallEnvelope):
    origin: Literal["agent", "system", "human_boundary"]
    execution_ref: str | None = None
    tool_call_ref: str | None = None
    page_id: str | None = None
    command: BrowserCommand


class CommandResponse(WorkerReplyEnvelope):
    result: BrowserCommandResult | None = None
    active_page_id: str | None = None
    page_inventory_revision: int = 0
    human_required: HumanRequiredSignal | None = None
    event_facts: ActionEventFacts | None = None


# ── observe (S2 §5.4) ──


class ObserveRequest(WorkerCallEnvelope):
    include: list[
        Literal["pages", "dialogs", "downloads", "file_choosers", "permissions", "human_episode"]
    ] = Field(default_factory=lambda: ["pages", "dialogs", "downloads"])
    since_inventory_revision: int | None = None


class ObserveResponse(WorkerReplyEnvelope):
    page_inventory: PageInventory | None = None
    human_episode: HumanEpisodeSummary | None = None


# ── capture (S2 §5.5) ──


class PresignedUpload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method: Literal["PUT"]
    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    expires_at: datetime


class CapturedArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["screenshot", "trace", "video"]
    media_type: str
    byte_count: int
    content_hash: str
    width: int | None = None
    height: int | None = None
    uploaded: bool = False
    image_base64: str | None = None
    masked_selector_count: int = 0
    redaction_policy_version: str


class CaptureRequest(WorkerCallEnvelope):
    kind: Literal["screenshot", "trace_start", "trace_stop", "video_start", "video_stop"]
    reason: CaptureReason
    page_id: str | None = None
    full_page: bool = False
    selector: str | None = None
    mask_selectors: list[str] = Field(default_factory=list)
    redaction_policy_version: str
    upload_target: PresignedUpload | None = None
    return_base64: bool = False


class CaptureResponse(WorkerReplyEnvelope):
    captured: bool = False
    suppressed_reason: str | None = None
    artifact: CapturedArtifact | None = None


# ── controller_transition (S2 §5.6) ──


class ControllerTransitionRequest(WorkerCallEnvelope):
    to_state: Literal["agent_control", "handoff_requested", "human_control", "resume_pending"]
    reason: str
    new_fencing_token: str
    new_fencing_revision: int
    controller_ref: str | None = None
    handoff_id: str | None = None
    drain_timeout_ms: int = 30_000
    boundary_capture: CaptureRequest | None = None
    enable_human_input: bool


class ControllerTransitionResponse(WorkerReplyEnvelope):
    from_state: ControllerStateName
    to_state: ControllerStateName
    queue_drained: bool = False
    drained_command_count: int = 0
    abandoned_command_count: int = 0
    human_input_enabled: bool = False
    boundary_artifact: CapturedArtifact | None = None
    page_inventory: PageInventory | None = None


# ── checkpoint (S2 §5.7) ──


class CheckpointManifestFacts(BaseModel):
    model_config = ConfigDict(extra="forbid")

    checkpoint_id: str
    profile_format_version: int
    archive_format_version: int
    chromium_version: str
    key_version: str
    plaintext_hash: str
    ciphertext_hash: str
    byte_count: int


class CheckpointRequest(WorkerCallEnvelope):
    checkpoint_id: str
    mode: Literal["close_and_archive", "archive_only_after_close"]
    reason: Literal["stop", "boundary", "post_login", "pre_move", "operator", "scheduled"]
    dek_plaintext_b64: str
    dek_wrapped_b64: str
    key_version: str
    nonce_b64: str
    archive_format_version: int
    upload_target: PresignedUpload
    drain_timeout_ms: int = Field(default=30_000, ge=0, le=120_000)
    zeroize_after: bool = True


class CheckpointResponse(WorkerReplyEnvelope):
    checkpoint_id: str
    chromium_exited_cleanly: bool = False
    plaintext_hash: str = ""
    ciphertext_hash: str = ""
    byte_count: int = 0
    uploaded: bool = False
    manifest: CheckpointManifestFacts | None = None
    zeroized: bool = False
    context_relaunched: bool = False


# ── shutdown (S2 §5.8) ──


class ShutdownRequest(WorkerCallEnvelope):
    reason: Literal[
        "normal_stop",
        "idle",
        "expired",
        "moved",
        "revoked",
        "operator",
        "reopen_for_handoff",
        "emergency_fence",
    ]
    drain_timeout_ms: int = 30_000
    final_checkpoint: CheckpointRequest | None = None


class ShutdownResponse(WorkerReplyEnvelope):
    stopped: bool = False
    queue_drained: bool = False
    abandoned_command_count: int = 0
    checkpoint: CheckpointResponse | None = None
    uncheckpointed_state: bool = False
    host_lock_released: bool = False
    zeroized: bool = False


# ── worker → manager events (S2 §6) ──


class WorkerEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    run_id: str
    profile_id: str
    worker_id: str
    fencing_revision: int
    emitted_at: datetime
    kind: Literal[
        "handoff_requested",
        "browser_crashed",
        "page_opened",
        "page_closed",
        "dialog_opened",
        "download_started",
        "download_completed",
        "download_failed",
        "queue_idle",
        "idle_stop_pending",
        "egress_blocked",
        "worker_degraded",
    ]
    page_id: str | None = None
    handoff_reason: HandoffReason | None = None
    safe_url: str | None = None
    detail_code: str | None = None

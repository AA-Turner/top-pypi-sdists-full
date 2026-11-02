"""Session workflow output type."""

import enum

from pydantic import BaseModel, field_validator


class TerminationReason(enum.StrEnum):
    COMPLETED = "completed"
    TIMED_OUT = "timed_out"
    STOPPED = "stopped"
    FAILED = "failed"


CANONICAL_TERMINATION_REASONS: frozenset[str] = frozenset(r.value for r in TerminationReason)


class SessionLimitCause(enum.StrEnum):
    """Which Session limit ended a stopped Session."""

    LIFETIME_LIMIT = "lifetime_limit"
    IDLE_LIMIT = "idle_limit"


class SessionWorkflowFailureCode(enum.StrEnum):
    SANDBOX_EXPIRED = "sandbox_expired"
    SANDBOX_SETUP_FAILED = "sandbox_setup_failed"
    QUOTA_UNAVAILABLE = "quota_unavailable"
    GITHUB_AUTHORIZATION_TIMED_OUT = "github_authorization_timed_out"
    GITHUB_APP_INSTALLATION_MISSING = "github_app_installation_missing"
    VCS_GIT_SETUP_FAILED = "vcs_git_setup_failed"
    VCS_GIT_PROXY_SETUP_FAILED = "vcs_git_proxy_setup_failed"
    VCS_CLONE_FAILED = "vcs_clone_failed"
    VCS_DIFF_APPLY_FAILED = "vcs_diff_apply_failed"
    VCS_NOT_CONNECTED = "vcs_not_connected"
    VCS_RECONNECT_REQUIRED = "vcs_reconnect_required"
    # Workspace persistence could not be synced to VibeFS before the sandbox
    # was taken down (suspend or delete). Terminal and observable by design:
    # the sandbox is kept alive rather than silently deleting unsynced data.
    VIBEFS_SYNC_FAILED = "vibefs_sync_failed"
    # Deprecated aliases - kept for attribute-level backward compatibility only.
    # Do not use in new code; use the VCS_* names above.
    GITHUB_GIT_SETUP_FAILED = "vcs_git_setup_failed"
    GITHUB_GIT_PROXY_SETUP_FAILED = "vcs_git_proxy_setup_failed"
    GITHUB_CLONE_FAILED = "vcs_clone_failed"
    GITHUB_DIFF_APPLY_FAILED = "vcs_diff_apply_failed"


# Wire values written before AGE-1113 used github_* prefixes. Map them to the
# canonical vcs_* values so that stored Temporal completion events continue to
# deserialize correctly.
_LEGACY_FAILURE_CODE_WIRE_MAP: dict[str, str] = {
    "github_clone_failed": "vcs_clone_failed",
    "github_git_setup_failed": "vcs_git_setup_failed",
    "github_git_proxy_setup_failed": "vcs_git_proxy_setup_failed",
    "github_diff_apply_failed": "vcs_diff_apply_failed",
    # The App installation is now verified once (no poll loop), so the former
    # *_TIMED_OUT wire value is remapped to the missing-installation code so stored
    # Temporal payloads continue to deserialize to the closest current semantics.
    "github_app_installation_timed_out": "github_app_installation_missing",
}


class SessionWorkflowOutput(BaseModel):
    final_message: str | None = None
    public_final_message: str | None = None
    failure_code: SessionWorkflowFailureCode | None = None
    actions_summary: str | None = None
    termination_reason: TerminationReason | None = None
    # Set on a stopped Session that a Session limit ended, rather than a stop command. A plain
    # string, so a control plane reads a cause that a newer worker adds.
    end_cause: str | None = None

    @field_validator("failure_code", mode="before")
    @classmethod
    def _migrate_legacy_failure_code(cls, v: object) -> object:
        if isinstance(v, str):
            return _LEGACY_FAILURE_CODE_WIRE_MAP.get(v, v)
        return v


__all__ = [
    "CANONICAL_TERMINATION_REASONS",
    "SessionLimitCause",
    "SessionWorkflowFailureCode",
    "SessionWorkflowOutput",
    "TerminationReason",
]

# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.models.overseer.model_agent_scope_presets
# COMPAT_REMOVAL_DATE: 2027-01-01

"""Pre-defined agent scope presets as named constants.

Each preset is a frozenset of string permission tokens representing the
capabilities granted to a specific agent role. Using frozensets guarantees
immutability — presets cannot be mutated at runtime.

Permission tokens follow the convention: <domain>:<action>
  e.g. "git:rebase", "pr:auto_merge", "pr:admin_merge", "git:force_push"

Prevents drift between agent roles by defining permitted operations here
rather than scattering them across callers.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Permission token constants — single source of truth for token strings
# ---------------------------------------------------------------------------

PERM_GIT_REBASE: str = "git:rebase"
PERM_GIT_FORCE_PUSH: str = "git:force_push"
PERM_PR_AUTO_MERGE: str = "pr:auto_merge"
PERM_PR_ADMIN_MERGE: str = "pr:admin_merge"
PERM_REPO_READ: str = "repo:read"
PERM_REPO_WRITE: str = "repo:write"
PERM_QUEUE_READ: str = "queue:read"
PERM_QUEUE_WRITE: str = "queue:write"
PERM_QUEUE_ADMIN: str = "queue:admin"
PERM_TICKET_READ: str = "ticket:read"
PERM_TICKET_WRITE: str = "ticket:write"

# ---------------------------------------------------------------------------
# Agent scope presets
# ---------------------------------------------------------------------------

# merge-sweep: scans open PRs, enables auto-merge, nudges stuck queues.
# Needs rebase + auto-merge; must NOT admin-merge directly.
SCOPE_MERGE_SWEEP: frozenset[str] = frozenset(
    {
        PERM_GIT_REBASE,
        PERM_PR_AUTO_MERGE,
        PERM_REPO_READ,
        PERM_QUEUE_READ,
        PERM_TICKET_READ,
    }
)

# ticket-work: implements a single Linear ticket end-to-end.
# Needs repo write + auto-merge but must NOT admin-merge or force-push.
SCOPE_TICKET_WORK: frozenset[str] = frozenset(
    {
        PERM_GIT_REBASE,
        PERM_PR_AUTO_MERGE,
        PERM_REPO_READ,
        PERM_REPO_WRITE,
        PERM_TICKET_READ,
        PERM_TICKET_WRITE,
    }
)

# sweep: read-only audit agents (contract-sweep, aislop-sweep, etc.).
# Read access to repo and queue; no write or merge permissions.
SCOPE_SWEEP: frozenset[str] = frozenset(
    {
        PERM_REPO_READ,
        PERM_QUEUE_READ,
        PERM_TICKET_READ,
    }
)

# active-queue-manager: manages the merge queue, can admin-merge to unblock.
# Has admin-merge; explicitly excluded from force-push.
SCOPE_ACTIVE_QUEUE_MANAGER: frozenset[str] = frozenset(
    {
        PERM_GIT_REBASE,
        PERM_PR_AUTO_MERGE,
        PERM_PR_ADMIN_MERGE,
        PERM_REPO_READ,
        PERM_QUEUE_READ,
        PERM_QUEUE_WRITE,
        PERM_QUEUE_ADMIN,
        PERM_TICKET_READ,
    }
)

__all__: list[str] = [
    # Permission token constants
    "PERM_GIT_REBASE",
    "PERM_GIT_FORCE_PUSH",
    "PERM_PR_AUTO_MERGE",
    "PERM_PR_ADMIN_MERGE",
    "PERM_REPO_READ",
    "PERM_REPO_WRITE",
    "PERM_QUEUE_READ",
    "PERM_QUEUE_WRITE",
    "PERM_QUEUE_ADMIN",
    "PERM_TICKET_READ",
    "PERM_TICKET_WRITE",
    # Scope presets
    "SCOPE_MERGE_SWEEP",
    "SCOPE_TICKET_WORK",
    "SCOPE_SWEEP",
    "SCOPE_ACTIVE_QUEUE_MANAGER",
]

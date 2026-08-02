# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.overseer — routing engine output contracts and session wire types."""

from omnibase_compat.overseer.model_agent_scope_presets import (
    PERM_GIT_FORCE_PUSH,
    PERM_GIT_REBASE,
    PERM_PR_ADMIN_MERGE,
    PERM_PR_AUTO_MERGE,
    PERM_QUEUE_ADMIN,
    PERM_QUEUE_READ,
    PERM_QUEUE_WRITE,
    PERM_REPO_READ,
    PERM_REPO_WRITE,
    PERM_TICKET_READ,
    PERM_TICKET_WRITE,
    SCOPE_ACTIVE_QUEUE_MANAGER,
    SCOPE_MERGE_SWEEP,
    SCOPE_SWEEP,
    SCOPE_TICKET_WORK,
)
from omnibase_compat.overseer.model_routing_decision import ModelRoutingDecision

__all__: list[str] = [
    "ModelRoutingDecision",
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

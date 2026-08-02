# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Tests for omnibase_compat.overseer exports.

After OMN-7326 removed dead shims (including ModelSessionContract),
the overseer module exports only ModelRoutingDecision.
"""

from __future__ import annotations

import importlib


def test_overseer_module_importable() -> None:
    """omnibase_compat.overseer must be importable."""
    spec = importlib.util.find_spec("omnibase_compat.overseer")
    assert spec is not None, "omnibase_compat.overseer module not found"


def test_overseer_exports_routing_decision_and_permission_tokens() -> None:
    """__all__ must contain ModelRoutingDecision and permission/scope constants."""
    from omnibase_compat import overseer

    expected = {
        "ModelRoutingDecision",
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
        "SCOPE_MERGE_SWEEP",
        "SCOPE_TICKET_WORK",
        "SCOPE_SWEEP",
        "SCOPE_ACTIVE_QUEUE_MANAGER",
    }
    assert set(overseer.__all__) == expected, (
        f"overseer.__all__ mismatch: got {set(overseer.__all__)}"
    )


def test_model_routing_decision_still_exported() -> None:
    """ModelRoutingDecision must still be exported (regression guard for OMN-8038)."""
    from omnibase_compat.overseer import ModelRoutingDecision

    assert ModelRoutingDecision is not None

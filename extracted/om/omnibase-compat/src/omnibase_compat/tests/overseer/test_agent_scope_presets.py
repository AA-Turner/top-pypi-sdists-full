# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for agent scope presets — OMN-8061."""

from __future__ import annotations

from omnibase_compat.overseer.model_agent_scope_presets import (
    PERM_GIT_FORCE_PUSH,
    PERM_GIT_REBASE,
    PERM_PR_ADMIN_MERGE,
    PERM_PR_AUTO_MERGE,
    PERM_QUEUE_ADMIN,
    SCOPE_ACTIVE_QUEUE_MANAGER,
    SCOPE_MERGE_SWEEP,
    SCOPE_SWEEP,
    SCOPE_TICKET_WORK,
)


def test_merge_sweep_has_rebase_and_auto_merge() -> None:
    assert PERM_GIT_REBASE in SCOPE_MERGE_SWEEP
    assert PERM_PR_AUTO_MERGE in SCOPE_MERGE_SWEEP


def test_ticket_work_cannot_admin_merge() -> None:
    assert PERM_PR_ADMIN_MERGE not in SCOPE_TICKET_WORK


def test_sweep_is_read_only_for_code_repository() -> None:
    write_tokens = {t for t in SCOPE_SWEEP if ":write" in t or ":admin" in t}
    merge_tokens = {t for t in SCOPE_SWEEP if t in (PERM_PR_AUTO_MERGE, PERM_PR_ADMIN_MERGE)}
    git_write_tokens = {t for t in SCOPE_SWEEP if t in (PERM_GIT_REBASE, PERM_GIT_FORCE_PUSH)}
    assert not write_tokens, f"sweep has write tokens: {write_tokens}"
    assert not merge_tokens, f"sweep has merge tokens: {merge_tokens}"
    assert not git_write_tokens, f"sweep has git write tokens: {git_write_tokens}"


def test_queue_manager_has_admin_merge_but_not_force_push() -> None:
    assert PERM_PR_ADMIN_MERGE in SCOPE_ACTIVE_QUEUE_MANAGER
    assert PERM_GIT_FORCE_PUSH not in SCOPE_ACTIVE_QUEUE_MANAGER


def test_merge_sweep_cannot_admin_merge() -> None:
    assert PERM_PR_ADMIN_MERGE not in SCOPE_MERGE_SWEEP


def test_merge_sweep_cannot_force_push() -> None:
    assert PERM_GIT_FORCE_PUSH not in SCOPE_MERGE_SWEEP


def test_ticket_work_cannot_force_push() -> None:
    assert PERM_GIT_FORCE_PUSH not in SCOPE_TICKET_WORK


def test_queue_manager_has_queue_admin() -> None:
    assert PERM_QUEUE_ADMIN in SCOPE_ACTIVE_QUEUE_MANAGER


def test_presets_are_frozensets() -> None:
    for preset in (SCOPE_MERGE_SWEEP, SCOPE_TICKET_WORK, SCOPE_SWEEP, SCOPE_ACTIVE_QUEUE_MANAGER):
        assert isinstance(preset, frozenset), f"preset {preset!r} is not a frozenset"


def test_presets_are_immutable() -> None:
    try:
        SCOPE_MERGE_SWEEP.add("should:fail")  # type: ignore[attr-defined]
        raise AssertionError("frozenset.add should raise AttributeError")
    except AttributeError:
        pass

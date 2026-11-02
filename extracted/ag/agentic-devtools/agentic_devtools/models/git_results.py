"""Structured result dataclasses for the worktree setup and Git operations nodes.

These result types are returned by the LangChain ``setup`` and ``commit`` nodes.
Following the clarified design (spec.md), a blocked/failed outcome is signalled by
embedding a :class:`BlockedState` in the result's ``error`` field rather than by
raising an exception — LangGraph conditional edges inspect the returned result to
decide the next node, so exceptions would bypass the graph's routing logic.

Key invariants:

- ``SetupResult`` / ``CommitResult`` success fields are all optional so a failed
  result (``error`` set before any worktree/branch/commit exists) need not carry
  empty-string placeholders. Callers MUST check ``error`` before reading success
  fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# Category enum for BlockedState. Categorised so the workflow engine's retry logic
# can classify a failure as transient (retryable) vs. permanent (escalate).
BlockedCategory = Literal[
    "transient",  # network error, lock contention — safe to retry
    "corruption",  # stale/invalid worktree directory — needs manual cleanup
    "conflict",  # rebase/merge/stash conflict — needs manual resolution
    "protection",  # branch protection rule rejected the push
    "auth",  # authentication/permission failure on push
    "context_mismatch",  # pre-flight context validation failed
]

SetupMode = Literal["created", "resumed"]


@dataclass
class BlockedState:
    """A structured error descriptor embedded in ``SetupResult``/``CommitResult``.

    Attributes:
        category: The failure classification (see :data:`BlockedCategory`). The
            workflow engine's retry logic uses this to decide whether to re-attempt
            (``transient``) or escalate (``conflict``, ``protection``, etc.).
        message: A human-readable description of the failure.
        details: Optional extra context (e.g. the list of conflicting files for a
            rebase conflict). ``None`` when no additional detail applies.
    """

    category: BlockedCategory
    message: str
    details: list[str] | None = None


@dataclass
class SetupResult:
    """Outcome of the setup node's execution.

    When ``error`` is ``None`` the result indicates success and ``worktree_path``,
    ``branch_name``, and ``mode`` are guaranteed to be set — the setup node converts
    any branch-lookup failure on the resume path into a ``context_mismatch``
    :class:`BlockedState` rather than producing a success result with
    ``branch_name`` unset. When ``error`` is non-``None`` the node returned before
    a worktree/branch was established (e.g. a ``git fetch origin`` failure), so the
    success fields MAY be ``None`` — callers MUST check ``error`` first.
    """

    worktree_path: str | None = None
    branch_name: str | None = None
    mode: SetupMode | None = None
    error: BlockedState | None = None


@dataclass
class CommitResult:
    """Outcome of the commit node's execution.

    When ``error`` is ``None`` all success fields are populated. When ``error`` is
    non-``None`` (rebase conflict, push rejection, git failure), ``commit_sha``,
    ``commit_message_title``, and ``is_amend`` MAY be ``None`` and ``push_succeeded``
    is ``False`` — callers MUST check ``error`` first.

    A no-op outcome (``no_op=True`` with ``error=None``) means there were no staged
    changes; the pull-request node still proceeds so a previously-pushed commit can
    open/update a PR (FR-008).
    """

    commit_sha: str | None = None
    commit_message_title: str | None = None
    is_amend: bool | None = None
    push_succeeded: bool = False
    no_op: bool = False
    error: BlockedState | None = None

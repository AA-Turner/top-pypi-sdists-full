"""
cvc.agent.parallel_safety — Hermes-style guardrails for parallel tool dispatch.

Problem
-------
CVC's ``TelepathicToolExecutor`` runs *every* tool call in parallel, including
``write_file``, ``patch_file``, and ``terminal``.  That is unsafe:

  • Two parallel writes to the same path race.
  • Interactive tools (``clarify``) cannot be parallelised.
  • Global-state tools (``terminal`` background, cron create) corrupt each other.
  • Every parallel call spawns a full CVC branch + commit + merge — insane
    overhead for 5 concurrent ``read_file``s.

This module ports Hermes Agent's parallel-tool guardrails to CVC:

  • ``PARALLEL_SAFE_TOOLS``    — read-only, no side effects, always parallelisable.
  • ``NEVER_PARALLEL_TOOLS``   — interactive or global-state, always sequential.
  • ``PATH_SCOPED_TOOLS``      — file tools, parallel only when paths differ.
  • ``detect_path_conflicts()`` — find two calls touching the same file.
  • ``partition_for_parallel()`` — split a batch into (parallel, sequential).

Decision = allow | block | path_check
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Iterable

logger = logging.getLogger("cvc.agent.parallel_safety")


# ── Allowlists / blocklists ──────────────────────────────────────────────────

#: Read-only tools with no side effects. Always safe to run concurrently.
PARALLEL_SAFE_TOOLS: frozenset[str] = frozenset({
    # File inspection
    "read_file", "list_dir", "glob", "grep", "search_files",
    "file_search", "find_files",
    # Knowledge / search
    "web_search", "web_extract", "session_search", "skill_view", "skills_list",
    # Analysis
    "vision_analyze", "video_analyze",
    # CVC read-only
    "cvc_log", "cvc_status", "cvc_recall", "cvc_context", "cvc_diff",
    "cvc_timeline", "cvc_get_context", "cvc_export",
    "cvc_audit", "cvc_stats", "cvc_branch",  # branch *list*, not create
    "cvc_hive_read", "cvc_hive_stats",
    "cvc_cognome_status", "cvc_cognome_compile", "cvc_cognome_audit",
    # Cost / usage (read-only)
    "cost_report", "usage_stats",
})

#: Interactive or global-state tools. Must ALWAYS run alone.
NEVER_PARALLEL_TOOLS: frozenset[str] = frozenset({
    "clarify", "ask_user", "prompt_user",  # interactive — needs user attention
    "terminal", "bash", "shell",           # global PTY / cwd state
    "task_create", "task_wait", "task_kill",  # background process registry
    "cron_create", "cron_update", "cron_delete",  # shared cron state
    "cvc_commit", "cvc_restore", "cvc_merge",     # cognitive state mutation
    "cvc_branch_create",                          # branch creation
    "send_message",                               # outward comms — serialise
    "memory", "fact_store",                       # persistent memory writes
    "delegate_task", "parallel_agents",           # sub-agent fan-out (own path)
})

#: File-mutating tools — parallel only when targeting different paths.
PATH_SCOPED_TOOLS: frozenset[str] = frozenset({
    "write_file", "edit_file", "patch_file", "patch",
    "create_file", "delete_file", "move_file",
})


# ── Decision enum ────────────────────────────────────────────────────────────

ALLOW = "allow"        # safe to parallelise
BLOCK = "block"        # must run sequentially
PATH_CHECK = "path"    # safe iff no other call in the batch touches the same path


@dataclass(frozen=True)
class ParallelDecision:
    """Per-tool-call parallelism decision."""
    decision: str          # ALLOW | BLOCK | PATH_CHECK
    reason: str = ""
    path_key: str | None = None   # normalised path for conflict detection


# ── Path extraction ──────────────────────────────────────────────────────────

def _normalise_path(p: str) -> str:
    """Normalise a path for conflict detection (lowercase, strip trailing /)."""
    if not p:
        return ""
    p = str(p).strip()
    # Collapse repeated slashes, strip trailing slash, lowercase (case-insensitive FS)
    import os
    p = os.path.normpath(p) if "/" in p or "\\" in p else p
    return p.lower()


def _extract_path(tool_name: str, args: dict[str, Any]) -> str | None:
    """
    Extract the filesystem path a PATH_SCOPED tool will touch.
    Returns None for tools without a path arg (treated as global → always conflict).
    """
    if not isinstance(args, dict):
        return None
    # Try common path argument names
    for key in ("path", "file_path", "filepath", "file", "filename"):
        v = args.get(key)
        if isinstance(v, str) and v:
            return _normalise_path(v)
    # patch tool uses 'path' too
    if tool_name in ("patch", "patch_file") and "path" in args:
        return _normalise_path(str(args["path"]))
    return None  # no path found → treat as global conflict


# ── Classification ───────────────────────────────────────────────────────────

def classify_tool(tool_name: str, args: dict[str, Any] | None = None) -> ParallelDecision:
    """
    Classify a single tool call for parallel-safety.

    Returns a ``ParallelDecision`` with:
      - ``ALLOW``      → safe to run concurrently with anything
      - ``BLOCK``      → must run alone (interactive / global state)
      - ``PATH_CHECK`` → safe iff no other call in the batch touches the same path
    """
    args = args or {}
    name = (tool_name or "").strip().lower()

    # Blocklist wins
    if name in NEVER_PARALLEL_TOOLS:
        return ParallelDecision(BLOCK, reason=f"{name} is interactive/global-state")

    # Path-scoped tools need conflict check
    if name in PATH_SCOPED_TOOLS:
        path = _extract_path(name, args)
        if path is None:
            return ParallelDecision(BLOCK, reason=f"{name} has no resolvable path")
        return ParallelDecision(PATH_CHECK, reason=f"{name} touches {path}", path_key=path)

    # Explicit allowlist
    if name in PARALLEL_SAFE_TOOLS:
        return ParallelDecision(ALLOW, reason=f"{name} is read-only")

    # Unknown tool — conservative default: allow if it looks read-only, else block.
    # Read-only heuristic: name contains read/list/get/search/show/view/log/status
    _READ_HEURISTIC = ("read", "list", "get", "search", "show", "view", "log",
                       "status", "inspect", "describe", "query", "fetch", "check")
    if any(h in name for h in _READ_HEURISTIC):
        return ParallelDecision(ALLOW, reason=f"{name} matches read-only heuristic")
    # Default: block unknown mutating tools
    return ParallelDecision(BLOCK, reason=f"{name} is unknown — conservative block")


# ── Batch partitioning ───────────────────────────────────────────────────────

@dataclass
class ParallelPartition:
    """Result of partitioning a batch of tool calls."""
    parallel: list[int]          # indices that can run concurrently
    sequential: list[int]        # indices that must run alone, in order
    conflicts: list[tuple[int, int]]  # pairs of indices that conflict on path
    decisions: list[ParallelDecision]  # per-index decision


def partition_for_parallel(
    tool_calls: list[dict[str, Any]],
) -> ParallelPartition:
    """
    Partition a batch of tool calls into (parallel-safe, must-sequential).

    Rules:
      1. ALLOW → parallel candidate.
      2. PATH_CHECK → parallel candidate iff no other PATH_CHECK call shares the
         same normalised path.
      3. BLOCK → always sequential.
      4. If any BLOCK is present, the whole batch runs sequentially (safest:
         the agent loop already handles single-tool dispatch efficiently, and
         mixing parallel + serial in one turn complicates ordering).

    Returns indices, not the calls themselves.
    """
    decisions = [
        classify_tool(tc.get("name", ""), tc.get("args", {}))
        for tc in tool_calls
    ]

    # Detect path conflicts among PATH_CHECK calls
    path_map: dict[str, list[int]] = {}
    conflicts: list[tuple[int, int]] = []
    for i, d in enumerate(decisions):
        if d.decision == PATH_CHECK and d.path_key:
            path_map.setdefault(d.path_key, []).append(i)
    for path_key, idxs in path_map.items():
        if len(idxs) > 1:
            # All pairs conflict
            for a_i in range(len(idxs)):
                for b_i in range(a_i + 1, len(idxs)):
                    conflicts.append((idxs[a_i], idxs[b_i]))

    # If any BLOCK or any path conflict → run whole batch sequentially
    has_block = any(d.decision == BLOCK for d in decisions)
    has_conflict = bool(conflicts)

    if has_block or has_conflict:
        return ParallelPartition(
            parallel=[],
            sequential=list(range(len(tool_calls))),
            conflicts=conflicts,
            decisions=decisions,
        )

    # All clear — everything is either ALLOW or non-conflicting PATH_CHECK
    return ParallelPartition(
        parallel=list(range(len(tool_calls))),
        sequential=[],
        conflicts=[],
        decisions=decisions,
    )


# ── Convenience predicate ────────────────────────────────────────────────────

def can_run_all_in_parallel(tool_calls: list[dict[str, Any]]) -> bool:
    """True iff every call in the batch is safe to run concurrently."""
    if len(tool_calls) <= 1:
        return False  # trivially serial — no need for parallel path
    part = partition_for_parallel(tool_calls)
    return len(part.parallel) == len(tool_calls) and not part.conflicts


__all__ = [
    "PARALLEL_SAFE_TOOLS",
    "NEVER_PARALLEL_TOOLS",
    "PATH_SCOPED_TOOLS",
    "ALLOW", "BLOCK", "PATH_CHECK",
    "ParallelDecision",
    "ParallelPartition",
    "classify_tool",
    "partition_for_parallel",
    "can_run_all_in_parallel",
]

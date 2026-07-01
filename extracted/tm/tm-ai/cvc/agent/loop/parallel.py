"""Parallel tool execution dispatcher.

Tool calls that are safe to run concurrently are fanned out across a
worker pool (default 8). Tools that touch the filesystem are scoped by
target path so non-overlapping calls still parallelize, while overlapping
ones fall back to sequential.
"""
from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Set


# Safe to dispatch in parallel — read-only or naturally idempotent.
_PARALLEL_SAFE_TOOLS: Set[str] = {
    "read_file",
    "search_files",
    "web_search",
    "web_extract",
    "session_search",
    "skill_view",
    "skills_list",
    "vision_analyze",
    "video_analyze",
    "browser_get_images",
    "fact_store",
    "memory",
}

# Never dispatch in parallel — interactive or globally serializing.
_NEVER_PARALLEL_TOOLS: Set[str] = {
    "clarify",
    "send_message",
    "execute_code",
    "terminal",  # shared shell session state
}

# Tools whose conflicts depend on a path argument.
_PATH_SCOPED_TOOLS: Dict[str, str] = {
    "read_file": "path",
    "search_files": "path",
    "write_file": "path",
    "patch": "path",
}


@dataclass
class ToolCall:
    name: str
    arguments: Dict[str, Any]
    call_id: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    call_id: str
    name: str
    output: Any
    error: str | None = None


def _path_key(call: ToolCall) -> str | None:
    arg_name = _PATH_SCOPED_TOOLS.get(call.name)
    if not arg_name:
        return None
    val = call.arguments.get(arg_name)
    if not isinstance(val, str):
        return None
    try:
        return os.path.realpath(os.path.expanduser(val))
    except Exception:
        return val


def _conflicts(a: ToolCall, b: ToolCall) -> bool:
    """Two calls conflict if they target the same path scope."""
    pa, pb = _path_key(a), _path_key(b)
    if pa is None or pb is None:
        return False
    # Conflict if one path is a prefix of the other (parent/child dir overlap).
    return pa == pb or pa.startswith(pb + os.sep) or pb.startswith(pa + os.sep)


def partition_calls(calls: List[ToolCall]) -> List[List[ToolCall]]:
    """Group calls into waves: each wave runs in parallel; waves run sequentially."""
    waves: List[List[ToolCall]] = []
    pending = list(calls)

    while pending:
        wave: List[ToolCall] = []
        leftover: List[ToolCall] = []
        for call in pending:
            if call.name in _NEVER_PARALLEL_TOOLS:
                if not wave:
                    wave.append(call)
                else:
                    leftover.append(call)
                continue
            if call.name not in _PARALLEL_SAFE_TOOLS and call.name not in _PATH_SCOPED_TOOLS:
                # Unknown / mutating tool → run alone.
                if not wave:
                    wave.append(call)
                else:
                    leftover.append(call)
                continue
            if any(_conflicts(call, existing) for existing in wave):
                leftover.append(call)
                continue
            wave.append(call)
        if not wave:
            wave = [pending[0]]
            leftover = pending[1:]
        waves.append(wave)
        pending = leftover

    return waves


def execute_parallel(
    calls: List[ToolCall],
    dispatcher: Callable[[ToolCall], ToolResult],
    *,
    max_workers: int = 8,
) -> List[ToolResult]:
    """Run a list of tool calls, parallelizing safe ones up to max_workers."""
    if not calls:
        return []

    waves = partition_calls(calls)
    results: Dict[str, ToolResult] = {}
    lock = threading.Lock()

    def _run(call: ToolCall) -> None:
        try:
            res = dispatcher(call)
        except Exception as exc:  # noqa: BLE001
            res = ToolResult(call_id=call.call_id, name=call.name, output=None, error=str(exc))
        with lock:
            results[call.call_id or f"{call.name}:{id(call)}"] = res

    with ThreadPoolExecutor(max_workers=max(1, max_workers)) as pool:
        for wave in waves:
            futures: List[Future] = [pool.submit(_run, c) for c in wave]
            for f in futures:
                f.result()

    # Preserve original order.
    out: List[ToolResult] = []
    for c in calls:
        key = c.call_id or f"{c.name}:{id(c)}"
        if key in results:
            out.append(results[key])
    return out


__all__ = [
    "ToolCall",
    "ToolResult",
    "partition_calls",
    "execute_parallel",
    "_PARALLEL_SAFE_TOOLS",
    "_NEVER_PARALLEL_TOOLS",
    "_PATH_SCOPED_TOOLS",
]

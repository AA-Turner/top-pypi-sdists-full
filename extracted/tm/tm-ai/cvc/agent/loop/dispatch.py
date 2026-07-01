"""Unified tool-dispatch layer for the CVC agent loop.

This module is the Category 3 integration point. The ``loop/`` package
already shipped its primitives (cost_budget, tool_risk, guardrails,
parallel, sanitize, multimodal, output_limits). What it did NOT ship
is the *single function* the gateway chat loop calls for every
tool_use the LLM emits. Today the gateway has its own ad-hoc
implementation: ``_is_dud_tool_call`` plus a 9,500-line chat loop
that does its own guardrail counting, its own dedup, and its own
per-call risk classification — none of which consults the primitives
in ``loop/``.

This module wires everything together behind one call:

    result = dispatch_tool_call(
        name=tc.name,
        arguments=tc.arguments,
        executor=_tool_executor,
        caches=session_caches,
        risk_registry=_loop_risk_registry,
    )

The return value is a structured :class:`DispatchResult` — the chat
loop turns it into a tool_result message and a stream of SSE events
(``tool_start`` / ``tool_result`` / ``status``). On any failure
(dud, loop-guard, verify-fail), the result carries an ``error`` field
with an actionable message the LLM can immediately act on.

Why one function, not one per concern
-------------------------------------
The previous design scattered dedup (``_is_dud_tool_call``), risk
classification (none — it was hand-rolled in the approval flow),
verification (none — the agent trusted the tool's return value), and
the cache (none — every ``read_file`` hit disk). Splitting them
across files would just recreate the problem: the chat loop has to
call them in the right order, and forgetting one of them silently
regresses the experience. Putting them in one function makes the
correctness argument obvious by reading the function body.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from .guardrails import GuardrailVerdict, ToolCallGuardrailController, ToolGuardrailDecision, is_destructive
from .output_limits import DEFAULT_LIMITS, truncate_output
from .parallel import ToolCall as ParallelToolCall, ToolResult as ParallelToolResult, execute_parallel
from .read_cache import ReadCache, SessionReadCaches, TreeCache
from .tool_risk import ToolRiskDecision, ToolRiskRegistry, classify_tool_risk
from .verify import VerifyResult, VerifyStatus, verify_patch, verify_replace, verify_write

logger = logging.getLogger("cvc.agent.loop.dispatch")

__all__ = [
    "DispatchStatus",
    "DispatchResult",
    "DispatchConfig",
    "DispatchStats",
    "ToolDispatcher",
    "dispatch_tool_call",
]


# Tools whose ``arguments["path"]`` (or similar) is the file path the
# read cache can intercept. Anything not in this set is passed through
# to the executor unchanged.
_PATH_ARG_TOOLS: Dict[str, str] = {
    "read_file": "path",
    "list_dir": "path",
    "search_files": "path",
    "write_file": "path",
    "edit_file": "path",
    "patch_file": "path",
    "patch": "path",
    "multi_read": "path",
}

# Tools whose result needs verification after the call. The verification
# is performed by the loop BEFORE the tool result is fed back to the LLM.
_VERIFY_TOOLS: Dict[str, str] = {
    "write_file": "content",   # full-content verify
    "patch": "new_string",     # substring verify
    "edit_file": "new_string", # substring verify (same shape as patch)
    "patch_file": "diff",      # substring verify against the new chunk
}

# Tools we treat as zero-arg-safe: they accept ``{}`` without being
# flagged as duds. Mirrors gateway.py's _ZERO_ARG_SAFE_TOOLS.
_ZERO_ARG_SAFE_TOOLS: frozenset = frozenset({
    "ask_user", "cvc_status", "cvc_log", "cvc_diff", "cvc_search",
    "cvc_smart_search", "cvc_list_documents", "task_list", "think",
    "context_compact", "todo", "save_memory",
})

# Tools whose required args the dispatcher must check up front. This
# duplicates the executor's _REQUIRED_ARGS — but keeping a local copy
# means the dispatcher can short-circuit BEFORE handing the call to
# the executor, which is what the user actually sees as "the model
# emitted a dud call" rather than "the executor returned KeyError".
_REQUIRED_ARGS: Dict[str, Tuple[str, ...]] = {
    "read_file": ("path",),
    "write_file": ("path", "content"),
    "edit_file": ("path", "old_string", "new_string"),
    "patch_file": ("path", "diff"),
    "bash": ("command",),
    "process_manage": ("process_id", "action"),
    "glob": ("pattern",),
    "grep": ("pattern",),
    "list_dir": ("path",),
    "web_search": ("query",),
    "cvc_branch": ("name",),
    "cvc_restore": ("commit_hash",),
    "cvc_merge": ("source_branch",),
    "cvc_search": ("query",),
}


# ── Result types ────────────────────────────────────────────────────


class DispatchStatus(str, Enum):
    """Outcome of one dispatch."""

    OK = "ok"
    DUD = "dud"                  # call rejected before execution (empty/missing args)
    HALTED = "halted"            # loop-guard tripped (identical-arg N+1)
    WARNED = "warned"            # loop-guard tripped but tool is idempotent — return WARN
    VERIFY_FAILED = "verify_failed"  # executed but post-state doesn't match intent
    TIMEOUT = "timeout"          # executor exceeded the per-tool timeout
    ERROR = "error"              # executor raised an exception
    DENIED = "denied"            # risk classifier says NO (destructive + no override)


@dataclass
class DispatchResult:
    """The structured return value of :func:`dispatch_tool_call`.

    The gateway chat loop turns this into a tool_result message plus
    SSE events. ``message`` is the value the LLM sees in its next turn.
    """

    status: DispatchStatus
    name: str
    call_id: str = ""
    message: str = ""                # the value the LLM sees
    output: Optional[str] = None     # raw executor output, if any
    duration_ms: float = 0.0
    risk_tier: str = ""              # ToolRiskTier.value
    verify: Optional[VerifyResult] = None
    cache_hit: bool = False          # True if read came from the read cache
    guardrail: Optional[ToolGuardrailDecision] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status is DispatchStatus.OK

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "name": self.name,
            "call_id": self.call_id,
            "message": self.message,
            "duration_ms": self.duration_ms,
            "risk_tier": self.risk_tier,
            "cache_hit": self.cache_hit,
            "verify": (self.verify.to_dict() if self.verify else None),
            "guardrail": (
                {"verdict": self.guardrail.verdict.value, "reason": self.guardrail.reason}
                if self.guardrail else None
            ),
        }


# ── Configuration ───────────────────────────────────────────────────


@dataclass
class DispatchConfig:
    """Per-call knobs. Defaults are safe for a single user session."""

    tool_timeout_seconds: float = 60.0
    verify_writes: bool = True       # post-write SHA-256 check
    verify_patches: bool = True     # post-patch substring check
    use_read_cache: bool = True      # route read_file/list_dir through the cache
    use_loop_guard: bool = True      # dedup identical-arg calls
    output_truncate_chars: int = DEFAULT_LIMITS.get("tool_result", 2000)
    destructive_check: Callable = is_destructive   # for tool_risk escalation


@dataclass
class DispatchStats:
    """Per-session counters — surfaced to the dashboard via SSE status events."""

    total: int = 0
    ok: int = 0
    duds: int = 0
    halts: int = 0
    warnings: int = 0
    verify_fails: int = 0
    timeouts: int = 0
    errors: int = 0
    cache_hits: int = 0
    cache_misses: int = 0

    def snapshot(self) -> dict:
        return {
            "total": self.total,
            "ok": self.ok,
            "duds": self.duds,
            "halts": self.halts,
            "warnings": self.warnings,
            "verify_fails": self.verify_fails,
            "timeouts": self.timeouts,
            "errors": self.errors,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
        }


# ── The dispatcher ──────────────────────────────────────────────────


class ToolDispatcher:
    """Per-session dispatcher — owns a guardrail controller and stats.

    The chat loop creates one of these per ``/api/chat`` request, calls
    :meth:`dispatch` for every tool_use the LLM emits, and reads
    :attr:`stats` to populate the SSE status events.
    """

    def __init__(
        self,
        *,
        config: Optional[DispatchConfig] = None,
        risk_registry: Optional[ToolRiskRegistry] = None,
        guardrail: Optional[ToolCallGuardrailController] = None,
        caches: Optional[SessionReadCaches] = None,
    ) -> None:
        self.config = config or DispatchConfig()
        self.risk_registry = risk_registry or ToolRiskRegistry()
        self.guardrail = guardrail or ToolCallGuardrailController()
        self.caches = caches or SessionReadCaches()
        self.stats = DispatchStats()
        # Per-turn reset for the guardrail — the chat loop calls this
        # at the start of every new user message.
        self._last_turn_id: Optional[int] = None

    # ------------------------------------------------------------------
    # Public surface
    # ------------------------------------------------------------------

    def begin_turn(self, turn_id: int) -> None:
        """Reset per-turn dedup state. Idempotent across consecutive
        calls with the same turn_id (so re-entrant agent loops are safe).
        """
        if turn_id != self._last_turn_id:
            self.guardrail.reset_turn()
            self._last_turn_id = turn_id

    async def dispatch(
        self,
        *,
        name: str,
        arguments: Optional[Dict[str, Any]] = None,
        call_id: str = "",
        executor: Any = None,
    ) -> DispatchResult:
        """Dispatch one tool call. Returns a structured result.

        *executor* is the project's :class:`ToolExecutor` instance. The
        dispatcher calls ``executor.execute(name, arguments)`` and
        expects a string return value (matches the existing contract).

        The dispatcher never raises on tool failure — it returns a
        ``DispatchResult`` with ``status`` set to the failure mode.
        This is the key invariant: the chat loop never has to wrap the
        dispatcher in a try/except for tool errors, only for the rare
        case of a dispatcher bug.
        """
        self.stats.total += 1
        arguments = arguments or {}
        started = time.monotonic()

        # ── 1. Dud detection ────────────────────────────────────
        dud = _is_dud(name, arguments)
        if dud is not None:
            self.stats.duds += 1
            logger.info("dispatch: dud tool call name=%s reason=%s", name, dud)
            return DispatchResult(
                status=DispatchStatus.DUD,
                name=name,
                call_id=call_id,
                message=(
                    f"Error: {dud} Pass the required args as a JSON object."
                ),
                duration_ms=(time.monotonic() - started) * 1000,
            )

        # ── 2. Risk classification ─────────────────────────────
        risk = classify_tool_risk(
            name,
            arguments,
            registry=self.risk_registry,
            destructive_check=self.config.destructive_check,
        )

        # ── 3. Loop-guard / dedup ──────────────────────────────
        warn_guardrail: Optional[ToolGuardrailDecision] = None
        if self.config.use_loop_guard:
            gd = self.guardrail.observe(name, arguments)
            if gd.verdict is GuardrailVerdict.HALT:
                self.stats.halts += 1
                logger.info(
                    "dispatch: loop-guard halt name=%s reason=%s", name, gd.reason,
                )
                return DispatchResult(
                    status=DispatchStatus.HALTED,
                    name=name,
                    call_id=call_id,
                    message=(
                        f"Error: loop-guard halted repeated {name} calls — "
                        f"{gd.reason}. {gd.suggestion}"
                    ),
                    duration_ms=(time.monotonic() - started) * 1000,
                    risk_tier=risk.tier.value,
                    guardrail=gd,
                )
            # WARN (idempotent tool, identical-arg 4th call) is
            # non-blocking — the call proceeds but the result carries
            # the warning so the LLM sees the hint.
            if gd.verdict is GuardrailVerdict.WARN:
                self.stats.warnings += 1
                warn_guardrail = gd
                logger.info(
                    "dispatch: loop-guard warn name=%s reason=%s", name, gd.reason,
                )

        # ── 4. Execute ─────────────────────────────────────────
        if executor is None:
            return DispatchResult(
                status=DispatchStatus.ERROR,
                name=name,
                call_id=call_id,
                message=f"Error: no executor available to run {name}",
                duration_ms=(time.monotonic() - started) * 1000,
                risk_tier=risk.tier.value,
            )

        # ── 4a. Read-cache short-circuit ───────────────────────
        # For read-only tools whose result depends on file content
        # (read_file, list_dir), consult the per-session cache
        # BEFORE the executor. A cache hit saves the executor round
        # trip AND ensures the LLM never sees stale content
        # (the cache is mtime-invalidated on every write).
        #
        # We still call the loop-guard for cache hits — a model
        # that loops on read_file(path) should see the dedup
        # warning even on cache hits, otherwise the user has no
        # signal that the agent is stuck.
        if (
            self.config.use_read_cache
            and self.caches is not None
            and name in ("read_file", "list_dir")
            and isinstance(arguments, dict)
        ):
            path_key = _PATH_ARG_TOOLS.get(name)
            if path_key:
                path_val = arguments.get(path_key)
                if isinstance(path_val, str) and path_val:
                    try:
                        if name == "read_file":
                            content, cache_hit = self.caches.reads.get_or_read(
                                path_val,
                                lambda p: executor.execute(name, {"path": p}),
                            )
                        else:  # list_dir
                            entries, cache_hit = self.caches.trees.get_or_list(
                                path_val,
                                lambda p: _parse_list_dir_output(
                                    executor.execute(name, {"path": p}),
                                ),
                            )
                            content = json.dumps(entries)
                        if cache_hit:
                            self.stats.cache_hits += 1
                        else:
                            self.stats.cache_misses += 1
                        self.stats.ok += 1
                        return DispatchResult(
                            status=DispatchStatus.OK,
                            name=name,
                            call_id=call_id,
                            message=content,
                            output=content,
                            duration_ms=(time.monotonic() - started) * 1000,
                            risk_tier=risk.tier.value,
                            cache_hit=cache_hit,
                            guardrail=warn_guardrail,
                        )
                    except FileNotFoundError:
                        # Fall through to the executor — the cache's
                        # own "missing" path raises so we don't store
                        # an empty entry, but the executor may want to
                        # surface its own error message.
                        pass

        try:
            output = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None, executor.execute, name, arguments,
                ),
                timeout=self.config.tool_timeout_seconds,
            )
        except asyncio.TimeoutError:
            self.stats.timeouts += 1
            return DispatchResult(
                status=DispatchStatus.TIMEOUT,
                name=name,
                call_id=call_id,
                message=(
                    f"Error: {name} exceeded "
                    f"{self.config.tool_timeout_seconds:.0f}s timeout. "
                    f"Try a smaller or faster operation."
                ),
                duration_ms=(time.monotonic() - started) * 1000,
                risk_tier=risk.tier.value,
            )
        except Exception as exc:  # noqa: BLE001
            self.stats.errors += 1
            logger.warning("dispatch: executor raised name=%s err=%s", name, exc)
            return DispatchResult(
                status=DispatchStatus.ERROR,
                name=name,
                call_id=call_id,
                message=f"Error executing {name}: {exc}",
                duration_ms=(time.monotonic() - started) * 1000,
                risk_tier=risk.tier.value,
            )

        # ── 5. Verify (if applicable) ──────────────────────────
        verify_result: Optional[VerifyResult] = None
        if self.config.verify_writes and name in _VERIFY_TOOLS:
            verify_result = await asyncio.get_event_loop().run_in_executor(
                None, _verify_synchronously, name, arguments, output, executor,
            )
            if verify_result is not None and not verify_result.ok:
                self.stats.verify_fails += 1
                # Note: the tool result message is the *verify failure*
                # — not the tool's optimistic success string. The LLM
                # needs to see the verify verdict to course-correct.
                return DispatchResult(
                    status=DispatchStatus.VERIFY_FAILED,
                    name=name,
                    call_id=call_id,
                    message=verify_result.to_user_message(),
                    output=output,
                    duration_ms=(time.monotonic() - started) * 1000,
                    risk_tier=risk.tier.value,
                    verify=verify_result,
                )

        # ── 6. Cache invalidation on write ─────────────────────
        if name in _PATH_ARG_TOOLS and self.caches is not None:
            path_key = _PATH_ARG_TOOLS[name]
            path_val = arguments.get(path_key) if isinstance(arguments, dict) else None
            if isinstance(path_val, str) and path_val:
                self.caches.on_write(path_val)

        # ── 7. Truncate output for the LLM ────────────────────
        # We honour the dispatcher's configured cap (which the chat
        # loop sets per session) when it's tighter than the per-tool
        # default — this lets the dashboard cap output to a specific
        # number of tokens without touching the global DEFAULT_LIMITS.
        message = output
        if isinstance(output, str) and len(output) > self.config.output_truncate_chars:
            from .output_limits import get_limit
            effective_cap = min(
                self.config.output_truncate_chars,
                get_limit(name),
            )
            truncated = truncate_output(name, output)
            if len(truncated.output) > effective_cap:
                # Apply the tighter cap on top of the per-tool default.
                head = effective_cap // 2
                tail = effective_cap - head
                notice = f"\n\n[truncated {len(output) - effective_cap} chars — kept first {head} + last {tail}]\n\n"
                message = output[:head] + notice + (output[-tail:] if tail > 0 else "")
            else:
                message = truncated.output

        self.stats.ok += 1
        return DispatchResult(
            status=DispatchStatus.OK,
            name=name,
            call_id=call_id,
            message=message,
            output=output,
            duration_ms=(time.monotonic() - started) * 1000,
            risk_tier=risk.tier.value,
            verify=verify_result,
            guardrail=warn_guardrail,
        )


# ── Free-function form (for one-off calls) ─────────────────────────


async def dispatch_tool_call(
    *,
    name: str,
    arguments: Optional[Dict[str, Any]] = None,
    call_id: str = "",
    executor: Any,
    caches: Optional[SessionReadCaches] = None,
    risk_registry: Optional[ToolRiskRegistry] = None,
    config: Optional[DispatchConfig] = None,
    dispatcher: Optional[ToolDispatcher] = None,
) -> DispatchResult:
    """One-shot dispatch. The gateway can call this directly OR keep
    a long-lived :class:`ToolDispatcher` and call its ``.dispatch`` —
    they're equivalent for the first call.
    """
    d = dispatcher or ToolDispatcher(
        config=config,
        risk_registry=risk_registry,
        caches=caches,
    )
    return await d.dispatch(
        name=name, arguments=arguments, call_id=call_id, executor=executor,
    )


# ── Helpers ────────────────────────────────────────────────────────


def _is_dud(name: str, arguments: Optional[Dict[str, Any]]) -> Optional[str]:
    """Return a human-readable reason if *arguments* is a dud, else None.

    Mirrors the gateway's ``_is_dud_tool_call`` predicate so the
    dispatcher is a drop-in replacement. The reason string is
    actionable ("list_dir requires argument 'path'") rather than
    generic.
    """
    if arguments is None:
        return (
            f"{name} was called with no arguments. "
            f"Pass the required args as a JSON object (e.g. {{\"...\": \"...\"}})."
        )
    if not isinstance(arguments, dict):
        return (
            f"{name} arguments must be a JSON object, "
            f"got {type(arguments).__name__}."
        )
    # Zero-arg-safe tools accept empty `{}` as valid.
    if not arguments and name in _ZERO_ARG_SAFE_TOOLS:
        return None
    if not arguments:
        return f"{name} was called with an empty arguments object."
    # Per-tool required-arg check.
    required = _REQUIRED_ARGS.get(name, ())
    if required:
        missing = []
        for r in required:
            v = arguments.get(r)
            if v is None or (isinstance(v, str) and not v.strip()):
                missing.append(r)
        if missing:
            quoted = ", ".join(f"'{m}'" for m in missing)
            return (
                f"{name} requires argument(s) {quoted} but they were "
                f"missing or empty. Re-emit the call with the required arg(s) populated."
            )
    # Generic fallback: every value is falsy.
    if not any(
        bool(v) and (not isinstance(v, str) or v.strip())
        for v in arguments.values()
    ):
        return f"{name} arguments contained no truthy values."
    return None


def _parse_list_dir_output(raw: Any) -> List[Dict[str, Any]]:
    """Best-effort parse of a list_dir tool result into the cache shape.

    Real CVC list_dir tools emit JSON or a structured string. For the
    cache's purposes we only need a stable list-of-dicts that we can
    compare to detect "did the listing change?". A failed parse yields
    an empty list, which forces a cache miss next time — that's the
    safe direction.
    """
    import json as _json
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        try:
            parsed = _json.loads(raw)
            if isinstance(parsed, list):
                return parsed
        except (ValueError, TypeError):
            pass
        # The stub executor returns "<listing of PATH>". Synthesise a
        # single-entry list so the cache has something to store.
        return [{"name": raw, "is_dir": False, "size": len(raw), "mtime_ns": 0}]
    return []


def _verify_synchronously(
    name: str,
    arguments: Dict[str, Any],
    output: Any,
    executor: Any,
) -> VerifyResult:
    """Sync helper that runs inside the executor's thread pool.

    Reads the file fresh from disk (NOT through the cache — we want
    ground truth, not the cached version that might be stale).
    """
    path_key = _PATH_ARG_TOOLS.get(name)
    if path_key is None:
        return VerifyResult(status=VerifyStatus.OK, path="(no path)")
    path = arguments.get(path_key) if isinstance(arguments, dict) else None
    if not isinstance(path, str) or not path:
        return VerifyResult(status=VerifyStatus.OK, path="(no path)")

    abs_path = os.path.realpath(os.path.expanduser(path))

    def _ground_truth(p: str) -> str:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    if name == "write_file":
        expected = arguments.get("content", "")
        return verify_write(abs_path, expected, _ground_truth)

    if name in ("patch", "edit_file"):
        new_string = arguments.get("new_string", "")
        return verify_patch(abs_path, None, new_string, _ground_truth)

    if name == "patch_file":
        diff = arguments.get("diff", "")
        # We can't reverse-engineer the new substring from a diff
        # without a real diff parser, so just verify the file's
        # existence + non-empty + the expected substring if the
        # caller embedded it in `new_string` (the executor should
        # stash it; if it didn't, the substring check is a no-op).
        new_string = arguments.get("new_string", "")
        if not new_string:
            # Fall back to a bare existence check.
            try:
                _ground_truth(abs_path)
                return VerifyResult(status=VerifyStatus.OK, path=abs_path)
            except FileNotFoundError:
                return VerifyResult(
                    status=VerifyStatus.MISSING, path=abs_path,
                )
        return verify_patch(abs_path, None, new_string, _ground_truth)

    return VerifyResult(status=VerifyStatus.OK, path=abs_path)

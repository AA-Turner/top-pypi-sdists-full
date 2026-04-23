"""Runtime hook dispatch for PreToolUse and PostToolUse events (#1271).

Consumes the frozen hook config contract from #1489 (HooksConfig,
HookEntryConfig, HookMatcherConfig, HookRunnerConfig).

Ordering invariant
------------------
Hard rule-enforcer deny  →  pre-tool hooks  →  approval flow  →  tool dispatch
→  post-tool hooks

A hook ``allow`` decision never overrides a static rule-enforcer deny.
Hook failures default to ``allow`` (fail-open) so that misconfigured hooks
do not silently block all tools.

Phase-1 scope
-------------
- PreToolUse and PostToolUse events only
- Shell command (``asyncio.create_subprocess_shell``) and HTTP webhook runners
- Tool-name fnmatch + argument value matching
- No input rewriting; post-tool may observe and deny continuation

Phase-2 lifecycle events (reserved — not yet wired into the runtime, #1494)
----------------------------------------------------------------------------
The constants below are declared so the codebase is honest about the full
hook taxonomy.  Config validation rejects these event names with a clear
"coming in a later release" message so operators are not left guessing.

- ``HOOK_EVENT_SESSION_START``    — fires once when a new session is created
- ``HOOK_EVENT_STOP``             — fires when the agent loop exits normally
- ``HOOK_EVENT_APPROVAL_REQUESTED`` — fires when an approval gate opens
- ``HOOK_EVENT_APPROVAL_RESOLVED``  — fires when an approval gate closes
- ``HOOK_EVENT_NOTIFICATION``     — fires for informational agent narration events

Audit (#1490)
-------------
Every matched hook execution emits a lineage event via
``services.lineage.emit_hook_lifecycle``.  ``error_type`` on the returned
``HookDecision`` carries the internal failure mode so the audit record can
distinguish ``timed_out`` and ``exception`` paths from normal ``allow``.
"""

from __future__ import annotations

import asyncio
import fnmatch
import json
import logging
import os
import time
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from ..config import HookEntryConfig, HooksConfig
    from .audit import AuditWriter

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Hook event taxonomy
# ---------------------------------------------------------------------------

# Phase-1 events — fully wired into the runtime dispatch.
HOOK_EVENT_PRE_TOOL: str = "pre_tool"
HOOK_EVENT_POST_TOOL: str = "post_tool"

# Phase-2 events — reserved constants; NOT yet dispatched by the runtime
# (#1494).  Config validation surfaces a clear error when these appear in
# hook config so operators know they are coming in a later release rather
# than silently ignored.
HOOK_EVENT_SESSION_START: str = "session_start"
HOOK_EVENT_STOP: str = "stop"
HOOK_EVENT_APPROVAL_REQUESTED: str = "approval_requested"
HOOK_EVENT_APPROVAL_RESOLVED: str = "approval_resolved"
HOOK_EVENT_NOTIFICATION: str = "notification"

# Frozen sets used by config validation and dispatch.
PHASE_1_HOOK_EVENTS: frozenset[str] = frozenset({HOOK_EVENT_PRE_TOOL, HOOK_EVENT_POST_TOOL})
PHASE_2_HOOK_EVENTS: frozenset[str] = frozenset(
    {
        HOOK_EVENT_SESSION_START,
        HOOK_EVENT_STOP,
        HOOK_EVENT_APPROVAL_REQUESTED,
        HOOK_EVENT_APPROVAL_RESOLVED,
        HOOK_EVENT_NOTIFICATION,
    }
)
ALL_HOOK_EVENTS: frozenset[str] = PHASE_1_HOOK_EVENTS | PHASE_2_HOOK_EVENTS

# ---------------------------------------------------------------------------
# Decision model
# ---------------------------------------------------------------------------

_VALID_OUTCOMES: frozenset[str] = frozenset({"allow", "deny", "ask"})


@dataclass(frozen=True)
class HookDecision:
    """Outcome of evaluating one or more hooks against a tool call.

    outcome:
        ``"allow"`` — proceed normally (default when no hooks match or hooks succeed)
        ``"deny"``  — block the tool call; surface ``message`` to the user
        ``"ask"``   — route through the existing approval flow with ``message`` as context

    error_type:
        Internal failure mode for audit purposes only — does not affect routing.
        ``""``          — normal execution
        ``"timeout"``   — runner timed out (fail-open)
        ``"exception"`` — runner raised an unexpected exception (fail-open)

    execution_ms:
        Wall-clock duration of the runner in milliseconds (set by ``_run_single_hook``).
    """

    outcome: Literal["allow", "deny", "ask"] = "allow"
    message: str = ""
    hook_id: str = ""
    error_type: str = ""
    execution_ms: float = 0.0


_ALLOW = HookDecision(outcome="allow")


# ---------------------------------------------------------------------------
# Ordering classifier
# ---------------------------------------------------------------------------


def classify_pre_hook_result(decision: "HookDecision") -> "Literal['continue', 'deny', 'require_approval']":
    """Map a pre-tool HookDecision to the ordering bucket it belongs to.

    Ordering contract (enforced in tools/__init__.py call_tool):
      static hard deny  →  pre-tool hooks  →  approval  →  dispatch

    A hook ``allow`` never overrides a static deny already issued by the
    rule enforcer or safety config — the rule enforcer check runs first and
    returns early, so this function is only called when the static gate
    already passed.

    Returns:
        ``"continue"``          — hook allows; proceed to tier-based approval
        ``"deny"``              — hook blocks the tool call unconditionally
        ``"require_approval"``  — hook escalates to the user approval flow
    """
    if decision.outcome == "deny":
        return "deny"
    if decision.outcome == "ask":
        return "require_approval"
    if decision.outcome != "allow":
        # Unknown outcome — log and fail-open (consistent with the runner fail-open contract).
        logger.warning(
            "classify_pre_hook_result: unrecognized outcome %r for hook %r — defaulting to continue",
            decision.outcome,
            decision.hook_id,
        )
    return "continue"


# ---------------------------------------------------------------------------
# Matcher
# ---------------------------------------------------------------------------


def match_hook(entry: HookEntryConfig, tool_name: str, arguments: dict[str, Any]) -> bool:
    """Return True if *entry* fires for this tool call.

    Both conditions must hold:
    1. ``entry.matcher.tool_name`` fnmatch-matches *tool_name*
    2. Every key/value pair in ``entry.matcher.arguments`` is present in
       *arguments* with a matching string value (empty dict matches anything)
    """
    if not fnmatch.fnmatch(tool_name, entry.matcher.tool_name):
        return False
    for key, value in entry.matcher.arguments.items():
        if str(arguments.get(key, "")) != value:
            return False
    return True


# ---------------------------------------------------------------------------
# Context helpers
# ---------------------------------------------------------------------------


def _build_hook_env(
    event: str,
    tool_name: str,
    arguments: dict[str, Any],
    output: dict[str, Any] | None = None,
    *,
    parent_conversation_id: str = "",
    parent_tool_call_id: str = "",
    child_agent_id: str = "",
    detached_run_id: str = "",
) -> dict[str, str]:
    """Build environment variables for command hooks."""
    env: dict[str, str] = {
        **{k: v for k, v in os.environ.items() if isinstance(v, str)},
        "ANTEROOM_HOOK_EVENT": event,
        "ANTEROOM_HOOK_TOOL_NAME": tool_name,
        "ANTEROOM_HOOK_ARGUMENTS": json.dumps(arguments),
    }
    if output is not None:
        env["ANTEROOM_HOOK_OUTPUT"] = json.dumps(output)
    if parent_conversation_id:
        env["ANTEROOM_HOOK_PARENT_CONVERSATION_ID"] = parent_conversation_id
    if parent_tool_call_id:
        env["ANTEROOM_HOOK_PARENT_TOOL_CALL_ID"] = parent_tool_call_id
    if child_agent_id:
        env["ANTEROOM_HOOK_CHILD_AGENT_ID"] = child_agent_id
    if detached_run_id:
        env["ANTEROOM_HOOK_DETACHED_RUN_ID"] = detached_run_id
    return env


def _build_hook_payload(
    event: str,
    tool_name: str,
    arguments: dict[str, Any],
    output: dict[str, Any] | None = None,
    *,
    parent_conversation_id: str = "",
    parent_tool_call_id: str = "",
    child_agent_id: str = "",
    detached_run_id: str = "",
) -> dict[str, Any]:
    """Build JSON payload for webhook hooks."""
    payload: dict[str, Any] = {
        "event": event,
        "tool_name": tool_name,
        "arguments": arguments,
    }
    if output is not None:
        payload["output"] = output
    if parent_conversation_id:
        payload["parent_conversation_id"] = parent_conversation_id
    if parent_tool_call_id:
        payload["parent_tool_call_id"] = parent_tool_call_id
    if child_agent_id:
        payload["child_agent_id"] = child_agent_id
    if detached_run_id:
        payload["detached_run_id"] = detached_run_id
    return payload


def _parse_decision(raw: str, hook_id: str) -> HookDecision:
    """Parse a JSON decision string from a hook response.

    Expected format: ``{"decision": "allow"|"deny"|"ask", "message": "..."}``

    Returns an ``allow`` decision on parse failure (fail-open).  The returned
    decision always carries *hook_id* so downstream audit emission can trace
    the originating hook even when the body is empty or malformed.
    """
    stripped = raw.strip()
    if not stripped:
        return HookDecision(outcome="allow", hook_id=hook_id)
    try:
        data = json.loads(stripped)
    except (json.JSONDecodeError, ValueError):
        logger.debug("Hook %r returned non-JSON %r — defaulting to allow", hook_id, stripped[:200])
        return HookDecision(outcome="allow", hook_id=hook_id)
    if not isinstance(data, dict):
        logger.debug("Hook %r returned non-dict JSON — defaulting to allow", hook_id)
        return HookDecision(outcome="allow", hook_id=hook_id)
    outcome = data.get("decision", "allow")
    if outcome not in _VALID_OUTCOMES:
        logger.warning("Hook %r unknown decision %r — defaulting to allow", hook_id, outcome)
        return HookDecision(outcome="allow", hook_id=hook_id)
    message = str(data.get("message", ""))
    return HookDecision(outcome=outcome, message=message, hook_id=hook_id)


# ---------------------------------------------------------------------------
# Runners
# ---------------------------------------------------------------------------


async def run_command_hook(
    entry: HookEntryConfig,
    event: str,
    tool_name: str,
    arguments: dict[str, Any],
    output: dict[str, Any] | None = None,
    *,
    parent_conversation_id: str = "",
    parent_tool_call_id: str = "",
    child_agent_id: str = "",
    detached_run_id: str = "",
) -> HookDecision:
    """Run a shell command hook and return its decision.

    Context is passed via environment variables:

    - ``ANTEROOM_HOOK_EVENT`` — ``"pre_tool"`` or ``"post_tool"``
    - ``ANTEROOM_HOOK_TOOL_NAME`` — tool being called
    - ``ANTEROOM_HOOK_ARGUMENTS`` — JSON of the tool arguments
    - ``ANTEROOM_HOOK_OUTPUT`` — JSON of the tool output (post-tool only)
    - ``ANTEROOM_HOOK_PARENT_CONVERSATION_ID`` — parent conversation (subagent only)
    - ``ANTEROOM_HOOK_PARENT_TOOL_CALL_ID`` — parent run_agent tool call ID (subagent only)
    - ``ANTEROOM_HOOK_CHILD_AGENT_ID`` — child agent identifier (subagent only)
    - ``ANTEROOM_HOOK_DETACHED_RUN_ID`` — detached run ID (detached subagent only)

    The command's stdout is parsed as a JSON decision object.
    Timeout, stderr output, and process failures all default to ``allow``
    (fail-open).
    """
    command = entry.runner.command
    if not command:
        logger.warning("Hook %r has no command — skipping", entry.id)
        return HookDecision(outcome="allow", hook_id=entry.id)

    hook_env = _build_hook_env(
        event,
        tool_name,
        arguments,
        output,
        parent_conversation_id=parent_conversation_id,
        parent_tool_call_id=parent_tool_call_id,
        child_agent_id=child_agent_id,
        detached_run_id=detached_run_id,
    )
    timeout = float(entry.runner.timeout)

    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=hook_env,
        )
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            try:
                proc.kill()
                await proc.wait()
            except Exception:
                pass
            logger.warning("Hook %r timed out after %.0fs — defaulting to allow", entry.id, timeout)
            return HookDecision(outcome="allow", hook_id=entry.id, error_type="timeout")

        if proc.returncode != 0:
            stderr_preview = (stderr_bytes or b"")[:300].decode("utf-8", errors="replace")
            logger.debug("Hook %r exited %d stderr=%r", entry.id, proc.returncode, stderr_preview)

        stdout_text = (stdout_bytes or b"").decode("utf-8", errors="replace")
        return _parse_decision(stdout_text, entry.id)

    except Exception:
        logger.warning("Hook %r command failed — defaulting to allow", entry.id, exc_info=True)
        return HookDecision(outcome="allow", hook_id=entry.id, error_type="exception")


async def run_webhook_hook(
    entry: HookEntryConfig,
    event: str,
    tool_name: str,
    arguments: dict[str, Any],
    output: dict[str, Any] | None = None,
    *,
    allowed_domains: Sequence[str] = (),
    block_localhost: bool = False,
    parent_conversation_id: str = "",
    parent_tool_call_id: str = "",
    child_agent_id: str = "",
    detached_run_id: str = "",
) -> HookDecision:
    """HTTP POST to a webhook hook endpoint and return its decision.

    Request body: ``{"event": ..., "tool_name": ..., "arguments": ..., "output": ...}``

    Subagent correlation fields are included in the payload when present:
    ``parent_conversation_id``, ``parent_tool_call_id``, ``child_agent_id``,
    ``detached_run_id``.

    Response body is parsed as a JSON decision object (same format as command hooks).
    Transport failures and timeouts default to ``allow`` (fail-open).
    """
    url = entry.runner.url
    if not url:
        logger.warning("Hook %r has no URL — skipping", entry.id)
        return HookDecision(outcome="allow", hook_id=entry.id)

    # Validate URL against the configured egress policy (same enforcement as
    # workflow_hooks / ai_service). Operator-sourced URLs must still respect
    # allowed_domains / block_localhost_api config.
    try:
        from .egress_allowlist import check_egress_allowed as _check_egress

        if not _check_egress(url, allowed_domains, block_localhost=block_localhost):
            logger.warning("Hook %r webhook URL blocked by egress allowlist — skipping", entry.id)
            return HookDecision(outcome="allow", hook_id=entry.id)
    except Exception:
        logger.warning("Hook %r egress allowlist check failed — skipping webhook", entry.id, exc_info=True)
        return _ALLOW

    payload = _build_hook_payload(
        event,
        tool_name,
        arguments,
        output,
        parent_conversation_id=parent_conversation_id,
        parent_tool_call_id=parent_tool_call_id,
        child_agent_id=child_agent_id,
        detached_run_id=detached_run_id,
    )
    timeout = float(entry.runner.timeout)

    try:
        import httpx

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code >= 400:
                logger.warning("Hook %r webhook returned %d — defaulting to allow", entry.id, resp.status_code)
                return HookDecision(outcome="allow", hook_id=entry.id)
            return _parse_decision(resp.text, entry.id)

    except asyncio.TimeoutError:
        logger.warning("Hook %r webhook timed out after %.0fs — defaulting to allow", entry.id, timeout)
        return HookDecision(outcome="allow", hook_id=entry.id, error_type="timeout")
    except Exception as _exc:
        # httpx raises its own ``TimeoutException`` hierarchy which is *not*
        # a subclass of ``asyncio.TimeoutError``. Without this check, a real
        # httpx timeout would be classified as ``hook.failed`` (exception)
        # instead of ``hook.timed_out`` in the audit trail (#1490).
        try:
            import httpx as _httpx

            if isinstance(_exc, _httpx.TimeoutException):
                logger.warning("Hook %r webhook timed out after %.0fs — defaulting to allow", entry.id, timeout)
                return HookDecision(outcome="allow", hook_id=entry.id, error_type="timeout")
        except ImportError:
            pass
        logger.warning("Hook %r webhook failed — defaulting to allow", entry.id, exc_info=True)
        return HookDecision(outcome="allow", hook_id=entry.id, error_type="exception")


# ---------------------------------------------------------------------------
# Audit emission helper
# ---------------------------------------------------------------------------


def _emit_hook_audit(
    audit_writer: AuditWriter | None,
    decision: HookDecision,
    *,
    hook_event: str,
    tool_name: str,
    tool_call_id: str = "",
    conversation_id: str = "",
    user_id: str = "",
    extra_details: dict[str, Any] | None = None,
) -> None:
    """Emit a ``hook.*`` lineage event for one resolved hook decision.

    Maps (outcome, error_type) → lineage event suffix:
    - error_type="timeout"   → ``hook.timed_out``
    - error_type="exception" → ``hook.failed``
    - outcome="deny"         → ``hook.denied``
    - outcome="ask"          → ``hook.completed`` (escalated, recorded in details)
    - outcome="allow"        → ``hook.completed``

    Never raises — audit emission is best-effort.
    """
    if audit_writer is None:
        return
    try:
        from .lineage import emit_hook_lifecycle

        if decision.error_type == "timeout":
            lifecycle_event = "timed_out"
        elif decision.error_type == "exception":
            lifecycle_event = "failed"
        elif decision.outcome == "deny":
            lifecycle_event = "denied"
        else:
            lifecycle_event = "completed"
        emit_hook_lifecycle(
            audit_writer,
            lifecycle_event,
            hook_id=decision.hook_id,
            hook_event=hook_event,
            tool_name=tool_name,
            outcome=decision.outcome,
            execution_ms=decision.execution_ms,
            message=decision.message,
            tool_call_id=tool_call_id,
            conversation_id=conversation_id,
            user_id=user_id,
            details=extra_details,
        )
    except Exception:
        logger.warning("Failed to emit hook audit event for hook %r", decision.hook_id, exc_info=True)


# ---------------------------------------------------------------------------
# Shared dispatch
# ---------------------------------------------------------------------------


async def _run_single_hook(
    entry: HookEntryConfig,
    event: str,
    tool_name: str,
    arguments: dict[str, Any],
    output: dict[str, Any] | None = None,
    *,
    audit_writer: AuditWriter | None = None,
    tool_call_id: str = "",
    conversation_id: str = "",
    user_id: str = "",
    allowed_domains: Sequence[str] = (),
    block_localhost: bool = False,
    parent_conversation_id: str = "",
    parent_tool_call_id: str = "",
    child_agent_id: str = "",
    detached_run_id: str = "",
) -> HookDecision:
    """Dispatch one hook entry based on its runner type.

    Non-executable hooks (``is_executable=False``) are silently skipped —
    they exist in the config from pack sources and are deferred to #1272.

    Emits a ``hook.*`` lineage event via *audit_writer* after each matched
    execution so every hook decision, timeout, and failure is traceable (#1490).

    Subagent correlation fields (``parent_conversation_id``,
    ``parent_tool_call_id``, ``child_agent_id``, ``detached_run_id``) are
    forwarded to runners and to the audit payload so operators can trace hook
    decisions back to the originating subagent (#1493).
    """
    if not entry.is_executable:
        logger.debug(
            "Hook %r skipped — not executable (trust_source=%r)",
            entry.id,
            entry.trust_source,
        )
        return _ALLOW
    t0 = time.monotonic()
    if entry.runner.type == "command":
        decision = await run_command_hook(
            entry,
            event,
            tool_name,
            arguments,
            output,
            parent_conversation_id=parent_conversation_id,
            parent_tool_call_id=parent_tool_call_id,
            child_agent_id=child_agent_id,
            detached_run_id=detached_run_id,
        )
    elif entry.runner.type == "webhook":
        decision = await run_webhook_hook(
            entry,
            event,
            tool_name,
            arguments,
            output,
            allowed_domains=allowed_domains,
            block_localhost=block_localhost,
            parent_conversation_id=parent_conversation_id,
            parent_tool_call_id=parent_tool_call_id,
            child_agent_id=child_agent_id,
            detached_run_id=detached_run_id,
        )
    else:
        logger.warning("Hook %r has unknown runner type %r — skipping", entry.id, entry.runner.type)
        return _ALLOW
    elapsed_ms = (time.monotonic() - t0) * 1000
    from dataclasses import replace as _dc_replace

    decision = _dc_replace(
        decision,
        execution_ms=elapsed_ms,
        hook_id=decision.hook_id or entry.id,
    )
    subagent_details: dict[str, Any] = {}
    if parent_conversation_id:
        subagent_details["parent_conversation_id"] = parent_conversation_id
    if parent_tool_call_id:
        subagent_details["parent_tool_call_id"] = parent_tool_call_id
    if child_agent_id:
        subagent_details["child_agent_id"] = child_agent_id
    if detached_run_id:
        subagent_details["detached_run_id"] = detached_run_id
    _emit_hook_audit(
        audit_writer,
        decision,
        hook_event=event,
        tool_name=tool_name,
        tool_call_id=tool_call_id,
        conversation_id=conversation_id,
        user_id=user_id,
        extra_details=subagent_details if subagent_details else None,
    )
    return decision


async def run_pre_tool_hooks(
    hooks_config: HooksConfig,
    tool_name: str,
    arguments: dict[str, Any],
    *,
    audit_writer: AuditWriter | None = None,
    tool_call_id: str = "",
    conversation_id: str = "",
    user_id: str = "",
    allowed_domains: Sequence[str] = (),
    block_localhost: bool = False,
    parent_conversation_id: str = "",
    parent_tool_call_id: str = "",
    child_agent_id: str = "",
    detached_run_id: str = "",
) -> HookDecision:
    """Evaluate all pre-tool hooks for a tool call.

    Hooks are evaluated in list order.  The first non-allow decision
    short-circuits evaluation and is returned immediately.

    *audit_writer* receives a ``hook.*`` lineage event for each matched
    hook execution (#1490).

    Subagent correlation fields are forwarded to each runner and the audit
    trail so hook decisions from within a subagent are attributable to the
    originating run (#1493).

    Returns ``_ALLOW`` when no hooks match or all matching hooks allow.
    """
    for entry in hooks_config.pre_tool:
        if not match_hook(entry, tool_name, arguments):
            continue
        decision = await _run_single_hook(
            entry,
            "pre_tool",
            tool_name,
            arguments,
            audit_writer=audit_writer,
            tool_call_id=tool_call_id,
            conversation_id=conversation_id,
            user_id=user_id,
            allowed_domains=allowed_domains,
            block_localhost=block_localhost,
            parent_conversation_id=parent_conversation_id,
            parent_tool_call_id=parent_tool_call_id,
            child_agent_id=child_agent_id,
            detached_run_id=detached_run_id,
        )
        if decision.outcome != "allow":
            return decision
    return _ALLOW


async def run_post_tool_hooks(
    hooks_config: HooksConfig,
    tool_name: str,
    arguments: dict[str, Any],
    output: dict[str, Any],
    *,
    audit_writer: AuditWriter | None = None,
    tool_call_id: str = "",
    conversation_id: str = "",
    user_id: str = "",
    allowed_domains: Sequence[str] = (),
    block_localhost: bool = False,
    parent_conversation_id: str = "",
    parent_tool_call_id: str = "",
    child_agent_id: str = "",
    detached_run_id: str = "",
) -> HookDecision:
    """Evaluate all post-tool hooks after a tool call completes.

    Post-tool hooks receive both the original call arguments (for matching)
    and the tool output (for inspection).  A hook may deny continuation
    (e.g. to block on dangerous output).  Input rewriting is not supported
    in phase 1.

    *audit_writer* receives a ``hook.*`` lineage event for each matched
    hook execution (#1490).

    Subagent correlation fields are forwarded to each runner and the audit
    trail so hook decisions from within a subagent are attributable to the
    originating run (#1493).

    Returns ``_ALLOW`` when no hooks match or all matching hooks allow.
    """
    for entry in hooks_config.post_tool:
        if not match_hook(entry, tool_name, arguments):
            continue
        decision = await _run_single_hook(
            entry,
            "post_tool",
            tool_name,
            arguments,
            output,
            audit_writer=audit_writer,
            tool_call_id=tool_call_id,
            conversation_id=conversation_id,
            user_id=user_id,
            allowed_domains=allowed_domains,
            block_localhost=block_localhost,
            parent_conversation_id=parent_conversation_id,
            parent_tool_call_id=parent_tool_call_id,
            child_agent_id=child_agent_id,
            detached_run_id=detached_run_id,
        )
        if decision.outcome != "allow":
            return decision
    return _ALLOW


# ---------------------------------------------------------------------------
# Dry-run replay (developer tooling)
# ---------------------------------------------------------------------------


@dataclass
class HookReplayEntry:
    """Record of a single hook's evaluation during a dry-run replay.

    Covers all hooks in the list regardless of match result so that
    authors can see the full decision sequence.

    skipped_reason:
        ``""``               — hook was matched and dispatched
        ``"no_match"``       — hook matcher did not fire for this tool call
        ``"not_executable"`` — hook matched but has non-executable trust_source
                               (e.g. ``"pack"`` in phase 1 pending #1272)
    """

    hook_id: str
    trust_source: str
    is_executable: bool
    matched: bool
    skipped_reason: str
    decision: HookDecision | None
    execution_ms: float


@dataclass
class ReplayResult:
    """Full trace of hook evaluation for a single dry-run replay event.

    Unlike production evaluation, *all* hooks are visited (no short-circuit)
    so authors can inspect the complete decision sequence.  ``final_decision``
    mirrors what the production runtime would have returned: the first
    non-allow decision from an executable matched hook, or ``_ALLOW``.
    """

    event: str
    tool_name: str
    entries: list[HookReplayEntry]
    final_decision: HookDecision

    @property
    def executable_count(self) -> int:
        return sum(1 for e in self.entries if e.is_executable)

    @property
    def skipped_count(self) -> int:
        return sum(1 for e in self.entries if e.skipped_reason != "")

    @property
    def matched_count(self) -> int:
        return sum(1 for e in self.entries if e.matched)


async def replay_hook_event(
    hooks_config: HooksConfig,
    event: str,
    tool_name: str,
    arguments: dict[str, Any],
    output: dict[str, Any] | None = None,
    *,
    allowed_domains: Sequence[str] = (),
    block_localhost: bool = False,
) -> ReplayResult:
    """Dry-run replay of hooks for a single tool lifecycle event.

    Compared to ``run_pre_tool_hooks`` / ``run_post_tool_hooks``:

    - Evaluates **all** hooks (no short-circuit) for full visibility
    - Never emits audit events (``audit_writer`` is always ``None``)
    - Surfaces skipped non-executable hooks so authors can see which
      pack-sourced hooks would be skipped by the production runtime
    - Computes ``final_decision`` as the first non-allow from an executable
      matched hook, matching production short-circuit semantics

    ``event`` must be ``"pre_tool"`` or ``"post_tool"``.
    """
    hook_list = hooks_config.pre_tool if event == "pre_tool" else hooks_config.post_tool
    entries: list[HookReplayEntry] = []
    final_decision: HookDecision = _ALLOW

    for entry in hook_list:
        matched = match_hook(entry, tool_name, arguments)
        if not matched:
            entries.append(
                HookReplayEntry(
                    hook_id=entry.id,
                    trust_source=entry.trust_source,
                    is_executable=entry.is_executable,
                    matched=False,
                    skipped_reason="no_match",
                    decision=None,
                    execution_ms=0.0,
                )
            )
            continue

        if not entry.is_executable:
            entries.append(
                HookReplayEntry(
                    hook_id=entry.id,
                    trust_source=entry.trust_source,
                    is_executable=False,
                    matched=True,
                    skipped_reason="not_executable",
                    decision=None,
                    execution_ms=0.0,
                )
            )
            continue

        if entry.runner.type not in ("command", "webhook"):
            entries.append(
                HookReplayEntry(
                    hook_id=entry.id,
                    trust_source=entry.trust_source,
                    is_executable=True,
                    matched=True,
                    skipped_reason="unknown_runner",
                    decision=None,
                    execution_ms=0.0,
                )
            )
            continue

        t0 = time.monotonic()
        if entry.runner.type == "command":
            decision = await run_command_hook(entry, event, tool_name, arguments, output)
        else:
            decision = await run_webhook_hook(
                entry,
                event,
                tool_name,
                arguments,
                output,
                allowed_domains=allowed_domains,
                block_localhost=block_localhost,
            )
        elapsed_ms = (time.monotonic() - t0) * 1000
        from dataclasses import replace as _dc_replace

        decision = _dc_replace(decision, execution_ms=elapsed_ms, hook_id=decision.hook_id or entry.id)

        entries.append(
            HookReplayEntry(
                hook_id=entry.id,
                trust_source=entry.trust_source,
                is_executable=True,
                matched=True,
                skipped_reason="",
                decision=decision,
                execution_ms=elapsed_ms,
            )
        )

        if final_decision.outcome == "allow" and decision.outcome != "allow":
            final_decision = decision

    return ReplayResult(
        event=event,
        tool_name=tool_name,
        entries=entries,
        final_decision=final_decision,
    )

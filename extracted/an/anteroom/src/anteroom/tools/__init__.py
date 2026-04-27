"""Built-in tool registry for the agentic CLI."""

from __future__ import annotations

import logging
import time
from typing import Any, Callable, Coroutine

from ..config import SafetyConfig
from ..services.diagnostic_context import log_debug, shape_metadata
from ..services.rule_enforcer import RuleEnforcer
from ..services.tool_rate_limit import ToolRateLimiter
from .safety import SafetyVerdict, check_bash_command, check_bypass_immune_path, check_write_path
from .security import check_hard_block
from .tiers import ToolTier as ToolTier
from .tiers import get_tool_tier, parse_approval_mode, should_require_approval

logger = logging.getLogger(__name__)

ToolHandler = Callable[..., Coroutine[Any, Any, dict[str, Any]]]
ConfirmCallback = Callable[[SafetyVerdict], Coroutine[Any, Any, bool]]

# Tools whose output contains external/filesystem content — tagged untrusted for prompt injection defense.
_UNTRUSTED_TOOLS = {
    "read_file",
    "grep",
    "glob_files",
    "bash",
    "write_file",
    "edit_file",
    "run_agent",
    "docx",
    "xlsx",
    "pptx",
}


def _hook_call_kwargs(
    *,
    audit_writer: Any | None,
    extra_context: dict[str, Any] | None,
    allowed_domains: tuple[str, ...],
    block_localhost: bool,
) -> dict[str, Any]:
    """Build hook kwargs without forcing empty audit/context metadata through.

    Includes subagent correlation IDs (parent_conversation_id, parent_tool_call_id,
    child_agent_id, detached_run_id) when present in extra_context (#1493).
    """
    hook_kwargs: dict[str, Any] = {
        "allowed_domains": allowed_domains,
        "block_localhost": block_localhost,
    }
    if audit_writer is not None:
        hook_kwargs["audit_writer"] = audit_writer
    if extra_context:
        for source_key, target_key in (
            ("tool_call_id", "tool_call_id"),
            ("conversation_id", "conversation_id"),
            ("user_id", "user_id"),
            ("parent_conversation_id", "parent_conversation_id"),
            ("parent_tool_call_id", "parent_tool_call_id"),
            ("child_agent_id", "child_agent_id"),
            ("detached_run_id", "detached_run_id"),
        ):
            value = extra_context.get(source_key)
            if value:
                hook_kwargs[target_key] = value
    return hook_kwargs


class ToolRegistry:
    """Registry of built-in tools with OpenAI function-call format."""

    def __init__(self) -> None:
        self._handlers: dict[str, ToolHandler] = {}
        self._definitions: dict[str, dict[str, Any]] = {}
        self._confirm_callback: ConfirmCallback | None = None
        self._safety_config: SafetyConfig | None = None
        self._working_dir: str | None = None
        self._session_allowed: set[str] = set()
        self._rate_limiter: ToolRateLimiter | None = None
        self._rule_enforcer: RuleEnforcer | None = None

    def set_confirm_callback(self, callback: ConfirmCallback | None) -> None:
        self._confirm_callback = callback

    def set_safety_config(self, config: SafetyConfig, working_dir: str | None = None) -> None:
        self._safety_config = config
        self._working_dir = working_dir

    def grant_session_permission(self, tool_name: str) -> None:
        import re

        if not re.match(r"^[a-zA-Z0-9_\-]{1,128}$", tool_name):
            logger.warning("Rejected invalid tool name for session permission: %r", tool_name)
            return
        self._session_allowed.add(tool_name)

    def clear_session_permissions(self) -> None:
        self._session_allowed.clear()

    def set_rate_limiter(self, limiter: ToolRateLimiter | None) -> None:
        self._rate_limiter = limiter

    def set_rule_enforcer(self, enforcer: RuleEnforcer | None) -> None:
        self._rule_enforcer = enforcer

    def register(self, name: str, handler: ToolHandler, definition: dict[str, Any]) -> None:
        self._handlers[name] = handler
        self._definitions[name] = definition

    def has_tool(self, name: str) -> bool:
        return name in self._handlers

    def get_openai_tools(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": defn.get("description", ""),
                    "parameters": defn.get("parameters", {}),
                },
            }
            for name, defn in self._definitions.items()
        ]

    def check_safety(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        *,
        rule_enforcer_override: RuleEnforcer | None = None,
    ) -> SafetyVerdict | None:
        """Check whether a tool call requires approval.

        Returns a SafetyVerdict if approval is needed/denied, or None if auto-allowed.
        A verdict with hard_denied=True means the tool is blocked by config (denied_tools
        or per-tool enabled=false) and must be blocked without prompting.

        *rule_enforcer_override* lets callers provide a per-request enforcer
        without mutating the shared instance field, avoiding concurrency issues.
        """
        # Hard rule enforcement runs unconditionally — even when safety is
        # disabled — so that ``enforce: hard`` pack rules cannot be bypassed.
        enforcer = rule_enforcer_override or self._rule_enforcer
        if enforcer is not None:
            blocked, reason, rule_fqn = enforcer.check_tool_call(tool_name, arguments)
            if blocked:
                return SafetyVerdict(
                    needs_approval=True,
                    reason=f"Blocked by rule {rule_fqn}: {reason}",
                    tool_name=tool_name,
                    hard_denied=True,
                )

        config = self._safety_config
        if not config or not config.enabled:
            return None

        # Per-tool enabled toggle: when false, hard-deny the tool entirely.
        if tool_name == "bash" and not config.bash.enabled:
            return SafetyVerdict(
                needs_approval=True,
                reason=f"Tool '{tool_name}' is disabled in safety config",
                tool_name=tool_name,
                hard_denied=True,
            )
        if tool_name == "write_file" and not config.write_file.enabled:
            return SafetyVerdict(
                needs_approval=True,
                reason=f"Tool '{tool_name}' is disabled in safety config",
                tool_name=tool_name,
                hard_denied=True,
            )
        if tool_name == "docx" and str(arguments.get("path") or "").lower().endswith(".pdf"):
            return SafetyVerdict(
                needs_approval=True,
                reason="Tool 'docx' only handles .docx files; PDFs are extracted inline before model routing",
                tool_name=tool_name,
                hard_denied=True,
            )

        tier = get_tool_tier(tool_name, tier_overrides=config.tool_tiers)

        # Read-only mode: hard-deny any tool above READ tier as defense-in-depth.
        # The tool list is already filtered at assembly time, but this backstop
        # catches any tool call that bypasses the filtered list (e.g. via prompt
        # injection or a misbehaving model emitting unlisted tool calls).
        if config.read_only and tier != ToolTier.READ:
            return SafetyVerdict(
                needs_approval=True,
                reason=f"Tool '{tool_name}' blocked: read-only mode is active",
                tool_name=tool_name,
                hard_denied=True,
            )

        # Bypass-immune path check: runs unconditionally before
        # should_require_approval() so that AUTO mode, allowed_tools, and
        # session permissions cannot skip it.  Hard-block rules (checked above
        # via the rule enforcer) still take precedence.
        #
        # For write_file/edit_file we return immediately — those tools don't go
        # through _enrich_with_hard_block(), so there's no harder verdict to
        # discover.  For bash we defer: store the verdict and continue so that
        # _enrich_with_hard_block() can upgrade it to hard-blocked if the
        # command also matches a hard-block pattern.
        immune_verdict = check_bypass_immune_path(
            tool_name,
            arguments,
            self._working_dir or ".",
            immune_paths=config.bypass_immune_paths,
        )
        if immune_verdict is not None and tool_name != "bash":
            return immune_verdict

        mode = parse_approval_mode(config.approval_mode)

        result = should_require_approval(
            tool_name=tool_name,
            tool_tier=tier,
            mode=mode,
            allowed_tools=set(config.allowed_tools) if config.allowed_tools else None,
            denied_tools=set(config.denied_tools) if config.denied_tools else None,
            session_allowed=self._session_allowed or None,
        )

        if result is None:
            return SafetyVerdict(
                needs_approval=True,
                reason=f"Tool '{tool_name}' is in the denied tools list",
                tool_name=tool_name,
                hard_denied=True,
            )

        # Check tool-specific destructive patterns even when tier says auto-allow,
        # but NOT in auto mode (auto mode bypasses everything).
        from .tiers import ApprovalMode

        if result is False and mode != ApprovalMode.AUTO:
            if tool_name == "bash":
                verdict = check_bash_command(arguments.get("command", ""), custom_patterns=config.custom_patterns)
                if verdict.needs_approval:
                    enriched = self._enrich_with_hard_block(verdict, arguments)
                    # Hard-block always wins over bypass-immune.
                    if enriched.is_hard_blocked:
                        return enriched
                    # No hard-block: if this command also targets an immune path,
                    # surface the immune verdict so the caller knows to require
                    # approval even in AUTO mode.
                    return immune_verdict if immune_verdict is not None else enriched
                # No destructive pattern — if an immune path was matched, still check for
                # hard-block patterns (e.g. dd if=/dev/urandom > .git/hooks/pre-commit).
                if immune_verdict is not None:
                    return self._enrich_with_hard_block(immune_verdict, arguments)
                return None
            if tool_name == "write_file":
                verdict = check_write_path(
                    arguments.get("path", ""), self._working_dir or ".", sensitive_paths=config.sensitive_paths
                )
                if verdict.needs_approval:
                    return verdict
            return None

        if result is False:
            # AUTO mode: bypass-immune still forces approval for bash.
            # If an immune_verdict is pending, run hard-block enrichment so that
            # catastrophic commands (e.g. dd if=/dev/urandom > .git/hooks/...)
            # are flagged is_hard_blocked even when the approval mode is AUTO.
            if immune_verdict is not None and tool_name == "bash":
                return self._enrich_with_hard_block(immune_verdict, arguments)
            return None

        # Tier-based approval required — return generic verdict for the tool
        if tool_name == "bash":
            verdict = SafetyVerdict(
                needs_approval=True,
                reason=f"Tool '{tool_name}' requires approval (mode: {config.approval_mode})",
                tool_name=tool_name,
                details={"command": arguments.get("command", "")},
            )
            enriched = self._enrich_with_hard_block(verdict, arguments)
            # Hard-block wins; otherwise prefer immune_verdict (carries bypass_immune flag).
            if enriched.is_hard_blocked:
                return enriched
            return immune_verdict if immune_verdict is not None else enriched

        if tool_name == "write_file":
            return SafetyVerdict(
                needs_approval=True,
                reason=f"Tool '{tool_name}' requires approval (mode: {config.approval_mode})",
                tool_name=tool_name,
                details={"path": arguments.get("path", "")},
            )

        # Generic approval for other tools (edit_file, MCP tools, etc.)
        return SafetyVerdict(
            needs_approval=True,
            reason=f"Tool '{tool_name}' requires approval (mode: {config.approval_mode})",
            tool_name=tool_name,
            details={},
        )

    @staticmethod
    def _enrich_with_hard_block(verdict: SafetyVerdict, arguments: dict[str, Any]) -> SafetyVerdict:
        """Check if a bash command matches a hard-block pattern and enrich the verdict."""
        command = arguments.get("command", "")
        description = check_hard_block(command)
        if description:
            verdict.is_hard_blocked = True
            verdict.hard_block_description = description
            verdict.reason = f"DESTRUCTIVE command ({description}): {command}"
        return verdict

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
        confirm_callback: ConfirmCallback | None = None,
        *,
        rule_enforcer_override: RuleEnforcer | None = None,
        _hooks_config: Any | None = None,
        _audit_writer: Any | None = None,
        _extra_env: dict[str, str] | None = None,
        _extra_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        started_at = time.monotonic()
        log_debug(
            logger,
            "tool.dispatch.start",
            lifecycle="start",
            phase="tool_exec",
            tool_name=name,
            argument_shape=lambda: shape_metadata(arguments),
        )
        handler = self._handlers.get(name)
        if not handler:
            log_debug(
                logger,
                "tool.dispatch.failure",
                lifecycle="failure",
                phase="tool_exec",
                tool_name=name,
                error_class="ValueError",
                _started_at=started_at,
            )
            raise ValueError(f"Unknown built-in tool: {name}")

        verdict = self.check_safety(name, arguments, rule_enforcer_override=rule_enforcer_override)
        approval_decision = "auto"
        user_approved_hard_block = False

        # Static hard deny blocks immediately — hooks cannot override this.
        if verdict and verdict.hard_denied:
            log_debug(
                logger,
                "tool.dispatch.failure",
                lifecycle="failure",
                phase="tool_exec",
                tool_name=name,
                status="hard_denied",
                approval_decision="hard_denied",
                _started_at=started_at,
            )
            logger.warning("Tool hard-denied by config: %s — %s", name, verdict.reason)
            return {
                "error": verdict.reason,
                "safety_blocked": True,
                "_approval_decision": "hard_denied",
            }

        # Pre-tool hooks: run after hard-deny gate, before tier-based approval (#1271).
        hook_allowed_domains: tuple[str, ...] = ()
        hook_block_localhost = False
        if _extra_context is not None:
            hook_config = _extra_context.get("config")
            hook_ai_config = getattr(hook_config, "ai", None)
            if hook_ai_config is not None:
                raw_allowed_domains = getattr(hook_ai_config, "allowed_domains", ()) or ()
                hook_allowed_domains = tuple(str(domain) for domain in raw_allowed_domains if domain)
                hook_block_localhost = bool(getattr(hook_ai_config, "block_localhost_api", False))

        if _hooks_config is not None and _hooks_config.pre_tool:
            from ..services.hooks import classify_pre_hook_result as _classify_hook
            from ..services.hooks import run_pre_tool_hooks as _run_pre_tool_hooks

            _pre_decision = await _run_pre_tool_hooks(
                _hooks_config,
                name,
                arguments,
                **_hook_call_kwargs(
                    audit_writer=_audit_writer,
                    extra_context=_extra_context,
                    allowed_domains=hook_allowed_domains,
                    block_localhost=hook_block_localhost,
                ),
            )
            _hook_bucket = _classify_hook(_pre_decision)
            if _hook_bucket == "deny":
                log_debug(
                    logger,
                    "tool.dispatch.failure",
                    lifecycle="failure",
                    phase="tool_exec",
                    tool_name=name,
                    status="hook_denied",
                    approval_decision="hook_denied",
                    _started_at=started_at,
                )
                return {
                    "error": _pre_decision.message or f"Tool '{name}' blocked by hook",
                    "hook_blocked": True,
                    "_approval_decision": "hook_denied",
                }
            if _hook_bucket == "require_approval":
                _hook_cb = confirm_callback or self._confirm_callback
                if _hook_cb is None:
                    # No approval channel: fail closed. This is not a user decision,
                    # so _approval_decision is "denied" (not hook_escalated_denied).
                    return {
                        "error": _pre_decision.message or f"Hook requires approval for '{name}'",
                        "hook_blocked": True,
                        "_approval_decision": "denied",
                    }
                _hook_verdict = SafetyVerdict(
                    needs_approval=True,
                    reason=_pre_decision.message or f"Hook requires approval for '{name}'",
                    tool_name=name,
                )
                _hook_approved = await _hook_cb(_hook_verdict)
                # Emit hook.approval_resolved so audit trail distinguishes hook-driven
                # escalations from tier-based approval prompts (#1492).
                try:
                    from ..services.lineage import emit_hook_approval_resolved as _emit_hook_resolved

                    _emit_hook_resolved(
                        _audit_writer,
                        hook_id=_pre_decision.hook_id or "",
                        tool_name=name,
                        resolution="approved" if _hook_approved else "denied",
                        tool_call_id=(_extra_context or {}).get("tool_call_id", "") or "",
                        conversation_id=(_extra_context or {}).get("conversation_id", "") or "",
                        user_id=(_extra_context or {}).get("user_id", "") or "",
                    )
                except Exception:
                    logger.warning("Failed to emit hook.approval_resolved for hook %r", _pre_decision.hook_id)
                if not _hook_approved:
                    log_debug(
                        logger,
                        "tool.dispatch.failure",
                        lifecycle="failure",
                        phase="tool_exec",
                        tool_name=name,
                        status="hook_escalated_denied",
                        approval_decision="hook_escalated_denied",
                        _started_at=started_at,
                    )
                    return {
                        "error": "Operation denied by user",
                        "exit_code": -1,
                        "_approval_decision": "hook_escalated_denied",
                    }
                approval_decision = "hook_escalated_approved"

        # Tier-based approval (non-hard-denied needs_approval).
        if verdict and verdict.needs_approval:
            # Hard-blocked commands with no approval channel: block silently
            # (safety net for auto mode / unattended agents).
            callback = confirm_callback or self._confirm_callback
            if callback is None:
                if verdict.is_hard_blocked:
                    logger.info("Hard-block safety net (no approval channel): %s", verdict.hard_block_description)
                else:
                    logger.warning("Safety gate blocked (no approval channel): %s", verdict.reason)
                log_debug(
                    logger,
                    "tool.dispatch.failure",
                    lifecycle="failure",
                    phase="tool_exec",
                    tool_name=name,
                    status="approval_unavailable",
                    approval_decision="denied",
                    _started_at=started_at,
                )
                return {
                    "error": "Operation blocked: no approval channel available",
                    "safety_blocked": True,
                    "_approval_decision": "denied",
                }
            confirmed = await callback(verdict)
            if not confirmed:
                log_debug(
                    logger,
                    "tool.dispatch.failure",
                    lifecycle="failure",
                    phase="tool_exec",
                    tool_name=name,
                    status="denied",
                    approval_decision="denied",
                    _started_at=started_at,
                )
                return {"error": "Operation denied by user", "exit_code": -1, "_approval_decision": "denied"}
            if approval_decision == "auto":
                approval_decision = "allowed_once"
            if verdict.is_hard_blocked:
                user_approved_hard_block = True

        # Rate limiting check (after safety, before execution)
        if self._rate_limiter:
            rl_verdict = self._rate_limiter.check(name)
            if rl_verdict and rl_verdict.exceeded:
                if self._rate_limiter.config.action == "block":
                    log_debug(
                        logger,
                        "tool.dispatch.failure",
                        lifecycle="failure",
                        phase="tool_exec",
                        tool_name=name,
                        status="rate_limited",
                        approval_decision="rate_limited",
                        _started_at=started_at,
                    )
                    logger.warning("Tool rate-limited: %s — %s", name, rl_verdict.reason)
                    return {
                        "error": rl_verdict.reason,
                        "safety_blocked": True,
                        "rate_limited": True,
                        "_approval_decision": "rate_limited",
                    }
                logger.warning("Tool rate limit warning: %s — %s", name, rl_verdict.reason)

        extra_kwargs: dict[str, Any] = {}
        if user_approved_hard_block:
            extra_kwargs["_bypass_hard_block"] = True
        if name == "bash" and self._safety_config is not None:
            extra_kwargs["_sandbox_config"] = self._safety_config.bash
        # Per-step credential env injection for workflow bash tool calls (#970)
        if name == "bash" and _extra_env is not None:
            extra_kwargs["_env"] = _extra_env
        # Background task manager injection (#1311)
        if name in ("bash", "bash_background_status", "bash_task_output") and _extra_context:
            if "bg_manager" in _extra_context:
                extra_kwargs["_bg_manager"] = _extra_context["bg_manager"]
            if "conversation_id" in _extra_context:
                extra_kwargs["_conversation_id"] = _extra_context["conversation_id"]
            if "db" in _extra_context:
                extra_kwargs["_db"] = _extra_context["db"]
        # Detached subagent manager injection (#1314)
        if name in ("run_agent", "agent_run_status") and _extra_context:
            if "detach_manager" in _extra_context:
                extra_kwargs["_detach_manager"] = _extra_context["detach_manager"]
            if "conversation_id" in _extra_context:
                extra_kwargs["_conversation_id"] = _extra_context["conversation_id"]
            if "db" in _extra_context:
                extra_kwargs["_db"] = _extra_context["db"]
        # save_memory promotion-pipeline context injection (#217)
        if name == "save_memory" and _extra_context:
            if "db" in _extra_context:
                extra_kwargs["_db"] = _extra_context["db"]
            if "conversation_id" in _extra_context:
                extra_kwargs["_conversation_id"] = _extra_context["conversation_id"]
            if "config" in _extra_context:
                extra_kwargs["_config"] = _extra_context["config"]
            if "user_id" in _extra_context:
                extra_kwargs["_user_id"] = _extra_context["user_id"]
        # Strip 'background'/'detach' from LLM arguments before passing to handler
        if name == "bash" and "background" in arguments:
            extra_kwargs["_background"] = arguments.pop("background")
        if name == "run_agent" and "detach" in arguments:
            extra_kwargs["_detach"] = arguments.pop("detach")
        try:
            result = await handler(**arguments, **extra_kwargs)
        except Exception as exc:
            log_debug(
                logger,
                "tool.dispatch.failure",
                lifecycle="failure",
                phase="tool_exec",
                tool_name=name,
                error_class=type(exc).__name__,
                _started_at=started_at,
            )
            raise

        # Post-tool hooks: may observe output and deny continuation (#1271).
        if _hooks_config is not None and _hooks_config.post_tool:
            from ..services.hooks import run_post_tool_hooks as _run_post_tool_hooks

            _post_decision = await _run_post_tool_hooks(
                _hooks_config,
                name,
                arguments,
                result,
                **_hook_call_kwargs(
                    audit_writer=_audit_writer,
                    extra_context=_extra_context,
                    allowed_domains=hook_allowed_domains,
                    block_localhost=hook_block_localhost,
                ),
            )
            if _post_decision.outcome == "deny":
                log_debug(
                    logger,
                    "tool.dispatch.failure",
                    lifecycle="failure",
                    phase="tool_exec",
                    tool_name=name,
                    status="post_hook_denied",
                    approval_decision="post_hook_denied",
                    output_shape=lambda: shape_metadata(result),
                    _started_at=started_at,
                )
                return {
                    "error": _post_decision.message or f"Tool '{name}' output blocked by hook",
                    "hook_blocked": True,
                    "_approval_decision": "post_hook_denied",
                }

        result["_approval_decision"] = approval_decision
        result["_context_trust"] = "untrusted" if name in _UNTRUSTED_TOOLS else "trusted"
        if name in _UNTRUSTED_TOOLS:
            result["_context_origin"] = f"builtin:{name}"

        # Record the call for rate limiting
        if self._rate_limiter:
            self._rate_limiter.record_call(success="error" not in result)

        log_debug(
            logger,
            "tool.dispatch.success",
            lifecycle="success",
            phase="tool_exec",
            tool_name=name,
            status="error" if "error" in result else "success",
            approval_decision=result.get("_approval_decision"),
            output_shape=lambda: shape_metadata(result),
            _started_at=started_at,
        )
        return result

    def list_tools(self) -> list[str]:
        return list(self._handlers.keys())


def cap_tools(
    tools: list[dict[str, Any]],
    builtin_names: set[str],
    limit: int = 128,
) -> list[dict[str, Any]]:
    """Cap the tools list to *limit*, prioritising built-in tools over MCP.

    Returns the (possibly truncated) list.  Logs a warning when tools are dropped.
    A *limit* of 0 means unlimited (no cap applied).
    """
    if limit <= 0 or len(tools) <= limit:
        return tools

    builtin: list[dict[str, Any]] = []
    mcp: list[dict[str, Any]] = []
    for t in tools:
        name = t.get("function", {}).get("name", "")
        if name in builtin_names:
            builtin.append(t)
        else:
            mcp.append(t)

    mcp.sort(key=lambda t: t.get("function", {}).get("name", ""))
    remaining = limit - len(builtin)
    if remaining < 0:
        remaining = 0
    kept_mcp = mcp[:remaining]
    dropped = mcp[remaining:]

    if dropped:
        names = [t.get("function", {}).get("name", "?") for t in dropped]
        logger.warning(
            "Tool limit (%d) exceeded — dropped %d MCP tool(s): %s",
            limit,
            len(dropped),
            ", ".join(names),
        )

    return builtin + kept_mcp


def register_default_tools(registry: ToolRegistry, working_dir: str | None = None) -> None:
    """Register all built-in tools."""
    from . import ask_user, bash, edit, glob_tool, grep, introspect, read, save_memory, subagent, write
    from .canvas import (
        CANVAS_CREATE_DEFINITION,
        CANVAS_PATCH_DEFINITION,
        CANVAS_UPDATE_DEFINITION,
        handle_create_canvas,
        handle_patch_canvas,
        handle_update_canvas,
    )

    for module in [read, write, edit, bash, glob_tool, grep]:
        handler = module.handle
        defn = module.DEFINITION
        if working_dir and hasattr(module, "set_working_dir"):
            module.set_working_dir(working_dir)
        registry.register(defn["name"], handler, defn)

    registry.register(CANVAS_CREATE_DEFINITION["name"], handle_create_canvas, CANVAS_CREATE_DEFINITION)
    registry.register(CANVAS_UPDATE_DEFINITION["name"], handle_update_canvas, CANVAS_UPDATE_DEFINITION)
    registry.register(CANVAS_PATCH_DEFINITION["name"], handle_patch_canvas, CANVAS_PATCH_DEFINITION)
    registry.register(subagent.DEFINITION["name"], subagent.handle, subagent.DEFINITION)
    registry.register(ask_user.DEFINITION["name"], ask_user.handle, ask_user.DEFINITION)
    registry.register(introspect.DEFINITION["name"], introspect.handle, introspect.DEFINITION)
    # save_memory (#217) — agent-initiated memory candidates via memory_promotion pipeline
    registry.register(save_memory.DEFINITION["name"], save_memory.handle, save_memory.DEFINITION)

    # Background task status tool (#1311)
    registry.register(
        bash.BACKGROUND_STATUS_DEFINITION["name"],
        bash.handle_background_status,
        bash.BACKGROUND_STATUS_DEFINITION,
    )

    # Detached agent run status tool (#1314)
    registry.register(
        subagent.AGENT_RUN_STATUS_DEFINITION["name"],
        subagent.handle_run_status,
        subagent.AGENT_RUN_STATUS_DEFINITION,
    )

    # Background task output tool (#1312) — registered alongside defaults;
    # the _extra_context injection wires _bg_manager at call time.
    from .bash import TASK_OUTPUT_DEFINITION, handle_task_output

    registry.register(TASK_OUTPUT_DEFINITION["name"], handle_task_output, TASK_OUTPUT_DEFINITION)
    _register_optional_office_tools(registry, working_dir)


def register_mission_tools(registry: ToolRegistry) -> None:
    """Register mission tools (opt-in, not called by register_default_tools).

    Call site is in the CLI mission talk handler (#1049).
    """
    from .mission import MISSION_TOOL_DEFINITIONS, MISSION_TOOL_HANDLERS

    for defn in MISSION_TOOL_DEFINITIONS:
        name = defn["name"]
        registry.register(name, MISSION_TOOL_HANDLERS[name], defn)


def _register_optional_office_tools(registry: ToolRegistry, working_dir: str | None = None) -> None:
    """Register office tools if their optional dependencies are installed."""
    import importlib

    for mod_name in ("office_docx", "office_xlsx", "office_pptx"):
        try:
            module = importlib.import_module(f".{mod_name}", package=__package__)
        except ImportError:
            continue
        if not getattr(module, "AVAILABLE", False):
            continue
        if working_dir and hasattr(module, "set_working_dir"):
            module.set_working_dir(working_dir)
        registry.register(module.DEFINITION["name"], module.handle, module.DEFINITION)

"""Shared helpers used by the Claude Agent SDK patch wrapper bodies."""

import asyncio
import functools
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def _extract_agent_name(system_prompt: str, model: str, aigie: Any = None) -> str:
    """
    Resolve the trace display name. Honors `aigie.init(agent_name=...)` first,
    then falls back to a heuristic on the system prompt, then to a model-based
    name. The explicit `agent_name` is the contract customers see in the SDK
    and must take precedence.
    """
    explicit = getattr(aigie, "_agent_name", None) if aigie is not None else None
    if explicit:
        return str(explicit)

    if system_prompt:
        # Look for "You are a/an [role]" pattern
        match = re.search(r"You are (?:a |an |the )?([^.!\n]+)", system_prompt, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            # Remove trailing relative clauses (who, that, which, and their content)
            role = re.sub(r"\s+(?:who|that|which)\s+.*$", "", role, flags=re.IGNORECASE)
            # If role is still too long, take just the first 4 words
            words = role.split()
            if len(words) > 4:
                role = " ".join(words[:4])
            if role:
                return role.title()

    # Fall back to model-based name
    return _shorten_model_name(model) + " Agent"


def _shorten_model_name(model: str) -> str:
    """Convert full model name to short display name."""
    if not model:
        return "Claude"
    model_lower = model.lower()
    if "sonnet" in model_lower:
        return "Sonnet"
    if "haiku" in model_lower:
        return "Haiku"
    if "opus" in model_lower:
        return "Opus"
    return "Claude"


def _enable_hook_events(options: Any) -> None:
    """Force ClaudeAgentOptions.include_hook_events=True so any CLI-side hook
    events flow through receive_response (HookEventMessage). User-defined
    in-process HookCallbacks do NOT trigger these events — those are wrapped
    separately by _wrap_user_hooks().
    """
    if options is None:
        return
    try:
        if getattr(options, "include_hook_events", False) is False:
            options.include_hook_events = True
    except Exception as exc:  # noqa: BLE001
        logger.debug("could not enable include_hook_events on options" + ": %s", exc)


def _wrap_user_hooks(options: Any, handler: Any):  # noqa: C901, PLR0915
    """Wrap each user-supplied HookCallback in `options.hooks` so aigie
    records the invocation on the matching tool span. The original callback
    is awaited and its output is returned unchanged."""
    if options is None or handler is None:
        return
    hooks_dict = getattr(options, "hooks", None)
    if not hooks_dict:
        return

    def _make_wrapper(event_name: str, original_cb: Any) -> Any:
        async def wrapped(input_data: Any, tool_use_id: Any, context: Any):
            try:
                tuid = tool_use_id
                if tuid is None and isinstance(input_data, dict):
                    tuid = input_data.get("tool_use_id") or input_data.get("toolUseId")
                tool_name = None
                if isinstance(input_data, dict):
                    tool_name = input_data.get("tool_name")
                handler._record_user_hook(event_name, tuid, tool_name)
            except Exception as exc:  # noqa: BLE001
                logger.debug("user hook record failed" + ": %s", exc)
            return await original_cb(input_data, tool_use_id, context)

        return wrapped

    for event_name, matchers in list(hooks_dict.items()):
        if not isinstance(matchers, list):
            continue
        for matcher in matchers:
            cb_list = getattr(matcher, "hooks", None)
            if not cb_list:
                continue
            matcher.hooks = [_make_wrapper(event_name, cb) for cb in cb_list]


def _wrap_tools_with_remediation(  # noqa: C901, PLR0915
    tools: list[Any], engine, config, handler, dispatcher=None
) -> list[Any]:  # noqa: C901, PLR0915
    """Wrap each callable tool to catch errors and append remediation guidance.

    When a tool raises an exception, the Claude Agent SDK surfaces the error
    to the model. By appending guidance to the error message, the model sees
    the remediation advice alongside the error.

    In autonomous mode with a dispatcher, also checks for pending gateway
    interventions before execution, and actually retries on retriable errors.
    """
    wrapped: list[Any] = []
    for tool in tools:
        if callable(tool):

            @functools.wraps(tool)
            async def remediation_tool(*args, _orig=tool, **kw):  # noqa: C901, PLR0912, PLR0915
                tool_name = getattr(_orig, "__name__", "unknown")

                # Check pending gateway intervention before executing
                if dispatcher and handler.trace_id and config.remediation_mode == "autonomous":
                    signal = dispatcher.pop_pending(handler.trace_id)
                    if signal:
                        if signal.intervention_type == "delay":
                            delay_ms = signal.payload.get("delay_ms", 1000)
                            await asyncio.sleep(delay_ms / 1000.0)
                        elif signal.intervention_type == "inject_correction":
                            corrections = signal.payload.get("corrections", {})
                            if corrections:
                                kw = {**kw, **corrections}
                        elif signal.intervention_type == "break_loop":
                            raise RuntimeError(f"[Aigie] {signal.reason}")

                try:
                    if asyncio.iscoroutinefunction(_orig):
                        return await _orig(*args, **kw)
                    return _orig(*args, **kw)
                except Exception as e:
                    try:
                        rem = await engine.evaluate(
                            str(e),
                            tool_name,
                            "",
                            handler.trace_id or "",
                            mode=config.remediation_mode,
                        )
                        if rem and config.remediation_mode == "autonomous":
                            applied_programmatic = False
                            # Try structured fix via AutoFixApplicator
                            if rem.action_type:
                                try:
                                    fix_action = engine.to_fix_action(rem)
                                    if fix_action:
                                        from aigie.interceptor.protocols import InterceptionContext
                                        from aigie.realtime.auto_fix import AutoFixApplicator

                                        applicator = AutoFixApplicator()

                                        async def _retry_executor(**kwargs):
                                            if asyncio.iscoroutinefunction(_orig):
                                                return await _orig(*args, **kw)
                                            return _orig(*args, **kw)

                                        applicator.set_retry_executor(_retry_executor)
                                        ctx = InterceptionContext(
                                            provider="claude_agent_sdk",
                                            model="",
                                            messages=[],
                                            response_content=str(e),
                                        )
                                        fix_result = await applicator.apply_fixes(ctx, [fix_action])
                                        if fix_result.success:
                                            applied_programmatic = True
                                            engine.mark_applied(rem)
                                            if fix_result.modified_response is not None:
                                                return fix_result.modified_response
                                except Exception as fix_err:
                                    logger.debug(f"[AIGIE] Programmatic fix failed: {fix_err}")

                            # Fall back to text guidance injection
                            if not applied_programmatic and rem.guidance_text:
                                engine.mark_applied(rem)
                                raise type(e)(f"{e}\n\n{rem.guidance_text}") from e
                    except type(e):
                        raise  # Re-raise the enhanced error
                    except Exception as exc:  # noqa: BLE001
                        logger.debug("remediation query failed, raising original" + ": %s", exc)
                    raise

            wrapped.append(remediation_tool)
        else:
            wrapped.append(tool)  # Pass through non-callable (schema-based tools)
    return wrapped

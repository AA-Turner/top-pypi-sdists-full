"""The ``claude-code`` engine — delegates the agent loop to Claude Code.

Runs the Claude Agent SDK (a wrapper over the ``claude`` CLI's ``stream-json``
protocol) and translates its message stream into native ``AgentEvent``s, so a
Claude Code agent is session-backed, evaluable, optimizable, and governed like a
native agent. See ``specs/capabilities/engines.md`` and the M1 milestone.

Locality: the harness runs as a subprocess (the SDK spawns the ``claude`` CLI).
In the runtime this subprocess lives inside the sandbox (the isolation boundary).

Governance: this engine declares a *partial* enforcement surface — it enforces
autonomy (``permission_mode``) and the step budget (``max_turns``), bridges tool
approval (``can_use_tool`` → ``prompt.required``), can only observe mid-loop guard
steering, and has no native equivalent for token/cost/time budgets (enforced by
killing the run via the inference gateway). The runtime reconciles this against
the session policy (CAP-EGOV-*).
"""

import asyncio
import json
import os
import typing as t

from dreadnode.agents.engines.base import (
    AgentEngine,
    CapabilityComponent,
    EnforcementSurface,
    EngineContext,
    PolicyFacet,
)
from dreadnode.agents.events import (
    AgentEnd,
    AgentEvent,
    AgentStart,
    GenerationContent,
    GenerationStep,
    ToolEnd,
    ToolStart,
    ToolStep,
)
from dreadnode.agents.tools import FunctionCall, ToolCall
from dreadnode.generators.generator import Usage
from dreadnode.generators.message import Message

if t.TYPE_CHECKING:
    from collections.abc import AsyncIterator

# Config fields a full harness honors; everything else on Agent is ignored
# (the runtime warns via honored_config + reconciliation, CAP-EGOV-006).
# NOTE: ``tools`` is intentionally absent — under Decision A (CAP-ENG-022) the
# harness uses its OWN tools; our capability tool rules are not applied here.
_HONORED_CONFIG = {"model", "instructions", "max_steps"}

# Env var holding the inference-gateway base URL the harness's model calls are
# routed through (recovers usage/cost + budget kill-switch + model allowlist).
# Wired to the real gateway in M3; honored here if the runtime sets it.
_GATEWAY_ENV = "DREADNODE_INFERENCE_BASE_URL"


def _load_sdk() -> t.Any:
    """Import ``claude_agent_sdk`` lazily with an actionable error if missing."""
    try:
        import claude_agent_sdk
    except ImportError as exc:  # pragma: no cover - exercised via the message
        raise ImportError(
            "The 'claude-code' engine requires the Claude Agent SDK. "
            "Install with: pip install 'dreadnode[claude-code]' (and ensure the "
            "`claude` CLI is on PATH)."
        ) from exc
    return claude_agent_sdk


class ClaudeCodeEngine(AgentEngine):
    """Runs Claude Code as the agent loop, translating its stream to native events."""

    name = "claude-code"
    dispatches_internally = False

    # Overridable in tests with a fake module exposing the SDK surface.
    _sdk: t.Any = None

    def _sdk_module(self) -> t.Any:
        return self._sdk if self._sdk is not None else _load_sdk()

    # ------------------------------------------------------------------ #
    # Governance declaration
    # ------------------------------------------------------------------ #

    def describe_enforcement(self, policy: t.Any) -> EnforcementSurface:  # noqa: ARG002
        return EnforcementSurface(
            enforces=frozenset({PolicyFacet.AUTONOMY, PolicyFacet.STEP_BUDGET}),
            bridges=frozenset({PolicyFacet.TOOL_APPROVAL}),
            observes_only=frozenset({PolicyFacet.GUARD_STEERING, PolicyFacet.SCORERS}),
            no_equivalent=frozenset(
                {PolicyFacet.TOKEN_BUDGET, PolicyFacet.COST_BUDGET, PolicyFacet.TIME_BUDGET}
            ),
        )

    def honored_config(self) -> set[str] | None:
        return set(_HONORED_CONFIG)

    def consumed_components(self) -> set[CapabilityComponent]:
        # Decision A: Claude Code uses its own built-in tools, so capability
        # Python ``@tool`` / MCP tools are not injected. Skills are portable in
        # principle (shared SKILL.md standard) but materialization into the
        # harness skill path is not wired yet — so nothing is consumed today.
        # Tool *approval* still covers every harness tool via the permission
        # bridge (can_use_tool), independent of injection (CAP-ENG-024).
        # Planned: Option B exports capability tools via SDK MCP (see engines.md).
        return set()

    # ------------------------------------------------------------------ #
    # Options + permission bridge
    # ------------------------------------------------------------------ #

    def _build_options(self, ctx: EngineContext) -> t.Any:
        sdk = self._sdk_module()
        agent = ctx.agent

        kwargs: dict[str, t.Any] = {}
        if agent.instructions:
            kwargs["system_prompt"] = agent.instructions
        harness_model = self._harness_model(agent.model_name)
        if harness_model:
            kwargs["model"] = harness_model
        # max_steps (native, react-step unit) maps best-effort to max_turns
        # (assistant-turn unit). Documented unit mismatch (CAP-ENG / governance).
        if agent.max_steps:
            kwargs["max_turns"] = agent.max_steps

        # Per-turn token deltas are only emitted as StreamEvents when partial
        # messages are on — otherwise usage is lost. Force it (the PRD's
        # transcript-fidelity mitigation). ResultMessage totals are also captured
        # as a fallback in _on_result.
        kwargs["include_partial_messages"] = True

        # Route model calls through the inference gateway when the runtime set it.
        gateway = os.environ.get(_GATEWAY_ENV)
        if gateway:
            kwargs["env"] = {"ANTHROPIC_BASE_URL": gateway}

        # Permission handling:
        #  - HITL context (a permission bridge is present, i.e. a non-autonomous
        #    session): consult ``can_use_tool`` so the harness's tool requests
        #    route through our prompt.required/respond UX (CAP-EGOV-007). Use
        #    ``default`` mode so the callback is invoked.
        #  - No HITL (autonomous/eval, or bare-SDK use): run tools freely, matching
        #    native autonomous behavior — per-tool human prompts do not fire there.
        if ctx.permission is not None:
            kwargs["can_use_tool"] = self._make_can_use_tool(ctx)
            kwargs["permission_mode"] = "default"
            # Don't inherit local/project claude settings — they may pre-approve
            # tools (e.g. Bash), which would bypass can_use_tool and silently
            # defeat the platform's HITL governance. With no settings loaded,
            # can_use_tool is authoritative for every tool the harness runs.
            kwargs["setting_sources"] = []
        else:
            kwargs["permission_mode"] = "bypassPermissions"

        return sdk.ClaudeAgentOptions(**kwargs)

    def _prompt_input(self, ctx: EngineContext, turn_done: "asyncio.Event") -> t.Any:
        """Build the ``query`` prompt input.

        A plain string works for one-shot runs, but the SDK's ``can_use_tool``
        callback requires **streaming input mode** — an async iterable of message
        dicts. So when a permission bridge is wired (non-autonomous), stream the
        goal as a single user message. The generator must then stay open until
        the turn ends (``turn_done``): closing stdin early kills the bidirectional
        control channel the can_use_tool round-trip rides on ("Stream closed").
        """
        if ctx.permission is None:
            return ctx.goal

        goal = ctx.goal

        async def _stream() -> "t.AsyncIterator[dict[str, t.Any]]":
            yield {"type": "user", "message": {"role": "user", "content": goal}}
            await turn_done.wait()

        return _stream()

    @staticmethod
    def _harness_model(model_name: str | None) -> str | None:
        """Map a litellm model id to a claude-CLI-acceptable model name.

        The CLI wants a bare name (``claude-sonnet-4-5-20250929``) or alias, not a
        provider-prefixed id (``anthropic/claude-...``). Strip the provider
        segment; bare names and aliases pass through unchanged.
        """
        if not model_name:
            return None
        return model_name.rsplit("/", 1)[-1]

    def _make_can_use_tool(self, ctx: EngineContext) -> t.Any:
        sdk = self._sdk_module()

        async def can_use_tool(
            tool_name: str,
            tool_input: dict[str, t.Any],
            context: t.Any = None,  # noqa: ARG001  (SDK callback signature)
        ) -> t.Any:
            assert ctx.permission is not None  # guarded by caller
            allowed = await ctx.permission.request_tool_approval(
                tool_name=tool_name, tool_input=tool_input
            )
            if allowed:
                return sdk.PermissionResultAllow(updated_input=tool_input)
            return sdk.PermissionResultDeny(message="Denied by session policy.")

        return can_use_tool

    # ------------------------------------------------------------------ #
    # Loop
    # ------------------------------------------------------------------ #

    async def run_loop(self, ctx: EngineContext) -> "AsyncIterator[AgentEvent]":
        sdk = self._sdk_module()
        agent = ctx.agent
        options = self._build_options(ctx)

        state = ClaudeCodeTranslationState()
        error: str | None = None
        # When gating tools, the prompt is a streaming input that must stay open
        # for the can_use_tool control round-trip; this lets it close once the
        # turn's ResultMessage arrives (see _prompt_input).
        turn_done = asyncio.Event()

        async for event in self._dispatch(
            ctx,
            state,
            AgentStart(
                agent_id=agent.agent_id,
                agent_name=agent.name,
                inputs={"goal": ctx.goal},
                params={
                    "engine": self.name,
                    **({"model": agent.model_name} if agent.model_name else {}),
                },
            ),
        ):
            yield event

        try:
            async for message in sdk.query(
                prompt=self._prompt_input(ctx, turn_done), options=options
            ):
                if isinstance(message, sdk.ResultMessage):
                    turn_done.set()  # let the streaming input close after the turn
                for event in self._translate(ctx, message, state):
                    async for out in self._dispatch(ctx, state, event):
                        yield out
                    if state.stop:
                        break
                if state.stop:
                    break
        except Exception as exc:
            error = str(exc)
        finally:
            turn_done.set()  # ensure the input generator can always exit

        async for event in self._dispatch(
            ctx,
            state,
            AgentEnd(
                agent_id=agent.agent_id,
                agent_name=agent.name,
                status="errored" if (error or state.error) else "finished",
                stop_reason="error" if (error or state.error) else "finished",
                error=error or state.error,
            ),
        ):
            yield event

    async def _dispatch(
        self, ctx: EngineContext, state: "ClaudeCodeTranslationState", event: AgentEvent
    ) -> "AsyncIterator[AgentEvent]":
        """Run an event through observational hooks; honor terminal reactions.

        Foreign engines can't honor mid-loop steering (Continue/Retry) — the
        runtime refuses such policies (CAP-EGOV-005). Terminal reactions
        (Finish/Fail) set ``state.stop`` so the harness loop breaks.
        """
        from dreadnode.agents.reactions import Fail, Finish, Reaction

        try:
            async for out in ctx.dispatch(event):
                yield out
        except Finish:
            state.stop = True
        except Fail as f:
            state.stop = True
            state.error = str(f.error)
        except Reaction:
            # Continue/Retry can't steer a foreign loop; reconciliation should
            # have refused the policy. Ignore defensively rather than crash.
            pass

    # ------------------------------------------------------------------ #
    # Message → native event translation
    # ------------------------------------------------------------------ #

    def translate(
        self, ctx: EngineContext, message: t.Any, state: "ClaudeCodeTranslationState"
    ) -> list[AgentEvent]:
        """Translate one Claude Agent SDK message into native ``AgentEvent``s.

        Public entry point for custom engines that subclass ``ClaudeCodeEngine``
        and drive their own orchestration. Pair it with a per-run
        :class:`ClaudeCodeTranslationState` and ``ctx.dispatch`` — see the custom engines
        guide. ``message`` is a ``claude_agent_sdk`` message (AssistantMessage,
        UserMessage, StreamEvent, ResultMessage); unknown types yield nothing.
        """
        return self._translate(ctx, message, state)

    def _translate(
        self, ctx: EngineContext, message: t.Any, state: "ClaudeCodeTranslationState"
    ) -> list[AgentEvent]:
        sdk = self._sdk_module()
        if isinstance(message, sdk.AssistantMessage):
            return self._on_assistant(ctx, message, state)
        if isinstance(message, sdk.UserMessage):
            return self._on_user(ctx, message, state)
        if isinstance(message, sdk.StreamEvent):
            self._on_stream_event(message, state)
            return []
        if isinstance(message, sdk.ResultMessage):
            self._on_result(message, state)
            return []
        return []

    def _on_assistant(
        self, ctx: EngineContext, msg: t.Any, state: "ClaudeCodeTranslationState"
    ) -> list[AgentEvent]:
        sdk = self._sdk_module()
        agent = ctx.agent
        state.step += 1

        text_parts: list[str] = []
        thinking_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        tool_call_meta: list[dict[str, t.Any]] = []

        for block in msg.content or []:
            if isinstance(block, sdk.TextBlock):
                text_parts.append(block.text)
            elif isinstance(block, sdk.ThinkingBlock):
                thinking_parts.append(getattr(block, "thinking", "") or "")
            elif isinstance(block, sdk.ToolUseBlock):
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        function=FunctionCall(
                            name=block.name, arguments=json.dumps(block.input or {})
                        ),
                    )
                )
                tool_call_meta.append({"id": block.id, "name": block.name})
                state.pending_tools[block.id] = {"name": block.name, "input": block.input or {}}

        usage = state.drain_usage(model=getattr(msg, "model", None) or agent.model_name)
        reasoning = "\n".join(p for p in thinking_parts if p) or None
        content = "\n".join(text_parts) or None
        extra: dict[str, t.Any] = {}
        if reasoning:
            extra["reasoning_content"] = reasoning

        events: list[AgentEvent] = [
            GenerationContent(
                agent_id=agent.agent_id,
                agent_name=agent.name,
                step=state.step,
                content=content,
                tool_calls=tool_call_meta,
                extra=extra,
            )
        ]

        assistant_msg = Message(
            "assistant",
            content or "",
            metadata={"agent": agent.name, "model": agent.model_name, **extra},
        )
        if tool_calls:
            assistant_msg.tool_calls = tool_calls

        # Seed the first step with the initiating user message, mirroring the
        # native loop (which starts from [user_message, *generated]). Without
        # this the goal never appears in the transcript.
        step_messages: list[Message] = []
        if state.step == 1:
            step_messages.append(
                Message(
                    "user",
                    str(ctx.goal or ""),
                    metadata={"agent": agent.name, "model": agent.model_name},
                )
            )
        step_messages.append(assistant_msg)

        events.append(
            GenerationStep(
                agent_id=agent.agent_id,
                agent_name=agent.name,
                status="running",
                step=state.step,
                messages=step_messages,
                usage=usage,
                stop_reason="tool_use" if tool_calls else "end_turn",
                extra=extra,
            )
        )
        return events

    def _on_user(
        self, ctx: EngineContext, msg: t.Any, state: "ClaudeCodeTranslationState"
    ) -> list[AgentEvent]:
        sdk = self._sdk_module()
        agent = ctx.agent
        content = msg.content if isinstance(msg.content, list) else []
        events: list[AgentEvent] = []

        for block in content:
            if not isinstance(block, sdk.ToolResultBlock):
                continue
            tool_info = state.pending_tools.pop(block.tool_use_id, None)
            if tool_info is None:
                continue
            result_text = _extract_tool_result(block.content)
            is_error = bool(getattr(block, "is_error", False))
            tool_call = ToolCall(
                id=block.tool_use_id,
                function=FunctionCall(
                    name=tool_info["name"], arguments=json.dumps(tool_info["input"])
                ),
            )
            events.append(
                ToolStart(agent_id=agent.agent_id, agent_name=agent.name, tool_call=tool_call)
            )
            events.append(
                ToolEnd(
                    agent_id=agent.agent_id,
                    agent_name=agent.name,
                    tool_call=tool_call,
                    result=result_text,
                    error=result_text if is_error else None,
                )
            )
            events.append(
                ToolStep(
                    agent_id=agent.agent_id,
                    agent_name=agent.name,
                    status="running",
                    step=state.step,
                    messages=[
                        Message(
                            "tool",
                            result_text or "",
                            tool_call_id=block.tool_use_id,
                            metadata={"agent": agent.name},
                        )
                    ],
                    tool_call=tool_call,
                    stop=False,
                )
            )
        return events

    def _on_stream_event(self, msg: t.Any, state: "ClaudeCodeTranslationState") -> None:
        evt = getattr(msg, "event", None)
        if not isinstance(evt, dict):
            return
        if evt.get("type") == "message_start":
            usage = evt.get("message", {}).get("usage", {})
            state.pending_tokens["input_tokens"] = usage.get("input_tokens", 0)
            state.pending_tokens["cache_read_input_tokens"] = usage.get(
                "cache_read_input_tokens", 0
            )
            state.pending_tokens["cache_creation_input_tokens"] = usage.get(
                "cache_creation_input_tokens", 0
            )
        elif evt.get("type") == "message_delta":
            usage = evt.get("usage", {})
            state.pending_tokens["output_tokens"] = state.pending_tokens.get(
                "output_tokens", 0
            ) + usage.get("output_tokens", 0)

    def _on_result(self, msg: t.Any, state: "ClaudeCodeTranslationState") -> None:
        state.result_text = getattr(msg, "result", "") or ""
        if getattr(msg, "is_error", False):
            state.error = state.error or "Harness reported an error result."


def _extract_tool_result(content: t.Any) -> str:
    """Flatten a ToolResultBlock content (str or list of blocks) to text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [
            block.get("text", "") if isinstance(block, dict) else str(block) for block in content
        ]
        return "\n".join(p for p in parts if p)
    return "" if content is None else str(content)


class ClaudeCodeTranslationState:
    """Per-run mutable state for stream translation."""

    def __init__(self) -> None:
        self.step = 0
        self.stop = False
        self.error: str | None = None
        self.result_text = ""
        self.pending_tools: dict[str, dict[str, t.Any]] = {}
        self.pending_tokens: dict[str, int] = {}

    def drain_usage(self, *, model: str | None = None) -> Usage:  # noqa: ARG002
        inp = self.pending_tokens.pop("input_tokens", 0)
        out = self.pending_tokens.pop("output_tokens", 0)
        cache_read = self.pending_tokens.pop("cache_read_input_tokens", 0)
        cache_write = self.pending_tokens.pop("cache_creation_input_tokens", 0)
        return Usage(
            input_tokens=inp,
            output_tokens=out,
            total_tokens=inp + out,
            cache_read_input_tokens=cache_read,
            cache_creation_input_tokens=cache_write,
        )

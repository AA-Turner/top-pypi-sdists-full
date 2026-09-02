"""MockChat — a no-cost fake chat provider that follows the EXACT real path.

Why this exists
---------------
Testing sub-agent fan-out (10+ agents at once, deep nesting, background spawns)
against real providers is slow, non-deterministic, and expensive. MockChat is a
real provider client in every structural sense — it is dispatched by
``unified_client.execute`` exactly like OpenAI/Anthropic/etc., reads the emitter
from the ``AppContext``, streams chunks, returns a ``UnifiedResponse`` + a
``TokenUsage``, and can emit tool calls that the orchestrator dispatches for
real — but it NEVER makes a network call. Everything upstream and downstream of
the network boundary (orchestrator loop, persistence coordinator, streaming,
usage/cost rollup, tool execution) runs the genuine code path, so the side
effects we need to observe are real while the provider call is free.

Routing
-------
A real ``ai_model`` row routes through its offering to the ai.api row whose
``translator_key`` is ``"mock_chat"``, which maps to the ``MockChat`` factory in
``_PROVIDER_FACTORIES``. As far as the entire system is concerned it is just
another model.

Controlling behavior — the ``mock`` spec
-----------------------------------------
Behavior is driven by a dict on ``config.metadata["mock"]`` (mirrors how the
extraction path reads ``config.metadata["extraction"]``). Bake it into a test
agent's ``settings.metadata.mock`` (or inject it per request). Every field is
optional — with no spec, the model echoes the last user message after a short
simulated latency. Supported keys (see ``MockSpec``):

    latency_ms       total simulated wall-clock time (capped at MOCK_MAX_LATENCY_MS)
    ttft_ms          time-to-first-token before streaming starts
    chunks           how many stream chunks to split the text into
    text             the final assistant text (default: echo last user text)
    mode             "text" | "echo" | "json"
    json             structured object to emit (mode == "json")
    input_tokens     simulated prompt tokens (default: estimated from messages)
    output_tokens    simulated completion tokens (default: estimated from text)
    tool_calls       [{"name": str, "arguments": dict}] — emitted as REAL tool
                     calls on the first pass; on the follow-up turn (once a tool
                     result is present in the message history) the model returns
                     ``text``. This exercises the full tool round-trip for free.
    fail             if true, simulate a provider error (raises after send_error)
    error_message    the message used when ``fail`` is set

Package independence
---------------------
No host/aidream imports. Emitter is read through the same ``AppContext`` seam
every other provider uses, so MockChat is importable wherever matrx-ai is.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from matrx_ai.config import (
    TextContent,
    TokenUsage,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.config.tools_config import ToolCallContent
if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

# CAPS — behavior knobs, not env vars (changing them is a code push, never a
# silent per-environment default). A bad/hostile spec must not be able to hang a
# test forever, so total simulated latency is hard-capped.
MOCK_DEFAULT_LATENCY_MS = 400
MOCK_DEFAULT_TTFT_MS = 80
MOCK_DEFAULT_CHUNKS = 6
MOCK_MAX_LATENCY_MS = 120_000
_CHARS_PER_TOKEN = 4  # crude token estimate, only for simulated usage numbers


@dataclass
class MockSpec:
    latency_ms: int = MOCK_DEFAULT_LATENCY_MS
    ttft_ms: int = MOCK_DEFAULT_TTFT_MS
    chunks: int = MOCK_DEFAULT_CHUNKS
    text: str | None = None
    mode: str = "echo"  # echo | text | json
    json_payload: dict[str, Any] | list[Any] | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    fail: bool = False
    error_message: str = "Simulated mock provider failure."

    @classmethod
    def from_metadata(cls, raw: Any) -> MockSpec:
        if not isinstance(raw, dict):
            return cls()
        return cls(
            latency_ms=_clamp_int(
                raw.get("latency_ms"), MOCK_DEFAULT_LATENCY_MS, 0, MOCK_MAX_LATENCY_MS
            ),
            ttft_ms=_clamp_int(raw.get("ttft_ms"), MOCK_DEFAULT_TTFT_MS, 0, MOCK_MAX_LATENCY_MS),
            chunks=_clamp_int(raw.get("chunks"), MOCK_DEFAULT_CHUNKS, 1, 500),
            text=raw.get("text") if isinstance(raw.get("text"), str) else None,
            mode=raw.get("mode") if raw.get("mode") in ("echo", "text", "json") else "echo",
            json_payload=raw.get("json") if isinstance(raw.get("json"), (dict, list)) else None,
            input_tokens=_opt_int(raw.get("input_tokens")),
            output_tokens=_opt_int(raw.get("output_tokens")),
            tool_calls=[
                tc for tc in raw.get("tool_calls", []) if isinstance(tc, dict) and tc.get("name")
            ],
            fail=bool(raw.get("fail", False)),
            error_message=str(raw.get("error_message", "Simulated mock provider failure.")),
        )


def _opt_int(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _clamp_int(value: Any, default: int, lo: int, hi: int) -> int:
    n = _opt_int(value)
    if n is None:
        n = default
    return max(lo, min(hi, n))


class MockChat:
    """No-cost fake chat client. See module docstring for the full contract."""

    def __init__(self, debug: bool = False):
        self.endpoint_name = "[MOCK CHAT]"
        self.debug = debug

    async def execute(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        debug: bool = False,
    ) -> UnifiedResponse:
        # The mock provider has no wire; usage/logging label off the profile.
        wire_label = profile.wire_format
        from matrx_ai.context.app_context import get_app_context

        emitter = get_app_context().emitter
        model_name = unified_config.model
        spec = MockSpec.from_metadata(self._raw_spec(unified_config))

        if debug or self.debug:
            vcprint(
                data={
                    "model": model_name,
                    "mode": spec.mode,
                    "latency_ms": spec.latency_ms,
                    "tool_calls": len(spec.tool_calls),
                    "fail": spec.fail,
                },
                title=f"[MockChat] execute wire={wire_label}",
                color="magenta",
            )

        if spec.fail:
            # Run the real error path so failure handling/persistence is exercised.
            await emitter.send_error(
                error_type="mock_failure",
                message=spec.error_message,
                user_message=spec.error_message,
            )
            raise RuntimeError(f"[MockChat] {spec.error_message}")

        # ── Tool-call round-trip ────────────────────────────────────────────
        # First pass (no tool result in history yet) → emit the configured tool
        # calls so the orchestrator dispatches them for real. Follow-up pass
        # (a tool result is present) → fall through to the normal text answer.
        if spec.tool_calls and not self._history_has_tool_result(unified_config):
            return await self._respond_with_tool_calls(
                spec, unified_config, emitter, model_name, wire_label
            )

        return await self._respond_with_text(spec, unified_config, emitter, model_name, wire_label)

    # ------------------------------------------------------------------ #
    # Response builders
    # ------------------------------------------------------------------ #

    async def _respond_with_text(
        self,
        spec: MockSpec,
        unified_config: UnifiedConfig,
        emitter: Any,
        model_name: str,
        wire_label: str,
    ) -> UnifiedResponse:
        text = self._resolve_text(spec, unified_config)
        await self._simulate_stream(text, spec, emitter)

        usage = self._build_usage(spec, unified_config, text, model_name, wire_label)
        message = UnifiedMessage(role="assistant", content=[TextContent(text=text)])
        return UnifiedResponse(
            messages=[message],
            usage=usage,
            stop_reason="stop",
            finish_reason="stop",
            metadata={"mock": True, "model": model_name, "mode": spec.mode},
        )

    async def _respond_with_tool_calls(
        self,
        spec: MockSpec,
        unified_config: UnifiedConfig,
        emitter: Any,
        model_name: str,
        wire_label: str,
    ) -> UnifiedResponse:
        # A brief simulated "deciding to call tools" delay, no text chunks.
        await asyncio.sleep(min(spec.ttft_ms, MOCK_MAX_LATENCY_MS) / 1000.0)

        content: list[Any] = []
        for tc in spec.tool_calls:
            args = tc.get("arguments")
            content.append(
                ToolCallContent(
                    type="tool_call",
                    id=str(uuid.uuid4()),
                    name=str(tc["name"]),
                    arguments=args if isinstance(args, dict) else {},
                    metadata={"mock": True},
                )
            )

        # Pass unified_config so the tool-emitting turn still reports estimated
        # input tokens (otherwise the first pass records input_tokens=0).
        usage = self._build_usage(spec, unified_config, "", model_name, wire_label)
        message = UnifiedMessage(role="assistant", content=content)
        return UnifiedResponse(
            messages=[message],
            usage=usage,
            stop_reason="tool_calls",
            finish_reason="tool_calls",
            metadata={"mock": True, "model": model_name, "tool_calls": len(content)},
        )

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _raw_spec(unified_config: UnifiedConfig) -> Any:
        meta = getattr(unified_config, "metadata", None)
        if isinstance(meta, dict):
            return meta.get("mock")
        return None

    def _resolve_text(self, spec: MockSpec, unified_config: UnifiedConfig) -> str:
        if spec.mode == "json":
            payload = spec.json_payload if spec.json_payload is not None else {"mock": True}
            return json.dumps(payload, ensure_ascii=False)
        if spec.mode == "text" and spec.text is not None:
            return spec.text
        if spec.text is not None:
            return spec.text
        # echo (default): reflect the last user message so callers can assert
        # the round-trip end-to-end without configuring anything.
        echoed = self._last_user_text(unified_config)
        return f"[mock:{unified_config.model}] {echoed}".strip()

    async def _simulate_stream(self, text: str, spec: MockSpec, emitter: Any) -> None:
        await asyncio.sleep(min(spec.ttft_ms, MOCK_MAX_LATENCY_MS) / 1000.0)
        if not text:
            return
        n = max(1, min(spec.chunks, len(text)))
        size = max(1, (len(text) + n - 1) // n)
        pieces = [text[i : i + size] for i in range(0, len(text), size)]
        remaining_ms = max(0, spec.latency_ms - spec.ttft_ms)
        per_chunk_s = (remaining_ms / 1000.0) / max(1, len(pieces))
        for piece in pieces:
            await emitter.send_chunk(piece)
            if per_chunk_s:
                await asyncio.sleep(per_chunk_s)

    def _build_usage(
        self,
        spec: MockSpec,
        unified_config: UnifiedConfig | None,
        text: str,
        model_name: str,
        wire_label: str,
    ) -> TokenUsage:
        in_tok = spec.input_tokens
        if in_tok is None:
            in_tok = self._estimate_input_tokens(unified_config)
        out_tok = spec.output_tokens
        if out_tok is None:
            out_tok = max(1, len(text) // _CHARS_PER_TOKEN) if text else 0
        return TokenUsage(
            input_tokens=in_tok,
            output_tokens=out_tok,
            matrx_model_name=model_name,
            api=wire_label,
        )

    @staticmethod
    def _estimate_input_tokens(unified_config: UnifiedConfig | None) -> int:
        if unified_config is None:
            return 0
        total = 0
        for msg in getattr(unified_config, "messages", []) or []:
            for block in getattr(msg, "content", []) or []:
                text = getattr(block, "text", None)
                if isinstance(text, str):
                    total += len(text)
        return max(0, total // _CHARS_PER_TOKEN)

    @staticmethod
    def _history_has_tool_result(unified_config: UnifiedConfig) -> bool:
        for msg in getattr(unified_config, "messages", []) or []:
            if getattr(msg, "role", "") in ("tool", "function"):
                return True
            for block in getattr(msg, "content", []) or []:
                btype = getattr(block, "type", "")
                if btype in ("tool_result", "function_call_output"):
                    return True
        return False

    @staticmethod
    def _last_user_text(unified_config: UnifiedConfig) -> str:
        messages = getattr(unified_config, "messages", []) or []
        for msg in reversed(messages):
            if getattr(msg, "role", "") != "user":
                continue
            parts: list[str] = []
            for block in getattr(msg, "content", []) or []:
                text = getattr(block, "text", None)
                if isinstance(text, str) and text:
                    parts.append(text)
            if parts:
                return " ".join(parts)
        return ""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

from matrx_connect.context.events import InfoPayload
from matrx_utils import vcprint
from openai import AsyncOpenAI

from matrx_ai.config import (
    FinishReason,
    TextContent,
    ThinkingContent,
    TokenUsage,
    ToolCallContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
    openai_compatible_usage_counts,
    serialize_provider_usage,
)
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.providers.outbound_capture import (
    make_capture_http_client,
    stamp_call_meta,
)
from matrx_ai.providers.reasoning import (
    emit_complete_reasoning_block,
    openai_compatible_reasoning_text,
)
from matrx_ai.providers.snapshot import capture_request_payload

from .translator import GenericOpenAITranslator

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

DEBUG_OVERRIDE = False


class GenericOpenAIChat:
    """
    Generic OpenAI-compatible endpoint implementation.

    Works with any provider that exposes an OpenAI-compatible chat completions API:
    - HuggingFace Inference Endpoints (TGI, llama.cpp)
    - vLLM
    - LocalAI
    - Ollama
    - Any other OpenAI-compatible server

    Usage:
        client = GenericOpenAIChat(
            base_url="https://your-endpoint.huggingface.cloud",
            api_key_env="HUGGING_FACE_TOKEN_ID",
            provider_name="huggingface",
        )
    """

    client: AsyncOpenAI
    endpoint_name: str
    provider_name: str
    debug: bool

    def __init__(
        self,
        base_url: str,
        api_key_env: str = "HUGGING_FACE_TOKEN_ID",
        provider_name: str = "generic_openai",
        api_key: str | None = None,
        debug: bool = False,
    ):
        # An EXPLICIT api_key pins the client (local llama-server passes
        # "none"); otherwise the named env var resolves through the host key
        # seam and the client re-keys when the host rotates the token.
        self._base_url = base_url.rstrip("/") + "/v1"
        self._explicit_api_key = api_key
        self._api_key_env = api_key_env
        self._client: AsyncOpenAI | None = None
        self._client_key: str | None = None
        self._client_pinned = False
        self.provider_name = provider_name
        self.endpoint_name = f"[{provider_name.upper()} CHAT]"
        self.translator = GenericOpenAITranslator(debug=debug)
        self.debug = debug

        if DEBUG_OVERRIDE:
            self.debug = True

    @property
    def client(self) -> AsyncOpenAI:
        if self._client_pinned:
            return self._client  # type: ignore[return-value]
        from matrx_ai.providers.keys import resolve_api_key

        resolved = (
            self._explicit_api_key
            if self._explicit_api_key is not None
            else (resolve_api_key(self._api_key_env) or "")
        )
        if self._client is None or self._client_key != resolved:
            # HuggingFace TGI / llama.cpp expects the Bearer token as the API key
            self._client = AsyncOpenAI(
                api_key=resolved,
                base_url=self._base_url,
                http_client=make_capture_http_client(),
            )
            self._client_key = resolved
        return self._client

    @client.setter
    def client(self, value: AsyncOpenAI) -> None:
        # Test/host override — pin the injected client and disable re-keying.
        self._client = value
        self._client_pinned = True

    def to_provider_config(
        self, config: UnifiedConfig, profile: ResolvedCallProfile
    ) -> dict[str, Any]:
        return self.translator.build_request(config, profile)

    def to_unified_response(
        self, response: Any, matrx_model_name: str = ""
    ) -> UnifiedResponse:
        return self.translator.from_generic_openai(
            response,
            self.provider_name,
            matrx_model_name=matrx_model_name,
        )

    async def execute(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        debug: bool = False,
    ) -> UnifiedResponse:
        from matrx_ai.context.app_context import get_app_context

        emitter = get_app_context().emitter
        self.debug = debug
        if DEBUG_OVERRIDE:
            self.debug = True
        self.translator.debug = debug

        config_data = self.to_provider_config(unified_config, profile)
        matrx_model_name = unified_config.matrx_model_name or profile.model_name
        provider_model_name = unified_config.model
        capture_request_payload(
            config_data,
            provider=self.provider_name,
            wire_format=profile.wire_format,
            debug=debug,
        )
        stamp_call_meta(
            provider=self.provider_name,
            model=matrx_model_name,
            is_streaming=bool(config_data.get("stream", False)),
        )

        vcprint(config_data, f"{self.endpoint_name} Config Data", color="blue", verbose=debug)

        try:
            if config_data.get("stream", False):
                return await self._execute_streaming(
                    config_data, emitter, matrx_model_name, provider_model_name
                )
            else:
                return await self._execute_non_streaming(
                    config_data, emitter, matrx_model_name
                )

        except Exception as e:
            from matrx_ai.providers.errors import classify_provider_error

            error_info = classify_provider_error(self.provider_name, e)

            e.error_info = error_info
            raise

    async def _execute_non_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        vcprint(f"{self.endpoint_name} Starting API call (non-streaming)...", color="cyan")

        response = await self.client.chat.completions.create(**config_data)

        vcprint(f"{self.endpoint_name} API call completed, processing response...", color="cyan")
        vcprint(response, f"{self.endpoint_name} Response", color="green", verbose=self.debug)

        converted_response = self.to_unified_response(response, matrx_model_name)
        vcprint(
            f"{self.endpoint_name} Conversion complete. {len(converted_response.messages)} messages",
            color="cyan",
        )

        # Citations (Perplexity-style / annotation dialects) are captured by the
        # translator onto the text blocks — emit the typed events at settle.
        from matrx_ai.providers.citation_emit import emit_citations_from_response

        await emit_citations_from_response(
            converted_response, emitter, self.provider_name.upper()
        )

        for message in converted_response.messages:
            for content in message.content:
                if isinstance(content, ThinkingContent):
                    await emit_complete_reasoning_block(emitter, content.text)
                elif isinstance(content, TextContent):
                    await emitter.send_chunk(content.text)
                elif isinstance(content, ToolCallContent):
                    await emitter.send_info(InfoPayload(
                        code="tool_processing",
                        system_message=f"Executing {content.name}",
                        user_message=f"Using tool {content.name}",
                        metadata={"tool_call": content.name},
                    ))

        vcprint(f"{self.endpoint_name} Non-streaming execution completed successfully", color="green")
        return converted_response

    async def _execute_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        matrx_model_name: str,
        provider_model_name: str,
    ) -> UnifiedResponse:
        vcprint(f"{self.endpoint_name} Starting API call (streaming)...", color="cyan")

        stream = await self.client.chat.completions.create(**config_data)

        vcprint(f"{self.endpoint_name} Stream connection established, processing chunks...", color="cyan")

        accumulated_content = ""
        accumulated_reasoning = ""
        accumulated_tool_calls: list[dict[str, str]] = []
        # Perplexity-style endpoints repeat the full top-level `citations` list
        # on chunks (last seen wins); annotation dialects arrive on deltas.
        last_top_level_citations: Any = None
        accumulated_annotations: list[Any] = []
        usage_data = None
        finish_reason = None
        response_id = None
        in_think_block = False
        chunks_received = 0
        chunks_with_choices = 0
        chunk_usage_seen = False
        choice_usage_seen = False
        terminal_choice_shape: dict[str, Any] | None = None

        from matrx_ai.providers.errors import openai_stream_usage, stream_with_billed_usage

        async for chunk in stream_with_billed_usage(
            stream, model=matrx_model_name, api=self.provider_name
        ):
            chunks_received += 1
            response_id = getattr(chunk, "id", None) or response_id

            chunk_usage = getattr(chunk, "usage", None)
            if chunk_usage:
                chunk_usage_seen = True
            choices = getattr(chunk, "choices", None) or []
            for stream_choice in choices:
                if getattr(stream_choice, "usage", None):
                    choice_usage_seen = True
            usage_data = openai_stream_usage(chunk) or usage_data

            chunk_citations = getattr(chunk, "citations", None)
            if chunk_citations:
                last_top_level_citations = chunk_citations

            if not choices:
                continue

            chunks_with_choices += 1
            choice = choices[0]
            delta = choice.delta

            delta_annotations = getattr(delta, "annotations", None)
            if delta_annotations:
                accumulated_annotations.extend(delta_annotations)

            reasoning_chunk = openai_compatible_reasoning_text(delta)
            if reasoning_chunk:
                accumulated_reasoning += reasoning_chunk
                if not in_think_block:
                    await emitter.send_reasoning_state("started")
                    await emitter.send_chunk("<reasoning>")
                    in_think_block = True
                await emitter.send_chunk(reasoning_chunk)
                await asyncio.sleep(0)

            if delta.content:
                # Close reasoning block before first real content token
                if in_think_block:
                    await emitter.send_chunk("\n</reasoning>\n")
                    await emitter.send_reasoning_state("stopped")
                    in_think_block = False
                accumulated_content += delta.content
                await emitter.send_chunk(delta.content)
                await asyncio.sleep(0)

            if hasattr(delta, "tool_calls") and delta.tool_calls:
                for tc in delta.tool_calls:
                    tc_index_raw = (
                        tc.get("index") if isinstance(tc, dict) else getattr(tc, "index", None)
                    )
                    tc_index = int(tc_index_raw) if tc_index_raw is not None else None
                    if tc_index is None:
                        continue

                    tc_id = tc.get("id") if isinstance(tc, dict) else getattr(tc, "id", None)
                    tc_func = (
                        tc.get("function") if isinstance(tc, dict) else getattr(tc, "function", None)
                    )

                    while len(accumulated_tool_calls) <= tc_index:
                        accumulated_tool_calls.append({"id": "", "name": "", "arguments": ""})

                    if tc_id:
                        accumulated_tool_calls[tc_index]["id"] = tc_id

                    if tc_func:
                        func_name = (
                            tc_func.get("name") if isinstance(tc_func, dict) else getattr(tc_func, "name", None)
                        )
                        func_args = (
                            tc_func.get("arguments") if isinstance(tc_func, dict) else getattr(tc_func, "arguments", None)
                        )
                        if func_name:
                            accumulated_tool_calls[tc_index]["name"] = func_name
                        if func_args:
                            if isinstance(func_args, dict):
                                accumulated_tool_calls[tc_index]["arguments"] = json.dumps(func_args)
                            else:
                                accumulated_tool_calls[tc_index]["arguments"] += func_args

            if choice.finish_reason:
                finish_reason = choice.finish_reason
                terminal_choice_shape = {
                    "choice_fields": sorted(
                        key for key in vars(choice) if not key.startswith("_")
                    ) if hasattr(choice, "__dict__") else [],
                    "finish_reason": finish_reason,
                    "has_choice_usage": bool(getattr(choice, "usage", None)),
                }

        # Close unclosed reasoning block (e.g. hit max_tokens mid-reasoning)
        if in_think_block:
            await emitter.send_chunk("\n</reasoning>")
            await emitter.send_reasoning_state("stopped")

        content = []

        if accumulated_reasoning:
            content.append(
                ThinkingContent(
                    text=accumulated_reasoning,
                    provider="moonshot" if self.provider_name == "moonshot" else "generic_openai",
                )
            )
        if accumulated_content:
            content.append(TextContent(text=accumulated_content))

        for tc_data in accumulated_tool_calls:
            if tc_data["name"]:
                arguments = json.loads(tc_data["arguments"]) if tc_data["arguments"] else {}
                content.append(
                    ToolCallContent(id=tc_data["id"], name=tc_data["name"], arguments=arguments)
                )

        # Settle-time citation capture — mirror the non-streaming translator:
        # normalize the terminal top-level `citations` / accumulated delta
        # `annotations` onto the text block's metadata["citations"]. Guarded:
        # malformed citations must never abort the answer.
        if last_top_level_citations or accumulated_annotations:
            try:
                from matrx_ai.config.citations import normalize_openai_compatible_citations

                compatible_citations = normalize_openai_compatible_citations(
                    {"citations": last_top_level_citations},
                    {"annotations": accumulated_annotations},
                    accumulated_content,
                )
                if compatible_citations:
                    normalized_dicts = [
                        c.model_dump(exclude_none=True) for c in compatible_citations
                    ]
                    for block in content:
                        if isinstance(block, TextContent):
                            block.metadata.setdefault("citations", normalized_dicts)
            except Exception as citation_exc:
                vcprint(
                    f"{self.endpoint_name} citation capture failed — skipping "
                    f"citations only (answer unaffected): {citation_exc}",
                    color="red",
                )

        messages = []
        if content:
            messages.append(UnifiedMessage(role="assistant", content=content))

        token_usage = None
        if usage_data:
            input_tokens, output_tokens, cached_input_tokens = openai_compatible_usage_counts(
                usage_data
            )
            token_usage = TokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cached_input_tokens=cached_input_tokens,
                matrx_model_name=matrx_model_name,
                provider_model_name=provider_model_name,
                api=self.provider_name,
                response_id=response_id or "",
                raw_usage=serialize_provider_usage(usage_data),
            )
        else:
            # A successful answer without terminal usage must remain a visible
            # billing-data fault, not quietly become a zero-token/cost record.
            # Log only structural observations: no prompt, completion text,
            # tool arguments, auth, or raw provider payload is exposed.
            vcprint(
                {
                    "provider": self.provider_name,
                    "model": matrx_model_name,
                    "provider_model": provider_model_name,
                    "response_id": response_id,
                    "chunks_received": chunks_received,
                    "chunks_with_choices": chunks_with_choices,
                    "chunk_usage_seen": chunk_usage_seen,
                    "choice_usage_seen": choice_usage_seen,
                    "requested_stream_usage": bool(
                        (config_data.get("stream_options") or {}).get("include_usage")
                    ),
                    "terminal_choice": terminal_choice_shape,
                },
                f"{self.endpoint_name} STREAM USAGE MISSING — cost reconciliation required",
                color="red",
            )

        unified_finish_reason = None
        if finish_reason == "stop":
            unified_finish_reason = FinishReason.STOP
        elif finish_reason == "length":
            unified_finish_reason = FinishReason.MAX_TOKENS
        elif finish_reason == "tool_calls":
            unified_finish_reason = FinishReason.TOOL_CALLS
        elif finish_reason == "content_filter":
            unified_finish_reason = FinishReason.CONTENT_FILTER

        vcprint(f"{self.endpoint_name} Streaming execution completed successfully", color="green")

        unified_response = UnifiedResponse(
            messages=messages,
            usage=token_usage,
            finish_reason=unified_finish_reason,
            stop_reason=finish_reason,
        )

        # Emit the typed citation events at settle (earliest possible point —
        # OpenAI-compatible endpoints deliver citations only on/with the
        # terminal chunks).
        from matrx_ai.providers.citation_emit import emit_citations_from_response

        await emit_citations_from_response(
            unified_response, emitter, self.provider_name.upper()
        )

        return unified_response

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

import anthropic as anthropic_sdk
from anthropic import AsyncAnthropic
from matrx_connect.chat_timing import chat_timing_mark
from matrx_connect.context.events import CitationPayload, InfoPayload, WarningPayload
from matrx_utils import vcprint

from matrx_ai.config import (
    UnifiedConfig,
    UnifiedResponse,
)
from matrx_ai.config.citations import normalize_anthropic_citation
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.providers.keys import keyed_provider_client
from matrx_ai.providers.outbound_capture import (
    make_capture_http_client,
    stamp_call_meta,
)
from matrx_ai.providers.reasoning_stream_state import (
    reasoning_state_for,
    reset_reasoning_state,
)
from matrx_ai.providers.sdk_drift import route_undeclared_params
from matrx_ai.providers.snapshot import capture_request_payload

from .translator import AnthropicTranslator

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

DEBUG_OVERRIDE = False

# The Anthropic SDK rejects non-streaming requests when the expected
# completion time exceeds 10 minutes.  The formula is:
#     expected_time = 3600 * max_tokens / 128_000
#     if expected_time > 600: raise ValueError
# Solving: max_tokens > 128_000 * 600 / 3600 = 21_333.
#
# This threshold applies to ALL Anthropic models at the provider level.
# Some models have even lower per-model ceilings in the SDK, but we use
# the general ceiling here so we never hardcode model names — if the SDK
# still rejects it (per-model override), the error classifier in errors.py
# catches it as non-retryable with a clear user message.
_ANTHROPIC_NONSTREAMING_MAX_TOKENS = 21_333
_MAX_HOSTED_TOOL_CONTINUATIONS = 4


class AnthropicChat:
    """Anthropic Messages API-specific endpoint implementation."""

    endpoint_name: str
    debug: bool

    # Memoized on the RESOLVED KEY VALUE — a host-side key rotation builds a
    # fresh SDK client on the next request (no process restart).
    client = keyed_provider_client(
        "ANTHROPIC_API_KEY",
        factory=lambda api_key: AsyncAnthropic(
            api_key=api_key,
            http_client=make_capture_http_client(sdk=anthropic_sdk),
        ),
    )

    def __init__(self, debug: bool = False):
        self.endpoint_name = "[ANTHROPIC CHAT]"
        self.translator = AnthropicTranslator(debug=debug)
        self.debug = debug
        # 🚨 NO PER-STREAM STATE ON `self`. This object is memoized
        # process-wide (unified_client._provider_client_cache), so it parses
        # every concurrent turn at once. The <reasoning> wrapper's open/closed
        # bookkeeping — and the content-less "reasoning started/stopped"
        # lifecycle signal — live per STREAM in
        # providers/reasoning_stream_state.py, keyed on that stream's emitter.
        # Holding them here made two simultaneous turns share one flag: one
        # turn's thinking leaked as visible prose, the other's answer rendered
        # inside the collapsed "Thought process" block (2026-09-12).

        if DEBUG_OVERRIDE:
            self.debug = True

    def to_provider_config(
        self, config: UnifiedConfig, profile: ResolvedCallProfile
    ) -> dict[str, Any]:
        return self.translator.build_request(config, profile)

    def to_unified_response(self, response: Any, matrx_model_name: str = "") -> UnifiedResponse:
        if hasattr(response, "model_dump"):
            response_dict = response.model_dump()
        else:
            # If for some reason it's not a Pydantic model, debug it
            vcprint(
                f"Unexpected response type: {type(response)}",
                "Warning: Response is not a Pydantic model",
                color="yellow",
            )
            vcprint(response, "Full Response Object", color="yellow")
            # Try to convert to dict as fallback
            if isinstance(response, dict):
                response_dict = response
            else:
                raise TypeError(
                    f"Unexpected response type: {type(response)}. Expected Pydantic model with model_dump()"
                )

        # Ensure model is set
        if not response_dict.get("model"):
            response_dict["model"] = matrx_model_name

        return self.translator.from_anthropic(response_dict, matrx_model_name)

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
        matrx_model_name = unified_config.model
        # Build provider-specific config
        config_data = self.to_provider_config(unified_config, profile)
        capture_request_payload(
            config_data,
            provider="anthropic",
            wire_format=profile.wire_format,
            debug=debug,
        )

        vcprint(config_data, "Anthropic API Config Data", color="blue", verbose=debug)

        # Auto-enable streaming when max_tokens exceeds the Anthropic SDK's
        # non-streaming ceiling (21,333 tokens for all models).  The SDK raises
        # a client-side ValueError before the request is sent — there is nothing
        # to retry, so we must prevent it proactively at the provider level.
        stream_requested = unified_config.stream
        max_tokens_for_check = config_data.get("max_tokens", 0)

        if not stream_requested and max_tokens_for_check > _ANTHROPIC_NONSTREAMING_MAX_TOKENS:
            model_name = config_data.get("model", "unknown")

            vcprint(
                f"⚠️  Anthropic auto-streaming override:\n"
                f"   model          = {model_name}\n"
                f"   max_tokens     = {max_tokens_for_check}\n"
                f"   provider ceiling (no-stream) = {_ANTHROPIC_NONSTREAMING_MAX_TOKENS}\n"
                f"   The SDK would raise ValueError because {max_tokens_for_check} > {_ANTHROPIC_NONSTREAMING_MAX_TOKENS}.\n"
                f"   Auto-enabling streaming to prevent the error.",
                color="yellow",
            )
            await emitter.send_warning(
                WarningPayload(
                    code="auto_streaming_override",
                    system_message=(
                        f"Anthropic non-streaming ceiling exceeded: max_tokens={max_tokens_for_check} "
                        f"but the provider limit is {_ANTHROPIC_NONSTREAMING_MAX_TOKENS} tokens without streaming. "
                        f"Streaming was auto-enabled. The frontend should either enable streaming by default "
                        f"or cap max_tokens to {_ANTHROPIC_NONSTREAMING_MAX_TOKENS} when streaming is disabled."
                    ),
                    user_message=(
                        f"Your token limit ({max_tokens_for_check:,}) exceeds the maximum allowed "
                        f"without streaming ({_ANTHROPIC_NONSTREAMING_MAX_TOKENS:,} tokens). "
                        f"Streaming was enabled automatically to complete your request."
                    ),
                    level="high",
                    recoverable=True,
                    metadata={
                        "model": model_name,
                        "max_tokens_requested": max_tokens_for_check,
                        "non_streaming_ceiling": _ANTHROPIC_NONSTREAMING_MAX_TOKENS,
                        "action_taken": "auto_enabled_streaming",
                        "fix_suggestion": (
                            f"Either set stream=true in request, or ensure max_tokens <= "
                            f"{_ANTHROPIC_NONSTREAMING_MAX_TOKENS} when stream=false for Anthropic models."
                        ),
                    },
                )
            )

            from matrx_ai.ops.issue_capture import capture_issue

            await capture_issue(
                "anthropic.streaming_required",
                error_type="streaming_required",
                provider="anthropic",
                model=model_name,
                is_retryable=False,
                was_recovered=True,
                detail={
                    "max_tokens_requested": max_tokens_for_check,
                    "non_streaming_ceiling": _ANTHROPIC_NONSTREAMING_MAX_TOKENS,
                    "action": "auto_enabled_streaming",
                },
            )
            stream_requested = True

        async def _send(payload: dict[str, Any]) -> UnifiedResponse:
            stamp_call_meta(
                provider="anthropic",
                model=matrx_model_name,
                is_streaming=bool(stream_requested),
            )
            if stream_requested:
                return await self._execute_streaming(payload, emitter, matrx_model_name)
            return await self._execute_non_streaming(payload, emitter, matrx_model_name)

        try:
            return await _send(config_data)
        except Exception as e:
            from matrx_ai.schema.grammar_budget import is_grammar_too_large

            if is_grammar_too_large(e):
                recovered = await self._retry_over_grammar_budget(
                    config_data,
                    _send,
                    emitter,
                    matrx_model_name,
                    e,
                    response_format=unified_config.response_format,
                )
                if recovered is not None:
                    return recovered

            # Import here to avoid circular dependency
            from matrx_ai.providers.errors import classify_anthropic_error

            error_info = classify_anthropic_error(e)
            e.error_info = error_info
            raise

    async def _retry_over_grammar_budget(
        self,
        config_data: dict[str, Any],
        send: Any,
        emitter: Emitter,
        matrx_model_name: str,
        original: Exception,
        response_format: Any = None,
    ) -> UnifiedResponse | None:
        """Keep the request's contract ENFORCED if at all possible; shed only what
        the budget forces, and record every rung that was needed.

        Anthropic compiles the bound output schema together with the request's
        tools under one budget (measured 2026-09-27: roughly 70 properties, 16
        union parameters; a single tool spends part of it). The translator already
        sends the most faithful schema that fits the documented limits. When the
        provider still refuses, the rungs are, in order:

        1. **Narrow the schema** — every nullable union collapsed to its
           non-null branch. Answers remain valid under the declared contract and
           the provider still ENFORCES it; tools are untouched. This alone brought
           the Study Pack flashcards node (with its tool) and the agent factory's
           envelope under the budget.
        2. **Shed the tools, keep the (narrowed) schema.** On a turn bound to a
           kind the answer IS the deliverable; measured, 4 of 200 such turns
           called a tool. The shed is visible to the user and recorded.
        3. **Drop provider enforcement, RESTORE the tools.** The schema is above
           what Anthropic can compile at all (the resale report: 115 properties).
           The schema is appended to the request's system channel as a JSON text
           contract and the answer is CHECKED against the declared schema when the
           call ends — both halves of that sentence were false until 2026-09-27:
           this rung sent `with_format(config_data, None)` with no schema text
           anywhere, and the package contained no answer validation at all. The
           tools come back — until 2026-09-27 this rung ran on the tool-less
           payload of rung 2, so an 18-tool agent silently lost every tool AND its
           contract.

        Every rung that SERVES the turn records a finding naming the agent, the
        schema and what was given up (``structured_output_findings``) — the
        retry is kept (a user still gets an answer) and it is no longer quiet.
        Returns ``None`` when nothing could be shed, so the caller raises the
        provider's original error rather than inventing a success.
        """
        from matrx_ai.providers.structured_output_findings import (
            ENFORCEMENT_DROPPED,
            NARROWED,
            TOOLS_SHED,
            record_structured_output_finding,
            response_format_identity,
        )
        from matrx_ai.schema.grammar_budget import is_grammar_too_large
        from matrx_ai.schema.rules import (
            collapse_nullable_unions,
            count_union_params,
            dedupe_identical_subtrees,
            structured_output_size,
        )

        tools = config_data.get("tools") or []
        output_config = config_data.get("output_config") or {}
        fmt = output_config.get("format") if isinstance(output_config, dict) else None
        schema = fmt.get("schema") if isinstance(fmt, dict) else None
        if not tools and not fmt:
            return None  # nothing to shed — let the provider's error stand

        def with_format(base: dict[str, Any], new_format: dict[str, Any] | None) -> dict[str, Any]:
            out = dict(base)
            oc = dict(out.get("output_config") or {})
            if new_format is None:
                oc.pop("format", None)
            else:
                oc["format"] = new_format
            if oc:
                out["output_config"] = oc
            else:
                out.pop("output_config", None)
            return out

        rungs: list[tuple[str, str, dict[str, Any], list[str]]] = []
        if isinstance(schema, dict) and count_union_params(schema):
            narrowed_notes: list[str] = []
            narrowed_schema = dedupe_identical_subtrees(
                collapse_nullable_unions(
                    schema, keep=0, notes=narrowed_notes, reason="compiled grammar over budget"
                )
            )
            fmt = {**fmt, "schema": narrowed_schema}
            rungs.append(
                (
                    NARROWED,
                    "every nullable field narrowed to non-null (schema still enforced)",
                    with_format(config_data, fmt),
                    narrowed_notes,
                )
            )
        if tools and fmt:
            without_tools = {k: v for k, v in with_format(config_data, fmt).items() if k != "tools"}
            without_tools.pop("tool_choice", None)
            rungs.append(
                (
                    TOOLS_SHED,
                    f"dropped all {len(tools)} tool schemas (schema still enforced)",
                    without_tools,
                    [str(t.get("name")) for t in tools if isinstance(t, dict)],
                )
            )
        if fmt:
            # THE PROMPT-GUIDED HALF, which until 2026-09-27 did not exist: this
            # rung removed `output_config.format` and sent NOTHING in its place,
            # while the finding it wrote said the answer was "prompt-guided and
            # validated after the fact". Google does the opposite for the same
            # situation, and this now uses the same words
            # (`schema.answer_contract.json_text_contract`). The CHECK is the
            # other half, in `UnifiedAIClient._dispatch_with_billing_net`.
            from matrx_ai.schema.answer_contract import (
                append_json_text_contract_to_system,
                mark_enforcement_dropped,
            )

            prompt_guided = with_format(config_data, None)
            guided = isinstance(schema, dict)
            if guided:
                append_json_text_contract_to_system(prompt_guided, schema)
                mark_enforcement_dropped(
                    "Anthropic refused the compiled grammar at every smaller shape; "
                    "output_config.format dropped and the schema sent as a prompt contract"
                )
            rungs.append(
                (
                    ENFORCEMENT_DROPPED,
                    "dropped output_config.format — the schema now travels as a JSON text "
                    "contract in the prompt and the answer is checked against the declared "
                    f"contract afterwards, NOT provider-enforced{f'; all {len(tools)} tools kept' if tools else ''}"
                    if guided
                    else "dropped output_config.format — no schema was available to guide "
                    "the answer with",
                    prompt_guided,
                    [],
                )
            )

        identity = {
            **response_format_identity(response_format),
            "tool_count": len(tools),
            "tool_names": [t.get("name") for t in tools if isinstance(t, dict)][:30],
            "provider_error": str(original)[:300],
            # How far over the line the shape is — the measured ceiling is ~70
            # properties and 16 union parameters per request.
            "schema_size": structured_output_size(schema) if isinstance(schema, dict) else None,
        }
        last_error: Exception = original
        for key, detail, payload, gave_up in rungs:
            vcprint(
                f"⚠️  ANTHROPIC ADJUSTMENT: compiled grammar over budget — retrying with "
                f"{detail}. The request was NOT sent as configured.",
                color="yellow",
            )
            try:
                response = await send(payload)
            except Exception as exc:  # noqa: BLE001 — try the next rung
                last_error = exc
                if is_grammar_too_large(exc):
                    continue
                raise
            await record_structured_output_finding(
                key,
                provider="anthropic",
                model=matrx_model_name,
                detail={**identity, "action": detail, "gave_up": gave_up[:40]},
                was_recovered=True,
            )
            if key != NARROWED:
                await emitter.send_warning(
                    WarningPayload(
                        code="anthropic_grammar_over_budget",
                        system_message=(
                            "Anthropic rejected the request because the compiled grammar "
                            f"(bound output schema + {len(tools)} tool schemas) exceeded its "
                            f"budget. Recovered by: {detail}. Recorded as a "
                            f"'{key}' finding naming this agent and schema — fix the schema "
                            "(fewer properties / union fields) so it fits."
                        ),
                        user_message=(
                            "This step needed a simpler setup to run, so some optional "
                            "abilities were switched off for it. Your result is here."
                        ),
                        level="high",
                        recoverable=True,
                        metadata={"action": key, "model": matrx_model_name},
                    )
                )
            return response

        vcprint(
            "❌ ANTHROPIC: compiled grammar still over budget after narrowing the schema, "
            "shedding every tool and dropping the structured-output binding.",
            color="red",
        )
        if last_error is not original:
            raise last_error
        return None

    async def _execute_non_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        """Execute non-streaming Anthropic request"""

        # Remove stream parameter if present
        config_data_copy = config_data.copy()
        config_data_copy.pop("stream", None)

        accumulated_usage = None
        for continuation in range(_MAX_HOSTED_TOOL_CONTINUATIONS + 1):
            chat_timing_mark("provider_sdk_call", "anthropic messages.create")
            response = await self.client.messages.create(
                **route_undeclared_params(
                    self.client.messages.create, config_data_copy, provider="anthropic"
                )
            )
            chat_timing_mark("provider_sdk_complete", "anthropic messages.create complete")
            vcprint(response, "Anthropic Response", color="green", verbose=self.debug)

            if hasattr(response, "content"):
                for block in response.content:
                    await self._handle_content_block(block, emitter)

            converted_response = self.to_unified_response(response, matrx_model_name)
            accumulated_usage = (
                converted_response.usage
                if accumulated_usage is None
                else accumulated_usage + converted_response.usage
            )
            if getattr(response, "stop_reason", None) != "pause_turn":
                converted_response.usage = accumulated_usage
                return converted_response
            if continuation >= _MAX_HOSTED_TOOL_CONTINUATIONS:
                exc = RuntimeError(
                    "Anthropic hosted tool remained paused after "
                    f"{_MAX_HOSTED_TOOL_CONTINUATIONS} continuations."
                )
                from matrx_ai.providers.errors import attach_billed_usage

                attach_billed_usage(exc, accumulated_usage)
                raise exc
            messages = list(config_data_copy.get("messages") or [])
            messages.append({"role": "assistant", "content": response.content})
            config_data_copy = {**config_data_copy, "messages": messages}

        raise AssertionError("unreachable")

    async def _execute_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        """Execute streaming Anthropic request"""

        # Reset THIS stream's reasoning state. Scoped to this emitter: the
        # instance is shared process-wide, so a reset on `self` would clear a
        # CONCURRENT turn's open wrapper and strand its close.
        reset_reasoning_state(emitter)

        attempt_config = dict(config_data)
        accumulated_usage = None
        for continuation in range(_MAX_HOSTED_TOOL_CONTINUATIONS + 1):
            chat_timing_mark("provider_sdk_call", "anthropic messages.stream")
            # Anthropic's async helper recursively transforms the complete
            # request body before it returns its async context manager. Large
            # resumed conversations make that synchronous setup expensive, so
            # construct the manager off-loop; its actual async request and
            # stream consumption still run on this loop.
            stream_manager = await asyncio.to_thread(
                self.client.messages.stream,
                **route_undeclared_params(
                    self.client.messages.stream, attempt_config, provider="anthropic"
                ),
            )
            async with stream_manager as stream:
                try:
                    async for event in stream:
                        await self._handle_event(event, emitter)
                    final_message = await stream.get_final_message()
                except BaseException as exc:
                    # A provider bills us the instant the call starts. Anthropic
                    # accumulates usage incrementally on the message snapshot.
                    from matrx_ai.providers.errors import attach_billed_usage

                    attach_billed_usage(exc, accumulated_usage)
                    self._attach_billed_usage_from_stream(exc, stream, matrx_model_name)
                    raise

            chat_timing_mark("provider_sdk_complete", "anthropic messages.stream complete")
            vcprint(final_message, "Anthropic Final Message", color="green", verbose=self.debug)
            converted_response = self.to_unified_response(final_message, matrx_model_name)
            accumulated_usage = (
                converted_response.usage
                if accumulated_usage is None
                else accumulated_usage + converted_response.usage
            )

            if getattr(final_message, "stop_reason", None) != "pause_turn":
                converted_response.usage = accumulated_usage
                return converted_response
            if continuation >= _MAX_HOSTED_TOOL_CONTINUATIONS:
                exc = RuntimeError(
                    "Anthropic hosted tool remained paused after "
                    f"{_MAX_HOSTED_TOOL_CONTINUATIONS} continuations."
                )
                from matrx_ai.providers.errors import attach_billed_usage

                attach_billed_usage(exc, accumulated_usage)
                raise exc

            # Hosted tools such as web_search can pause a long-running turn.
            # Continue with the provider's entire assistant block unchanged;
            # server_tool_use/web_search_tool_result blocks are provider state,
            # never local function calls.
            prior_messages = list(attempt_config.get("messages") or [])
            prior_messages.append(
                {"role": "assistant", "content": getattr(final_message, "content", [])}
            )
            attempt_config = {**attempt_config, "messages": prior_messages}

        raise AssertionError("unreachable")

    def _attach_billed_usage_from_stream(
        self,
        exc: BaseException,
        stream: Any,
        matrx_model_name: str,
    ) -> None:
        """Best-effort: recover billed usage from the Anthropic stream's
        accumulated message snapshot and stamp it onto a failing/cancelling
        exception. Never raises, never overwrites an already-attached usage."""
        # LAYER 2: the mark means "an adapter LOOKED", which is true even when
        # there is nothing to attach — it must precede every early return.
        from matrx_ai.providers.errors import mark_billing_checked

        mark_billing_checked(exc)
        try:
            try:
                snapshot = getattr(stream, "current_message_snapshot", None)
            except AssertionError:
                # Anthropic's stream manager asserts when a pre-response failure
                # (for example HTTP 529) leaves its message snapshot uninitialized.
                # That means there is no provider usage object to inspect, not
                # that billing capture itself failed.
                return
            usage = getattr(snapshot, "usage", None) if snapshot is not None else None
            if usage is None:
                return
            from matrx_ai.config import TokenUsage
            from matrx_ai.providers.errors import accumulate_billed_usage

            token_usage = TokenUsage.from_anthropic(
                usage,
                matrx_model_name=matrx_model_name,
                response_id=getattr(snapshot, "id", "") or "",
            )
            accumulate_billed_usage(exc, token_usage)
        except Exception as err:
            from matrx_ai.providers.errors import report_billed_usage_capture_failure

            report_billed_usage_capture_failure("anthropic", err)

    async def _handle_event(self, event: Any, emitter: Emitter):
        """
        Handle individual streaming event.

        Note: Using getattr for streaming events is acceptable since event structures vary.
        If you need to see the actual event structure, set DEBUG_OVERRIDE = True at the top
        of this file to print raw events.
        """
        await asyncio.sleep(0)

        # Debug: Print raw event structure to understand what we're dealing with
        if DEBUG_OVERRIDE and self.debug:
            vcprint(
                event,
                f"Raw Event: {event.type if hasattr(event, 'type') else 'unknown'}",
                color="cyan",
            )

        event_type = getattr(event, "type", None)

        if event_type == "content_block_delta":
            # Text, thinking, or input delta
            delta = getattr(event, "delta", None)
            if delta:
                delta_type = getattr(delta, "type", None)

                if delta_type == "text_delta":
                    text = getattr(delta, "text", "")
                    if text:
                        await emitter.send_chunk(text)
                        await asyncio.sleep(0)

                elif delta_type == "thinking_delta":
                    # Thinking content being streamed. Open the <reasoning>
                    # wrapper lazily on the FIRST delta that carries text (same
                    # pattern as OpenAI's reasoning_summary_text.delta handler),
                    # so the UI gets a real "model is thinking" signal exactly
                    # when thinking text exists — and never an empty wrapper.
                    thinking = getattr(delta, "thinking", "")
                    if thinking:
                        reasoning_state = reasoning_state_for(emitter)
                        if not reasoning_state.open:
                            await emitter.send_chunk("\n<reasoning>\n")
                            reasoning_state.open = True
                        await emitter.send_chunk(thinking)
                        await asyncio.sleep(0)

                elif delta_type == "signature_delta":
                    # Encrypted thinking signature (multi-turn continuity). Not
                    # user-visible and not text — the SDK folds it into the
                    # final message snapshot, which from_anthropic() reads for
                    # persistence. Nothing to stream; explicitly a no-op so the
                    # branch is documented rather than silently falling through.
                    pass

                elif delta_type == "input_json_delta":
                    # Tool input being streamed (usually not needed for display)
                    pass

                elif delta_type == "citations_delta":
                    # Citation attaching to the current text block (documents /
                    # search results with citations enabled). Streamed LIVE as a
                    # typed `citation` event (normalized to the canonical
                    # cross-provider shape); the SDK ALSO accumulates each
                    # citation onto the block in the final message snapshot,
                    # which from_anthropic() folds into
                    # TextContent.metadata["citations"] for persistence.
                    # NOTE for the FE: a cited response arrives as MANY text
                    # blocks (one per cited span, mid-sentence); consecutive
                    # text blocks concatenate directly, never with separators.
                    citation = getattr(delta, "citation", None)
                    if citation is not None:
                        # A malformed citation must never abort the in-flight
                        # answer — it is a side-channel to the text stream. The
                        # final-message snapshot still carries the raw citation,
                        # so nothing is lost by skipping the live event.
                        try:
                            raw_citation = (
                                citation.model_dump()
                                if hasattr(citation, "model_dump")
                                else dict(citation)
                            )
                            normalized = normalize_anthropic_citation(raw_citation)
                            await emitter.send_citation(
                                CitationPayload(
                                    block_index=getattr(event, "index", None),
                                    citation=normalized.model_dump(exclude_none=True),
                                )
                            )
                        except Exception as citation_exc:
                            vcprint(
                                f"[ANTHROPIC CITATIONS] Failed to normalize/emit a "
                                f"citations_delta — skipping this citation only "
                                f"(answer stream unaffected): {citation_exc}",
                                color="red",
                            )
                        await asyncio.sleep(0)

        elif event_type == "content_block_start":
            # New content block starting
            content_block = getattr(event, "content_block", None)
            if content_block:
                block_type = getattr(content_block, "type", None)

                if block_type == "tool_use":
                    name = getattr(content_block, "name", "")
                    await emitter.send_info(
                        InfoPayload(
                            code="tool_processing",
                            system_message=f"Executing {name}",
                            user_message=f"Using tool {name}",
                            metadata={"tool_call": name},
                        )
                    )

                elif block_type == "thinking":
                    # Thinking block started. Do NOT open the <reasoning>
                    # wrapper here — under display="omitted" (or a turn the
                    # model skipped thinking on) this block produces no
                    # thinking_delta, so eagerly opening would emit an empty
                    # <reasoning></reasoning> and lie to the UI that the model
                    # was thinking. The wrapper is opened lazily on the first
                    # thinking_delta that carries text instead.
                    #
                    # BUT the content-LESS lifecycle signal fires here: Anthropic
                    # sends this thinking content_block_start even when the
                    # thinking text is omitted, so it is the one reliable "the
                    # model is thinking now" marker. Emit it so the UI can leave
                    # the silent heartbeat gap and show a thinking state.
                    reasoning_state_for(emitter).signaled = True
                    await emitter.send_reasoning_state("started")

        elif event_type == "content_block_stop":
            # Content block finished. Close the <reasoning> wrapper iff it was
            # actually opened by a thinking_delta. Keyed off our own state (not
            # the block type, which the stop event may not carry) so the close
            # always pairs with a real open and we never emit a stray close.
            reasoning_state = reasoning_state_for(emitter)
            if reasoning_state.open:
                await emitter.send_chunk("\n</reasoning>\n")
                reasoning_state.open = False
            # Close the lifecycle signal at the same block boundary. Anthropic
            # streams blocks sequentially (start N … stop N before start N+1),
            # so the first content_block_stop after a thinking start IS the
            # thinking block's stop — the same sequencing `state.open` relies
            # on. Fires whether or not any thinking text was streamed.
            if reasoning_state.signaled:
                reasoning_state.signaled = False
                await emitter.send_reasoning_state("stopped")

        elif event_type == "message_start":
            # Message started
            vcprint(
                "Anthropic Message Stream Started",
                color="cyan",
                verbose=self.debug,
            )

        elif event_type == "message_delta":
            # Message-level updates (usage, stop_reason) — always inspect stop_reason,
            # never silently swallow a truncation or refusal.
            delta = getattr(event, "delta", None)
            if delta:
                stop_reason = getattr(delta, "stop_reason", None)
                if stop_reason and stop_reason not in (
                    "end_turn",
                    "tool_use",
                    "stop_sequence",
                    "pause_turn",
                ):
                    print("\n")
                    print("=" * 70)
                    print(f"🚨  ANTHROPIC STREAM STOPPED: stop_reason = '{stop_reason}'")
                    print("=" * 70)
                    # RULE: ``message_delta`` fires AFTER content blocks have
                    # streamed to the UI. Any stop_reason surfaced here is a
                    # caveat about an already-delivered response, not a
                    # failure to deliver. Emit WARNING, not ERROR — the user
                    # already received whatever content the model produced
                    # and we already paid for those tokens.
                    # See StreamEmitter.send_error docstring for the rule.
                    if stop_reason == "max_tokens":
                        print("  The model hit the output token limit mid-stream.")
                        print("  The response is INCOMPLETE — content delivered but truncated.")
                        print("=" * 70)
                        print("\n")
                        await emitter.send_warning(
                            WarningPayload(
                                code="truncated_response",
                                system_message="Response truncated: model hit the output token limit (stop_reason=max_tokens).",
                                user_message="The response was cut short because the model reached its output limit. The answer may be incomplete.",
                                level="medium",
                                recoverable=True,
                                metadata={"stop_reason": stop_reason},
                            )
                        )
                    elif stop_reason == "refusal":
                        print("  The model refused to complete the request.")
                        print("=" * 70)
                        print("\n")
                        await emitter.send_warning(
                            WarningPayload(
                                code="model_refusal",
                                system_message="Model refused to complete the request.",
                                user_message="The model declined to respond to this request.",
                                level="high",
                                recoverable=False,
                                metadata={"stop_reason": stop_reason},
                            )
                        )
                    elif stop_reason == "model_context_window_exceeded":
                        # This is the one case where the API reports the
                        # condition before any content block — no chunks
                        # have streamed. Keep it as an ERROR because the
                        # response was never delivered.
                        print("  The input exceeded the model's context window.")
                        print("=" * 70)
                        print("\n")
                        await emitter.send_error(
                            error_type="context_window_exceeded",
                            message="Input exceeded the model's context window.",
                            user_message="The conversation is too long for this model to process.",
                        )
                    else:
                        print(
                            "  Unrecognized stop_reason — content already streamed, emitting warning."
                        )
                        print("=" * 70)
                        print("\n")
                        await emitter.send_warning(
                            WarningPayload(
                                code="unexpected_stop_reason",
                                system_message=f"Unexpected stop reason from Anthropic: '{stop_reason}'.",
                                user_message="The model stopped for an unexpected reason.",
                                level="medium",
                                recoverable=False,
                                metadata={"stop_reason": stop_reason},
                            )
                        )
                elif stop_reason and self.debug:
                    vcprint(f"Stop reason: {stop_reason}", color="cyan")

        elif event_type == "message_stop":
            # Message finished
            vcprint("Anthropic Message Stream Completed", color="green")

        elif event_type == "error":
            # Error occurred
            error = getattr(event, "error", {})
            await emitter.send_error(
                error_type="streaming_error",
                message=str(error),
                user_message="An error occurred during streaming.",
            )

        if self.debug:
            await self._debug_event(event)

    async def _handle_content_block(self, block: Any, emitter: Emitter):
        """Handle a content block from the response"""
        await asyncio.sleep(0)

        block_type = getattr(block, "type", None)

        if block_type == "text":
            # Text content
            text = getattr(block, "text", "")
            if text:
                await emitter.send_chunk(text)

        elif block_type == "tool_use":
            # Tool/function call
            name = getattr(block, "name", "")
            await emitter.send_info(
                InfoPayload(
                    code="tool_processing",
                    system_message=f"Executing {name}",
                    user_message=f"Using tool {name}",
                    metadata={"tool_call": name},
                )
            )

        elif block_type == "thinking":
            # Thinking block. Anthropic thinking blocks carry the text on
            # `.thinking` (NOT `.text` — that field is empty/absent here), so
            # reading `.text` silently dropped all non-streaming reasoning.
            # Under display="omitted" `.thinking` is empty and we correctly
            # emit nothing rather than an empty wrapper.
            thinking = getattr(block, "thinking", "")
            if thinking:
                await emitter.send_chunk(f"\n<reasoning>\n{thinking}\n</reasoning>\n")

    async def _debug_event(self, event: Any):
        """Debug logging for events - only aggregate/bigger events, not individual chunks"""
        event_type = getattr(event, "type", "unknown")

        # Only log significant events, not individual chunks
        if event_type == "content_block_start":
            content_block = getattr(event, "content_block", None)
            if content_block:
                block_type = getattr(content_block, "type", None)
                # Only log tool_use and thinking blocks
                if block_type in ("tool_use", "thinking"):
                    vcprint(f"Content Block Start. Type: {block_type}", color="blue")

        elif event_type == "content_block_stop":
            content_block = getattr(event, "content_block", None)
            if content_block:
                block_type = getattr(content_block, "type", None)
                # Only log completion of tool_use and thinking blocks
                if block_type in ("tool_use", "thinking"):
                    vcprint(content_block, "Content Block Stop", color="green")

        elif event_type == "message_start":
            vcprint("=================== MESSAGE STARTED ===================", color="blue")

        elif event_type == "message_stop":
            vcprint("=================== MESSAGE COMPLETED ===================", color="green")

        elif event_type == "message_delta":
            # Log usage and stop_reason updates
            delta = getattr(event, "delta", None)
            if delta:
                stop_reason = getattr(delta, "stop_reason", None)
                if stop_reason:
                    vcprint(f"Stop reason: {stop_reason}", color="yellow")
                usage = getattr(event, "usage", None)
                if usage:
                    vcprint(usage, "Usage Update", color="cyan")

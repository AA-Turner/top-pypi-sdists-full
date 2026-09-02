from __future__ import annotations

from typing import Any

from matrx_utils import vcprint

from matrx_ai.config import (
    FinishReason,
    TokenUsage,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.config.citations import (
    enforce_search_result_citation_uniformity,
    log_citations_disabled,
    resolve_citations_disabled_reason,
)
from matrx_ai.config.tool_result_guard import (
    LAYER_ANTHROPIC,
    dedupe_tool_result_dicts,
    report_tool_result_duplicates,
)
from matrx_ai.config.message_config import MessageSanitizationError
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.cache_guard import PROMPT_CACHING_ENABLED
from matrx_ai.providers.outbound_params import resolve_outbound_params

# ============================================================================
# ANTHROPIC TRANSLATOR
# ============================================================================


# CAUSE_FAILURES_FOR_TESTING = True  # Set to True to inject fake tool UUIDs and cause API failures for testing error handling


class AnthropicTranslator(BaseTranslator):
    """Translates between unified format and Anthropic Messages API"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)

    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = ""):
        return self.to_anthropic(config, self.require_profile(route_ctx))

    def to_anthropic(self, config: UnifiedConfig, profile: Any) -> dict[str, Any]:
        """
        Convert unified config to Anthropic Messages API format.

        System instruction comes from config.system_instruction field.
        Delegates message conversion to UnifiedMessage.to_anthropic_blocks().

        Note: Anthropic only supports "user" and "assistant" roles.
        Tool results (role="tool") are converted to role="user".

        Param shaping is DB-driven via ``profile.controls``: the
        ``anthropic_thinking`` processor (mode budget|adaptive per offering)
        owns thinking + the always-present max_tokens fallback, and the
        ``anthropic_temp_topp_exclusion`` processor owns the temperature/top_p
        mutual exclusion + the thinking-sampling 400 gates. The adaptive
        (claude-4.6+/5) sampling deprecation is supported:false rules on those
        offerings — no api_class branches here.
        """
        messages = []

        for msg in config.messages:
            message_content = msg.to_anthropic_blocks()

            if message_content:
                role = "user" if msg.role == "tool" else msg.role
                # Anthropic requires strictly alternating user/assistant roles.
                # Because role="tool" collapses to "user" here, a tool-result
                # turn followed by an actual user turn (e.g. a message drained
                # from the Turn-Boundary Inbox mid-loop) would otherwise produce
                # two consecutive "user" dicts and the API rejects it. Merge
                # consecutive same-role turns by concatenating their content
                # blocks — tool_result blocks + an injected user text block
                # become one valid user turn.
                if messages and messages[-1]["role"] == role:
                    messages[-1]["content"].extend(message_content)
                else:
                    messages.append({"role": role, "content": message_content})

        # LAST LINE OF DEFENSE — even if every upstream guard is bypassed (the
        # live-loop `dataclasses.replace` and cache-hit `deepcopy` paths both
        # skip MessageList.sanitize), the bytes about to hit the wire must not
        # carry two tool_result blocks for one tool_use_id. The same-role merge
        # above is exactly what concatenates a synthesised tool message and a
        # persisted one into a single user turn — so dedup AFTER the merge, per
        # final message. A catch here means an invariant already broke upstream;
        # we strip the duplicate so the request survives and SCREAM (red banner
        # + durable app_log ERROR) so the source gets fixed.
        all_duplicates: list[dict[str, Any]] = []
        total_tool_results = 0
        for _m in messages:
            _content = _m.get("content")
            if not isinstance(_content, list):
                continue
            total_tool_results += sum(
                1 for _b in _content if isinstance(_b, dict) and _b.get("type") == "tool_result"
            )
            _deduped, _dups = dedupe_tool_result_dicts(_content)
            if _dups:
                _m["content"] = _deduped
                all_duplicates.extend(_dups)
        if all_duplicates:
            report_tool_result_duplicates(
                layer=LAYER_ANTHROPIC,
                duplicates=all_duplicates,
                total_tool_results=total_tool_results,
            )

        # Anthropic treats a terminal assistant turn as response prefill. Some
        # older models accepted that shape, but current models may reject it;
        # in every normal Matrx execution the live trigger must be a user/tool
        # turn anyway. Refuse locally at the final wire boundary instead of
        # spending a provider request on a deterministically invalid payload.
        # Do not silently delete the assistant turn or invent a user message:
        # either would replay history under semantics the user did not request.
        if messages and messages[-1]["role"] == "assistant":
            raise MessageSanitizationError(
                "Anthropic request must end with a user/tool turn; terminal "
                "assistant history would be unsupported response prefill"
            )

        # ── CITATIONS — default-ON, machine-runs excluded LOUDLY ─────────────
        # DocumentContent.to_anthropic stamps citations:{enabled:true} on every
        # document block. Machine-consumed runs (structured-output extraction —
        # response_format set — or an explicit pipeline opt-out via
        # config.metadata["citations_enabled"]=False) must not carry them:
        # citation-split text blocks corrupt strict JSON extraction. The strip
        # is one gate, here, and always announces itself — never silent.
        disabled_reason = resolve_citations_disabled_reason(config.response_format, config.metadata)
        if disabled_reason:
            stripped_count = 0

            # 🚨 WEB SEARCH OVERRIDES THE STRIP for `search_result` blocks
            # (2026-08-26, run ae62da71): with the hosted web_search tool in
            # the request, Anthropic REQUIRES citations enabled on every
            # search_result block — a structured-output agent with
            # internal_web_search on was therefore unrunnable: the strip
            # (correct for extraction) produced a request the API rejects
            # outright ("When web search is enabled, citations must be enabled
            # on all `search_result` blocks"). The provider's hard constraint
            # wins over our extraction preference: keep search_result
            # citations when web search rides along, still strip documents.
            _strippable = (
                ("document",) if config.internal_web_search else ("document", "search_result")
            )

            def _strip_citable(_blocks: list[Any]) -> int:
                # document blocks AND search_result blocks (tool results emit
                # the latter via SearchResultContent) both carry citations —
                # a machine run must strip both, wherever they sit (unless web
                # search pins search_result citations on; see above).
                _n = 0
                for _i, _b in enumerate(_blocks):
                    if not isinstance(_b, dict):
                        continue
                    if _b.get("type") in _strippable and "citations" in _b:
                        # Copy before mutating — to_anthropic_blocks dicts may be
                        # shared across calls (same rule as the cache helpers below).
                        _blocks[_i] = {
                            k: v for k, v in _b.items() if k not in ("citations", "context")
                        }
                        _n += 1
                    elif _b.get("type") == "tool_result" and isinstance(_b.get("content"), list):
                        _inner = list(_b["content"])
                        _stripped = _strip_citable(_inner)
                        if _stripped:
                            _blocks[_i] = {**_b, "content": _inner}
                            _n += _stripped
                return _n

            for _m in messages:
                _content = _m.get("content")
                if isinstance(_content, list):
                    stripped_count += _strip_citable(_content)
            if stripped_count:
                log_citations_disabled(disabled_reason, stripped_count)

        # ── SEARCH_RESULT CITATION UNIFORMITY — last line of defense ─────────
        # Anthropic rejects a request whose `search_result` blocks disagree on
        # citations ("A mixture of enabling and disabling is not supported" —
        # live 400, 2026-08-21). Producers already stamp the same posture, but
        # this request is assembled from many of them (live typed blocks,
        # DB-rebuilt tool results, the metadata wrapper) plus the strip gate
        # above, so uniformity is enforced ONCE here, on the final bytes,
        # where nothing can bypass it. A correction means a producer regressed.
        corrected = enforce_search_result_citation_uniformity(messages)
        if corrected:
            vcprint(
                f"[citations] {corrected} `search_result` block(s) reached the "
                "Anthropic wire with citations disabled while others had them "
                "enabled — Anthropic 400s on that mixture. Enabled them to save "
                "the request; the producer that emitted a non-uniform block is "
                "the real defect and must be fixed (config/citations.py, wire "
                "invariant 2).",
                color="red",
            )

        anthropic_request = {
            "model": config.model,
            "messages": messages,
        }

        system_text = self.get_system_text(config)
        all_tools = self.build_provider_tools(config, "anthropic")
        if config.internal_web_search and not any(
            isinstance(tool, dict) and tool.get("type") == "web_search_20250305"
            for tool in all_tools
        ):
            # Anthropic-hosted tool: the provider executes it and returns the
            # final answer in the same turn. It must never enter matrx-ai's
            # local function-tool executor.
            all_tools.append(
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": 5,
                }
            )

        # ── PROMPT CACHING ────────────────────────────────────────────────────
        # Anthropic prompt caching is OPT-IN: without explicit cache_control
        # breakpoints the API caches NOTHING (cache_read_input_tokens stays 0)
        # and every round re-pays full input price. We place breakpoints on the
        # static prefix (tools + system) and a rolling one on the last message
        # so the growing conversation caches incrementally across a tool loop.
        #
        # Anthropic's cache order is tools → system → messages, and a breakpoint
        # caches everything BEFORE it. So a single breakpoint at the end of the
        # system block already covers all tools + system; the rolling
        # last-message breakpoint then extends the cached region over the
        # conversation history each turn. Breakpoints on a sub-threshold prompt
        # (<1024 tokens) are silently ignored by the API — safe to always add.
        # The flag lives in cache_guard so the guard's expectation can never
        # drift from what we actually send.
        if PROMPT_CACHING_ENABLED:
            if system_text:
                # System must be a block array (not a bare string) to carry
                # cache_control. This breakpoint caches tools + system.
                anthropic_request["system"] = [
                    {
                        "type": "text",
                        "text": system_text,
                        "cache_control": {"type": "ephemeral"},
                    }
                ]
                if all_tools:
                    anthropic_request["tools"] = all_tools
            elif all_tools:
                # No system prompt — put the static-prefix breakpoint on the
                # last tool so the tools block still caches.
                all_tools = self._mark_last_tool_cacheable(all_tools)
                anthropic_request["tools"] = all_tools
            # Rolling breakpoint on the last message → incremental history cache.
            self._mark_last_message_cacheable(messages)
        else:
            if system_text:
                anthropic_request["system"] = system_text
            if all_tools:
                anthropic_request["tools"] = all_tools

        # vcprint("\n================\n\nREMOVE THIS: Adding fake uuids to cause failures for testing", color="red")
        # anthropic_request["tools"] = ["9935dadd-2afc-41db-aeac-fc15ee842812", "2b0f6a3a-4cdb-40cb-9063-4c12d6c097f5"]
        # vcprint("="*50 + "\n", color="red")

        # DB-resolved params: max_tokens (processor-validated, always present),
        # thinking / output_config.effort, and the sampling params after the
        # exclusion + thinking-compatibility gates (all processor logic).
        anthropic_request.update(resolve_outbound_params(config, profile.controls))

        if config.tool_choice:
            if config.tool_choice == "auto":
                anthropic_request["tool_choice"] = {"type": "auto"}
            elif config.tool_choice == "required":
                anthropic_request["tool_choice"] = {"type": "any"}
            elif config.tool_choice == "none":
                anthropic_request["tool_choice"] = {"type": "none"}

        # max_tokens / thinking / sampling-compatibility all landed above via
        # the DB-resolved params (anthropic_thinking + temp/top_p exclusion
        # processors — Anthropic requires max_tokens on every request, so the
        # processor always emits a validated value).

        # Response format — Anthropic structured outputs go on
        # ``output_config.format`` (standard Messages API, no beta header).
        # MERGE into any existing ``output_config`` (the adaptive-thinking path
        # above sets ``output_config.effort``) — never clobber it. Structured
        # outputs and tools are compatible on Anthropic, so no tool handling is
        # needed here. Done last so the thinking block has already run.
        if config.response_format:
            output_format = self._build_anthropic_output_format(config.response_format)
            if output_format is not None:
                existing = anthropic_request.get("output_config")
                if isinstance(existing, dict):
                    existing["format"] = output_format
                else:
                    anthropic_request["output_config"] = {"format": output_format}

        return anthropic_request

    # ── Prompt-cache breakpoint helpers ──────────────────────────────────────
    # Both COPY before mutating: build_provider_tools may return declaration
    # dicts shared from the registry cache, and to_anthropic_blocks may return
    # content-block dicts shared across calls. Mutating them in place would
    # poison those caches for every future request.

    _CACHE_CONTROL_EPHEMERAL = {"type": "ephemeral"}
    _NON_CACHEABLE_MESSAGE_BLOCK_TYPES = frozenset({"thinking", "redacted_thinking"})

    @classmethod
    def _mark_last_tool_cacheable(cls, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return a copy of ``tools`` with a cache_control breakpoint on the
        last declaration (used only when there is no system prompt to carry it)."""
        if not tools:
            return tools
        out = list(tools)
        out[-1] = {**out[-1], "cache_control": dict(cls._CACHE_CONTROL_EPHEMERAL)}
        return out

    @classmethod
    def _mark_last_message_cacheable(cls, messages: list[dict[str, Any]]) -> None:
        """Attach a rolling cache breakpoint to the last eligible message block."""
        if not messages:
            return
        content = messages[-1].get("content")
        if not isinstance(content, list) or not content:
            return
        for index in range(len(content) - 1, -1, -1):
            block = content[index]
            if not isinstance(block, dict):
                continue
            if block.get("type") in cls._NON_CACHEABLE_MESSAGE_BLOCK_TYPES:
                continue
            content[index] = {
                **block,
                "cache_control": dict(cls._CACHE_CONTROL_EPHEMERAL),
            }
            return

    @staticmethod
    def _build_anthropic_output_format(
        response_format: Any,
    ) -> dict[str, Any] | None:
        """Map the unified ``response_format`` onto Anthropic's ``output_config.format``.

        Anthropic (https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
        takes ``{"type": "json_schema", "schema": {...}}`` — **schema only, no
        ``name`` and no ``strict``** (unlike OpenAI / Chat Completions). The schema
        root must be an object; Anthropic additionally requires
        ``additionalProperties:false`` + ``required`` on every object and validates
        this server-side.

        Returns ``None`` when no usable object-root schema is present. Anthropic has
        NO ``json_object`` fallback mode, so on ``None`` the caller simply omits
        ``output_config.format`` and the model falls back to prompt instructions.
        """
        if not isinstance(response_format, dict):
            return None

        fmt_type = response_format.get("type")
        # text / json_object have no Anthropic structured-output equivalent —
        # nothing to enforce, so leave output_config.format unset.
        if fmt_type != "json_schema":
            return None

        # Locate the schema across the shapes response_format can arrive in: a
        # full OpenAI-style envelope ({name, schema, strict}), a raw JSON Schema
        # nested under json_schema, or a bare {"type":"json_schema"} placeholder.
        inner = response_format.get("json_schema")
        schema: dict[str, Any] | None = None
        if isinstance(inner, dict):
            if isinstance(inner.get("schema"), dict):
                schema = inner["schema"]
            elif {"type", "properties", "items"} & inner.keys():
                schema = inner  # inner IS the raw JSON Schema
        elif isinstance(response_format.get("schema"), dict):
            schema = response_format["schema"]

        # Anthropic requires an object-root schema. No usable / non-object-root
        # schema → omit structured output. This is a runtime ADJUSTMENT (schema
        # NOT enforced) — log loudly so it's never mistaken for configured behaviour.
        downgrade_reason: str | None = None
        if not isinstance(schema, dict):
            downgrade_reason = "no JSON Schema was supplied with the json_schema request"
        elif not (
            schema.get("type") == "object"
            or (schema.get("type") is None and isinstance(schema.get("properties"), dict))
        ):
            downgrade_reason = (
                f"schema root is not an object (type={schema.get('type')!r}); "
                "Anthropic requires an object root"
            )
        if downgrade_reason is not None:
            vcprint(
                data={
                    "provider": "anthropic",
                    "requested": response_format,
                    "downgraded_to": "none (prompt-only)",
                    "reason": downgrade_reason,
                },
                title=(
                    "⚠️  ANTHROPIC ADJUSTMENT: structured output OMITTED — schema is "
                    "NOT enforced (prompt-only). Anthropic has no json_object fallback. "
                    "The frontend should reject this; do NOT persist it as a saved config."
                ),
                color="yellow",
                verbose=True,
            )
            return None

        # Anthropic validates server-side that EVERY object node carries
        # ``additionalProperties: false`` and 400s otherwise
        # (output_config.format.schema: For 'object' type, 'additionalProperties'
        # must be explicitly set to false). Schemas arrive from many sources
        # (NER, agent output_schema, saved configs) that don't pre-bake this, so
        # we enforce it here for ALL Anthropic structured outputs rather than
        # patching each producer.
        schema = AnthropicTranslator._enforce_anthropic_strict_schema(schema)

        # Anthropic rejects advisory array/string/number bounds — e.g.
        # "For 'array' type, 'minItems' values other than 0 or 1 are not supported
        # (got: [2, 5])". Reduce to the subset Anthropic accepts at the SAME seam
        # every other provider uses; the stored schema keeps the rich bounds.
        schema = AnthropicTranslator.sanitize_structured_output_schema(schema, "anthropic")

        # Anthropic accepts ``anyOf`` but 400s on ``oneOf`` ("Schema type
        # 'oneOf' is not supported"). Rewrite at the send boundary — a
        # relaxation (exactly-one → at-least-one) acceptable for output
        # guidance; the stored schema keeps ``oneOf``.
        from matrx_ai.schema.rules import rewrite_oneof_as_anyof

        schema = rewrite_oneof_as_anyof(schema)

        # schema only — Anthropic's JSONOutputFormatParam has no name/strict.
        return {"type": "json_schema", "schema": schema}

    @staticmethod
    def _enforce_anthropic_strict_schema(node: Any) -> Any:
        """Return a copy of ``node`` with ``additionalProperties: false`` set on
        every object node, recursively. Anthropic's structured-output validator
        requires this on every ``"type": "object"`` (and on property-bearing
        nodes that omit ``type``). The input is never mutated.

        Delegates to the single source of truth in ``matrx_ai.schema.rules`` so
        the standalone schema linter and this translator never drift."""
        from matrx_ai.schema.rules import enforce_additional_properties_false

        return enforce_additional_properties_false(node)

    def from_anthropic(self, response: dict[str, Any], matrx_model_name: str) -> UnifiedResponse:
        """Convert Anthropic Messages API response to unified format"""

        message_id = response.get("id")

        # UnifiedMessage.id is cx_message.id ONLY — the provider response id
        # lives on TokenUsage.response_id below. Stamping it here once leaked
        # "msg_*" into a cx_message UUID PK (2026-07-02).
        message = UnifiedMessage.from_anthropic_content(
            role=response.get("role"),
            content=response.get("content", []),
        )

        # Convert usage to TokenUsage if present
        token_usage = TokenUsage.from_anthropic(
            response["usage"], matrx_model_name=matrx_model_name, response_id=message_id
        )

        finish_reason = FinishReason.from_anthropic(response.get("stop_reason"))

        return UnifiedResponse(
            messages=[message],
            usage=token_usage,
            finish_reason=finish_reason,
            raw_response=response,
        )

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
from matrx_ai.config.message_config import MessageSanitizationError
from matrx_ai.config.tool_result_guard import (
    LAYER_ANTHROPIC,
    dedupe_tool_result_dicts,
    report_tool_result_duplicates,
)
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.cache_guard import PROMPT_CACHING_ENABLED
from matrx_ai.providers.outbound_params import resolve_outbound_params, resolve_structural_setting
from matrx_ai.providers.structured_output_findings import response_format_identity

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
        from matrx_ai.config.message_flags import flags_of

        # Message FLAGS: a `cache_boundary` message gets a breakpoint on its last
        # cacheable block; a trailing `prefill` assistant turn is sent AS the
        # prefill (the dispatch gate already refused / converted it for a model
        # without the `assistant_prefill` capability).
        boundary_blocks: list[dict[str, Any]] = []
        trailing_prefill = False
        wire_messages = list(config.messages)
        for position, msg in enumerate(wire_messages):
            message_content = msg.to_anthropic_blocks()
            flags = flags_of(msg)
            if message_content and flags.get("cache_boundary") and PROMPT_CACHING_ENABLED:
                marked = self._mark_blocks_cacheable(message_content)
                if marked is not None:
                    boundary_blocks.append(marked)
            if position == len(wire_messages) - 1 and flags.get("prefill") and msg.role == "assistant":
                trailing_prefill = True

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
        if trailing_prefill and messages and messages[-1]["role"] == "assistant":
            # An AUTHORED prefill: Anthropic continues the reply from it. The
            # API rejects a final assistant block that ends in whitespace.
            self._rstrip_prefill(messages[-1])
        elif messages and messages[-1]["role"] == "assistant":
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

        # The system channel is sent in TWO parts so the per-turn context block
        # can ride it without costing a prompt cache: the stable instruction
        # carries the cache breakpoint, the per-turn block follows it uncached.
        system_text = self.get_stable_system_text(config)
        turn_context_text = self.get_turn_context_text(config)
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
                system_blocks: list[dict[str, Any]] = [
                    {
                        "type": "text",
                        "text": system_text,
                        "cache_control": {"type": "ephemeral"},
                    }
                ]
                if turn_context_text:
                    # AFTER the breakpoint, deliberately uncached: this block is
                    # rebuilt every turn, so caching it would invalidate the
                    # prefix on every single call.
                    system_blocks.append({"type": "text", "text": turn_context_text})
                anthropic_request["system"] = system_blocks
                if all_tools:
                    anthropic_request["tools"] = all_tools
            elif all_tools:
                # No system prompt — put the static-prefix breakpoint on the
                # last tool so the tools block still caches.
                all_tools = self._mark_last_tool_cacheable(all_tools)
                anthropic_request["tools"] = all_tools
            if not system_text and turn_context_text:
                anthropic_request["system"] = [{"type": "text", "text": turn_context_text}]
            # Rolling breakpoint on the last message → incremental history cache.
            # With a trailing prefill the rolling breakpoint sits on the turn
            # before it (the prefill is not history that will be replayed).
            self._mark_last_message_cacheable(messages[:-1] if trailing_prefill else messages)
            # Anthropic allows at most 4 breakpoints per request. System (or last
            # tool) + rolling take up to 2; authored boundaries keep the LATEST
            # ones (a later boundary's prefix covers every earlier one).
            self._enforce_breakpoint_ceiling(anthropic_request, messages, boundary_blocks)
        else:
            joined_system = "\n\n".join(p for p in (system_text, turn_context_text) if p)
            if joined_system:
                anthropic_request["system"] = joined_system
            if all_tools:
                anthropic_request["tools"] = all_tools

        # vcprint("\n================\n\nREMOVE THIS: Adding fake uuids to cause failures for testing", color="red")
        # anthropic_request["tools"] = ["9935dadd-2afc-41db-aeac-fc15ee842812", "2b0f6a3a-4cdb-40cb-9063-4c12d6c097f5"]
        # vcprint("="*50 + "\n", color="red")

        # DB-resolved params: max_tokens (processor-validated, always present),
        # thinking / output_config.effort, and the sampling params after the
        # exclusion + thinking-compatibility gates (all processor logic).
        anthropic_request.update(resolve_outbound_params(config, profile.controls))

        # tool_choice is structural (this translator owns the wire shape), but the
        # offering's control rule decides WHETHER a value may be sent: Opus 5.5 /
        # Fable 5.1 reject forced tool use ({"type": "any"}), and their rule maps
        # "required" away loudly instead of letting the request 400.
        tool_choice = resolve_structural_setting(
            config.tool_choice, "tool_choice", profile.controls, model=getattr(config, "model", "?")
        )
        if tool_choice:
            if tool_choice == "auto":
                anthropic_request["tool_choice"] = {"type": "auto"}
            elif tool_choice == "required":
                anthropic_request["tool_choice"] = {"type": "any"}
            elif tool_choice == "none":
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
            output_format = self._build_anthropic_output_format(
                config.response_format,
                tool_count=len(anthropic_request.get("tools") or []),
            )
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

    _MAX_CACHE_BREAKPOINTS = 4

    @classmethod
    def _mark_blocks_cacheable(cls, content: list[dict[str, Any]]) -> dict[str, Any] | None:
        """Put a breakpoint on the last cacheable block of ONE message's blocks
        (replacing the dict in place in ``content``); returns the marked block."""
        for index in range(len(content) - 1, -1, -1):
            block = content[index]
            if not isinstance(block, dict) or block.get("type") in cls._NON_CACHEABLE_MESSAGE_BLOCK_TYPES:
                continue
            content[index] = {**block, "cache_control": dict(cls._CACHE_CONTROL_EPHEMERAL)}
            return content[index]
        return None

    @staticmethod
    def _rstrip_prefill(message: dict[str, Any]) -> None:
        content = message.get("content")
        if not isinstance(content, list):
            return
        for index in range(len(content) - 1, -1, -1):
            block = content[index]
            if isinstance(block, dict) and block.get("type") == "text":
                content[index] = {**block, "text": str(block.get("text", "")).rstrip()}
                return

    @classmethod
    def _enforce_breakpoint_ceiling(
        cls,
        request: dict[str, Any],
        messages: list[dict[str, Any]],
        boundary_blocks: list[dict[str, Any]],
    ) -> None:
        """Drop the EARLIEST authored boundaries beyond Anthropic's 4-breakpoint cap, loudly."""

        def _count(blocks: Any) -> int:
            return sum(
                1 for b in blocks or [] if isinstance(b, dict) and "cache_control" in b
            )

        total = _count(request.get("system") if isinstance(request.get("system"), list) else [])
        total += _count(request.get("tools"))
        for m in messages:
            total += _count(m.get("content") if isinstance(m.get("content"), list) else [])
        excess = total - cls._MAX_CACHE_BREAKPOINTS
        if excess <= 0:
            return
        dropped = 0
        for marked in boundary_blocks:
            if dropped >= excess:
                break
            for m in messages:
                content = m.get("content")
                if not isinstance(content, list):
                    continue
                for i, b in enumerate(content):
                    if b is marked:
                        content[i] = {k: v for k, v in b.items() if k != "cache_control"}
                        dropped += 1
                        break
        vcprint(
            f"[message flags] {dropped} earlier cache boundary(ies) not sent — Anthropic "
            f"allows {cls._MAX_CACHE_BREAKPOINTS} cache breakpoints per request and a later "
            "boundary already caches everything before it.",
            color="yellow",
        )

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
        *,
        tool_count: int = 0,
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
            # LOUD, never silent. `UnifiedConfig.response_format` is typed as a
            # dict and every translator reads it as one, but the dataclass does
            # not validate on assignment — so a caller that sets the Pydantic
            # model lands here, and returning None quietly meant the schema was
            # simply not enforced while the run looked normal. That is exactly
            # how the decision overlay's binding vanished on 2026-09-20.
            vcprint(
                data={
                    "provider": "anthropic",
                    "response_format_type": type(response_format).__name__,
                },
                title="RESPONSE FORMAT DROPPED",
                pretty=True,
                verbose=False,
                color="red",
            )
            vcprint(
                "🚨 CAPABILITY LEAK [anthropic]: response_format is a "
                f"{type(response_format).__name__}, not a dict, so NO structured "
                "output was requested and the model answered free-form. Normalize "
                "it at the call site (UnifiedConfig._normalize_response_format).",
                color="red",
            )
            from matrx_ai.providers.structured_output_findings import (
                ENFORCEMENT_DROPPED,
                record_structured_output_finding_sync,
            )
            from matrx_ai.schema.answer_contract import mark_enforcement_dropped

            mark_enforcement_dropped(
                f"response_format arrived as {type(response_format).__name__}, not a dict"
            )
            record_structured_output_finding_sync(
                ENFORCEMENT_DROPPED,
                provider="anthropic",
                model=None,
                detail={
                    "action": (
                        "structured output omitted entirely: response_format is a "
                        f"{type(response_format).__name__}, not a dict, so no schema could "
                        "be read from it"
                    ),
                    "remedy": (
                        "normalize response_format at the call site "
                        "(UnifiedConfig._normalize_response_format) — this is how the "
                        "decision overlay's binding vanished on 2026-09-20"
                    ),
                },
                was_recovered=False,
            )
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
            # `response_format_identity` is imported at MODULE scope. Importing it
            # here made it a local of the whole function, so the forcing-function
            # branch below raised UnboundLocalError on every schema whose
            # violations survived translation — the request died on a Python
            # error and the very finding that branch exists to write was never
            # written (SCHEMA-TRANSLATION-VERIFY.md, R9; 10 live schemas).
            from matrx_ai.providers.structured_output_findings import (
                ENFORCEMENT_DROPPED,
                record_structured_output_finding_sync,
            )
            from matrx_ai.schema.answer_contract import mark_enforcement_dropped

            mark_enforcement_dropped(downgrade_reason)
            record_structured_output_finding_sync(
                ENFORCEMENT_DROPPED,
                provider="anthropic",
                model=None,
                detail={
                    **response_format_identity(response_format),
                    "action": f"structured output omitted entirely — {downgrade_reason}",
                    "remedy": (
                        "give the contract an OBJECT root (wrap a list as "
                        '{"items": [...]}) — Anthropic has no json_object fallback, so '
                        "nothing enforces this request's shape at the provider"
                    ),
                },
                was_recovered=False,
            )
            return None

        schema, narrowed, relaxed = AnthropicTranslator.translate_output_schema(
            schema, tool_count=tool_count
        )
        from matrx_ai.providers.structured_output_findings import note_translation
        from matrx_ai.schema.rules import structured_output_schema_violations

        if narrowed or relaxed:
            vcprint(
                data={"provider": "anthropic", "narrowed": narrowed, "relaxed": relaxed},
                title=(
                    "⚠️  ANTHROPIC ADJUSTMENT: the schema was translated to the subset "
                    "Anthropic's decoder compiles. The stored schema is unchanged, and the "
                    "answer is checked against it when the call ends "
                    "(schema.answer_contract.verify_answer_and_record)."
                ),
                color="yellow",
                verbose=True,
            )
            note_translation(
                "anthropic",
                narrowed=narrowed,
                relaxed=relaxed,
                response_format=response_format,
            )

        # THE FORCING FUNCTION. Anything the subset still forbids is named HERE,
        # in our own logs, with the node path — instead of arriving as an opaque
        # provider 400 that a caller has no way to act on.
        violations = structured_output_schema_violations(schema)
        if violations:
            vcprint(
                data={"provider": "anthropic", "violations": violations},
                title="🚨 ANTHROPIC SCHEMA STILL OUT OF SUBSET",
                color="red",
                verbose=False,
            )
            vcprint(
                "🚨 CAPABILITY LEAK [anthropic]: the structured-output schema carries "
                f"{len(violations)} shape(s) Anthropic's validator rejects; this request "
                "will 400. Add the rule to matrx_ai.schema.rules — the normalization "
                "boundary is the ONE place this is fixed.",
                color="red",
            )
            from matrx_ai.providers.structured_output_findings import (
                RELAXED,
                record_structured_output_finding_sync,
            )

            # The forcing function fired, which means we are about to ship a 400 we
            # built ourselves. A console line is not where that belongs.
            record_structured_output_finding_sync(
                RELAXED,
                provider="anthropic",
                model=None,
                detail={
                    **response_format_identity(response_format),
                    "action": (
                        f"{len(violations)} shape(s) Anthropic's validator rejects survived "
                        "translation — this request is expected to 400"
                    ),
                    "violations": violations[:10],
                    "remedy": (
                        "add the rule to matrx_ai.schema.rules — the normalization boundary "
                        "is the ONE place this class is fixed"
                    ),
                },
                was_recovered=False,
            )

        # schema only — Anthropic's JSONOutputFormatParam has no name/strict.
        return {"type": "json_schema", "schema": schema}

    #: The largest compiled-grammar COST (``anthropic_grammar_cost``) this
    #: translator will spend on widened optional fields. Measured on 2,700
    #: distinct bodies probed against ``claude-sonnet-5`` on 2026-09-28: the
    #: lowest "compiled grammar is too large" refusal scored 72.0 (a body THIS
    #: translator had widened up to a 72 ceiling — the search pushes every body
    #: to the ceiling, so the ceiling needs a real margin, not a fitted edge);
    #: the next lowest 81.0. 64 keeps 8 below the lowest refusal and still admits
    #: 2,221 of the 2,476 accepted bodies. A schema whose forced form already
    #: costs more than this gets no widening at all — its wire body is the shape
    #: Anthropic accepted before any widening existed
    #: (SCHEMA-TRANSLATION-VERIFY.md, R5).
    GRAMMAR_COST_CEILING: float = 64.0
    #: What each attached tool is charged against that ceiling. Tools share the
    #: grammar with the schema (grammar_budget.py); a strict tool schema is
    #: typically several properties plus a union or two.
    GRAMMAR_COST_PER_TOOL: float = 8.0

    @staticmethod
    def translate_output_schema(
        schema: dict[str, Any], *, tool_count: int = 0
    ) -> tuple[dict[str, Any], list[str], list[str]]:
        """Translate a declared JSON Schema into the subset Anthropic compiles,
        spending the grammar budget on widened optional fields only while the
        request stays under the measured ceiling.

        An optional field is expressed as required-and-nullable (lossless) as long
        as the whole request still fits Anthropic's compiled-grammar budget and the
        16 union parameters; past that, the remaining optional fields are FORCED
        (the shape Anthropic accepted before any widening existed) and named in
        ``narrowed``. The author's own nullable fields keep their union slots
        first. Widening must never turn a request Anthropic accepts into one it
        refuses — that is what R5 measured happening on 29 live schemas.
        """
        from matrx_ai.schema.rules import (
            WideningBudget,
            anthropic_grammar_cost,
            count_union_params,
        )

        ceiling = AnthropicTranslator.GRAMMAR_COST_CEILING - (
            AnthropicTranslator.GRAMMAR_COST_PER_TOOL * tool_count
        )

        def attempt(limit: int | None) -> tuple[Any, WideningBudget]:
            budget = WideningBudget(limit=limit)
            return AnthropicTranslator._translate_output_schema_once(
                schema, tool_count=tool_count, budget=budget
            ), budget

        def fits(result: Any) -> bool:
            """Does the copy we are ABOUT TO SEND fit Anthropic's two ceilings?

            🚨 It used to read ``unions_before_collapse`` — the count BEFORE the
            nullable-union collapse ran — so the predicate answered a question
            about a schema that was never sent, in both directions. That is how 3
            live wires went out carrying 24 / 21 / 18 union parameters over
            Anthropic's documented 16 while the translator's own notes said it
            had narrowed 25 fields to respect the cap, and all 3 were refused
            live (SCHEMA-TRANSLATION-VERIFY.md, F7). Counting the wire is the
            only measurement that can be honest: a collapse that did NOT reach
            the cap (there is nothing nullable left to narrow) is now visible
            here, and the widening search stops spending budget on a request
            that cannot be accepted anyway.
            """
            wire, _narrowed, _relaxed, _unions_before_collapse, limit = result
            return count_union_params(wire) <= limit and anthropic_grammar_cost(wire) <= ceiling

        full, full_budget = attempt(None)
        if full_budget.widened == 0 or fits(full):
            return full[0], full[1], full[2]
        # Largest number of widened fields that still fits (widening only ever
        # adds cost, so the predicate is monotone in the limit).
        low, high = 0, full_budget.widened - 1
        best, _ = attempt(0)
        if not fits(best):
            # The forced form is already over the line: add nothing to it.
            return best[0], best[1], best[2]
        while low < high:
            mid = (low + high + 1) // 2
            candidate, _ = attempt(mid)
            if fits(candidate):
                low, best = mid, candidate
            else:
                high = mid - 1
        return best[0], best[1], best[2]

    @staticmethod
    def _translate_output_schema_once(
        schema: dict[str, Any], *, tool_count: int = 0, budget: Any = None
    ) -> tuple[dict[str, Any], list[str], list[str], int, int]:
        """Translate a declared JSON Schema into the subset Anthropic compiles.

        Returns ``(wire_schema, narrowed, relaxed)``:

        * ``narrowed`` — what the provider copy gave up while every answer it
          admits is STILL valid under the declared contract (a map emptied, a
          nullable made non-null, recursion cut at a depth);
        * ``relaxed`` — constraints the provider no longer enforces at all (they
          are enforced only by the platform's validation of the answer).

        Every rule below answers a refusal measured live against Anthropic
        (``claude-opus-5-5`` / ``claude-sonnet-5``, 2026-09-27; the corpus and the
        budget probes are in common-docs ``projects/checks-run-in-the-app/
        SCHEMA-TRANSLATION.md``):

          oneOf                       -> "Schema type 'oneOf' is not supported"
          allOf with siblings         -> "For 'anyOf', 'additionalProperties,
                                          properties, required, type' is not supported"
          discriminator/type by anyOf -> "For 'anyOf', '<key>' is not supported"
          items: [A, B]               -> "Array types must be specified with a
                                          single object schema for 'items'"
          {}                          -> "Empty schema ({}) ... specify a concrete type"
          additionalProperties {...}  -> "For 'object' type, 'additionalProperties:
                                          object' is not supported"
          a self-referencing $def     -> "Circular reference detected in schema
                                          definitions"
          > 16 union parameters       -> "Schemas contains too many parameters with
                                          union types"
          > 12 optional parameters    -> "Schema is too complex." (after up to 180 s)
          ~70+ properties             -> "The compiled grammar is too large"
        """
        from matrx_ai.schema.lint import make_portable
        from matrx_ai.schema.rules import (
            ANTHROPIC_UNION_PARAM_LIMIT,
            NORMALIZATION_NOTES_KEY,
            classify_normalization_notes,
            collapse_nullable_unions,
            OPEN_SCALAR_ITEM_SCHEMA,
            concretize_empty_schemas,
            count_nullable_union_params,
            count_optional_properties,
            count_union_params,
            dedupe_combinator_branches,
            dedupe_identical_subtrees,
            drop_refinement_combinators,
            enforce_additional_properties_false,
            enforce_all_required,
            flatten_allof,
            hoist_nested_defs,
            normalize_array_items,
            normalize_combinator_siblings,
            prune_unreachable_defs,
            rewrite_oneof_as_anyof,
            split_enum_from_type_union,
            take_normalization_notes,
            unroll_recursive_refs,
        )

        narrowed: list[str] = []
        relaxed: list[str] = []

        # THE SHARED FIRST STEP: the author's schema closed, every property listed
        # in `required`, each optional one widened to nullable while `budget`
        # allows and forced (and named) past it. Idempotent on a stored portable
        # copy.
        schema = make_portable(schema, budget=budget, notes=narrowed)

        # additionalProperties:false on every object (nullable objects included);
        # a dynamic-key map is NARROWED to {} and named — the only shape compiled.
        # Refinement-only combinators are validation logic, not shape — removed
        # FIRST, before any rule below can mistake a branch for a structure (the
        # union rules would distribute the parent into type-less branches and the
        # provider answers "Schema type is missing").
        # A `$ref` resolves from the document ROOT, so a schema embedded whole
        # under a parent's `properties` brings its own `$defs` down with it and
        # every pointer inside it names nothing: "Reference to non-existent
        # definition". Lift them first — lossless, and it must precede
        # `prune_unreachable_defs` so the hoisted entries are the ones counted.
        schema = hoist_nested_defs(schema)
        schema = drop_refinement_combinators(schema, relaxed)
        schema = enforce_additional_properties_false(schema, maps="narrow", notes=narrowed)
        # Advisory bounds (minItems 2+, pattern, minimum…) — stripped at the same
        # seam every provider uses; the stored schema keeps them.
        schema = AnthropicTranslator.sanitize_structured_output_schema(schema, "anthropic")
        # allOf is an intersection, so it MERGES into its parent (exact).
        schema = flatten_allof(schema)
        schema = rewrite_oneof_as_anyof(schema)
        schema = normalize_combinator_siblings(schema)
        schema = normalize_array_items(schema)
        # An unspecified array ELEMENT becomes the widest shape a strict decoder
        # compiles (every scalar and null), named as a narrowing — never `string`.
        schema = concretize_empty_schemas(schema, item_placeholder=OPEN_SCALAR_ITEM_SCHEMA)
        # Lossless, and it must run HERE — after the rules above, because they are
        # what CREATES the duplicates. `make_portable` already dropped the ones the
        # author wrote; `A | A` only appears in the Docker-Hub tool's `digest` once
        # `{"not": {}}` has been emptied and concretized into the same
        # `{"type": "string"}` its sibling already was. Left in place a degenerate
        # union costs a slot of Anthropic's 16 AND survives
        # `collapse_nullable_unions` — narrowing `anyOf: [anyOf: [A, A], null]`
        # leaves `anyOf: [A, A]`, still a union parameter — which is how 3 live
        # wires went out at 24 / 21 / 18 unions and were refused
        # (SCHEMA-TRANSLATION-VERIFY.md, F7). It runs before the count below.
        schema = dedupe_combinator_branches(schema)
        schema = prune_unreachable_defs(schema)
        # Recursion is refused outright; a bounded tree is the closest shape.
        schema = unroll_recursive_refs(schema, depth=4, notes=relaxed)
        # Nodes that only became objects during the merges above.
        schema = enforce_additional_properties_false(schema, maps="narrow", notes=narrowed)
        # EVERY PROPERTY REQUIRED **AND NULLABLE**. Optional parameters are the
        # most expensive thing in Anthropic's grammar: 13 optional properties
        # answer "Schema is too complex" after 45-180 s, so `required` must name
        # every property. But `required` ALONE narrows the contract — the claim
        # that "a Pydantic optional is anyOf: [X, null], so required still lets
        # the model answer null" holds only when the property IS nullable, and
        # 2,865 live schemas force a field that is not: `plan_node_specialist`'s
        # `gap_description` exists to be set only when there is a gap, and
        # forcing it made the model invent one on every call. Widening to
        # `[T, "null"]` spends one of the 16 union slots instead of one of the
        # ~12 optional slots — a strictly better trade in Anthropic's own
        # budget — and `collapse_nullable_unions` below takes back exactly the
        # excess, naming every field it narrows. A `const` (`__kind`) is forced
        # and not widened: its value is already determined, so nothing is lost.
        optional_before = count_optional_properties(schema)
        enforce_all_required(
            schema, express_optional_as_nullable=True, notes=narrowed, budget=budget
        )
        # An enum beside a type ARRAY is refused outright, so a nullable enum —
        # the widening above, and every Pydantic `Optional[SomeEnum]` that ever
        # reached here — becomes `anyOf` branches. Lossless, and it still costs
        # exactly one union parameter, so the budget collapse below is unaffected.
        schema = split_enum_from_type_union(schema)
        # The documented ceiling of 16 union parameters (one tool spends one).
        limit = ANTHROPIC_UNION_PARAM_LIMIT - (1 if tool_count else 0)
        total_unions = count_union_params(schema)
        unions_before_collapse = total_unions
        if total_unions > limit:
            # Only the NULLABLE unions can be narrowed; the others (a real choice
            # between shapes — and a nullable choice between SEVERAL shapes, which
            # stays a union once its null is gone) keep their slots first.
            source = schema
            keep = max(0, limit - (total_unions - count_nullable_union_params(schema)))
            while True:
                attempt_notes: list[str] = []
                schema = collapse_nullable_unions(
                    source,
                    keep=keep,
                    notes=attempt_notes,
                    reason=f"Anthropic compiles at most {limit} union parameters on this request",
                )
                excess = count_union_params(schema) - limit
                if excess <= 0 or keep == 0:
                    break
                keep = max(0, keep - excess)
            narrowed.extend(attempt_notes)
        # Identical object subtrees compile once when shared through $defs and
        # once PER COPY when inline — lossless, and a real budget lever.
        schema = dedupe_identical_subtrees(schema)
        schema, combinator_notes = take_normalization_notes(schema)
        more_narrowed, more_relaxed = classify_normalization_notes(combinator_notes)
        narrowed.extend(more_narrowed)
        relaxed.extend(more_relaxed)
        if optional_before:
            vcprint(
                f"[anthropic] {optional_before} optional propert"
                f"{'y' if optional_before == 1 else 'ies'} made required "
                "(Anthropic's grammar charges optional parameters exponentially).",
                color="yellow",
                verbose=True,
            )
        schema.pop(NORMALIZATION_NOTES_KEY, None)
        return schema, narrowed, relaxed, unions_before_collapse, limit

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

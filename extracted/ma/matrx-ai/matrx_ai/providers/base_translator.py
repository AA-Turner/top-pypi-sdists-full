"""Base class for all provider translators.

All provider-specific translators should inherit from this. It centralizes
any logic that is shared across providers at the translation boundary — in
particular, system instruction resolution.

Design rule
-----------
Translators must NEVER call str(config.system_instruction) directly.
They must NEVER access config.resolved_system_instruction directly either.
Instead, call self.get_system_text(config), which is the single, versioned
point where that resolution happens. If the resolution logic ever changes
(caching, fallback, logging, etc.), it changes here and nowhere else.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from matrx_utils import detached_task, vcprint

if TYPE_CHECKING:
    from matrx_ai.config.unified_config import UnifiedConfig


class BaseTranslator(ABC):
    """Minimal shared behaviour for all provider translators."""

    debug: bool

    def __init__(self, debug: bool = False):
        self.debug = debug

    # ------------------------------------------------------------------
    # The single validated entry every provider request goes through.
    # ------------------------------------------------------------------

    def build_request(self, config: UnifiedConfig, route_ctx: Any = "") -> Any:
        """THE single entry point for turning a ``UnifiedConfig`` into a provider
        request — call this, never ``_assemble_request`` / ``to_<provider>`` directly.

        ``route_ctx`` is the routing context for the call: the
        ``ResolvedCallProfile`` (param shaping reads ``profile.controls``;
        structural branches read ``profile.capabilities``) — enforce with
        :meth:`require_profile`. Every translator is flipped; nothing passes a
        legacy class string anymore.

        It runs the provider-agnostic CRITICAL validations on the message list
        (the same role :meth:`build_provider_tools` plays for tool declarations),
        then delegates to the provider's own assembly. ``MessageList.sanitize()``
        dedups duplicate ``tool_result`` blocks — two for one ``tool_use_id`` 400s
        EVERY provider, not just Anthropic — and enforces tool_use/tool_result
        pairing. Running it HERE means it covers ALL 7+ providers on EVERY call,
        including the ``dataclasses.replace`` / ``deepcopy`` config paths that never
        re-run ``UnifiedConfig.__post_init__`` (the live-loop and cache-hit paths
        that previously slipped a duplicate straight to the wire). Provider-specific
        final checks (e.g. Anthropic's post-merge dedup) stay in that provider's
        own assembly.
        """
        messages = getattr(config, "messages", None)
        if messages is not None and hasattr(messages, "sanitize"):
            messages.sanitize()
        return self._assemble_request(config, route_ctx)

    @abstractmethod
    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = "") -> Any:
        """Provider-specific request assembly: turn a (already-sanitized)
        ``UnifiedConfig`` into the provider SDK's request payload.

        EVERY translator MUST implement this — forgetting it raises ``TypeError``
        at instantiation (ABC enforcement), so a new provider can never silently
        skip the validated :meth:`build_request` chokepoint. Implementations are
        typically a one-line delegate to the provider's ``to_<provider>`` builder.
        """
        raise NotImplementedError

    def to_batch_request(self, payload: Any, *, response_format: Any = None) -> Any:
        """The provider's BATCH-endpoint spelling of a request ``build_request`` built.

        Identity by default: the Anthropic and OpenAI batch endpoints take the live
        body verbatim. A provider whose batch endpoint validates the body
        differently (Google — see ``GoogleTranslator.to_batch_request``) overrides
        this, so the difference lives in that provider's ONE translator and never
        in the transport (``matrx_batch``), which must not rewrite a request."""
        return payload

    @staticmethod
    def require_profile(route_ctx: Any) -> Any:
        """Loud gate for the flipped translators: their ``route_ctx`` MUST be a
        ``ResolvedCallProfile``. A bare string (or nothing) reaching a flipped
        translator is a caller bug — fail with instructions, never limp along
        with default params."""
        from matrx_ai.catalog.models import ResolvedCallProfile

        if not isinstance(route_ctx, ResolvedCallProfile):
            raise TypeError(
                "This translator is DB-driven (B4 flip): build_request's second "
                f"argument must be a ResolvedCallProfile, got {type(route_ctx).__name__!r}. "
                "Resolve one via matrx_ai.catalog.resolve.resolve_call_profile(model) "
                "or, in tests, matrx_ai.testing.profile_factory.make_profile(...)."
            )
        return route_ctx

    def get_system_text(self, config: UnifiedConfig) -> str | None:
        """Return the resolved system instruction string, or None if absent.

        This is the only place in the codebase where UnifiedConfig.system_instruction
        is resolved to a plain string for use in an API request. All translators
        must call this method instead of accessing resolved_system_instruction directly.

        It is also the SINGLE injection point for the Custom Dictionary: when
        config.dictionary is present we append the right shape for the model
        class (definitions+spellings block for tool-capable models; a terse
        pronunciation directive for TTS / non-function-calling models). Doing it
        here means every provider — and the Google-TTS path that folds system
        text into user content — inherits dictionary support for free, and the
        directive survives the chat-decoration stripping non-FC models undergo.
        """
        stable = self.get_stable_system_text(config)
        turn_context = self.get_turn_context_text(config)
        if not turn_context:
            return stable
        return f"{stable}\n\n{turn_context}" if stable else turn_context

    def get_stable_system_text(self, config: UnifiedConfig) -> str | None:
        """The system instruction WITHOUT this turn's context-channel block.

        This is the byte-stable part — the same string every turn of a frozen
        conversation — so it is what a prompt-cache breakpoint should cover.
        Anthropic's translator caches this and sends the per-turn block as a
        second, uncached system block; a non-chat prompt-fold path (image / TTS)
        uses this so per-turn reference material is never spoken or drawn.
        """
        base = config.resolved_system_instruction
        dict_block = self._render_dictionary(config)
        if not dict_block:
            return base
        return f"{base}\n\n{dict_block}" if base else dict_block

    def get_turn_context_text(self, config: UnifiedConfig) -> str | None:
        """This turn's platform context block, framed, or None.

        🚨 THE PERSON'S TURN IS THE PERSON'S ALONE (2026-09-22). Platform
        material is delivered HERE, in the system channel, and never
        concatenated into a user message — see the header of
        ``matrx_ai/config/unified_content.py`` for the Masterwork interview
        answer that proves why no framing inside the person's turn is safe.
        """
        messages = getattr(config, "messages", None)
        render = getattr(messages, "render_turn_context", None)
        if render is None:
            return None
        return render()

    def _render_dictionary(self, config: UnifiedConfig) -> str:
        """Render config.dictionary into the shape this model class needs."""
        raw = getattr(config, "dictionary", None)
        if raw is None:
            return ""
        from matrx_ai.config.dictionary_config import DictionaryConfig

        dictionary = DictionaryConfig.coerce(raw)
        if dictionary is None or dictionary.is_empty:
            return ""
        return dictionary.render_for_system(supports_tools=getattr(config, "supports_tools", True))

    @staticmethod
    def _declaration_name(decl: dict[str, Any]) -> str | None:
        """Extract the tool name from a provider-formatted declaration.

        Handles every shape ``get_provider_format`` emits: a top-level ``name``
        (anthropic / google / openai-responses / mcp) and the nested
        ``function.name`` of the OpenAI Chat-Completions shape. Returns ``None``
        for nameless declarations (native provider tools like web search) so
        they are never deduplicated against each other.
        """
        if not isinstance(decl, dict):
            return None
        name = decl.get("name")
        if isinstance(name, str):
            return name
        fn = decl.get("function")
        if isinstance(fn, dict) and isinstance(fn.get("name"), str):
            return fn["name"]
        return None

    @staticmethod
    def _rewrite_declaration_name(decl: dict[str, Any], wire_name: str) -> dict[str, Any]:
        """Return a copy of ``decl`` with its name replaced by ``wire_name``,
        in whichever position :meth:`_declaration_name` found it (top-level
        ``name`` or nested ``function.name``). Shallow-copies only the dicts
        it touches — schemas and other nested structures are shared.
        """
        if isinstance(decl.get("name"), str):
            return {**decl, "name": wire_name}
        fn = decl.get("function")
        if isinstance(fn, dict) and isinstance(fn.get("name"), str):
            return {**decl, "function": {**fn, "name": wire_name}}
        return decl

    @staticmethod
    async def _capture_unserializable_tool_name(*, name: str, provider: str) -> None:
        """Put a provider-boundary declaration loss into the repair queue."""
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            ValueError("Tool declaration cannot be serialized for the provider"),
            kind="provider_tool_name_unserializable",
            route="providers.build_provider_tools",
            error_type="ToolNameSerializationError",
            context={"tool_name": name, "provider": provider},
        )

    @classmethod
    def _schedule_unserializable_tool_name_capture(cls, *, name: str, provider: str) -> None:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return
        detached_task(
            cls._capture_unserializable_tool_name(name=name, provider=provider),
            name="capture_provider_tool_name_unserializable",
        )

    def build_provider_tools(self, config: UnifiedConfig, provider: str) -> list[dict[str, Any]]:
        """Assemble the full tool-declaration list for a provider request —
        registered tools (``config.tools``) followed by inline custom tools
        (``config.custom_tools``) — DEDUPED BY NAME.

        This is the single, provider-agnostic chokepoint every translator must
        use to turn a ``UnifiedConfig`` into the request's ``tools`` array. It
        exists to make one class of failure structurally impossible: **a
        provider must never receive two tool declarations with the same name.**
        Anthropic rejects it with 400 ``"tools: Tool names must be unique."``;
        Gemini and OpenAI fail or silently degrade the same way.

        The same logical tool legitimately reaches this point twice: a single
        ``tool_def`` can carry both a ``server:matrx_ai`` executor (injected as a
        registered tool into ``config.tools``) AND a client-delegated executor
        (injected as an inline copy into ``config.custom_tools`` by a capability
        auto-load, e.g. browser-dom). ``merge_request_tools`` keys registered
        tools by registry UUID and inline tools by name, so a cross-bucket name
        collision slips past its dedup. We close it here, at the boundary.

        The FIRST occurrence wins. Registered tools are emitted before inline,
        so the registry-resolved declaration is authoritative; this never
        changes execution routing — which client/server executor actually runs
        is decided independently by the delegation resolver at call time.

        It is ALSO the single outbound wire-name seam: internal tool names may
        carry a namespace colon (``bundle:list_supabase``) which every provider
        rejects (``^[a-zA-Z0-9_-]{1,64}$``). Each declaration's name is
        rewritten to its wire form (``:`` → ``__``) here; the executor reverses
        the transform at dispatch. See ``matrx_ai.config.wire_names``.
        """
        from matrx_ai.config.wire_names import is_wire_safe, to_wire_name
        from matrx_ai.tools.registry import ToolRegistry

        declarations: list[dict[str, Any]] = []
        if config.tools:
            declarations.extend(
                ToolRegistry.get_instance().get_provider_tools(config.tools, provider)
            )
        if config.custom_tools:
            declarations.extend(t.get_provider_format(provider) for t in config.custom_tools)

        seen: set[str] = set()
        deduped: list[dict[str, Any]] = []
        dropped: list[str] = []
        # wire form → internal name, to catch two internal names collapsing
        # onto one wire name (e.g. ``a:b`` vs ``a__b``) — a duplicate the
        # name-level dedup above cannot see but the provider will 400 on.
        wire_owner: dict[str, str] = {}
        unsafe_dropped: list[str] = []
        for decl in declarations:
            name = self._declaration_name(decl)
            if name is None:
                deduped.append(decl)  # nameless native tool — never a dup
                continue
            if name in seen:
                dropped.append(name)
                continue
            seen.add(name)
            wire = to_wire_name(name)
            prior_owner = wire_owner.get(wire)
            if prior_owner is not None:
                vcprint(
                    {
                        "wire_name": wire,
                        "kept_internal_name": prior_owner,
                        "dropped_internal_name": name,
                        "provider": provider,
                    },
                    "🚨 [tools] WIRE-NAME COLLISION at the provider boundary — two "
                    "internal tool names serialize to the same wire name. The second "
                    "declaration was DROPPED to keep the request alive. Rename one of "
                    "the tools; ':' and '__' collapse to the same wire form.",
                    color="red",
                )
                continue
            if not is_wire_safe(wire):
                unsafe_dropped.append(name)
                self._schedule_unserializable_tool_name_capture(name=name, provider=provider)
                vcprint(
                    {
                        "internal_name": name,
                        "wire_name": wire,
                        "provider": provider,
                    },
                    "🚨 [tools] UNSERIALIZABLE TOOL NAME at the provider boundary — "
                    "the wire form still fails ^[a-zA-Z0-9_-]{1,64}$ (too long or "
                    "illegal characters). Declaration DROPPED so the request survives; "
                    "the tool is NOT callable this turn. Fix the tool's name at the "
                    "source (tool.definition row / registration).",
                    color="red",
                )
                continue
            wire_owner[wire] = name
            if wire != name:
                decl = self._rewrite_declaration_name(decl, wire)
            deduped.append(decl)

        if dropped:
            vcprint(
                data={
                    "provider": provider,
                    "duplicate_tool_names": sorted(set(dropped)),
                    "registered_tools": list(config.tools or []),
                    "custom_tools": [getattr(t, "name", None) for t in (config.custom_tools or [])],
                },
                title=(
                    "⚠️  [tools] Dropped duplicate tool declaration(s) at the provider "
                    "boundary — the same name was present in both config.tools "
                    "(registered) and config.custom_tools (inline), or twice within one "
                    "bucket. Providers reject duplicate tool names; kept the first "
                    "(registered) occurrence so the request still goes through. Root "
                    "cause is upstream double-injection (a tool_def with both a server and "
                    "a client-delegated executor injected as registered AND inline) — "
                    "fix it in merge_request_tools / the capability auto-load set."
                ),
                color="yellow",
                verbose=True,
            )
        return deduped

    @staticmethod
    def sanitize_structured_output_schema(schema: dict[str, Any], provider: str) -> dict[str, Any]:
        """Strip the JSON-Schema keywords ``provider``'s structured-output engine
        rejects, returning a provider-safe copy (the input is never mutated).

        THE single seam every structured-output boundary calls — the OpenAI-
        compatible chat builder here plus the Anthropic / OpenAI-Responses /
        Google response-schema builders — so the "provider 400s on an advisory
        keyword it doesn't support" class dies in ONE place for ALL providers.
        Grammar-constrained engines differ in which advisory bounds
        (minItems/maxItems/pattern/…) they accept; fine-tuned OpenAI models and
        several compatible providers reject bounds that standard OpenAI models
        now accept. The platform saves the RICHEST schema and applies the current
        conservative provider policy HERE, at send time. Structure that drives
        the grammar (type/enum/required/$ref/$defs) is untouched. Providers known
        to honor the full stored schema (Gemini) strip nothing — see
        ``unsupported_structured_output_keywords``.

        It also re-hoists the ``__kind`` discriminator to the FIRST property of
        every object node. A constrained decoder emits keys in the schema's
        ``properties`` order, so the discriminator's position in the schema is
        its position on the wire — and a live surface cannot route a streaming
        payload until ``__kind`` arrives. Property order does NOT survive a
        jsonb column (see ``hoist_discriminator_first``), so schemas reach this
        seam reordered no matter how they were authored. Applied for EVERY
        provider, including those that strip nothing."""
        from matrx_ai.schema.rules import (
            hoist_discriminator_first,
            strip_unsupported_keywords,
            unsupported_structured_output_keywords,
        )

        unsupported = unsupported_structured_output_keywords(provider)
        if unsupported:
            schema = strip_unsupported_keywords(schema, unsupported)
        return hoist_discriminator_first(schema)

    #: What each OPENAI-COMPATIBLE chat endpoint actually does with a structured
    #: output schema, measured one request per shape against the real provider on
    #: 2026-09-27 (groq ``openai/gpt-oss-20b``, cerebras ``gpt-oss-120b``, xai
    #: ``grok-4-fast-non-reasoning``, together
    #: ``meta-llama/Llama-3.3-70B-Instruct-Turbo``). PROVIDER FACTS, not opinions —
    #: re-measure before changing a row, and never level a provider down to the
    #: strictest just because it is easier: narrowing a shape a provider accepts
    #: throws the author's contract away for nothing.
    #:
    #: ``refuses_tuple_items``  — ``items: [A, B]`` (draft-4 tuple validation).
    #:     groq 400 "not valid against metaschema", xai 400 "is not of type
    #:     object/boolean", together 422 "failed to compile grammar".
    #: ``refuses_recursion``    — a self-referencing ``$def``. together answers
    #:     **500 Internal server error**; cerebras (strict) "Recursive schemas are
    #:     currently not supported".
    #: ``strict_subset``        — the endpoint applies OpenAI's full strict rules
    #:     when ``strict: true`` is sent, so an opt-in strict request needs the
    #:     whole strict pass: cerebras refuses maps, ``{}``, ``oneOf``, and an
    #:     object without ``additionalProperties: false``; groq refuses the last.
    #:
    #: A dangling ``$ref`` is refused by groq, xai, together AND cerebras — four
    #: more providers than the two the review found — so the hoist is
    #: unconditional below, not a row here.
    _OPENAI_COMPATIBLE_SUBSET: dict[str, dict[str, bool]] = {
        # `strict_unions`: groq judges every `anyOf` it is sent (measured live
        # 2026-09-28, openai/gpt-oss-20b): `required` beside no/empty
        # `properties` is refused; an `anyOf` branch that is a `$ref` to a
        # primitive or enum is refused ("anyOf branches must be disambiguated")
        # while the same branch inlined is accepted; two branches that both
        # admit null are refused. All three are respelled losslessly.
        "groq": {
            "refuses_tuple_items": True,
            "refuses_recursion": False,
            "strict_subset": True,
            "strict_unions": True,
        },
        "cerebras": {"refuses_tuple_items": True, "refuses_recursion": True, "strict_subset": True},
        "xai": {"refuses_tuple_items": True, "refuses_recursion": False, "strict_subset": True},
        "together": {"refuses_tuple_items": True, "refuses_recursion": True, "strict_subset": True},
        # A self-hosted OpenAI-compatible server (llama-server, vLLM, Ollama,
        # LocalAI) — unmeasurable from here, so it gets the SAFE assumptions.
        "generic_openai": {
            "refuses_tuple_items": True,
            "refuses_recursion": True,
            "strict_subset": True,
        },
    }

    @staticmethod
    def translate_openai_compatible_output_schema(
        schema: dict[str, Any], provider: str, *, strict: bool = False
    ) -> tuple[dict[str, Any], list[str], list[str]]:
        """Translate a declared schema into the subset an OPENAI-COMPATIBLE chat
        endpoint accepts. Returns ``(wire_schema, narrowed, relaxed)`` exactly like
        the Anthropic and OpenAI translators.

        🚨 Until 2026-09-27 the five providers that reach the wire through
        :meth:`build_openai_chat_response_format` — cerebras, groq, xai, together,
        generic_openai — got NONE of the translation work the Anthropic and OpenAI
        translators got: only ``sanitize_structured_output_schema`` (an advisory
        keyword strip plus the ``__kind`` hoist), and no ``note_translation``, so
        every compromise on those providers was invisible. Arman, 2026-09-27: a
        provider rejecting our request is OUR translator's bug — which makes this
        gap five providers' worth of bugs waiting.

        The rules applied here are the ones the providers themselves refuse,
        measured (:data:`_OPENAI_COMPATIBLE_SUBSET`), and nothing more. The review
        that found this gap reported groq 400ing on dynamic-key maps, empty ``{}``
        and objects missing ``additionalProperties: false``; re-measured at an
        adequate token budget, those three are 200 and the 400 was
        ``json_validate_failed`` — groq's server-side check of a TRUNCATED answer,
        not a rejection of the schema. So they are deliberately NOT narrowed here:
        emptying a map or collapsing a ``oneOf`` a provider accepts would throw the
        author's contract away to fix a problem that does not exist.

        What IS refused, and is therefore fixed here for every one of them:

        * a ``$ref`` that does not resolve from the document root (a nested
          ``$defs``) — groq, xai, together and cerebras all refuse it by name;
        * ``items: [A, B]`` — refused by groq, xai and together;
        * recursion, on the endpoints that cannot compile it (together answers
          **500**, which no caller can classify).

        ``strict=True`` means the caller asked for OpenAI's strict rules, which
        these endpoints do apply: the full strict pass runs, including the
        narrowings it forces, and every one of them is reported.
        """
        from matrx_ai.schema.lint import make_portable
        from matrx_ai.schema.rules import (
            NORMALIZATION_NOTES_KEY,
            classify_normalization_notes,
            OPEN_SCALAR_ITEM_SCHEMA,
            concretize_empty_schemas,
            dedupe_combinator_branches,
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

        subset = BaseTranslator._OPENAI_COMPATIBLE_SUBSET.get(
            provider, BaseTranslator._OPENAI_COMPATIBLE_SUBSET["generic_openai"]
        )
        narrowed: list[str] = []
        relaxed: list[str] = []

        # THE SHARED FIRST STEP every translator runs on the author's schema (what
        # the wire envelope carries): closed, all-required, optional fields
        # widened to nullable, `__kind` first. Idempotent on a stored portable copy.
        schema = make_portable(schema, notes=narrowed)

        # Lossless, and refused by name on four of the five: a `$ref` resolves from
        # the document ROOT, so a schema embedded whole under a parent's
        # `properties` points at nothing.
        schema = hoist_nested_defs(schema)
        if strict:
            schema = drop_refinement_combinators(schema, relaxed)
            schema = enforce_additional_properties_false(schema, maps="narrow", notes=narrowed)
        else:
            # `maps="keep"` leaves a dynamic-key map exactly as declared — the
            # providers accept it, so it stays enforceable.
            schema = enforce_additional_properties_false(schema, maps="keep", notes=narrowed)
        schema = BaseTranslator.sanitize_structured_output_schema(schema, provider)
        if strict:
            schema = flatten_allof(schema)
            schema = rewrite_oneof_as_anyof(schema)
            schema = normalize_combinator_siblings(schema)
            # An unspecified array ELEMENT becomes the widest shape a strict decoder
            # compiles (every scalar and null), named as a narrowing — never `string`.
            schema = concretize_empty_schemas(schema, item_placeholder=OPEN_SCALAR_ITEM_SCHEMA)
        # Lossless, and AFTER the block above because those rules are what creates
        # a duplicate branch (`make_portable` already dropped the author's own):
        # an emptied refinement branch concretized into the type its sibling
        # already had leaves `anyOf: [A, A]`, compiled twice for nothing on every
        # one of these endpoints (SCHEMA-TRANSLATION-VERIFY.md, F7).
        schema = dedupe_combinator_branches(schema)
        if subset.get("refuses_tuple_items"):
            schema = normalize_array_items(schema)
        schema = prune_unreachable_defs(schema)
        if subset.get("refuses_recursion"):
            schema = unroll_recursive_refs(schema, depth=4, notes=relaxed)
        if strict:
            schema = enforce_additional_properties_false(schema, maps="narrow", notes=narrowed)
            enforce_all_required(schema, express_optional_as_nullable=True, notes=narrowed)
        # An enum beside a type ARRAY — what `Optional[SomeEnum]` emits, and what the
        # widening above can create — becomes `anyOf` branches. Unconditional: it is
        # lossless, and the one strict-subset endpoint measured here refuses the
        # union form exactly as Anthropic does.
        schema = split_enum_from_type_union(schema)
        if subset.get("strict_unions"):
            from matrx_ai.schema.rules import disambiguate_unions_for_strict_validators

            schema = disambiguate_unions_for_strict_validators(schema)
        schema, notes = take_normalization_notes(schema)
        more_narrowed, more_relaxed = classify_normalization_notes(notes)
        narrowed.extend(more_narrowed)
        relaxed.extend(more_relaxed)
        schema.pop(NORMALIZATION_NOTES_KEY, None)
        return schema, narrowed, relaxed

    @staticmethod
    def build_openai_chat_response_format(
        response_format: Any, provider_name: str
    ) -> dict[str, Any] | None:
        """Convert the unified ``response_format`` to the OpenAI **Chat Completions** shape.

        Single source of truth shared by every OpenAI-compatible chat provider
        (cerebras, groq, xai, together, generic_openai). These all validate the
        identical contract:
          - ``{"type": "text"}``        → the DEFAULT; we NEVER transmit it (see below)
          - ``{"type": "json_object"}``                       (valid JSON, no schema)
          - ``{"type": "json_schema",
                "json_schema": {"name", "schema", "strict"?}}`` (schema-enforced)

        ``json_schema`` *requires* the nested ``json_schema`` object with a
        ``name`` and ``schema``; sending ``{"type": "json_schema"}`` alone 400s.

        ``{"type": "text"}`` is the implicit default of every OpenAI-compatible
        endpoint — sending it changes nothing about the output, so we return
        ``None`` and the caller omits ``response_format`` entirely. This is not a
        cosmetic cleanup: Cerebras rejects ``tools`` combined with ANY
        ``response_format`` (``"tools" is incompatible with "response_format"``,
        400 ``wrong_api_format``), so transmitting the no-op default turned every
        tool-bearing request whose saved config carried ``response_format={"type":
        "text"}`` (e.g. any agent run that auto-injects ctx_get/ctx_batch for
        deferred context) into a hard failure — while the identical agent run
        WITHOUT context tools succeeded. Never emitting the default eliminates
        that entire class of failure at the boundary, for every OpenAI-style
        provider, instead of patching it per provider.

        This builds ONLY the shape. Provider-specific quirks stay at the call
        site — e.g. Groq forbids json mode combined with tools, and the OpenAI
        *Responses* API / Anthropic / Google use entirely different shapes and do
        NOT call this method.

        ``provider_name`` is used only to label the loud downgrade warning.
        """
        if not isinstance(response_format, dict):
            return None

        fmt_type = response_format.get("type")
        if fmt_type == "text":
            return None
        if fmt_type == "json_object":
            return {"type": "json_object"}
        if fmt_type != "json_schema":
            # Unknown intent — pass through untouched rather than guess.
            return response_format

        # Locate name / strict / schema across the shapes response_format can
        # arrive in: a full OpenAI envelope ({name, schema, strict}), a raw JSON
        # Schema nested under json_schema, or a bare {"type": "json_schema"}
        # placeholder with no schema at all.
        inner = response_format.get("json_schema")
        name: str | None = None
        strict: bool | None = None
        schema: dict[str, Any] | None = None
        if isinstance(inner, dict):
            if isinstance(inner.get("schema"), dict):
                schema = inner["schema"]
                name = inner.get("name")
                strict = inner.get("strict")
            elif {"type", "properties", "items"} & inner.keys():
                schema = inner  # inner IS the raw JSON Schema
        elif isinstance(response_format.get("schema"), dict):
            schema = response_format["schema"]
            name = response_format.get("name")
            strict = response_format.get("strict")

        # json_schema mode requires a schema whose ROOT is an object
        # ({"type": "object"}). A missing schema, or an array/scalar-root schema
        # (e.g. a top-level list of records), can't be used. The frontend should
        # reject non-object roots up front, but we downgrade defensively to
        # json_object here so a slip-through still produces valid JSON instead of
        # a 400. This is a runtime ADJUSTMENT (schema is NOT enforced) — log it
        # loudly so it's never mistaken for the configured behaviour.
        downgrade_reason: str | None = None
        if not isinstance(schema, dict):
            downgrade_reason = "no JSON Schema was supplied with the json_schema request"
        elif not (
            schema.get("type") == "object"
            or (schema.get("type") is None and isinstance(schema.get("properties"), dict))
        ):
            downgrade_reason = (
                f"schema root is not an object (type={schema.get('type')!r}); "
                "an object root is required"
            )
        if downgrade_reason is not None:
            vcprint(
                data={
                    "provider": provider_name,
                    "requested": response_format,
                    "downgraded_to": "json_object",
                    "reason": downgrade_reason,
                },
                title=(
                    f"⚠️  {provider_name.upper()} ADJUSTMENT: json_schema → json_object — "
                    "schema is NOT enforced (valid JSON only). The frontend should reject "
                    "this; do NOT persist it as a saved config."
                ),
                color="yellow",
                verbose=True,
            )
            return {"type": "json_object"}

        # Reduce the schema to the subset THIS provider's structured-output engine
        # actually accepts — the SAME translation the Anthropic and OpenAI
        # translators do, per provider and measured against the real endpoint,
        # instead of only the advisory-keyword strip these five used to get.
        schema, narrowed, relaxed = BaseTranslator.translate_openai_compatible_output_schema(
            schema, provider_name, strict=bool(strict)
        )
        if narrowed or relaxed:
            from matrx_ai.providers.structured_output_findings import note_translation

            vcprint(
                data={"provider": provider_name, "narrowed": narrowed, "relaxed": relaxed},
                title=(
                    f"⚠️  {provider_name.upper()} ADJUSTMENT: the schema was translated to "
                    "the subset this endpoint accepts. The stored schema is unchanged, and "
                    "the answer is checked against it when the call ends "
                    "(schema.answer_contract.verify_answer_and_record)."
                ),
                color="yellow",
                verbose=True,
            )
            note_translation(
                provider_name,
                narrowed=narrowed,
                relaxed=relaxed,
                response_format=response_format,
            )

        json_schema_block: dict[str, Any] = {
            "name": name or "response",
            "schema": schema,
        }
        # `strict` carries OpenAI's hard strict rules, which these endpoints DO
        # apply (measured 2026-09-27: cerebras under strict refuses maps, `{}`,
        # `oneOf` and an object without additionalProperties:false; groq refuses
        # the last). It is set only when the caller opted in — and DELIBERATELY not
        # defaulted on: flipping it would force this boundary to empty every map
        # and collapse every `oneOf` these endpoints accept today, which throws the
        # author's contract away to buy enforcement nobody asked for. Whether the
        # contract actually held is settled per call, empirically, by the answer
        # check in `UnifiedAIClient._dispatch_with_billing_net`.
        if strict is not None:
            json_schema_block["strict"] = bool(strict)

        return {"type": "json_schema", "json_schema": json_schema_block}

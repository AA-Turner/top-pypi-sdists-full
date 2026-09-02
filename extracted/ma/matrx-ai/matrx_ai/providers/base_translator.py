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

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

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
        base = config.resolved_system_instruction
        dict_block = self._render_dictionary(config)
        if not dict_block:
            return base
        return f"{base}\n\n{dict_block}" if base else dict_block

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
    def sanitize_structured_output_schema(
        schema: dict[str, Any], provider: str
    ) -> dict[str, Any]:
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
        # actually accepts (per-provider — Cerebras/groq/xai/together/generic all
        # reject the advisory bounds; see sanitize_structured_output_schema).
        schema = BaseTranslator.sanitize_structured_output_schema(schema, provider_name)

        json_schema_block: dict[str, Any] = {
            "name": name or "response",
            "schema": schema,
        }
        # strict carries hard schema constraints (object root, a restricted JSON
        # Schema subset) — enabling it on an arbitrary schema can itself 400.
        # Only set it when the caller explicitly opted in.
        if strict is not None:
            json_schema_block["strict"] = bool(strict)

        return {"type": "json_schema", "json_schema": json_schema_block}

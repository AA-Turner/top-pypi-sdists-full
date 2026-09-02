from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime

from .content_blocks_manager import get_content_blocks_manager
from .pattern_parser import resolve_matrx_patterns

# ---------------------------------------------------------------------------
# The "Current date" decoration — pinned once, uniquely marked, never doubled
# ---------------------------------------------------------------------------
#
# The date is a chat-only DECORATION. It must NEVER live inside base_instruction
# and it must be BYTE-STABLE for the whole life of a conversation (a system
# prefix that changes even one byte between rounds destroys prompt caching).
#
# Two failure classes this section makes extinct:
#
#   1. MIDNIGHT DRIFT — rendering ``datetime.now()`` fresh on every ``__str__``
#      silently changes the date at midnight, busting the cache mid-conversation
#      and showing the model an inconsistent date. FIX: the value is pinned once
#      (from an immutable host anchor, e.g. the conversation's ``created_at``, or
#      a single memoized ``now()`` fallback) and reused verbatim forever.
#
#   2. DOUBLE INJECTION — a previously-RENDERED system string fed back as
#      ``base_instruction`` on a DB reload would get the date prepended AGAIN,
#      one copy per persist↔reload cycle (the "Current date ×N" bug). The old
#      guard only matched a LEADING, exact-format line, so an ``intro`` (date no
#      longer leading) or any format shift defeated it. FIX: every date block is
#      wrapped in a unique sentinel and stripped ANYWHERE, ANY COUNT on ingest —
#      re-injection is structurally impossible and corrupted rows self-heal.
#
# The sentinel is an HTML comment: unique + greppable for us, invisible/ignored
# by every LLM. NEVER change these tokens without a migration — old rows carry
# them.
DATE_BLOCK_OPEN = "<!--matrx:current_date-->"
DATE_BLOCK_CLOSE = "<!--matrx:/current_date-->"

# Strip a sentinel-wrapped date block wherever it appears (DOTALL: the marked
# span may include newlines), any number of times.
_DATE_BLOCK_RE = re.compile(
    re.escape(DATE_BLOCK_OPEN) + r".*?" + re.escape(DATE_BLOCK_CLOSE),
    re.DOTALL,
)
# Backward-compat: rows written before the sentinel existed carry one OR MORE
# LEADING bare "Current date: YYYY-MM-DD" lines. Strip those too so legacy /
# already-corrupted rows self-heal on the next ingest.
_LEGACY_LEADING_DATE_RE = re.compile(r"^(?:Current date: \d{4}-\d{2}-\d{2}[ \t]*(?:\r?\n)+)+")


def render_date_block(date_str: str) -> str:
    """Render the sentinel-wrapped ``Current date`` decoration.

    The unique markers make the block recognizable (so it is never injected
    twice) and idempotently strippable (see ``strip_date_decorations``)."""
    return f"{DATE_BLOCK_OPEN}Current date: {date_str}{DATE_BLOCK_CLOSE}"


def strip_date_decorations(text: str) -> str:
    """Remove EVERY auto-injected ``Current date`` decoration from a system
    string so a rendered instruction can be safely re-ingested as
    ``base_instruction`` without ever duplicating the date at the next render.

    Removes sentinel-wrapped blocks anywhere in the text (current format) and
    leading bare ``Current date: …`` lines (legacy format), then trims the
    surrounding blank lines the removal leaves behind."""
    if not text:
        return text
    text = _DATE_BLOCK_RE.sub("", text)
    text = _LEGACY_LEADING_DATE_RE.sub("", text)
    return text.strip("\r\n")


# Back-compat alias: older imports referenced the leading-only name. Kept so
# external callers don't break; both now route through the robust strip.
strip_leading_date_decorations = strip_date_decorations


@dataclass
class SystemInstruction:
    """
    Flexible system instruction builder with optional components.
    Always returns a string when converted.
    """

    base_instruction: str
    intro: str = field(default_factory=str)
    outro: str = field(default_factory=str)
    append_sections: list[str] = field(default_factory=list)
    prepend_sections: list[str] = field(default_factory=list)
    content_blocks: list[str] = field(default_factory=list)
    tools_list: list[str] = field(default_factory=list)
    # Matrx Directives the agent can emit (output_directive types, e.g. "create_task").
    # The author sets `include_actions_guidance`; the resolver populates
    # `action_types` from the agent's output_schema at dispatch (resolved_system_
    # instruction). When non-empty, `_actions_guidance` is rendered like tools_list.
    action_types: list[str] = field(default_factory=list)

    # Optional flags for built-in sections
    include_date: bool = True
    include_code_guidelines: bool = False
    include_safety_guidelines: bool = False
    include_actions_guidance: bool = False

    # The date decoration is pinned ONCE and reused verbatim forever (see the
    # module header). ``date_anchor`` is the immutable, host-supplied value
    # (``YYYY-MM-DD``) — the resolver sets it from the conversation's persisted
    # ``created_at`` so the date is byte-identical across every turn AND every
    # reload for the conversation's whole life. When no anchor is supplied
    # (fresh, conversation-less runs), ``_pinned_date`` memoizes a single
    # ``now()`` so a live object still never drifts across midnight.
    date_anchor: str | None = None
    _pinned_date: str | None = field(default=None, init=False, repr=False)

    # Custom metadata (not rendered, just for tracking)
    version: str | None = None
    category: str | None = None

    # Controlled context injection — set via inject_context_block(), never directly
    include_context_block: bool = True
    injected_context_block: str | None = field(default=None, init=False, repr=False)

    # Internal cache for fetched content blocks
    _content_blocks_cache: list[str] = field(default_factory=list, init=False, repr=False)

    def effective_date(self) -> str:
        """The pinned ``YYYY-MM-DD`` date for this instruction.

        Prefers the immutable ``date_anchor`` (host-pinned to conversation
        creation). Falls back to a single memoized ``now()`` so the value never
        changes for the life of this object — no midnight drift within a run."""
        if self.date_anchor:
            return self.date_anchor
        if self._pinned_date is None:
            self._pinned_date = datetime.now().strftime("%Y-%m-%d")
        return self._pinned_date

    def inject_context_block(self, block: str) -> None:
        """Inject a condensed context awareness block into the system prompt.

        Idempotent — calling multiple times replaces the previous block.
        Has no effect when include_context_block is False (agent opted out).
        Only the infrastructure layer (apply_context_objects) calls this;
        agent developers should never call it directly.
        """
        if self.include_context_block:
            self.injected_context_block = block

    def clear_context_block(self) -> None:
        """Remove the injected context block (called after a turn completes)."""
        self.injected_context_block = None

    def strip_chat_decorations(self) -> None:
        """Drop chat-only auto-decorations, leaving the agent's own directive.

        The auto-prepended date ("Current date: …"), the tools-available list,
        the code/safety guidelines, and the context-awareness block are
        meaningful only for a chat/text model. A non-chat model (TTS / image /
        video) would speak them aloud or bake them into its generation prompt.
        The capability layer calls this for any model without FUNCTION_CALLING —
        the single, model-agnostic place decorations are gated (see
        unified_client), so it covers EVERY dispatch path, not just the HTTP
        routes.
        """
        self.include_date = False
        self.tools_list = []
        self.action_types = []
        self.include_actions_guidance = False
        self.include_code_guidelines = False
        self.include_safety_guidelines = False
        self.include_context_block = False
        self.injected_context_block = None

    async def load_content_blocks(self) -> SystemInstruction:
        """
        Fetch and cache content blocks from database.
        Call this before converting to string if you need content blocks.
        Returns self for chaining.
        """
        if self.content_blocks and not self._content_blocks_cache:
            manager = get_content_blocks_manager()
            for block_id in self.content_blocks:
                block_text = await manager.get_template_text(block_id)
                if block_text:
                    self._content_blocks_cache.append(block_text)
        return self

    def __str__(self) -> str:
        """Convert to final system instruction string"""
        parts = []

        # Author-owned text can arrive with a date decoration already baked in
        # (e.g. a previously-rendered string handed straight to the constructor,
        # bypassing from_value's strip). We strip it from EVERY author field
        # before assembly so the ONLY date that survives is the single, pinned,
        # sentinel-marked block we inject below — double injection is impossible
        # regardless of how this object was built.
        def _clean(text: str) -> str:
            return strip_date_decorations(text) if text else text

        # Always at the start
        if self.intro:
            parts.append(_clean(self.intro))

        # Date — pinned once, uniquely marked so it can never be doubled.
        if self.include_date:
            parts.append(render_date_block(self.effective_date()))

        # Prepended sections first
        if self.prepend_sections:
            parts.extend(_clean(s) for s in self.prepend_sections)

        # Base instruction (required)
        parts.append(_clean(self.base_instruction))

        # Optional built-in sections (after base)
        if self.tools_list:
            parts.append(self._tools_available(self.tools_list))

        if self.action_types:
            parts.append(self._actions_guidance(self.action_types))

        if self.include_code_guidelines:
            parts.append(self._code_guidelines())

        if self.include_safety_guidelines:
            parts.append(self._safety_guidelines())

        # Add cached content blocks (if loaded)
        if self._content_blocks_cache:
            parts.extend(_clean(s) for s in self._content_blocks_cache)

        # Appended sections last
        if self.append_sections:
            parts.extend(_clean(s) for s in self.append_sections)

        # Controlled context injection (deferred context awareness block)
        if self.injected_context_block:
            parts.append(_clean(self.injected_context_block))

        if self.outro:
            parts.append(_clean(self.outro))

        result = "\n\n".join(filter(None, parts))

        # Resolve any <<MATRX>> data-fetch patterns in the final string
        return resolve_matrx_patterns(result)

    @staticmethod
    def _tools_available(tools_list: list[str]) -> str:
        tools_List_string = "\n  * ".join(tools_list) if tools_list else ""
        return f"""## Tools/Functions Available
- You have the following tools available to you:
  * {tools_List_string}
  
- Utilize these tools ONLY if they will help you better handle the user's request.
- If a tool repeatedly fails to give you the expected result, stop using it and move to a different approach."""

    @staticmethod
    def _actions_guidance(action_types: list[str]) -> str:
        """Guidance describing the Matrx Directives this agent may emit. The model's
        output_schema (response_format) already constrains the exact envelope;
        this tells it WHEN/HOW to use it and lists the available action types."""
        bullets = "\n  * ".join(action_types) if action_types else ""
        return f"""## Available Kind Directives
- When the user's request calls for it, you can perform an action by emitting a
  Kind Directive as your final structured output — `__kind` FIRST, then items:
  `{{"__kind": "<directive>", "items": [ ... ]}}`
- Available directive(s):
  * {bullets}
- Follow your output schema for the exact item fields. Emit a directive ONLY when
  it genuinely fulfils the request; otherwise respond normally."""

    @staticmethod
    def _code_guidelines() -> str:
        return """## Code Guidelines
- Use TypeScript with strict typing
- Follow React 19 best practices
- Prefer functional components with hooks"""

    @staticmethod
    def _safety_guidelines() -> str:
        return """## Safety Guidelines
- Never expose sensitive credentials
- Validate all user inputs
- Follow security best practices"""

    def to_string(self) -> str:
        """Explicit conversion method (alternative to __str__)"""
        return str(self)

    def to_storage_text(self) -> str:
        """System text for PERSISTENCE.

        A conversation's prompt is now frozen after its first completed turn.
        Persist the fully rendered first-turn text so skills, action guidance,
        context awareness, and resolved patterns cannot disappear or be rebuilt
        differently on a continuation. ``from_value`` strips and re-pins the
        date decoration on reload, preserving its byte-stable value.
        """
        return str(self)

    @classmethod
    def from_value(cls, value: str | dict | SystemInstruction) -> SystemInstruction:
        """
        Single entry point to create a SystemInstruction from any supported input.

        - str: Treated as base_instruction. All defaults apply (include_date=True, etc.).
        - dict: Keys map to constructor args. "content" is accepted as an alias for
          "base_instruction". All unrecognized keys are ignored.
        - SystemInstruction: Returned as-is.

        This is the sync path used by UnifiedConfig.__post_init__. For async
        content_blocks loading, use from_dict() instead.
        """
        if isinstance(value, cls):
            return value

        if isinstance(value, str):
            # A reload may hand us a previously-RENDERED system string with the
            # date decoration baked in — strip it so the renderer doesn't double it.
            return cls(base_instruction=strip_date_decorations(value))

        if isinstance(value, dict):
            base_instruction = value.get("base_instruction", "")
            content = value.get("content", "")
            if content:
                if base_instruction:
                    base_instruction = f"{base_instruction}\n\n{content}"
                else:
                    base_instruction = content
            base_instruction = strip_date_decorations(base_instruction)

            return cls(
                base_instruction=base_instruction,
                intro=value.get("intro", ""),
                outro=value.get("outro", ""),
                append_sections=value.get("append_sections", []),
                prepend_sections=value.get("prepend_sections", []),
                content_blocks=value.get("content_blocks", []),
                tools_list=value.get("tools_list", []),
                action_types=value.get("action_types", []),
                date_anchor=value.get("date_anchor"),
                include_date=value.get("include_date", True),
                include_code_guidelines=value.get("include_code_guidelines", False),
                include_safety_guidelines=value.get("include_safety_guidelines", False),
                include_actions_guidance=value.get("include_actions_guidance", False),
                include_context_block=value.get("include_context_block", True),
                version=value.get("version"),
                category=value.get("category"),
            )

        raise TypeError(f"Cannot create SystemInstruction from {type(value)}")

    @classmethod
    async def from_dict(cls, data: dict) -> SystemInstruction:
        """
        Create a SystemInstruction from a dict and load content blocks (async).

        Delegates dict parsing to from_value(), then awaits content_blocks loading.
        Use this when the dict may contain content_blocks that require DB fetches.
        """
        # Handle legacy traditional format: {"role": "system", "content": "..."}
        if "role" in data and "content" in data and "base_instruction" not in data:
            if "intro" in data:
                data = {**data, "base_instruction": data["content"]}
            else:
                data = {**data, "base_instruction": "", "intro": data["content"]}
            data.pop("role", None)

        instance = cls.from_value(data)
        await instance.load_content_blocks()
        return instance

    @classmethod
    def for_code_review(cls, language: str = "TypeScript") -> SystemInstruction:
        return cls(
            base_instruction=f"You are an expert {language} code reviewer",
            include_code_guidelines=True,
            include_safety_guidelines=True,
            category="code-review",
        )

    @classmethod
    def for_ai_matrix(cls, additional_context: str = "") -> SystemInstruction:
        return cls(
            intro="You are 'AI MATRX Assistant'. The most advanced & intelligent assistant in the universe.",
            base_instruction="You are able to solve any problem, answer any question, and help with any task. Even though your knowledge cutoff may be months or years ago, you know today's date.",
            append_sections=[additional_context] if additional_context else [],
            outro="Always think about the user's request carefully and identify what they really want and then think through the best possible response.",
        )

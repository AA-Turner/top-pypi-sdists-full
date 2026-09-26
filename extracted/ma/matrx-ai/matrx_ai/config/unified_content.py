import base64
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from google.genai.types import Part
from matrx_utils import vcprint

from matrx_ai.config.decision_input_config import (
    DecisionAnswersContent,
    DecisionQuestionsContent,
)
from matrx_ai.config.speech_script_config import SpeechScriptContent
from matrx_ai.config.config_utils import (
    decode_binary_metadata,
    encode_binary_metadata,
)
from matrx_ai.config.extra_config import (
    CodeExecutionContent,
    CodeExecutionResultContent,
    HostedToolContent,
    WebSearchCallContent,
)
from matrx_ai.config.media_config import (
    AudioContent,
    DocumentContent,
    ImageContent,
    VideoContent,
    YouTubeVideoContent,
    reconstruct_media_content,
)
from matrx_ai.config.structured_input_config import (
    STRUCTURED_INPUT_TYPE_MAP,
    AgentAppInputContent,
    AgentInputContent,
    ContextInputContent,
    DataInputContent,
    DocumentInputContent,
    ListInputContent,
    NotesInputContent,
    ProjectInputContent,
    TableInputContent,
    TaskInputContent,
    TranscriptInputContent,
    TranscriptSessionInputContent,
    WebpageInputContent,
    WorkbookInputContent,
    reconstruct_structured_input,
)

from .tools_config import ToolCallContent, ToolResultContent

# ============================================================================


# THE PERSON'S TURN IS THE PERSON'S ALONE (2026-09-22).
#
# Platform material used to be concatenated INTO the user message's text,
# wrapped in a `<turn_context source="platform" speaker="not_the_user">` frame
# whose note told the model "the user did not write it ... Do not respond to
# it". On 2026-09-22 a Masterwork Scout interview (chat.conversation
# 2eefaf04-1d23-4db5-82a6-1d3c0bfc870e, position 17) opened its answer to an
# Expert with "Ignoring the injected block -- that's platform noise, not from
# you." The frame worked exactly as written and the model narrated its own
# compliance at a person who cannot see the block and has no idea what was
# injected into her words.
#
# There is no wording that fixes that while the block is inside her turn: the
# model answers her turn, so anything inside it is answerable. So the block
# left the turn. Per-turn platform material now travels in the CONTEXT CHANNEL
# -- MessageList.attach_turn_context() -> the provider's system channel (see
# providers/base_translator.get_system_text). TextContent carries what its
# author wrote and nothing else; there is deliberately no attach_ephemeral()
# door here any more.


# ============================================================================
# CORE UNIFIED TYPES (Provider-Agnostic - Pure/Reusable)
# These types are completely independent of AI Matrix
# ============================================================================


@dataclass
class TextContent:
    type: Literal["text"] = "text"
    text: str = ""
    id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_output(self) -> str:
        """Get the output text of the content."""
        return self.text

    def replace_variables(self, variables: dict[str, Any]) -> bool:
        """Substitute ``{{variable_name}}`` patterns in the text.

        Returns True iff this block should be DROPPED from the message —
        which happens when the block is role-tagged (e.g. via
        ``metadata.role = "negative_prompt"``) AND the post-substitution
        text is empty/whitespace. Role-tagged TextContent is a NAMED slot
        for the translator (negative prompt, style prompt, etc.); an empty
        slot means the user opted out and we should not pass empty text
        to the provider.

        Untagged TextContent (the main user prompt) never returns True —
        empty text is harmless ("Hello {{name}}" with name="" is just
        "Hello ", not a system fault).
        """
        original_text = self.text
        # THE PROMPT DOOR (round-1 F4): every variable that becomes prompt
        # text passes through prompt_safe_value here — structured values get
        # kind markers stripped and render as canonical JSON (never Python
        # repr), scalars stay scalars. This is the choke point, so no caller
        # has to remember the law.
        from matrx_ai.config.prompt_values import prompt_safe_value
        from matrx_ai.config.template_substitution import substitute_authored

        # Values are DATA: only placeholders the author wrote are slots, across
        # every pass (config/template_substitution.py). The first-seen text is
        # the authored template for the life of this block.
        template = getattr(self, "_authored_template", None)
        if template is None:
            template = original_text
            self._authored_template = template
        replaced_text = substitute_authored(original_text, template, variables, prompt_safe_value)
        self.text = replaced_text
        # AGT-N-7's first case: a placeholder nobody declared is still standing here,
        # verbatim, and used to reach the model with no warning anywhere in the chain.
        # This is the same choke point `prompt_safe_value` uses, so the law is recorded
        # once rather than remembered by every caller. It RECORDS and does not erase —
        # substitution is multi-pass (picklist envelopes, staged fence swaps, the
        # executor's send-clone), so eating an unresolved brace here would destroy a
        # later pass. See matrx_ai/config/undeclared.py.
        from matrx_ai.config.undeclared import note_unresolved

        note_unresolved(replaced_text, template=template)
        role = (self.metadata or {}).get("role")
        had_template = "{{" in original_text and "}}" in original_text
        if role and had_template and not replaced_text.strip():
            return True
        return False

    def append_text(self, text: str, separator: str = "\n") -> None:
        """
        Append text to existing content.

        Args:
            text: The text to append
            separator: Separator between existing and new text (default: newline)
        """
        self.text += f"{separator}{text}"

    def to_google(self) -> dict[str, Any]:
        """Convert to Google Gemini format"""
        part = {"text": self.text}
        # Retrieve Google's thought signature from metadata if present
        if "google_thought_signature" in self.metadata:
            part["thoughtSignature"] = self.metadata["google_thought_signature"]
        return part

    def to_openai(self, role: str | None = None) -> dict[str, Any]:
        """Convert to OpenAI format"""
        # Assistant messages use output_text, all others use input_text
        text_type = "output_text" if role == "assistant" else "input_text"
        return {"type": text_type, "text": self.text}

    def to_anthropic(self) -> dict[str, Any]:
        """Convert to Anthropic format"""
        return {"type": "text", "text": self.text}

    def _sanitize_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """DISPLAY ONLY — a human-readable stand-in for encrypted material.

        🚨 Used by ``__repr__`` and NOTHING that is rebuilt from. Replacing a
        value with ``<bytes length=N>`` destroys it; a dict carrying that
        placeholder cannot be re-issued to a provider. Serializers use
        ``encode_binary_metadata`` instead.

        Replaces these fields with their lengths:
        - anthropic_signature: str
        - google_thought_signature: bytes
        - encrypted_content: bytes
        """
        sanitized = metadata.copy()

        # Replace sensitive fields with length info
        if "anthropic_signature" in sanitized:
            sanitized["anthropic_signature"] = (
                f"<str length={len(sanitized['anthropic_signature'])}>"
            )

        if "google_thought_signature" in sanitized:
            sanitized["google_thought_signature"] = (
                f"<bytes length={len(sanitized['google_thought_signature'])}>"
            )

        if "encrypted_content" in sanitized:
            sanitized["encrypted_content"] = f"<bytes length={len(sanitized['encrypted_content'])}>"

        return sanitized

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary, LOSSLESSLY — binary metadata rides base64 under
        ``<key>__b64`` and ``reconstruct_content`` decodes it back to bytes.
        Use this instead of dataclasses.asdict(); for a printable form use
        ``repr()``, which is where the redacting display helper lives.
        """
        return {
            "type": self.type,
            "text": self.text,
            "id": self.id,
            "metadata": encode_binary_metadata(self.metadata),
        }

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format for database persistence (cx_message.content JSONB).

        ``self.text`` IS the pristine authored text — per-turn platform material
        never touches it any more (it travels in the context channel; see the
        module header). ``metadata["original_text"]`` is honoured for rows that
        predate that change.
        """
        text = self.metadata.get("original_text", self.text)
        result: dict[str, Any] = {"type": "text", "text": text}
        if self.id:
            result["id"] = self.id
        citations = self.metadata.get("citations")
        if citations:
            result["citations"] = citations
        return result

    def __repr__(self) -> str:
        """Override repr to show sanitized metadata instead of full encrypted content"""
        sanitized_metadata = self._sanitize_metadata(self.metadata)

        # Show first 35 and last 35 characters with ... in the middle
        if len(self.text) > 70:
            text_preview = f"{self.text[:35]}...{self.text[-35:]}"
        else:
            text_preview = self.text

        return (
            f"TextContent(type={self.type!r}, "
            f"text={text_preview!r}, "
            f"id={self.id!r}, "
            f"metadata={sanitized_metadata!r})"
        )

    @classmethod
    def from_openai(
        cls, content_item: Any, id: str
    ) -> Optional["TextContent"]:
        from matrx_ai.config.citations import normalize_openai_annotation

        text = content_item.text
        metadata = content_item.model_dump(exclude={"text"})
        metadata["id"] = id

        # Normalize Responses-API annotations (url_citation et al.) into the
        # canonical citations shape. The raw annotations stay in
        # metadata["annotations"] via the blanket model_dump above; each
        # normalized item also carries its original payload in ``raw``.
        annotations = metadata.get("annotations") or []
        if annotations:
            metadata["citations"] = [
                normalize_openai_annotation(annotation, text or "").model_dump(exclude_none=True)
                for annotation in annotations
            ]

        return cls(
            id=id,
            text=text,
            metadata=metadata,
        )

    @classmethod
    def from_openai_modified(cls, content_item: dict[str, Any]) -> Optional["TextContent"]:
        from matrx_ai.config.citations import normalize_openai_annotation

        text = content_item.get("content")
        metadata = content_item.get("metadata") or {}
        # Second OpenAI ingestion path — must capture annotations exactly like
        # from_openai, else citations silently vanish on this route.
        annotations = (
            content_item.get("annotations")
            or (metadata.get("annotations") if isinstance(metadata, dict) else None)
            or []
        )
        if annotations and isinstance(metadata, dict) and not metadata.get("citations"):
            metadata["citations"] = [
                normalize_openai_annotation(annotation, text or "").model_dump(exclude_none=True)
                for annotation in annotations
            ]
        return cls(
            text=text,
            metadata=metadata,
        )

    @classmethod
    def from_google(cls, part: Part) -> Optional["TextContent"]:
        """Create TextContent from Google Part object"""
        metadata = {}
        # Store Google's thought signature in metadata if present
        if part.thought_signature:
            metadata["google_thought_signature"] = part.thought_signature
        return cls(
            text=part.text,
            metadata=metadata,
        )

    @classmethod
    def from_anthropic(cls, content_block: dict[str, Any]) -> Optional["TextContent"]:
        """Create TextContent from Anthropic content block.

        Citations are normalized to the canonical ``NormalizedCitation`` shape
        at this ingestion point (raw provider payload preserved inside each
        item's ``raw``) — ``metadata["citations"]`` NEVER holds raw provider
        dicts past here.
        """
        from matrx_ai.config.citations import normalize_anthropic_citation

        metadata = {}
        citations = content_block.get("citations", [])
        if citations:
            metadata["citations"] = [
                normalize_anthropic_citation(citation).model_dump(exclude_none=True)
                for citation in citations
            ]
        return cls(
            text=content_block["text"],
            metadata=metadata,
        )


@dataclass
class SearchResultContent:
    """A CITABLE search/tool-result passage — the platform primitive that makes
    tool output quotable-with-citations.

    Any tool that returns passages the model may quote (document_search,
    rag_search, scrapers, …) emits these via ``ToolResult.provider_content``
    instead of JSON text. On the Anthropic wire each becomes a
    ``search_result`` block with citations enabled, so a model quote comes
    back as a ``search_result_location`` citation whose ``source`` echoes our
    ``matrx://`` identity URI — file_id + page round-trip with zero
    request-side bookkeeping (see ``config/citations.py``). Other providers
    receive a readable text rendering (no citation machinery to feed).

    ``texts`` is a LIST deliberately: each entry is its own inner text block,
    so Anthropic's block-level citations can point at ONE passage
    (``start_block_index``/``end_block_index``) instead of the whole result.
    """

    type: Literal["search_result"] = "search_result"
    texts: list[str] = field(default_factory=list)
    title: str = ""
    source: str = ""
    file_id: str = ""
    document_id: str = ""
    page: int | None = None
    # Anthropic requires ONE citations posture across every search_result
    # block in a request (wire invariant 2, config/citations.py) — flipping
    # this off for a single block among enabled ones is a 400. The translator
    # enforces uniformity at the wire; leave this True unless the whole
    # request is citations-off (machine runs strip there, not here).
    citations_enabled: bool = True
    id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_output(self) -> str:
        return "\n\n".join(t for t in self.texts if t)

    def resolved_source(self) -> str:
        """Explicit ``source`` wins; else build the matrx:// identity URI."""
        if self.source:
            return self.source
        from matrx_ai.config.citations import build_matrx_citation_source

        return build_matrx_citation_source(
            file_id=self.file_id or None,
            page=self.page,
            document_id=self.document_id or None,
        )

    def _render_text(self) -> str:
        """Readable fallback for providers without search_result blocks."""
        header = self.title or "Search result"
        source = self.resolved_source()
        lines = [f"[{header}]" + (f" ({source})" if source else "")]
        lines.extend(t for t in self.texts if t)
        return "\n".join(lines)

    def to_anthropic(self) -> dict[str, Any] | None:
        texts = [t for t in self.texts if t]
        if not texts:
            return None
        block: dict[str, Any] = {
            "type": "search_result",
            "source": self.resolved_source() or "matrx://unknown",
            "title": self.title or "Search result",
            "content": [{"type": "text", "text": t} for t in texts],
        }
        if self.citations_enabled:
            from matrx_ai.config.citations import search_result_citations

            block["citations"] = search_result_citations()
        return block

    def to_openai(self, role: str | None = None) -> dict[str, Any]:
        return {"type": "input_text", "text": self._render_text()}

    def to_google(self) -> dict[str, Any]:
        return {"text": self._render_text()}

    @property
    def text(self) -> str:
        """Serializer fallback (``_serialize_block_for_google`` reads ``.text``)."""
        return self._render_text()

    def to_dict(self) -> dict[str, Any]:
        return self.to_storage_dict()

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "search_result",
            "texts": list(self.texts),
            "title": self.title,
            "source": self.resolved_source(),
        }
        if self.file_id:
            result["file_id"] = self.file_id
        if self.document_id:
            result["document_id"] = self.document_id
        if self.page is not None:
            result["page"] = self.page
        if self.id:
            result["id"] = self.id
        return result


def cap_citable_blocks(
    blocks: list["SearchResultContent"], meta: dict[str, Any]
) -> list["SearchResultContent"]:
    """Enforce the platform citable-text budget on a live builder's passage
    blocks (MAX_CITABLE_TEXT_CHARS, config/citations.py). Whole lowest-ranked
    blocks drop first; the drop is recorded on ``meta['passages_dropped']`` and
    announced. This is the tool-side half of the size contract — provider
    typed-block lists bypass the string size gates, so builders MUST bound
    their own citable payload (the absolute ceiling backstop still alarms)."""
    from matrx_utils import vcprint

    from matrx_ai.config.citations import MAX_CITABLE_TEXT_CHARS

    kept: list[SearchResultContent] = []
    total = 0
    dropped = 0
    for block in blocks:
        block_chars = sum(len(t) for t in block.texts if t)
        if kept and total + block_chars > MAX_CITABLE_TEXT_CHARS:
            dropped += 1
            continue
        kept.append(block)
        total += block_chars
    if dropped:
        meta["passages_dropped"] = dropped
        vcprint(
            f"[citations] dropped {dropped} citable passage block(s) over the "
            f"{MAX_CITABLE_TEXT_CHARS}-char budget (kept {len(kept)}, {total} chars).",
            color="yellow",
        )
    return kept


@dataclass
class ThinkingContent:
    """
    Extended thinking content with normalized provider identification.

    Normalization:
    - provider: Explicitly identifies which AI provider generated this content
    - signature: Unified field for provider-specific encrypted/signature data
      (OpenAI's encrypted_content, Anthropic's signature, Google's thought_signature)
    - signature_encoding: "base64" iff `signature` was originally bytes and got
      base64-encoded for storage. None for opaque strings (OpenAI/Anthropic) that
      round-trip verbatim. Always emitted in to_storage_dict() so readers never
      have to guess whether absence means "raw" or "writer forgot to set it".

    Each provider can only process its own signature data. The to_* methods
    check the provider field and only include signature if it matches.
    """

    type: Literal["thinking"] = "thinking"
    text: str = ""
    id: str = ""
    summary: list[dict[str, Any]] = field(default_factory=list)

    # Normalized fields for database storage
    provider: (
        Literal[
            "openai",
            "anthropic",
            "google",
            "cerebras",
            "moonshot",
            "together",
            "groq",
            "xai",
            "generic_openai",
        ]
        | None
    ) = None
    signature: str | bytes | None = None  # Provider-specific encrypted/signature data
    signature_encoding: Literal["base64"] | None = None

    # metadata for truly optional/non-essential data only
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_output(self) -> str:
        text_output = ""
        if self.text:
            text_output += self.text
        if self.summary:
            text_output += "\n".join([item["text"] for item in self.summary])
        return text_output

    def _sanitize_signature(self) -> str:
        """Return a sanitized representation of the signature for display."""
        if self.signature is None:
            return "None"
        if isinstance(self.signature, bytes):
            return f"<bytes length={len(self.signature)}>"
        return f"<str length={len(self.signature)}>"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary, LOSSLESSLY and JSON-safely.

        A `bytes` signature (Google's thought_signature) is base64-encoded and
        tagged `signature_encoding="base64"` — the SAME contract
        `to_storage_dict` writes and `reconstruct_content` reads. Emitting the
        raw bytes here made any JSON coercion of this dict fall back to
        `repr()`, silently turning the signature into the string `b'...'`.
        Use `repr()` for a printable form.
        """
        signature_out: str | None = None
        encoding_out: str | None = self.signature_encoding
        if self.signature is not None:
            if isinstance(self.signature, bytes):
                signature_out = base64.b64encode(self.signature).decode("ascii")
                encoding_out = "base64"
            else:
                signature_out = self.signature

        result: dict[str, Any] = {
            "type": self.type,
            "text": self.text,
            "id": self.id,
            "summary": self.summary,
            "provider": self.provider,
            "signature": signature_out,
            "signature_encoding": encoding_out,
        }
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format for database persistence (cx_message.content JSONB).

        Contract: `signature_encoding` is always present in the output so readers
        never have to guess. It is `"base64"` iff `signature` is a base64-encoded
        binary blob (Google's thought_signature), otherwise `None` (OpenAI's
        encrypted_content, Anthropic's signature, or no signature at all).
        """
        import base64

        # Normalize the signature for storage and decide the encoding tag.
        # bytes (Google) → base64 string + "base64" tag.
        # str (OpenAI/Anthropic) → verbatim, no encoding tag.
        # None → no signature, no encoding.
        signature_out: str | None = None
        encoding_out: str | None = self.signature_encoding
        if self.signature is not None:
            if isinstance(self.signature, bytes):
                signature_out = base64.b64encode(self.signature).decode("ascii")
                encoding_out = "base64"
            else:
                signature_out = self.signature
                # If the dataclass was hand-built with a string signature and an
                # explicit encoding, respect it; otherwise it's an opaque string
                # that round-trips verbatim and has no encoding.
                if encoding_out is None:
                    encoding_out = None

        result: dict[str, Any] = {
            "type": "thinking",
            "id": self.id,
            "text": self.text,
            "provider": self.provider,
            "signature": signature_out,
            "signature_encoding": encoding_out,
            # Copy metadata to avoid mutating the live object's dict
            "metadata": dict(self.metadata) if self.metadata else {},
            "summary": [],
        }

        if self.summary:
            # summary items may be Pydantic models (e.g. OpenAI Summary) or plain dicts
            result["summary"] = [
                item.model_dump() if hasattr(item, "model_dump") else item for item in self.summary
            ]

        return result

    def __repr__(self) -> str:
        """Override repr to show sanitized signature instead of full encrypted content"""
        # Show first 35 and last 35 characters with ... in the middle
        if len(self.text) > 70:
            text_preview = f"{self.text[:35]}...{self.text[-35:]}"
        else:
            text_preview = self.text

        return (
            f"ThinkingContent(type={self.type!r}, "
            f"text={text_preview!r}, "
            f"id={self.id!r}, "
            f"summary={self.summary!r}, "
            f"provider={self.provider!r}, "
            f"signature={self._sanitize_signature()}, "
            f"signature_encoding={self.signature_encoding!r})"
        )

    def to_google(self) -> dict[str, Any] | None:
        if self.provider == "google" and self.signature is not None:
            part: dict[str, Any] = {"text": self.text, "thought": True}
            part["thoughtSignature"] = self.signature
            return part

        fallback_text = self._anthropic_fallback_text()
        if fallback_text:
            return {"text": fallback_text}
        return None

    def to_openai(self) -> dict[str, Any] | None:
        """Convert to OpenAI format. Only includes signature if provider is OpenAI."""
        # Only include encrypted_content if this content came from OpenAI
        if self.provider != "openai" or self.signature is None:
            return None

        return {
            "id": self.id,
            "summary": self.summary,
            "type": "reasoning",
            "encrypted_content": self.signature,
        }

    def _anthropic_fallback_text(self) -> str:
        if self.text.strip():
            return self.text
        summary_lines: list[str] = []
        for item in self.summary:
            if isinstance(item, dict):
                line = item.get("text")
            else:
                line = getattr(item, "text", None)
            if line:
                summary_lines.append(str(line))
        return "\n".join(summary_lines)

    def to_anthropic(self) -> dict[str, Any] | None:
        if self.provider == "anthropic" and self.signature is not None:
            result = {
                "type": "thinking",
                "thinking": self.text,
                "signature": self.signature,
            }
            if self.summary:
                result["summary"] = self.summary
            return result

        fallback_text = self._anthropic_fallback_text()
        if fallback_text:
            return {"type": "text", "text": fallback_text}
        return None

    @classmethod
    def from_google(cls, part: Part) -> Optional["ThinkingContent"]:
        """Create ThinkingContent from Google Part object"""
        # vcprint(part, "Google Part", color="yellow")
        return cls(
            text=part.text or "",
            provider="google",
            signature=part.thought_signature if part.thought_signature else None,
        )

    @classmethod
    def from_anthropic(cls, content_block: dict[str, Any]) -> Optional["ThinkingContent"]:
        """Create ThinkingContent from Anthropic content block"""
        return cls(
            text=content_block["thinking"],
            provider="anthropic",
            signature=content_block.get("signature"),
        )

    @classmethod
    def from_openai(cls, item: Any) -> Optional["ThinkingContent"]:
        """Create ThinkingContent from OpenAI reasoning item"""
        encrypted_content = getattr(item, "encrypted_content", None)
        summary = (
            [s.model_dump() if hasattr(s, "model_dump") else s for s in item.summary]
            if item.summary
            else []
        )

        return cls(
            summary=summary,
            id=item.id,
            provider="openai",
            signature=encrypted_content,
        )


# Union of all content types
# 🚨 THIS UNION MUST COVER EVERYTHING ``reconstruct_content`` CAN RETURN.
# It did not. Seven of the fourteen classes in STRUCTURED_INPUT_TYPE_MAP were
# missing, so `reconstruct_content` returned values outside its own declared
# return type — WorkbookInputContent for real stored `input_workbook` blocks,
# among others. Nothing raised, because Python does not enforce a return
# annotation; what broke was every consumer that trusts this union, including
# the contract-closure walk, which silently under-counted the engine contract.
# `test_unified_content_union_is_complete` now reconciles the two.
UnifiedContent = (
    TextContent
    | ImageContent
    | AudioContent
    | VideoContent
    | YouTubeVideoContent
    | DocumentContent
    | ToolCallContent
    | ToolResultContent
    | ThinkingContent
    | CodeExecutionContent
    | CodeExecutionResultContent
    | WebSearchCallContent
    | HostedToolContent
    # The full STRUCTURED_INPUT_TYPE_MAP, all fourteen.
    | WebpageInputContent
    | NotesInputContent
    | TaskInputContent
    | TableInputContent
    | ListInputContent
    | DataInputContent
    | ContextInputContent
    | AgentInputContent
    | ProjectInputContent
    | AgentAppInputContent
    | TranscriptInputContent
    | TranscriptSessionInputContent
    | WorkbookInputContent
    | DocumentInputContent
    | DecisionQuestionsContent
    | DecisionAnswersContent
    | SpeechScriptContent
)


def reconstruct_content(block: Any) -> UnifiedContent:
    """
    THE ONE tolerant block decoder (DD-187b). Every caller that needs to turn a single
    stored content item into a UnifiedContent object calls this — never a second, parallel
    copy of the shape rules. `from_cx_message`'s container-level reconstruction
    (``UnifiedMessage._reconstruct_stored_content`` in message_config.py) delegates to this
    function per item instead of re-implementing the string/dict/refusal branches itself.

    Tolerates every shape a writer has ever produced for ONE item (DD-187/DD-187b):
    a bare string becomes one text part; a dict is decoded by its 'type' discriminator
    (below); anything else — or an internal decode failure on a well-formed dict — becomes
    a named refusal ``TextContent`` instead of raising and killing the whole conversation
    load. Before this guard, a non-dict block reaching this function called ``.get`` on a
    string/int/etc. and raised, exactly like the bug DD-187 fixed one level up.

    Args:
        block: One item from the ``cx_message.content`` JSONB array — normally a dict with
            a 'type' discriminator, but tolerated in every shape a writer has produced.

    Returns:
        The appropriate UnifiedContent instance, or a named refusal TextContent.
    """
    if isinstance(block, str):
        return TextContent(text=block)
    if not isinstance(block, dict):
        return TextContent(text=f"[unrecoverable content item shape: {type(block).__name__}]")
    try:
        return _decode_content_block(block)
    except Exception as exc:  # noqa: BLE001 - named refusal, never a crash
        return TextContent(text=f"[unrecoverable content block: {exc}]")


def _decode_content_block(block: dict[str, Any]) -> UnifiedContent:
    """The real per-type dispatch, dict-only. Only `reconstruct_content` calls this —
    it is the internal half of the ONE tolerant decoder, not a second entry point."""
    block_type = block.get("type", "text")

    if block_type == "text":
        from matrx_ai.config.citations import ensure_normalized_citations

        # Preserve any client/stored metadata verbatim — this function is the
        # ONE deserializer for a storage block (parse_content delegates here),
        # so silently dropping a key here loses it on EVERY rebuild path.
        raw_text_meta = block.get("metadata")
        # `<key>__b64` decodes back to bytes — a text part carries Gemini's
        # `google_thought_signature` exactly like a tool_call part does, and
        # both sides of that encoding live in ONE place (config_utils).
        metadata: dict[str, Any] = (
            decode_binary_metadata(raw_text_meta) if isinstance(raw_text_meta, dict) else {}
        )
        citations = block.get("citations")
        if citations:
            # Historical rows may hold raw provider shapes; coerce to canonical.
            metadata["citations"] = ensure_normalized_citations(citations)
        return TextContent(
            text=block.get("text", ""),
            id=block.get("id", ""),
            metadata=metadata,
        )

    elif block_type in ("thinking", "reasoning"):
        import base64

        sig = block.get("signature")
        encoding = block.get("signature_encoding")
        # The encoding tag is purely a storage marker. If it says "base64", the
        # signature on disk is base64-encoded bytes (Google's thought_signature)
        # and we must decode back to bytes so the dataclass holds the original
        # shape. Once decoded, the encoding tag has no further meaning in-memory
        # — to_storage_dict() will recompute it on the next write.
        if sig and encoding == "base64":
            sig = base64.b64decode(sig)
            encoding = None

        id_from_metadata = block.get("metadata", {}).get("id")
        return ThinkingContent(
            text=block.get("text", ""),
            provider=block.get("provider"),
            signature=sig,
            signature_encoding=encoding,
            summary=block.get("summary", []),
            id=id_from_metadata or block.get("id", ""),
        )

    elif block_type == "media":
        result = reconstruct_media_content(block)
        if result is not None:
            return result
        return TextContent(text=f"[Unknown media kind: {block.get('kind')}]")

    elif block_type in ("tool_call", "function_call"):
        if "id" in block:
            vcprint(
                f"CRITICAL DATA INTEGRITY WARNING: 'id' field found in tool_call content block instead of 'call_id'. "
                f"This indicates unmigrated or improperly serialized data. Block: {block}",
                color="red",
            )
        # Restore provider continuity metadata persisted by to_storage_dict().
        # ``<key>__b64`` entries are base64-encoded bytes (e.g. Gemini's
        # google_thought_signature — REQUIRED on replay; Gemini 3 400s on a
        # functionCall part without its thoughtSignature). Mirrors the
        # thinking-block signature decode above.
        raw_meta = block.get("metadata") or {}
        tc_metadata: dict[str, Any] = decode_binary_metadata(raw_meta)
        _tc_id = block.get("call_id", "") or block.get("id", "")
        if not _tc_id:
            # A stored tool_call with NO join key means some writer rewrote the
            # row's content through a serializer that dropped call_id (the FE
            # assembled-block shape, a parse_content round-trip pre-alias-fix,
            # or a direct chat.message UPDATE bypassing the guarded RPC). The
            # pairing graph is now broken at the source: the provider will 400
            # on an empty tool_use.id and the paired tool_result becomes an
            # orphan. MessageList.sanitize repairs/drops it downstream — but the
            # DB row itself is corrupt and must be fixed. SCREAM so it is.
            vcprint(
                f"CRITICAL DATA INTEGRITY WARNING: stored tool_call block for "
                f"tool {block.get('name')!r} carries NO call_id/id — the "
                f"cx_message row was rewritten by a writer that dropped the "
                f"tool-pairing join key. Repair the row (restore call_id from "
                f"the adjacent tool_result) and find the rogue writer. "
                f"Block: {block}",
                color="red",
            )
        return ToolCallContent(
            id=_tc_id,
            name=block.get("name", ""),
            arguments=block.get("arguments", {}),
            metadata=tc_metadata,
        )

    elif block_type in ("tool_result", "function_result", "tool_call_result"):
        # Pointer-block format (new): no "content" key — the full output lives in
        # cx_tool_call.output and is joined by rebuild_conversation_messages().
        # Legacy format (pre-migration): has a "content" key with the full output.
        # We preserve the legacy path for backward compatibility; the rebuild path
        # always wins for conversation history reconstruction.
        #
        # Anthropic safeguard: ``content`` must be non-empty when
        # ``is_error=True``. There are real rows where the cx_tool_call write
        # never landed (or got later cascade-deleted) AND the pointer block
        # has no ``content`` AND ``is_error=True`` — sending that to
        # Anthropic raises ``messages.N.content.0.tool_result: content
        # cannot be empty if is_error is true``. We synthesise a stock
        # string here as a last-resort fallback so the rebuild's main
        # synthesis path (which uses cx_tool_call.error_type / error_message)
        # remains the preferred source when a tool_call row is present.
        is_error = block.get("is_error", False)
        content = block.get("content", "")
        if is_error and not content:
            tool_name = block.get("name") or "tool"
            content = f"[Tool '{tool_name}' errored — no output recorded]"
        # Defensive: a client may send a non-numeric output_chars. This is the
        # ONE deserializer for every rebuild path — it must never raise on a
        # cosmetic field and take the whole request down with it.
        try:
            _out_chars = int(block.get("output_chars", 0) or 0)
        except (TypeError, ValueError):
            _out_chars = 0
        return ToolResultContent(
            tool_use_id=block.get("tool_use_id", "") or block.get("call_id", ""),
            call_id=block.get("call_id", "") or block.get("tool_use_id", ""),
            name=block.get("name", ""),
            content=content,
            is_error=is_error,
            output_chars=_out_chars,
            output_preview=block.get("output_preview"),
            metadata=dict(block.get("metadata") or {}),
        )

    elif block_type == "code_exec":
        return CodeExecutionContent(
            language=block.get("language", ""),
            code=block.get("code", ""),
            metadata=dict(block.get("metadata") or {}),
        )

    elif block_type == "code_result":
        return CodeExecutionResultContent(
            output=block.get("output", ""),
            outcome=block.get("outcome", ""),
            metadata=dict(block.get("metadata") or {}),
        )

    elif block_type == "web_search":
        meta = block.get("metadata", {})
        return WebSearchCallContent(
            id=block.get("id", ""),
            status=block.get("status", ""),
            action=meta.get("action", {}),
        )

    elif block_type == "hosted_tool":
        raw_block = block.get("block")
        raw_meta = block.get("metadata")
        return HostedToolContent(
            provider=str(block.get("provider", "") or ""),
            block=dict(raw_block) if isinstance(raw_block, dict) else {},
            metadata=dict(raw_meta) if isinstance(raw_meta, dict) else {},
        )

    elif block_type == "decision_questions":
        # The decision modality's question part. Validation lives in the
        # registered kind (matrx_ai.decisions.kinds) — reconstructing a stored
        # block must stay tolerant (this is the ONE tolerant decoder), so a
        # malformed stored batch surfaces as a named refusal upstream rather
        # than killing a conversation load.
        return DecisionQuestionsContent(
            questions=list(block.get("questions") or []),
            metadata=dict(block.get("metadata") or {}),
        )

    elif block_type == "speech_script":
        # Tolerant like every stored-block decode: the kind validates at use
        # (translation / persistence), so a malformed stored script surfaces as
        # a named refusal there rather than killing a conversation load.
        return SpeechScriptContent(
            turns=[dict(turn) for turn in (block.get("turns") or []) if isinstance(turn, dict)],
            metadata=dict(block.get("metadata") or {}),
        )

    elif block_type == "decision_answers":
        from matrx_ai.decisions.kinds import DecisionAnswers

        return DecisionAnswersContent(
            answers=DecisionAnswers.model_validate(
                {key: value for key, value in block.items() if key not in ("type", "metadata")}
            ),
            metadata=dict(block.get("metadata") or {}),
        )

    elif block_type in STRUCTURED_INPUT_TYPE_MAP:
        obj = reconstruct_structured_input(block)
        if obj is not None:
            return obj
        vcprint(
            block,
            f"reconstruct_content: block_type '{block_type}' is in STRUCTURED_INPUT_TYPE_MAP but reconstruct_structured_input returned None — map/handler mismatch\n\n Temporarily not raising an error, but dropping the content block",
            color="red",
        )
        return TextContent(text=f"[Structured input reconstruction failed: {block_type}]")

    # Fallback: return as TextContent with warning
    vcprint(
        block,
        f"reconstruct_content: Unknown storage block type: {block_type}\n\n Temporarily not raising an error, but returning placeholder TextContent",
        color="red",
    )
    return TextContent(text=f"[Unknown block type: {block_type}]")

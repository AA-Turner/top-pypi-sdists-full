import json
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from google.genai.types import Part

from matrx_ai.config.config_utils import encode_binary_metadata
from matrx_ai.config.wire_names import to_wire_name
from matrx_ai.config.openai_responses_tool_ids import (
    openai_responses_tool_call_wire_ids,
    openai_responses_tool_result_call_id,
)


def _is_typed_block_list(content: Any) -> bool:
    """True iff ``content`` is a list whose entries carry the matrx-ai
    content-block protocol (``to_anthropic`` / ``to_openai`` / ``to_google``).

    This is how ``ToolResult.to_tool_result_content`` signals that the
    result carries structured blocks (e.g. an ImageContent + TextContent
    pair from a screenshot) instead of an opaque JSON-stringified payload.
    """
    if not isinstance(content, list) or not content:
        return False
    return any(
        hasattr(item, "to_anthropic") or hasattr(item, "to_openai") or hasattr(item, "to_google")
        for item in content
    )


def _serialize_block_for_anthropic(block: Any) -> dict[str, Any] | None:
    """Convert one typed content block to an Anthropic-shaped dict."""
    if hasattr(block, "to_anthropic"):
        try:
            out = block.to_anthropic()
        except Exception:
            return None
        if isinstance(out, dict):
            return out
        if isinstance(out, list) and out and isinstance(out[0], dict):
            return out[0]
        return None
    if isinstance(block, dict) and block.get("type"):
        return block
    return None


def _rebuild_citable_wire_blocks(tool_name: str, content: Any) -> list[dict[str, Any]] | None:
    """Best-effort citability restore for stored citable-search-tool outputs.

    Accepts the stored payload as a dict OR a JSON string; anything else (or a
    payload without passages) returns None and the caller keeps the plain path.
    """
    from matrx_ai.config.citations import CITABLE_SEARCH_TOOLS, citable_wire_blocks_from_output

    if tool_name not in CITABLE_SEARCH_TOOLS:
        return None
    payload = content
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            return None
    if not isinstance(payload, dict):
        return None
    return citable_wire_blocks_from_output(tool_name, payload)


def _homogenize_anthropic_search_results(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Anthropic rejects a tool_result mixing `search_result` blocks with any
    other type (400: "all blocks must be of that type" — live-verified
    2026-08-08). Citable tool results legitimately carry a trailing metadata
    text block, so at this one serialization choke point:

      - text blocks in a search_result-bearing result are wrapped as
        search_result blocks (title "Search metadata") — the model still sees
        the JSON, the wire stays homogeneous. The wrapper is citations-ENABLED
        like the passages beside it: Anthropic also rejects a mixture of
        enabled and disabled citations across search_result blocks (wire
        invariant 2, citations.py — live 400 on 2026-08-21);
      - if an unwrappable block type (image/document) is present, the
        search_result blocks degrade to plain text renderings instead — a
        valid request always beats citability, and the degradation screams.
    """
    from matrx_ai.config.citations import MATRX_METADATA_SOURCE, search_result_citations

    has_search = any(b.get("type") == "search_result" for b in blocks)
    if not has_search or all(b.get("type") == "search_result" for b in blocks):
        return blocks

    wrappable = all(b.get("type") in ("search_result", "text") for b in blocks)
    if wrappable:
        out: list[dict[str, Any]] = []
        for b in blocks:
            if b.get("type") == "text":
                out.append(
                    {
                        "type": "search_result",
                        "source": MATRX_METADATA_SOURCE,
                        "title": "Search metadata",
                        "content": [{"type": "text", "text": b.get("text") or ""}],
                        "citations": search_result_citations(),
                    }
                )
            else:
                out.append(b)
        return out

    from matrx_utils import vcprint

    vcprint(
        "[citations] tool_result mixes search_result blocks with non-text blocks "
        "Anthropic cannot combine — degrading search_result blocks to plain text "
        "(citability lost for this result). Emit passages and media in separate "
        "tool results to keep citations.",
        color="red",
    )
    out = []
    for b in blocks:
        if b.get("type") == "search_result":
            inner = "\n".join(
                c.get("text") or "" for c in b.get("content") or [] if isinstance(c, dict)
            )
            header = b.get("title") or "Search result"
            source = b.get("source") or ""
            out.append(
                {
                    "type": "text",
                    "text": f"[{header}]" + (f" ({source})" if source else "") + f"\n{inner}",
                }
            )
        else:
            out.append(b)
    return out


def _serialize_block_for_google(block: Any) -> str | None:
    """Best-effort string summary for a typed block when emitting Google
    functionResponse — the protocol is JSON-only."""
    if hasattr(block, "text") and isinstance(getattr(block, "text", None), str):
        return block.text
    if hasattr(block, "to_dict"):
        try:
            d = block.to_dict()
        except Exception:
            d = None
        if isinstance(d, dict):
            return json.dumps(d)
    if isinstance(block, dict):
        return json.dumps(block)
    return None


def _typed_blocks_for_openai(content: list[Any]) -> list[dict[str, Any]]:
    """Convert typed blocks to a flat list of dicts for OpenAI
    function_call_output — which only accepts string content."""
    result: list[dict[str, Any]] = []
    for block in content:
        if hasattr(block, "to_storage_dict"):
            try:
                d = block.to_storage_dict()
            except Exception:
                d = None
            if isinstance(d, dict):
                base64_data = d.get("base64_data")
                if isinstance(base64_data, str):
                    d["base64_data"] = f"<{len(base64_data)} chars>"
                result.append(d)
                continue
        if hasattr(block, "to_dict"):
            try:
                d = block.to_dict()
            except Exception:
                d = None
            if isinstance(d, dict):
                result.append(d)
                continue
        if hasattr(block, "text"):
            result.append({"type": "text", "text": getattr(block, "text", "")})
        elif isinstance(block, dict):
            result.append(block)
    return result


@dataclass
class ToolCallContent:
    """Unified tool call content block.

    ``id`` is always the **join key** — the value that matches ``cx_tool_call.call_id``
    and is used by the frontend to correlate calls with results.

    Provider-specific secondary identifiers (e.g. OpenAI's ``fc_...`` item id) are
    stored in ``metadata`` under a clearly-namespaced key (``openai_item_id``).
    """

    type: Literal["tool_call", "function_call"] = "tool_call"
    id: str = ""
    name: str = ""
    arguments: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    from openai.types.responses import (
        ResponseFunctionToolCall as OpenAIResponseFunctionToolCall,
    )

    def get_output(self) -> str:
        """Get the output of the tool call."""
        return json.dumps(self.to_dict())

    @property
    def wire_name(self) -> str:
        """Provider-safe form of ``name`` — the ONLY spelling that may reach
        a provider payload. A live-parsed call already carries the wire form
        (no-op); a DB-rebuilt block carries the canonical (possibly
        colon-namespaced) name, which providers reject — this converts it.
        Every translator that replays a tool call MUST use this, never
        ``.name``.
        """
        return to_wire_name(self.name)

    def to_google(self) -> dict[str, Any]:
        """Convert to Google Gemini format"""
        part = {
            "functionCall": {
                "name": self.wire_name,
                "args": self.arguments,
            }
        }
        # thoughtSignature must be at Part level, not inside functionCall
        # Retrieve Google's thought signature from metadata if present
        if "google_thought_signature" in self.metadata:
            part["thoughtSignature"] = self.metadata["google_thought_signature"]
        return part

    def to_openai(self) -> dict[str, Any]:
        """Convert to OpenAI format.

        Reconstructs OpenAI's ``call_id`` from our ``id`` (the join key) and
        ``id`` from metadata's ``openai_item_id`` (the ``fc_...`` item identifier).
        Foreign join keys (``toolu_``, ``gemini_``, …) are remapped on the wire
        without mutating the stored join key.
        """
        wire_fc_id, wire_call_id = openai_responses_tool_call_wire_ids(
            self.id,
            openai_item_id=self.metadata.get("openai_item_id"),
        )
        return {
            "type": "function_call",
            "id": wire_fc_id,
            "call_id": wire_call_id,
            "name": self.wire_name,
            "arguments": json.dumps(self.arguments),
        }

    def to_anthropic(self) -> dict[str, Any]:
        """Convert to Anthropic format"""
        return {
            "type": "tool_use",
            "id": self.id,
            "name": self.wire_name,
            "input": self.arguments,
        }

    def _sanitize_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """DISPLAY ONLY — a human-readable stand-in for encrypted material.

        🚨 Used by ``__repr__`` and NOTHING that is rebuilt from. See
        ``encode_binary_metadata`` — a ``functionCall`` part replayed with
        ``<bytes length=N>`` as its ``thoughtSignature`` is rejected by the
        Google SDK before the request leaves the process.

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
        ``<key>__b64`` and ``reconstruct_content`` decodes it back to bytes, so
        a request rebuilt from this dict carries the SAME provider-continuity
        material the original call sent. Use ``repr()`` for a printable form.
        """
        return {
            "type": self.type,
            "call_id": self.id,
            "name": self.name,
            "arguments": self.arguments,
            "metadata": encode_binary_metadata(self.metadata),
        }

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format for database persistence (cx_message.content JSONB).

        ``call_id`` is always the join key that matches ``cx_tool_call.call_id``.

        ``metadata`` carries provider continuity material that MUST survive a
        DB rebuild: Gemini 3 rejects a replayed ``functionCall`` part without
        its ``thoughtSignature`` (400 "Function call is missing a
        thought_signature"), and the OpenAI Responses API needs
        ``openai_item_id``. Dropping metadata here is what made every
        suspend→/resume round-trip die on Gemini once the AgentCache stopped
        masking the rebuild. Bytes values are base64-encoded under a
        ``<key>__b64`` name — same pattern as ThinkingContent's signature;
        ``reconstruct_content`` decodes them back to bytes.
        """
        result: dict[str, Any] = {
            "type": "tool_call",
            "name": self.name,
            "arguments": self.arguments,
        }
        if self.id:
            result["call_id"] = self.id
        if self.metadata:
            stored_meta = encode_binary_metadata(self.metadata)
            if stored_meta:
                result["metadata"] = stored_meta
        return result

    def __repr__(self) -> str:
        """Override repr to show sanitized metadata instead of full encrypted content"""
        sanitized_metadata = self._sanitize_metadata(self.metadata)

        # Truncate arguments JSON if too long
        args_str = json.dumps(self.arguments)
        if len(args_str) > 70:
            args_preview = f"{args_str[:35]}...{args_str[-35:]}"
        else:
            args_preview = args_str

        return (
            f"ToolCallContent(type={self.type!r}, "
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"arguments={args_preview}, "
            f"metadata={sanitized_metadata!r})"
        )

    @classmethod
    def from_google(cls, part: Part) -> Optional["ToolCallContent"]:
        """Create ToolCallContent from Google Part object.

        Gemini doesn't supply call ids, so we mint one. It MUST be unique per
        call: the old ``gemini_{hash(name)}`` form collided for every repeat
        call of the same tool — within one conversation AND across
        conversations in one process — producing duplicate ``cx_tool_call``
        rows under one call_id and ambiguous POST /tool_results matches. The
        id is internal-only for Google (``to_google`` replays name/args; the
        functionResponse pairs by name), so a random suffix is wire-safe.
        """
        if hasattr(part, "function_call") and part.function_call:
            import uuid

            metadata = {}
            # Store Google's thought signature in metadata if present
            if part.thought_signature:
                metadata["google_thought_signature"] = part.thought_signature
            return cls(
                id=f"gemini_{uuid.uuid4().hex[:16]}",
                name=part.function_call.name,
                arguments=part.function_call.args or {},
                metadata=metadata,
            )
        return None

    @classmethod
    def from_openai(cls, item: OpenAIResponseFunctionToolCall) -> Optional["ToolCallContent"]:
        """Create ToolCallContent from OpenAI item.

        ``id`` is set to ``item.call_id`` (the join key, e.g. ``call_...``).
        The OpenAI item identifier (``fc_...``) is preserved in metadata as
        ``openai_item_id`` so it can be reconstructed for the Responses API.
        """
        args = item.arguments
        if isinstance(args, str):
            args = json.loads(args)

        extra = item.model_dump(exclude={"id", "call_id", "name", "arguments"})
        if item.id:
            extra["openai_item_id"] = item.id

        return cls(
            id=item.call_id,
            name=item.name,
            arguments=args,
            metadata=extra,
        )

    @classmethod
    def from_anthropic(cls, content_block: dict[str, Any]) -> Optional["ToolCallContent"]:
        """Create ToolCallContent from Anthropic content block"""
        return cls(
            id=content_block["id"],
            name=content_block["name"],
            arguments=content_block["input"],
        )


@dataclass
class ToolResultContent:
    type: Literal["tool_result"] = "tool_result"
    tool_use_id: str = ""
    call_id: str = ""  # OpenAI-specific call_id (different from tool_use_id)
    name: str = ""
    content: list[dict[str, Any]] = field(default_factory=list)
    is_error: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    # Output metadata — populated synchronously by ToolExecutionLogger.prepare_metadata()
    # before the fire-and-forget DB task fires. Carried here so the persistence layer
    # can build cx_message pointer blocks without a DB round-trip.
    output_chars: int = 0
    output_preview: dict[str, Any] | None = None
    # An explicit per-result model-visible ceiling a tool authorized (mirrors
    # ToolResult.approved_max_chars). Read by MessageList.sanitize's Layer-2
    # absolute-ceiling pass so a deliberately-large self-managed result isn't
    # hard-truncated at the provider boundary. None ⇒ the default absolute ceiling.
    approved_max_chars: int | None = None

    def get_output(self) -> str:
        """Get the output of the tool result."""
        return json.dumps(self.to_storage_dict())

    @property
    def wire_name(self) -> str:
        """Provider-safe form of ``name`` (see ``ToolCallContent.wire_name``)."""
        return to_wire_name(self.name)

    def to_google(self) -> dict[str, Any]:
        """Convert to Google Gemini format.

        Google API requires functionResponse.response to be a dictionary.
        The content field can be various types due to backwards compatibility,
        so we normalize it here.

        Image-bearing tool results carry typed content blocks (ImageContent +
        TextContent) — Google's functionResponse can only carry a JSON object,
        so we surface the image via the ``parts`` mechanism alongside.
        """
        if _is_typed_block_list(self.content):
            text_segments: list[str] = []
            for block in self.content:
                serialized = _serialize_block_for_google(block)
                if serialized is not None:
                    text_segments.append(serialized)
            response_data: dict[str, Any] = {
                "result": "\n".join(text_segments) if text_segments else "",
            }
        elif isinstance(self.content, dict):
            response_data = self.content
        elif isinstance(self.content, str):
            response_data = {"result": self.content}
        elif isinstance(self.content, list):
            response_data = {"items": self.content} if self.content else {"result": ""}
        else:
            response_data = {"result": str(self.content) if self.content else ""}

        # wire_name: Gemini requires functionResponse.name to equal the
        # functionCall name — always the wire form. A fresh result carries
        # the internal (post-normalization) name; convert. Idempotent for
        # names that are already wire-safe.
        return {
            "functionResponse": {
                "name": self.wire_name,
                "response": response_data,
            }
        }

    def to_openai(self) -> dict[str, Any]:
        """Convert to OpenAI Responses API format (function_call_output).

        Image-bearing tool results emit a JSON-stringified summary that
        references the cloud-stored image via its resolved URL — OpenAI's
        ``function_call_output`` doesn't accept structured content blocks.
        The image itself flows back to the model as a separate user-message
        ``input_image`` block in the next iteration (handled by the
        provider translator).
        """
        if _is_typed_block_list(self.content):
            payload = {"blocks": _typed_blocks_for_openai(self.content)}
            output_str = json.dumps(payload)
        else:
            output_str = self.content
            if isinstance(output_str, (dict, list)):
                output_str = json.dumps(output_str)
            elif not isinstance(output_str, str):
                output_str = str(output_str)

        join_key = self.call_id or self.tool_use_id
        return {
            "type": "function_call_output",
            "call_id": openai_responses_tool_result_call_id(join_key),
            "output": output_str,
        }

    def to_anthropic(self) -> dict[str, Any]:
        """Convert to Anthropic format.

        When ``self.content`` is a list of typed content blocks (e.g. an
        ImageContent + TextContent emitted by ``ToolResult.to_tool_result_content``
        for image-bearing tools), pass each block through its own
        ``to_anthropic()`` so Anthropic sees a real ``image`` content block —
        never a base64 blob serialised as text.
        """
        if _is_typed_block_list(self.content):
            blocks: list[dict[str, Any]] = []
            for block in self.content:
                serialized = _serialize_block_for_anthropic(block)
                if serialized is not None:
                    blocks.append(serialized)
            blocks = _homogenize_anthropic_search_results(blocks)
            content = blocks if blocks else "[empty tool result]"
        else:
            # DB-rebuilt conversations lose the live typed provider_content
            # (never persisted) — a citable search tool's stored JSON output
            # would resend as plain text, silently un-citing every multi-turn
            # follow-up. Rebuild homogeneous search_result wire blocks from
            # the stored payload at this one boundary.
            rebuilt = _rebuild_citable_wire_blocks(self.name, self.content)
            if rebuilt is not None:
                content = rebuilt
            elif isinstance(self.content, str):
                content = self.content
            else:
                content = json.dumps(self.content)

        result = {
            "type": "tool_result",
            "tool_use_id": self.tool_use_id,
            "content": content,
        }
        if self.is_error:
            result["is_error"] = True
        return result

    def to_openai_chat(self) -> dict[str, Any]:
        """Convert to an OpenAI Chat Completions ``role=tool`` message.

        This is the wire shape every OpenAI-compatible Chat Completions
        endpoint speaks (Cerebras, Groq, xAI, Together, llama-server,
        vLLM, Ollama, LocalAI). Distinct from the Responses-API
        ``function_call_output`` shape returned by ``to_openai()``.

        Image-bearing tool results (typed-block lists) emit a
        JSON-stringified ``{"blocks": [...]}`` summary — Chat Completions
        ``role=tool`` only accepts a string ``content`` field, no
        structured content arrays. The image itself must flow back to
        the model as a separate ``user``-message ``image_url`` block in
        the next iteration; see ``extract_image_blocks()`` for the
        helper that surfaces those blocks.
        """
        if _is_typed_block_list(self.content):
            payload = {"blocks": _typed_blocks_for_openai(self.content)}
            output_str = json.dumps(payload)
        elif isinstance(self.content, (dict, list)):
            output_str = json.dumps(self.content)
        elif isinstance(self.content, str):
            output_str = self.content
        else:
            output_str = str(self.content) if self.content is not None else ""

        return {
            "role": "tool",
            "tool_call_id": self.tool_use_id or self.call_id,
            "content": output_str,
        }

    def extract_image_blocks(self) -> list[Any]:
        """Return the ImageContent (and ``input_image``-typed) blocks
        carried inside a typed-block tool result.

        OpenAI-compatible Chat Completions tool messages cannot carry
        structured image content, so providers surface these images as
        a follow-up ``user`` message with ``image_url`` parts on the
        next iteration. Returns an empty list when the tool result
        carries no typed blocks or no image-typed entries.
        """
        if not _is_typed_block_list(self.content):
            return []
        return [b for b in self.content if getattr(b, "type", None) in ("image", "input_image")]

    def extract_media_blocks(self) -> list[Any]:
        """Return image and document blocks nested in this tool result."""
        if not _is_typed_block_list(self.content):
            return []
        return [
            block
            for block in self.content
            if getattr(block, "type", None)
            in ("image", "input_image", "document", "input_document")
        ]

    def to_google_parts(self) -> list[dict[str, Any]]:
        """Return the function response followed by provider-native media parts."""
        parts = [self.to_google()]
        for block in self.extract_media_blocks():
            serialized = block.to_google()
            if isinstance(serialized, dict):
                parts.append(serialized)
        return parts

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to the in-memory representation used by the message pipeline.

        IMPORTANT: this dict is NOT written directly to cx_message.content.
        The persistence layer converts role='tool' messages into lightweight
        pointer blocks (ToolResultPart) that contain call_id, name, is_error,
        output_chars, and output_preview — but NOT the full content payload.

        The full output lives exclusively in cx_tool_call.output.

        This dict is used to carry the tool result through the execution
        pipeline (e.g. back to the LLM on the next iteration).
        """
        if _is_typed_block_list(self.content):
            content_value: Any = _typed_blocks_for_openai(self.content)
        else:
            content_value = self.content
        result: dict[str, Any] = {
            "type": "tool_result",
            "name": self.name,
            "content": content_value,
        }
        if self.tool_use_id:
            result["tool_use_id"] = self.tool_use_id
        if self.call_id:
            result["call_id"] = self.call_id
        if self.is_error:
            result["is_error"] = True
        return result

    @classmethod
    def from_google(cls, part: Part) -> Optional["ToolResultContent"]:
        """Create ToolResultContent from Google Part object"""
        if hasattr(part, "function_response") and part.function_response:
            return cls(
                tool_use_id="",
                name=part.function_response.name or "",
                content=part.function_response.response or [],
            )
        return None

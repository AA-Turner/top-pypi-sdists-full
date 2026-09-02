from __future__ import annotations

import ast
import hashlib
import json
import logging
import re
import traceback
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from matrx_utils import vcprint
from pydantic import BaseModel, Field, PrivateAttr, field_validator
from pydantic_core import to_jsonable_python

from matrx_ai.config import TokenUsage
from matrx_ai.config.custom_tool import CustomTool as CustomToolBase
from matrx_ai.config.custom_tool import CustomToolInputSchema as CustomToolInputSchemaBase
from matrx_ai.context.emitter_protocol import Emitter

# Path readers / agents can open to learn what this gate is and how to fix
# a trigger. Kept as a relative repo path so it works whether opened from
# the editor or quoted in a chat log.
TOOL_OUTPUT_GATE_DOCS = "packages/matrx-ai/matrx_ai/tools/TOOL_OUTPUT_VALIDATION_GATE.md"


def to_json_safe(value: Any) -> Any:
    return to_jsonable_python(value, serialize_unknown=True, fallback=str)


class ToolOutputContractError(ValueError):
    """Raised by the ``ToolResult.output`` validation gate in this file.

    THIS IS NOT A REAL ERROR. It means a tool's output payload tripped a
    structural check WE added to catch silent-failure antipatterns. The
    loud red banner that gets printed alongside the raise contains the
    full diagnostic — exception message is the short version. See
    TOOL_OUTPUT_VALIDATION_GATE.md for the full reference."""


# ---------------------------------------------------------------------------
# Google (Gemini) schema normalization — the single per-provider adapter
# ---------------------------------------------------------------------------
#
# Gemini's function-calling validator is STRICTER than OpenAI / Anthropic about
# the JSON Schema of tool parameters. The one that bites repeatedly: **every
# ``array`` property MUST carry an ``items`` subschema** (with a concrete type)
# or the whole request is rejected with HTTP 400 ``INVALID_ARGUMENT``:
#
#     GenerateContentRequest.tools[0].function_declarations[0]
#         .parameters.properties[<name>].items: missing field.
#
# Our internal param dicts (DB ``tool_def.parameters`` rows AND inline custom
# tools) can legitimately be loose — a tool author may declare ``ops: list``
# without an element type. OpenAI/Anthropic tolerate that; Gemini does not.
#
# The fix is per-provider adaptation at the translation boundary (NOT editing
# every tool's stored schema to appease Google — that treats the symptom, leaves
# the class of failure alive, and is exactly how this regressed: migration 0103
# patched the ``dictionary`` tool's DB row by hand, so the next loosely-typed
# tool (workbook/document) 400'd the same way). This normalizer guarantees a
# Gemini-valid schema for ANY input, so the failure class is structurally gone.
#
# When an array is missing its ``items``, we inject a permissive ``string`` item
# (the safest default that keeps the request valid) and warn ONCE per process so
# the under-typed tool gets properly typed at the source.

_GOOGLE_MISSING_ITEMS_WARNED: set[str] = set()


def _normalize_google_schema(
    node: dict[str, Any] | str, *, missing_items: list[str], path: str
) -> dict[str, Any]:
    """Convert a loose internal param/JSON-schema node into a Gemini-valid schema.

    Recurses through objects and arrays. The single hard guarantee: an
    ``array`` always comes out with a typed ``items`` subschema (Gemini rejects
    arrays without one). ``missing_items`` collects the dotted paths where a
    permissive default had to be injected, for a one-time warning by the caller.
    """
    if isinstance(node, str):
        return {"type": node}

    s: dict[str, Any] = {}
    ptype = node.get("type", "string")
    if isinstance(ptype, list):
        non_null = [t for t in ptype if t != "null"]
        ptype = non_null[0] if non_null else "string"
    if ptype == "any":
        # Gemini's schema dialect REQUIRES a type ("any" 400s the request).
        # A JSON string is the widest value Gemini can carry for an
        # any-typed param; the executor's Pydantic validation (Any) accepts
        # the string as-is.
        ptype = "string"
    s["type"] = ptype

    if node.get("description"):
        s["description"] = node["description"]
    if "enum" in node:
        s["enum"] = node["enum"]

    if ptype == "array":
        items = node.get("items")
        if isinstance(items, dict | str) and items != {}:
            s["items"] = _normalize_google_schema(
                items, missing_items=missing_items, path=f"{path}[]"
            )
        else:
            # Gemini requires items on every array — inject a permissive default
            # so the request is valid, and record the path so we can flag the
            # under-typed schema (the real fix is typing it at the source).
            missing_items.append(path)
            s["items"] = {"type": "string"}

    if ptype == "object" and "properties" in node:
        s["properties"] = {
            k: _normalize_google_schema(v, missing_items=missing_items, path=f"{path}.{k}")
            for k, v in node["properties"].items()
        }
        if "required" in node:
            s["required"] = node["required"]

    return s


def _warn_google_missing_items(tool_name: str, missing_items: list[str]) -> None:
    """One-time-per-process warning naming each array property Gemini would have
    rejected for a missing ``items`` subschema. The request still succeeds (a
    permissive ``string`` item was injected) — this just surfaces the loose tool
    schema so it gets typed properly at the source (DB ``tool_def`` row /
    Pydantic args model)."""
    fresh = [p for p in missing_items if f"{tool_name}:{p}" not in _GOOGLE_MISSING_ITEMS_WARNED]
    if not fresh:
        return
    for p in fresh:
        _GOOGLE_MISSING_ITEMS_WARNED.add(f"{tool_name}:{p}")
    vcprint(
        data={
            "tool": tool_name,
            "array_properties_missing_items": fresh,
            "injected_default": {"type": "string"},
        },
        title=(
            "⚠️  GOOGLE SCHEMA ADJUSTMENT: tool array property had no `items` — "
            "Gemini requires one (would 400 INVALID_ARGUMENT). Injected a permissive "
            "string item to keep the request valid. FIX THE SOURCE: add a typed `items` "
            "to this tool's parameters (DB tool_def row + Pydantic args model)."
        ),
        color="yellow",
        verbose=True,
    )


class ToolType(StrEnum):
    LOCAL = "local"
    EXTERNAL_MCP = "external"
    AGENT = "agent"
    EXTERNAL_HANDLER = "external_handler"


def _is_image_ref_output(output: Any) -> bool:
    return isinstance(output, dict) and output.get("kind") == "image_ref" and "media_ref" in output


def _is_image_ref_list_output(output: Any) -> bool:
    return (
        isinstance(output, dict)
        and output.get("kind") == "image_ref_list"
        and isinstance(output.get("items"), list)
    )


def _is_document_ref_output(output: Any) -> bool:
    return (
        isinstance(output, dict)
        and output.get("kind") == "document_ref"
        # Key presence, not dict-ness: a FAILED persist sets ``media_ref`` to
        # None beside a ``media_ref_error``, and that case must still reach the
        # builder so the model is told the media is unavailable — falling
        # through to raw JSON buries it (matches ``_is_image_ref_output``).
        and "media_ref" in output
    )


def _is_audio_ref_output(output: Any) -> bool:
    return (
        isinstance(output, dict)
        and output.get("kind") == "audio_ref"
        # Key presence, not dict-ness: a FAILED persist sets ``media_ref`` to
        # None beside a ``media_ref_error``, and that case must still reach the
        # builder so the model is told the media is unavailable — falling
        # through to raw JSON buries it (matches ``_is_image_ref_output``).
        and "media_ref" in output
    )


def _is_video_ref_output(output: Any) -> bool:
    return (
        isinstance(output, dict)
        and output.get("kind") == "video_ref"
        # Key presence, not dict-ness: a FAILED persist sets ``media_ref`` to
        # None beside a ``media_ref_error``, and that case must still reach the
        # builder so the model is told the media is unavailable — falling
        # through to raw JSON buries it (matches ``_is_image_ref_output``).
        and "media_ref" in output
    )


def _is_media_ref_list_output(output: Any) -> bool:
    return (
        isinstance(output, dict)
        and output.get("kind") == "media_ref_list"
        and isinstance(output.get("items"), list)
    )


def _ref_details_text(output: dict[str, Any], *, file_id: Any, mime_type: str) -> str:
    """The trailing JSON block that keeps a media envelope's non-media fields
    (and its identity) visible to the model. Same contract as the document
    builder: the media block never costs the tool its structured payload."""
    details = {
        key: value
        for key, value in output.items()
        if key not in {"kind", "media_ref", "media_type"}
    }
    details["attached_file_id"] = file_id
    details["attached_mime_type"] = mime_type
    return json.dumps(details, default=str, skipkeys=True)


def _build_audio_ref_blocks(output: dict[str, Any]) -> list[Any]:
    """Turn an ``audio_ref`` tool output into provider-native content blocks.

    Sibling of ``_build_image_ref_blocks`` / ``_build_document_ref_blocks``:
    the audio is addressed by ``file_id`` (the provider path resolves it to
    bytes before the call), never by a URL that expires between the tool
    result and the next turn that replays it.
    """
    from matrx_ai.config import AudioContent, TextContent

    media_ref = output.get("media_ref") or {}
    file_id = media_ref.get("file_id") if isinstance(media_ref, dict) else None
    mime_type = (
        (media_ref.get("mime_type") if isinstance(media_ref, dict) else None)
        or output.get("media_type")
        or "audio/mpeg"
    )

    blocks: list[Any] = []
    if file_id:
        blocks.append(AudioContent(file_id=file_id, mime_type=mime_type))
    else:
        err = output.get("media_ref_error") or "audio_upload_failed"
        blocks.append(TextContent(text=f"[audio attachment unavailable: {err}]"))
    blocks.append(TextContent(text=_ref_details_text(output, file_id=file_id, mime_type=mime_type)))
    return blocks


def _build_video_ref_blocks(output: dict[str, Any]) -> list[Any]:
    """``_build_audio_ref_blocks`` for video — identity in, expiring url out."""
    from matrx_ai.config import TextContent, VideoContent

    media_ref = output.get("media_ref") or {}
    file_id = media_ref.get("file_id") if isinstance(media_ref, dict) else None
    mime_type = (
        (media_ref.get("mime_type") if isinstance(media_ref, dict) else None)
        or output.get("media_type")
        or "video/mp4"
    )

    blocks: list[Any] = []
    if file_id:
        blocks.append(VideoContent(file_id=file_id, mime_type=mime_type))
    else:
        err = output.get("media_ref_error") or "video_upload_failed"
        blocks.append(TextContent(text=f"[video attachment unavailable: {err}]"))
    blocks.append(TextContent(text=_ref_details_text(output, file_id=file_id, mime_type=mime_type)))
    return blocks


def _build_media_ref_list_blocks(output: dict[str, Any]) -> list[Any]:
    """A tool output that carried SEVERAL media blobs — one typed block per
    item, in order, each routed to its own kind's builder.

    ``file_ref`` items (a .docx, an opaque octet-stream: no provider has a
    native block for them) fall through to the trailing JSON, which carries
    their ``file_id`` — the handle a file-reading tool needs.
    """
    from matrx_ai.config import TextContent

    blocks: list[Any] = []
    leftovers: list[Any] = []
    for item in output.get("items") or []:
        if _is_image_ref_output(item):
            blocks.extend(_build_image_ref_blocks(item))
        elif _is_audio_ref_output(item):
            blocks.extend(_build_audio_ref_blocks(item))
        elif _is_video_ref_output(item):
            blocks.extend(_build_video_ref_blocks(item))
        elif _is_document_ref_output(item):
            blocks.extend(_build_document_ref_blocks(item))
        else:
            leftovers.append(item)

    rest = {k: v for k, v in output.items() if k not in {"kind", "items"}}
    if leftovers:
        rest["items"] = leftovers
    blocks.append(TextContent(text=json.dumps(to_json_safe(rest), default=str, skipkeys=True)))
    return blocks


def _build_document_ref_blocks(output: dict[str, Any]) -> list[Any]:
    """Turn a cloud-backed tool document into provider-native content blocks."""
    from matrx_ai.config import DocumentContent, TextContent

    media_ref = output.get("media_ref") or {}
    file_id = media_ref.get("file_id")
    mime_type = media_ref.get("mime_type") or output.get("media_type") or "application/pdf"
    # Carry the document's human name so the Anthropic citations enable path
    # (DocumentContent.to_anthropic → _anthropic_citation_fields) can stamp a
    # meaningful `title` — citations against an untitled document are useless.
    ref_metadata = media_ref.get("metadata") if isinstance(media_ref.get("metadata"), dict) else {}
    title = None
    for candidate in (
        output.get("title"),
        output.get("file_name"),
        output.get("filename"),
        output.get("name"),
        media_ref.get("file_name"),
        ref_metadata.get("file_name"),
        ref_metadata.get("original_name"),
        ref_metadata.get("name"),
    ):
        if isinstance(candidate, str) and candidate.strip():
            title = candidate.strip()
            break
    blocks: list[Any] = []
    if file_id:
        doc_metadata: dict[str, Any] = {}
        if title:
            doc_metadata["title"] = title
        blocks.append(DocumentContent(file_id=file_id, mime_type=mime_type, metadata=doc_metadata))
    else:
        blocks.append(TextContent(text="[document attachment unavailable: missing file_id]"))

    details = {
        key: value
        for key, value in output.items()
        if key not in {"kind", "media_ref", "media_type"}
    }
    details["attached_file_id"] = file_id
    details["attached_mime_type"] = mime_type
    blocks.append(TextContent(text=json.dumps(details, default=str, skipkeys=True)))
    return blocks


def _build_image_ref_list_blocks(output: dict[str, Any]) -> list[Any]:
    """Sibling of ``_build_image_ref_blocks`` for a tool result carrying several
    images (e.g. multi-viewport page capture) — one ``ImageContent``/``TextContent``
    pair per item, in order, so a multimodal model sees every screenshot.

    An optional ``details`` dict on the list output (attached by the tool after
    ``upload_image_masters``, e.g. cms_verify's http_status/console_errors) is
    emitted as one trailing ``TextContent`` JSON block — images AND structured
    metadata both reach the model, never one at the expense of the other."""
    from matrx_ai.config import TextContent

    blocks: list[Any] = []
    for item in output.get("items") or []:
        if isinstance(item, dict) and item.get("kind") == "image_ref":
            blocks.extend(_build_image_ref_blocks(item))
    details = output.get("details")
    if isinstance(details, dict) and details:
        try:
            # skipkeys: a non-str key must degrade to a dropped entry, never
            # fail the whole tool-result serialization (adversarial F3).
            text = json.dumps(details, default=str, skipkeys=True)
        except (TypeError, ValueError):  # e.g. circular reference
            text = str(details)[:4000]
        blocks.append(TextContent(text=text))
    return blocks


def build_agent_media_content(output: Any, media_refs: list[dict]) -> list[Any] | None:
    """The blocks a CALLING model sees when a child agent produced media.

    Both agent-as-tool funnels use this — ``agent_call`` and
    ``register_agent_as_tool`` — so a media agent behaves identically whichever
    way it was invoked.

    Deliberately NOT the ``image_ref`` envelope: that is the screenshot shape,
    and ``_build_image_ref_blocks`` keeps only width/height/bytes/session/format
    and labels the block "Screenshot captured.". Routing an agent through it told
    the model a false thing about an image it commissioned and silently dropped
    the agent's own answer, its name, and the ``remember`` write-back status that
    exists precisely so the model learns the write-back FAILED.

    Images become real ``ImageContent`` (the provider path resolves them to bytes
    before the call, so the model SEES them); everything else stays as text,
    addressed by ``file_id`` so the model can hand it to a tool that reads it.
    Returns None when there is no media, so ordinary calls keep their existing
    text-only serialisation byte for byte.
    """
    if not media_refs:
        return None

    from matrx_ai.config import ImageContent, TextContent

    blocks: list[Any] = []
    for ref in media_refs:
        if ref.get("kind") != "image":
            continue
        file_id = ref.get("file_id")
        if not file_id:
            continue
        blocks.append(ImageContent(file_id=file_id, mime_type=ref.get("mime_type") or "image/png"))

    try:
        text = json.dumps(to_json_safe(output), ensure_ascii=False)
    except (TypeError, ValueError):  # the blocks matter more than perfect text
        text = str(output)[:4000]
    blocks.append(TextContent(text=text))
    return blocks


def _build_image_ref_blocks(output: dict[str, Any]) -> list[Any]:
    """Convert an ``image_ref`` output dict into a list of typed content
    blocks suitable for ``ToolResultContent.content``.

    Returns a list mixing ``ImageContent`` (with ``file_id`` /
    ``vision_class`` populated) and ``TextContent`` (descriptive metadata).
    Provider serialisers downstream walk this list, calling each block's
    own ``to_<provider>()`` method.
    """
    from matrx_ai.config import ImageContent, TextContent

    blocks: list[Any] = []
    media_ref = output.get("media_ref") or {}
    file_id = media_ref.get("file_id") if isinstance(media_ref, dict) else None
    vision_class = media_ref.get("vision_class") if isinstance(media_ref, dict) else None
    media_type = output.get("media_type") or "image/png"

    if file_id:
        blocks.append(
            ImageContent(
                file_id=file_id,
                mime_type=media_type,
                vision_class=vision_class,
            )
        )
    else:
        # Upload failed earlier — surface a structured error block to the
        # model so it knows the screenshot wasn't captured.
        err = output.get("media_ref_error") or "image_upload_failed"
        blocks.append(TextContent(text=f"[image upload failed: {err}]"))

    summary_parts: list[str] = []
    if output.get("source_width") and output.get("source_height"):
        summary_parts.append(f"{output['source_width']}x{output['source_height']}")
    if output.get("size_bytes"):
        summary_parts.append(f"{output['size_bytes']} bytes")
    extra: list[str] = []
    for key in ("session_id", "url", "format", "viewport"):
        val = output.get(key)
        if isinstance(val, str) and val:
            extra.append(f"{key}={val}")
    summary_parts.extend(extra)
    summary = "Screenshot: " + ", ".join(summary_parts) if summary_parts else "Screenshot captured."
    blocks.append(TextContent(text=summary))
    return blocks


logger = logging.getLogger(__name__)

_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


class ToolError(BaseModel):
    error_type: str
    message: str
    traceback: str | None = None
    is_retryable: bool = False
    suggested_action: str | None = None

    @field_validator("message", "traceback", "suggested_action")
    @classmethod
    def _strip_ansi(cls, value: str | None) -> str | None:
        # Backstop: ANSI escape codes must never reach a provider payload —
        # they are pure token waste and unreadable to the model. Any hit here
        # means an upstream tool stringified a terminal-formatted error
        # (str(exc) on a matrx-orm exception is the classic) — scream so the
        # source gets fixed, but ship the cleaned text.
        if value and "\x1b[" in value:
            logger.warning(
                "[ToolError] stripped ANSI escape codes from an error field — "
                "an upstream tool is passing terminal-formatted text to the "
                "model (str(exc) on an ORM error?). Fix the source. Head: %r",
                value[:120],
            )
            return _ANSI_ESCAPE_RE.sub("", value)
        return value

    @classmethod
    def from_exception(
        cls,
        exc: BaseException,
        *,
        error_type: str,
        message: str | None = None,
        is_retryable: bool = False,
        suggested_action: str | None = None,
    ) -> ToolError:
        """Build a ToolError from a caught exception WITHOUT losing the stack.

        The canonical way for a tool to turn an exception into a failed
        ``ToolResult``. Use this instead of hand-rolling
        ``ToolError(error_type=..., message=f"... {exc}")`` — that idiom reads
        fine and is quietly catastrophic: it throws the traceback away before
        anything can record it, so the failure reaches the operator as a bare
        one-line string with no file, no line, no stack. A whole class of tool
        bugs has been undebuggable for exactly this reason (the 2026-07-13 RAG
        `$5: 0 (expected str, got int)` hunt: 4 failed calls, zero stack).

        The exception must be handled INSIDE an ``except`` block — the stack is
        read from ``exc.__traceback__``.
        """
        tb_text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        return cls(
            error_type=error_type,
            message=message or f"{type(exc).__name__}: {exc}",
            traceback=tb_text,
            is_retryable=is_retryable,
            suggested_action=suggested_action,
        )

    def to_agent_message(self) -> str:
        parts = [f"TOOL ERROR [{self.error_type}]: {self.message}"]
        if self.suggested_action:
            parts.append(f"Suggested action: {self.suggested_action}")
        if self.traceback:
            parts.append(f"Technical details:\n{self.traceback}")
        return "\n".join(parts)


class HandoffOutcome(BaseModel):
    """The terminal handoff payload: agent B's final answer, delivered as the
    caller's own response. Carried on ``ToolResult.handoff`` when a
    handoff-flagged agent tool succeeds — the orchestrator exits its loop and
    persists ``final_text`` as the conversation's assistant response instead of
    calling the model again."""

    final_text: str
    agent_id: str | None = None
    agent_version_id: str | None = None
    child_conversation_id: str | None = None
    child_execution_id: str | None = None
    model_id: str | None = None
    response_chars: int = 0
    value_ref_key: str | None = None


class ToolResult(BaseModel):
    success: bool
    output: Any = None
    error: ToolError | None = None

    # Process-private provider boundary override. Local executors use this to
    # hand a model typed media blocks sourced from durable local bytes while
    # keeping ``output`` as the compact Content IR value. It is excluded from
    # dumps, logs, database rows, delegation payloads, and API responses.
    provider_content: Any = Field(default=None, exclude=True, repr=False)

    # Delegation channel — distinct from success/failure. True means the call
    # was handed to the client and SUSPENDS the turn: no result has been
    # produced yet, the cx_tool_call row is 'delegated', and the orchestrator must
    # end the turn (not loop) so the client can POST results + /resume. A
    # pending result is NEVER fed to the model as a tool result.
    # See docs/tool_delegation/DELEGATION_LOOP_BUGS.md.
    delegated_pending: bool = False

    # Value-store linkage (Pattern 2 grooming). value_ref_key: this result's
    # content lives in (or was served from) the host's conversation value store
    # under this key — the logger stamps it onto cx_tool_call.value_ref_key so
    # grooming can find the row. auto_stub: the consumer declared the content is
    # needed for THIS turn only — the logger stamps model_stub_at immediately,
    # so the next rebuild replaces the output with the compact stub (the durable
    # copy in the value store is untouched and fetchable).
    value_ref_key: str | None = None
    auto_stub: bool = False

    # Terminal handoff (Pattern 1). Set ONLY on a successful handoff-flagged
    # agent-tool run: the caller's loop exits and delivers handoff.final_text
    # as the conversation's own response — control never returns to the caller
    # (a FAILED handoff rides the normal error tool_result and the loop
    # continues, so the caller can correct and retry).
    handoff_final: bool = False
    handoff: HandoffOutcome | None = None

    # Content IR travels out-of-band beside the unchanged tool payload. These
    # fields are runtime/persistence metadata and are never sent in the model's
    # tool-call arguments or injected into ``output``.
    input_kind: str | None = None
    input_kind_version: int | None = None
    input_kind_checked: bool = False
    input_kind_errors: list[str] = Field(default_factory=list)
    output_kind: str | None = None
    output_kind_version: int | None = None
    output_kind_checked: bool = False
    output_kind_errors: list[str] = Field(default_factory=list)

    @field_validator("output")
    @classmethod
    def _reject_stringified_structures(cls, v: Any) -> Any:
        """Catches the silent-failure antipattern where a tool stringifies a
        dict and assigns it to a scalar output field. Full reference:
        TOOL_OUTPUT_VALIDATION_GATE.md."""
        if not isinstance(v, dict):
            return v
        # Typed byte/text-reader envelopes preserve decoded bytes verbatim. They
        # may legitimately contain a complete JSON/Python object because that is
        # what the process printed or the file contains. Parsing that text here
        # would change the reader's observable output contract. Keep this map
        # closed and keyed by declared ``__kind`` so similarly named fields on
        # ordinary structured tool outputs remain protected by the gate.
        opaque_text_fields_by_kind = {
            "shell_execution": {"stdout", "stderr"},
            "file_read_result": {"content"},
        }
        opaque_text_fields = opaque_text_fields_by_kind.get(v.get("__kind"), set())
        for key, val in v.items():
            if key in opaque_text_fields:
                continue
            if not isinstance(val, str):
                continue
            s = val.strip()
            if len(s) < 2 or s[0] not in "{[" or s[-1] not in "}]":
                continue
            parsed: Any | None = None
            try:
                parsed = json.loads(s)
            except (json.JSONDecodeError, ValueError):
                try:
                    parsed = ast.literal_eval(s)
                except (ValueError, SyntaxError, MemoryError, TypeError):
                    parsed = None
            if not isinstance(parsed, dict | list):
                continue

            parsed_type = type(parsed).__name__

            # ───── LOUD BANNER ─────
            # This is the diagnostic the human / future agent actually
            # reads. No traceback (this gate IS the cause — a traceback
            # would point at pydantic internals and waste reader time).
            # Full state, no truncation. Self-identifying: who, where,
            # why, what was caught, how to fix.
            banner = (
                "\n"
                "================================================================================\n"
                "  MATRX VALIDATION GATE TRIPPED — THIS IS NOT A REAL ERROR\n"
                "================================================================================\n"
                "  Who I am:  ToolResult._reject_stringified_structures\n"
                "             (a Pydantic @field_validator on ToolResult.output)\n"
                "  Where:     packages/matrx-ai/matrx_ai/tools/models.py\n"
                f"  Docs:      {TOOL_OUTPUT_GATE_DOCS}\n"
                "\n"
                "  My job:    Catch the 'silent failure' antipattern where a tool stringifies a\n"
                "             dict / JSON object and assigns it to a scalar output field. When\n"
                "             that happens the outer ToolResult.success usually stays True and\n"
                "             the orchestrator records the call as OK even though the underlying\n"
                "             operation failed. I exist to make that impossible.\n"
                "\n"
                "  WHAT I CAUGHT:\n"
                f"             • output[{key!r}] is a string that parses cleanly as a {parsed_type}.\n"
                "             • That is exactly the shape the antipattern produces.\n"
                "             • I cannot tell from here whether this tool meant to do this\n"
                "               or did it by accident — both look identical at this layer.\n"
                "\n"
                "  HOW TO FIX:\n"
                f"             • If the tool MEANT to return structured data, put the native\n"
                f"               {parsed_type} into output[{key!r}] directly. Do not json.dumps()\n"
                "               it first. The provider serializes tool results to JSON when\n"
                "               handing them to the model anyway, so the model sees the same\n"
                "               payload either way — one fewer escape layer is better.\n"
                "             • If the field is genuinely supposed to be an opaque string blob\n"
                "               that happens to look like JSON, refactor it so the tool returns\n"
                "               the parsed structure under a typed key. The gate has no per-\n"
                "               field opt-out by design — see the docs for the rationale.\n"
                "================================================================================"
            )
            vcprint(banner, color="red")
            vcprint(
                v,
                "[MATRX GATE: ToolResult.output] ↑ FULL output dict received — every key, no truncation",
                color="red",
            )

            # Short, clean exception message — the banner above is the
            # diagnostic. No traceback noise, no Pydantic URL, no preview
            # vomit. Tool except-blocks should detect ToolOutputContractError
            # and emit this message verbatim instead of wrapping it in the
            # default "tool_name failed: <pydantic vomit>" pattern.
            raise ToolOutputContractError(
                f"[MATRX GATE] ToolResult.output[{key!r}] is a stringified "
                f"{parsed_type}. See the red banner in stdout / logs above "
                f"for the full diagnostic. Docs: {TOOL_OUTPUT_GATE_DOCS}"
            )
        return v

    usage: dict[str, Any] | None = None
    child_usages: list[TokenUsage] = Field(default_factory=list)

    started_at: float = 0.0
    completed_at: float = 0.0
    duration_ms: int = 0

    tool_name: str = ""
    call_id: str = ""
    retry_count: int = 0

    should_persist_output: bool = False
    persist_key: str | None = None

    # Output metadata — populated by ToolExecutionLogger after serialization.
    # Tools that want to control what the UI shows can set output_preview before
    # returning. If left as None the logger synthesizes a sensible default.
    output_chars: int = 0
    """Character count of the serialized output. Set by the logger, not the tool."""

    output_preview: dict[str, Any] | None = None
    """Lightweight structured hint for UI rendering (max ~20 keys / 500 chars).
    Tools can return a custom dict here (e.g. {"pages_scraped": 5, "urls": [...]}).
    If None the logger synthesizes a default from the output type and size."""

    # ── Output-size self-management contract (the tool-result size gate) ──────────
    # The platform caps how many characters a single tool result may put in front
    # of the model (matrx_ai.tools.output_caps.TOOL_RESULT_SOFT_CAP_CHARS), then a
    # hard absolute ceiling at the provider boundary. A blunt generic truncation
    # DESTROYS structured results, so the real contract is: every tool that can
    # produce a large result is RESPONSIBLE for truncating it surgically itself
    # and declaring it did. These two fields are how a tool declares that.
    output_self_capped: bool = False
    """The tool managed its own output size (truncated long fields surgically and
    offered the agent a way to fetch more). When True, the universal SOFT cap
    stands down — the tool is trusted. If a tool produces an oversized result
    WITHOUT setting this, the soft cap fires AND records a 'tool defect' alarm:
    that tool needs to be taught to manage itself. See output_caps.py."""

    approved_max_chars: int | None = None
    """An explicit, tool-authorized model-visible character ceiling for THIS result
    (e.g. the agent asked for a higher per-item limit and the tool honored it).
    Raises the absolute provider-boundary ceiling for this one result only. When
    None, even a self-capped result is still bounded by the absolute ceiling —
    fail-safe, so a tool that forgets to authorize a huge payload is still caught."""

    model_config = {"arbitrary_types_allowed": True}

    def compute_duration(self) -> None:
        if self.started_at and self.completed_at:
            self.duration_ms = int((self.completed_at - self.started_at) * 1000)

    def to_tool_result_content(self) -> dict[str, Any]:
        """Return a dict that can construct an existing ToolResultContent dataclass.

        Keys match the ToolResultContent.__init__ signature defined in
        ai.config.tools_config so the caller can do:
            ToolResultContent(**result.to_tool_result_content())

        Canonical media-ref outputs become typed content blocks so provider
        serializers receive real image/document inputs, never cloud IDs or
        base64 blobs serialized as ordinary tool-result text.
        """
        if self.success:
            if self.provider_content is not None:
                content = self.provider_content
            else:
                content = self.output
                if _is_image_ref_output(content):
                    content = _build_image_ref_blocks(content)
                elif _is_image_ref_list_output(content):
                    content = _build_image_ref_list_blocks(content)
                elif _is_document_ref_output(content):
                    content = _build_document_ref_blocks(content)
                elif _is_audio_ref_output(content):
                    content = _build_audio_ref_blocks(content)
                elif _is_video_ref_output(content):
                    content = _build_video_ref_blocks(content)
                elif _is_media_ref_list_output(content):
                    content = _build_media_ref_list_blocks(content)
                elif not isinstance(content, str):
                    content = (
                        json.dumps(to_json_safe(content), ensure_ascii=False)
                        if content is not None
                        else ""
                    )
        else:
            # Failure: lead with the error message, but ALSO include any
            # structured output the tool returned. Some tools (shell_execute,
            # shell_python, db_*) put genuinely useful diagnostic data in
            # ``output`` even when ``exit_code != 0`` — stdout/stderr,
            # partial query rows, etc. Hiding it leaves the agent with
            # only "TOOL ERROR" and no way to recover; surfacing it lets
            # the agent reason about what actually happened.
            error_text = self.error.to_agent_message() if self.error else "Unknown error"
            if self.output not in (None, "", {}, []):
                output_text = self.output
                if isinstance(output_text, dict | list):
                    output_text = json.dumps(to_json_safe(output_text), ensure_ascii=False)
                elif not isinstance(output_text, str):
                    output_text = str(output_text)
                content = f"{error_text}\n\n--- output ---\n{output_text}"
            else:
                content = error_text

        payload: dict[str, Any] = {
            "tool_use_id": self.call_id,
            "call_id": self.call_id,
            "name": self.tool_name,
            "content": content,
            "is_error": not self.success,
            "output_chars": self.output_chars,
            "output_preview": self.output_preview,
            "approved_max_chars": self.approved_max_chars,
        }
        # Side-channel for cx_request.tool_calls_details enrichment — stripped
        # before ToolResultContent(**…) so it never reaches the provider wire.
        if not self.success and self.error is not None:
            payload["error"] = self.error.model_dump(exclude_none=True)
        return payload


class GuardrailResult(BaseModel):
    blocked: bool = False
    reason: str | None = None
    error_type: str = "guardrail"
    suggested_action: str | None = None

    def to_tool_result_content(self, call_id: str = "", tool_name: str = "") -> dict[str, Any]:
        error_msg = f"TOOL BLOCKED [{self.error_type}]: {self.reason or 'Guardrail triggered'}"
        if self.suggested_action:
            error_msg += f"\nSuggested action: {self.suggested_action}"
        error_obj: dict[str, Any] = {
            "error_type": self.error_type,
            "message": self.reason or "Guardrail triggered",
        }
        if self.suggested_action:
            error_obj["suggested_action"] = self.suggested_action
        return {
            "tool_use_id": call_id,
            "call_id": call_id,
            "name": tool_name,
            "content": error_msg,
            "is_error": True,
            "error": error_obj,
        }


# Canonical AppContext.metadata key carrying the current agent-nesting depth.
# One SSOT for BOTH nesting guards: agent_call's MAX_AGENT_CALL_DEPTH check and
# the ToolType.AGENT max_recursion_depth guardrail. Bumped on the parent's
# metadata BEFORE an agent fork (the child's copied metadata inherits it),
# restored after, and read by the orchestrator when building ToolContexts so a
# CHILD agent's loop knows how deep it already is. Without this threading the
# guardrail sees depth 0 forever and nested agents recurse unbounded.
AGENT_DEPTH_METADATA_KEY = "agent_call_depth"


def read_agent_depth(metadata: dict[str, Any] | None) -> int:
    try:
        return int((metadata or {}).get(AGENT_DEPTH_METADATA_KEY, 0) or 0)
    except (TypeError, ValueError):
        return 0


class ToolContext(BaseModel):
    call_id: str
    tool_name: str = ""
    iteration: int = 0
    message_id: str | None = None
    parent_agent_name: str | None = None
    user_role: str = "user"
    recursion_depth: int = 0
    cost_budget_remaining: float | None = None
    calls_remaining_this_conversation: int | None = None

    model_config = {"arbitrary_types_allowed": True}

    @property
    def user_id(self) -> str:
        from matrx_ai.context.app_context import get_app_context

        return get_app_context().user_id

    @property
    def conversation_id(self) -> str:
        from matrx_ai.context.app_context import get_app_context

        return get_app_context().conversation_id

    @property
    def request_id(self) -> str:
        from matrx_ai.context.app_context import get_app_context

        return get_app_context().request_id

    @property
    def emitter(self) -> Emitter | None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        return ctx.emitter if ctx else None

    @property
    def api_keys(self) -> dict[str, str]:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        # Return a copy so no tool can accidentally mutate the parent context's key store.
        return dict(ctx.api_keys) if ctx else {}

    @property
    def project_id(self) -> str | None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        return ctx.project_id if ctx else None

    @property
    def organization_id(self) -> str | None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        return ctx.organization_id if ctx else None

    # ------------------------------------------------------------------
    # Phase D-loop — dynamic mid-loop tool mutation API.
    # A registered tool can call ``ctx.queue_tool_changes(...)`` from
    # inside its handler. Pending mutations are drained between turns by
    # the orchestrator and applied via ``merge_request_tools``. The next
    # API call to the model sees the updated tool set.
    # ------------------------------------------------------------------

    def queue_tool_changes(
        self,
        *,
        add: list[Any] | None = None,
        remove: list[str] | None = None,
    ) -> None:
        """Queue a mutation of the agent's active tool set.

        The orchestrator drains queued mutations between iterations and
        feeds them through ``merge_request_tools``. Mutations apply to the
        rest of the *current request* only — phase D-loop's persistence
        layer (cx_conversation.dynamic_tool_state) will land in a follow-up
        and extend that to cross-request continuity.

        Parameters
        ----------
        add
            List of ``ToolSpec`` dicts (or pre-validated ``ToolSpec``
            instances) to merge into the active set on the next turn.
        remove
            List of tool names to drop from the active set on the next
            turn. Useful for "discovery" tools that remove themselves
            after loading the relevant subset for the agent.

        Notes
        -----
        Order doesn't matter — adds and removes within the same call are
        both applied at the next drain. Conflicts (same name in both
        lists) result in removal winning. Mutations queued by a tool
        within iteration N take effect at iteration N+1; tools cannot
        affect the iteration they're running in.

        Cross-task safety
        -----------------
        Tools run inside ``asyncio.gather(...)`` child Tasks. Each Task
        gets its OWN copy of the ``_app_context`` ContextVar at creation
        (Python's ``contextvars.copy_context()``), so calling
        ``set_app_context`` from a tool would update only the child Task's
        snapshot — the parent orchestrator would never see the queued
        mutations. To bridge the gap, this method mutates the
        ``ctx.metadata`` **dict in place**. The dict object is shared
        between the parent's AppContext and the child's snapshot (the dict
        reference was copied, not the dict itself), so an in-place update
        is visible from both. See AppContext docstring re: mutable metadata.
        """
        if not add and not remove:
            return

        from matrx_utils import vcprint

        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        if ctx is None:
            vcprint(
                f"[queue_tool_changes] no AppContext — mutation dropped (by={self.tool_name!r})",
                color="yellow",
            )
            return  # No active request context — defensive no-op.

        # Mutate in place so the parent task's AppContext sees the queue.
        # ``setdefault`` on the SAME dict object the parent holds.
        pending = ctx.metadata.setdefault(_PENDING_TOOL_MUTATIONS_KEY, [])

        # Serialise specs so we don't keep references to BaseModel instances
        # across context boundaries.
        if add:
            serialised: list[Any] = []
            for spec in add:
                if hasattr(spec, "model_dump"):
                    serialised.append(spec.model_dump())
                elif isinstance(spec, dict):
                    serialised.append(dict(spec))
                else:
                    raise TypeError(
                        f"queue_tool_changes(add=...) requires ToolSpec "
                        f"instances or dicts; got {type(spec).__name__}"
                    )
            pending.append({"action": "add", "specs": serialised, "by": self.tool_name})
        if remove:
            pending.append({"action": "remove", "names": list(remove), "by": self.tool_name})

        vcprint(
            f"[queue_tool_changes] by={self.tool_name!r} +{len(add or [])} "
            f"-{len(remove or [])} (queue depth now {len(pending)})",
            color="cyan",
        )


# Key under AppContext.metadata where queued mutations live until drained.
_PENDING_TOOL_MUTATIONS_KEY = "pending_tool_mutations"


CustomToolInputSchema = CustomToolInputSchemaBase


class CustomTool(CustomToolBase):
    """Inline tool with provider formatting — extends the wire schema in custom_tool.py."""

    def get_provider_format(self, provider: str) -> dict[str, Any]:
        """Render this tool in the format expected by the given provider.

        Matches the ToolDefinition.get_provider_format() interface so
        translators can treat CustomTool and ToolDefinition identically.
        """
        schema = self.input_schema.model_dump(by_alias=True, exclude_none=True)
        schema["additionalProperties"] = False
        property_dicts = {
            name: prop.model_dump(by_alias=True, exclude_none=True)
            for name, prop in self.input_schema.properties.items()
        }
        if provider in ("openai",):
            return {
                "type": "function",
                "name": self.name,
                "description": self.description,
                "parameters": schema,
            }
        if provider in ("cerebras", "xai", "together", "groq", "generic_openai"):
            return {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": schema,
                },
            }
        if provider == "anthropic":
            return {
                "name": self.name,
                "description": self.description,
                "input_schema": schema,
            }
        if provider == "google":
            missing_items: list[str] = []
            properties: dict[str, Any] = {
                param_name: _normalize_google_schema(
                    param_schema, missing_items=missing_items, path=param_name
                )
                for param_name, param_schema in property_dicts.items()
            }
            if missing_items:
                _warn_google_missing_items(self.name, missing_items)
            params: dict[str, Any] = {"type": "object", "properties": properties}
            if self.input_schema.required:
                params["required"] = self.input_schema.required
            return {
                "name": self.name,
                "description": self.description,
                "parameters": params,
            }
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": schema,
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CustomTool:
        """Reconstruct from a stored JSONB dict (agents.custom_tools rows)."""
        raw_schema = data.get("input_schema", data.get("inputSchema", {}))
        if isinstance(raw_schema, dict):
            schema = CustomToolInputSchema(
                type=raw_schema.get("type", "object"),
                properties=raw_schema.get("properties", {}),
                required=raw_schema.get("required", []),
            )
        else:
            schema = CustomToolInputSchema()
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            input_schema=schema,
        )


class ToolDefinition(BaseModel):
    name: str = Field(description="Unique tool identifier")
    tool_id: str | None = Field(default=None, description="Database UUID for this tool")
    description: str = ""
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Internal parameter schema (key→property dict). Converted to JSON Schema by format methods.",
    )
    required_params: list[str] = Field(
        default_factory=list,
        description=(
            "Top-level required parameter names carried alongside "
            "``parameters``. The internal notation marks a required param "
            "with a per-property ``required: true`` BOOL — but that key is "
            "overloaded (on an object-typed property it holds the NESTED "
            "required LIST), so a source that supplies a full JSON schema "
            "(a tool.definition row's ``{type, properties, required}``) "
            "records its top-level required list here instead. "
            "``_build_json_schema`` merges both notations."
        ),
    )
    output_schema: dict[str, Any] | None = None
    annotations: list[dict[str, Any]] = Field(default_factory=list)

    @field_validator("annotations", mode="before")
    @classmethod
    def _coerce_annotations(cls, value: Any) -> Any:
        # Registry rows may carry MCP-style annotations — ONE object
        # ({"title": ..., "destructiveHint": false}) — while this field is
        # list-shaped. A dict-shaped row must not fail validation: one such
        # row aborted a client host's entire remote-tool refresh (matrx-local,
        # 2026-08-30). Wrap the object form; None means "none".
        if value is None:
            return []
        if isinstance(value, dict):
            return [value]
        return value
    side_effect_class: str | None = Field(
        default=None,
        description=(
            "Host-classified execution effect. NULL/unknown is intentionally "
            "handled as maximally consequential by host authorization policy."
        ),
    )

    tool_type: ToolType = ToolType.LOCAL
    function_path: str = Field(default="", description="Dotted import path or 'agent:<prompt_id>'")
    source_kind: str = Field(
        default="native",
        description=(
            "Origin classification for this tool row. One of "
            "'native' (first-party server tool), 'mcp_discovered' "
            "(synced from an external MCP server), 'admin_authored' "
            "(custom tool created in the admin UI), 'agent_authored' "
            "(custom tool created by an agent / inline injection)."
        ),
    )
    managed_by_server_id: str | None = Field(
        default=None,
        description=(
            "FK to tool_mcp_server.id when this tool is owned by a remote "
            "MCP server (source_kind='mcp_discovered'). NULL otherwise."
        ),
    )

    category: str | None = None
    tags: list[str] = Field(default_factory=list)
    icon: str | None = None
    is_active: bool = True
    semver: str = "1.0.0"
    version: int = 1

    # ``gating`` is a list of ``{"gate": <name>, "args": {...}}`` entries the
    # discovery handler reads to filter tools per-request (admin gate,
    # optional-permission gate, etc.). The named gates themselves live in
    # code, not in a DB table.
    tier: str | None = None
    admin_only: bool = False
    gating: list[dict[str, Any]] = Field(default_factory=list)

    prompt_id: str | None = None
    prompt_is_version: bool = Field(
        default=False,
        description=(
            "For agent-type tools: prompt_id points at an agent VERSION row, "
            "so dispatch must load it with is_version=True."
        ),
    )
    result_mode: str = Field(
        default="inline",
        description=(
            "For agent-type tools: 'inline' returns the child's full output in "
            "the tool_result; 'reference' stores it in the host's conversation "
            "value store and returns only a bounded descriptor; 'inline_once' "
            "does both (full output now, stored for later stubbing)."
        ),
    )
    handoff_terminal: bool = Field(
        default=False,
        description=(
            "For agent-type tools: a successful run ENDS the caller's loop and "
            "delivers the child's streamed answer as the conversation's own "
            "response (Pattern 1 — Agent Handoff). Failure returns to the "
            "caller as a normal error tool_result."
        ),
    )
    mcp_server_url: str | None = None
    mcp_server_auth: dict[str, Any] | None = None
    mcp_transport: str | None = Field(
        default=None,
        description="MCP transport resolved from tool.mcp_server (http or stdio).",
    )
    mcp_command: str | None = Field(
        default=None,
        description="Executable for a local stdio MCP launch recipe.",
    )
    mcp_args: list[str] = Field(
        default_factory=list,
        description="Arguments for a local stdio MCP launch recipe.",
    )
    mcp_env: dict[str, str] = Field(
        default_factory=dict,
        description="Non-secret environment values for a local MCP subprocess.",
    )
    mcp_tool_allowlist: list[str] = Field(
        default_factory=list,
        description=(
            "Remote-local MCP names this registered server permits. Empty means "
            "the server did not declare a catalog-level restriction."
        ),
    )

    max_calls_per_conversation: int | None = None
    max_calls_per_minute: int | None = None
    cost_cap_per_call: float | None = None
    dedupe_exempt: bool = False
    timeout_seconds: float = 120.0
    must_complete: bool = Field(
        default=False,
        description=(
            "The execution may outlive its timeout and request task. Use for "
            "paid or otherwise irreversible work that must reach a provider "
            "terminal result before cancellation is propagated."
        ),
    )
    max_client_wait_seconds: int | None = None
    max_recursion_depth: int = 3

    on_call_message_template: str | None = None

    _callable: Callable[..., Awaitable[Any]] | None = PrivateAttr(default=None)
    _routed_to_vfs: bool = PrivateAttr(default=False)
    _original_function_path: str | None = PrivateAttr(default=None)

    model_config = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context: Any) -> None:
        if self.tool_type == ToolType.AGENT:
            self.must_complete = True

    # ------------------------------------------------------------------
    # JSON Schema helpers (ported from mcp_server/core/definitions.py)
    # ------------------------------------------------------------------

    def _provider_parameters(self) -> dict[str, Any]:
        variants = self.parameters.get("$variants")
        if not isinstance(variants, dict) or not variants:
            return self.parameters

        variant_names = set(variants)
        discriminator: str | None = None
        for key, raw_spec in self.parameters.items():
            if key.startswith("$") or not isinstance(raw_spec, dict):
                continue
            enum = raw_spec.get("enum")
            if isinstance(enum, list) and set(enum) == variant_names:
                discriminator = key
                break
        if discriminator is None:
            return self.parameters

        variant_maps: list[dict[str, Any]] = []
        variant_required: list[set[str]] = []
        for value in variants.values():
            if not isinstance(value, dict):
                return self.parameters
            # Generated registry contracts store each action as a standalone
            # JSON-Schema object. Older hand-authored rows stored the property
            # map directly; accept both shapes while producing one provider
            # schema.
            properties = value.get("properties")
            if isinstance(properties, dict):
                variant_maps.append(properties)
                required = value.get("required", [])
                variant_required.append(set(required) if isinstance(required, list) else set())
            else:
                variant_maps.append(value)
                variant_required.append(
                    {
                        key
                        for key, spec in value.items()
                        if isinstance(spec, dict) and spec.get("required") is True
                    }
                )
        if len(variant_maps) != len(variants):
            return self.parameters

        flattened: dict[str, Any] = {
            discriminator: self.parameters[discriminator],
        }
        all_fields = {key for variant in variant_maps for key in variant}
        required_in_all = set.intersection(*variant_required)

        for key in sorted(all_fields):
            variant_specs = [
                variant[key]
                for variant in variant_maps
                if key in variant and isinstance(variant[key], dict)
            ]
            first_variant_spec = next(
                (
                    variant[key]
                    for variant in variant_maps
                    if key in variant and isinstance(variant[key], dict)
                ),
                {},
            )
            root_spec = self.parameters.get(key)
            variant_types = {
                spec["type"]
                for spec in variant_specs
                if isinstance(spec.get("type"), str)
            }
            if len(variant_types) > 1:
                # A generated dispatcher root can retain the first variant's
                # stale scalar type even though the variants are the execution
                # authority. Flattening cannot express an action-dependent
                # field, so incompatible types stay unconstrained.
                chosen = {
                    "description": (
                        root_spec.get("description", "")
                        if isinstance(root_spec, dict)
                        else ""
                    )
                }
            elif isinstance(root_spec, dict) and "type" not in root_spec and "anyOf" not in root_spec:
                # The generated root is the union contract.  An omitted type
                # deliberately means that this field has incompatible shapes
                # across actions (dataset.data is array on create and object
                # on update_row).  Do not let whichever variant appears first
                # narrow that union back to its own local shape.
                chosen = root_spec
            else:
                chosen = (
                    {**root_spec, **first_variant_spec}
                    if isinstance(root_spec, dict)
                    else first_variant_spec
                )
            flattened[key] = {**chosen, "required": key in required_in_all}

        return flattened

    def _build_json_schema(self, *, strip_openai_unsupported: bool = False) -> dict[str, Any]:
        properties: dict[str, Any] = {}
        required: list[str] = []

        for key, param in self._provider_parameters().items():
            if key.startswith("$"):
                # `$`-prefixed keys (e.g. `$variants`) are internal contract
                # metadata, NOT tool parameters. They must never reach a provider's
                # input_schema — Anthropic rejects property keys that fall outside
                # `^[a-zA-Z0-9_.-]{1,64}$`. The drift validator reads `$variants`
                # straight from the raw tool_def row, so skipping it here is safe.
                continue
            if isinstance(param, str):
                param = {"type": param}
            if isinstance(param.get("anyOf"), list) and "type" not in param:
                # Union-shaped parameter WITHOUT a resolved type (e.g. an OPEN
                # enum from projected agent variables: anyOf [enum, string] —
                # "these options OR any string"). anyOf is valid JSON Schema
                # for every provider we target; pass the variants through
                # verbatim. (Registry rows that carry anyOf BESIDE a resolved
                # `type` keep the historical type-first path below.)
                prop = {
                    "anyOf": [
                        self._process_nested(v, strip_openai_unsupported) for v in param["anyOf"]
                    ],
                    "description": param.get("description", ""),
                }
                if "default" in param:
                    prop["default"] = param["default"]
                properties[key] = prop
                if param.get("required", False):
                    required.append(key)
                continue
            # In JSON Schema, an omitted ``type`` means any JSON value. DB-backed
            # dispatcher rows legitimately use that shape when one action accepts
            # an object while another accepts a different shape under the same
            # field name. Defaulting the omission to ``string`` made the provider
            # and Content IR contracts narrower than the row and the executor.
            raw_type = param.get("type", "any")
            if isinstance(raw_type, list):
                non_null = [t for t in raw_type if t != "null"]
                # A nullable scalar can keep its one concrete provider type.
                # A genuine multi-type union cannot: choosing the first member
                # silently narrows the execution contract. An omitted type is
                # the honest flattened representation of any JSON value.
                raw_type = non_null[0] if len(non_null) == 1 else "any"
            if raw_type == "any":
                # The internal notation for a Pydantic ``Any`` field. NOT a
                # valid JSON-Schema type ("any" 400s Anthropic AND Gemini) —
                # a property with NO type constraint is the spec-correct way
                # to say "any value" (draft 2020-12).
                properties[key] = {"description": param.get("description", "")}
                if param.get("required", False):
                    required.append(key)
                continue
            prop: dict[str, Any] = {
                "type": raw_type,
                "description": param.get("description", ""),
            }
            if raw_type == "array" and "items" in param:
                prop["items"] = self._process_nested(param["items"], strip_openai_unsupported)
            for f in (
                "minItems",
                "maxItems",
                "uniqueItems",
                "minimum",
                "maximum",
                "multipleOf",
                "pattern",
            ):
                if f in param and not strip_openai_unsupported:
                    prop[f] = param[f]
            if "default" in param:
                prop["default"] = param["default"]
            if "enum" in param:
                prop["enum"] = param["enum"]
            if prop["type"] == "object" and "properties" in param:
                prop["properties"] = {
                    sk: self._process_nested(sv, strip_openai_unsupported)
                    for sk, sv in param["properties"].items()
                }
                nested_required = param.get("required", [])
                prop["required"] = nested_required if isinstance(nested_required, list) else []
                prop["additionalProperties"] = False

            properties[key] = prop
            if param.get("required", False):
                required.append(key)

        # Merge the schema-level required list (tool.definition rows carry
        # ``required: [...]`` at the top of the JSON schema; the per-property
        # bool notation can't express it for object-typed params without
        # clobbering their NESTED required list — see required_params).
        for key in self.required_params:
            if key in properties and key not in required:
                required.append(key)

        return {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        }

    def content_ir_contracts(self) -> tuple[Any, Any | None]:
        """Return exact framed I/O contracts using provider-normalized input.

        The stable identity includes the database UUID when available so two
        organizations may use the same display name without sharing a kind.
        An undeclared output remains intentionally opaque (``None``).
        """
        from matrx_graph.contract_kinds import (
            ContractDirection,
            ContractFamily,
            contract_definition,
        )

        input_schema = self._build_json_schema()
        if self.tool_id:
            source_name = f"{self.name}:{self.tool_id}"
        else:
            # Inline/client-surface tools deliberately reuse one display name
            # with request-local schemas.  The schema is therefore part of the
            # contract's identity: name-only identity merged unrelated surface
            # targets into one generated kind and one patrol error class.
            schema_digest = hashlib.sha256(
                json.dumps(
                    input_schema,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=True,
                ).encode("utf-8")
            ).hexdigest()[:16]
            source_name = f"{self.name}:schema:{schema_digest}"
        input_contract = contract_definition(
            family=ContractFamily.TOOL_IO,
            source_name=source_name,
            direction=ContractDirection.INPUT,
            json_schema=input_schema,
            label=f"{self.name} input",
            version=self.version,
            source_id=str(self.tool_id) if self.tool_id else None,
        )
        output_contract = (
            contract_definition(
                family=ContractFamily.TOOL_IO,
                source_name=source_name,
                direction=ContractDirection.OUTPUT,
                json_schema=self.output_schema,
                label=f"{self.name} output",
                version=self.version,
                source_id=str(self.tool_id) if self.tool_id else None,
            )
            if isinstance(self.output_schema, dict)
            else None
        )
        return input_contract, output_contract

    @staticmethod
    def _process_nested(schema: dict[str, Any] | str, strip_unsupported: bool) -> dict[str, Any]:
        if isinstance(schema, str):
            return {"type": schema}
        processed = schema.copy()
        if strip_unsupported:
            for f in (
                "minItems",
                "maxItems",
                "uniqueItems",
                "minimum",
                "maximum",
                "multipleOf",
                "pattern",
            ):
                processed.pop(f, None)
        if processed.get("type") == "object" and "properties" in processed:
            processed["additionalProperties"] = False
            nested_required = processed.get("required", [])
            processed["required"] = nested_required if isinstance(nested_required, list) else []
            processed["properties"] = {
                k: ToolDefinition._process_nested(v, strip_unsupported)
                for k, v in processed["properties"].items()
            }
        elif processed.get("type") == "array" and "items" in processed:
            processed["items"] = ToolDefinition._process_nested(
                processed["items"], strip_unsupported
            )
        return processed

    # ------------------------------------------------------------------
    # Provider format converters
    # ------------------------------------------------------------------

    def to_mcp_format(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self._build_json_schema(),
            "output_schema": self.output_schema or {"type": "null"},
            "annotations": self.annotations,
        }

    def to_openai_format(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self._build_json_schema(strip_openai_unsupported=True),
            },
        }

    def to_openai_responses_format(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self._build_json_schema(strip_openai_unsupported=True),
        }

    def to_google_format(self) -> dict[str, Any]:
        properties: dict[str, Any] = {}
        required: list[str] = []
        missing_items: list[str] = []
        for key, param in self.parameters.items():
            if key.startswith("$"):
                continue  # internal meta ($variants, …) — not a tool parameter
            properties[key] = _normalize_google_schema(param, missing_items=missing_items, path=key)
            if isinstance(param, dict) and param.get("required", False):
                required.append(key)

        if missing_items:
            _warn_google_missing_items(self.name, missing_items)

        for key in self.required_params:
            if key in properties and key not in required:
                required.append(key)

        params_schema: dict[str, Any] = {"type": "object", "properties": properties}
        if required:
            params_schema["required"] = required
        return {
            "name": self.name,
            "description": self.description,
            "parameters": params_schema,
        }

    def to_anthropic_format(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self._build_json_schema(),
        }

    def get_provider_format(self, provider: str) -> dict[str, Any]:
        formatters: dict[str, Callable[[], dict[str, Any]]] = {
            "openai": self.to_openai_responses_format,
            "anthropic": self.to_anthropic_format,
            "google": self.to_google_format,
            "cerebras": self.to_openai_format,
            "xai": self.to_openai_format,
            "together": self.to_openai_format,
            "groq": self.to_openai_format,
            "mcp": self.to_mcp_format,
        }
        return formatters.get(provider, self.to_openai_format)()

    # ------------------------------------------------------------------
    # User-facing message
    # ------------------------------------------------------------------

    def format_user_message(self, arguments: dict[str, Any]) -> str:
        if not self.on_call_message_template:
            return f"Executing {' '.join(self.name.split('_')).title()}"
        message = self.on_call_message_template
        for placeholder in re.findall(r"\{\{(\w+)\}\}", message):
            if placeholder in arguments:
                val = arguments[placeholder]
                replacement = ", ".join(str(i) for i in val) if isinstance(val, list) else str(val)
                message = message.replace(f"{{{{{placeholder}}}}}", replacement)
        return message


CxToolCallStatus = Literal["pending", "running", "completed", "error"]


class CxToolCallRecord(BaseModel):
    """Row in the ``cx_tool_call`` table — single source of truth for a tool call.

    Two-phase lifecycle:
      1. INSERT with status='running' when execution starts (captures the attempt)
      2. UPDATE with status='completed'/'error' when execution finishes

    cx_message rows with role='tool' are lightweight positional markers;
    the full data lives here.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    # Relationships
    conversation_id: str
    message_id: str | None = None
    created_by: str
    request_id: str | None = None

    # Tool identity
    tool_name: str
    tool_type: ToolType = ToolType.LOCAL
    call_id: str

    # Lifecycle status
    status: CxToolCallStatus = "pending"

    # Input
    arguments: dict[str, Any] = Field(default_factory=dict)

    # Output (single source of truth)
    success: bool = True
    output: str | None = None
    output_type: str = "text"
    is_error: bool = False
    error_type: str | None = None
    error_message: str | None = None

    # Performance
    duration_ms: int = 0
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Cost / usage
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: Decimal = Decimal("0")

    # Execution context
    iteration: int = 0
    retry_count: int = 0
    parent_call_id: str | None = None

    # Streaming events (accumulated during execution, written once)
    execution_events: list[dict[str, Any]] = Field(default_factory=list)

    # Persistence
    persist_key: str | None = None
    file_path: str | None = None

    # Output metadata (mirrors ToolResult fields; written by the logger)
    output_chars: int = 0
    """Character count of the serialized output — enables size display without loading output."""

    output_preview: dict[str, Any] | None = None
    """Lightweight structured hint for UI rendering. Tool-supplied or logger-synthesized."""

    # Standard cx_ fields
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime | None = None

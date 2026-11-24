"""The media-fallback handler — the central "DO SOMETHING" seam for media a
provider can't accept.

When a request carries a document / video / YouTube URL the target provider would
SILENTLY drop (no native support, no transcribe-style fallback — see
``provider_io_capabilities``), this handler runs BEFORE dispatch and, per media item:

  1. routes it to a registered RESOLVER for its container, if one exists;
  2. a resolver RETURNS a ``TextContent`` replacement the model can read;
  3. ALWAYS logs loudly AND emits an inline ``MediaNoticeData`` stream event so the
     (agentic-engineer) user sees exactly what happened, right where it happened;
  4. tracks any extra model-call usage so cost isn't lost.

No resolver, a resolver exception, or an empty conversion is a terminal
``MediaFallbackResolutionError`` after the notice/log. Unsupported media is never
silently omitted and the provider is never called with a partially stripped request.

Mirrors ``processing/audio/audio_preprocessing.py`` (which swaps AudioContent → text via
transcription). Audio is handled there and is intentionally NOT seen here (it has its own
fallback). Wired from ``unified_client.execute`` after audio preprocessing.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config import MessageList, TextContent, TokenUsage, UnifiedMessage
from matrx_ai.providers.provider_io_capabilities import (
    MediaContainer,
    container_for_content,
    content_needs_fallback,
    find_unsupported_media,
)


@dataclass
class MediaResolveContext:
    endpoint: str | None
    model_name: str
    # The user's accompanying text in the request — passed to a resolver so it can
    # extract intelligently ("the user is asking about X in this video").
    user_text_hint: str = ""
    debug: bool = False


@dataclass
class ResolverResult:
    # None means conversion failed and the request must terminate. A TextContent
    # means the media was converted and can replace the original item.
    replacement: TextContent | None
    action: str  # "extracted" | "transcribed" | "converted" | "dropped"
    user_message: str  # FE-facing, shown inline in the stream
    system_message: str = ""  # fuller detail for the loud log
    usage: list[TokenUsage] = field(default_factory=list)


Resolver = Callable[[Any, MediaResolveContext], Awaitable[ResolverResult]]

_RESOLVERS: dict[MediaContainer, Resolver] = {}


class MediaFallbackResolutionError(RuntimeError):
    def __init__(
        self,
        container: MediaContainer,
        *,
        model_name: str,
        endpoint: str | None,
        detail: str,
    ) -> None:
        self.container = container
        self.model_name = model_name
        self.endpoint = endpoint
        self.detail = detail
        super().__init__(
            f"{container.value} media could not be converted for model "
            f"{model_name!r} (endpoint={endpoint!r}): {detail}"
        )


def register_media_resolver(container: MediaContainer, resolver: Resolver) -> None:
    """Register the resolver for a media container. The seam: adding real handling
    for video/youtube/etc. later is a single call here."""
    _RESOLVERS[container] = resolver


def assert_media_resolvers_registered(
    required: set[MediaContainer] | frozenset[MediaContainer],
) -> None:
    missing = sorted(container.value for container in required if container not in _RESOLVERS)
    if missing:
        raise RuntimeError(
            "Required media fallback resolvers are not registered: " + ", ".join(missing)
        )


_DEFAULT_DROP_MESSAGES: dict[MediaContainer, str] = {
    MediaContainer.YOUTUBE: (
        "YouTube video removed — this model can't accept YouTube videos as input. "
        "Use a Google/Gemini model (it ingests YouTube URLs directly)."
    ),
    MediaContainer.VIDEO: (
        "Video removed — this model can't accept video files as input. "
        "Use a Google/Gemini model for native video."
    ),
    MediaContainer.DOCUMENT: (
        "Document removed — this provider can't accept documents and the content "
        "couldn't be extracted to text."
    ),
}


def _default_drop(container: MediaContainer, ctx: MediaResolveContext) -> ResolverResult:
    msg = _DEFAULT_DROP_MESSAGES.get(
        container, f"{container.value.capitalize()} removed — this model can't accept it."
    )
    return ResolverResult(
        replacement=None,
        action="dropped",
        user_message=msg,
        system_message=(
            f"{container.value} dropped for model {ctx.model_name} (endpoint "
            f"{ctx.endpoint}) — no resolver registered; emitting notice and dropping."
        ),
    )


async def _safe_resolve(
    container: MediaContainer, content: Any, ctx: MediaResolveContext
) -> ResolverResult:
    resolver = _RESOLVERS.get(container)
    if resolver is None:
        return _default_drop(container, ctx)
    try:
        return await resolver(content, ctx)
    except Exception as exc:  # noqa: BLE001 — a resolver failure must degrade to a clean drop
        # A caller refusal (HIPAA/BAA, allowance, ...) is a decision, not a conversion failure:
        # it keeps its own type and honest message instead of becoming a "dropped" result that
        # the error classifier then reads as a connection failure.
        if getattr(exc, "is_caller_refusal", False):
            raise
        return ResolverResult(
            replacement=None,
            action="dropped",
            user_message=_DEFAULT_DROP_MESSAGES.get(
                container, f"{container.value.capitalize()} removed — couldn't be processed."
            ),
            system_message=f"resolver for {container.value} raised: {exc!r} — dropped.",
        )


#: ``request_snapshot_metadata`` field holding every media notice of the turn, stored beside
#: the wire request it explains (PB-05: a dropped/converted attachment must never be only a
#: console line). Same staging seam as ``tool_adaptations`` / ``settings_adjustments``.
SNAPSHOT_FIELD = "media_notices"


def stage_media_notice(record: dict[str, Any]) -> None:
    """Append a notice to the turn's staged request-snapshot metadata, once per request.

    Sync and import-light so serializers can call it too. A tool loop re-runs the
    preprocessor every round; the same notice is stored once.
    """
    try:
        from matrx_connect.context.app_context import try_get_app_context

        from matrx_ai.orchestrator.snapshot_metadata import REQUEST_SNAPSHOT_METADATA_KEY
    except Exception:  # noqa: BLE001
        return
    app_ctx = try_get_app_context()
    metadata = getattr(app_ctx, "metadata", None) if app_ctx is not None else None
    if not isinstance(metadata, dict):
        return
    staged = dict(metadata.get(REQUEST_SNAPSHOT_METADATA_KEY) or {})
    existing = list(staged.get(SNAPSHOT_FIELD) or [])
    if record in existing:
        return
    staged[SNAPSHOT_FIELD] = [*existing, record]
    metadata[REQUEST_SNAPSHOT_METADATA_KEY] = staged


#: Keys on a media item's own ``metadata`` (persisted with the item by ``to_storage_dict``, so a
#: reloaded history carries them): the converted text, and that the person has been told once.
CONVERSION_CACHE_KEY = "media_conversion"
CONVERSION_SAID_KEY = "media_conversion_said"


def _item_metadata(content: Any) -> dict[str, Any] | None:
    metadata = getattr(content, "metadata", None)
    return metadata if isinstance(metadata, dict) else None


def _cached_replacement(content: Any) -> TextContent | None:
    """The text a past turn already made of this item, or None. Never re-converts (an image's
    OCR, a video's paid transcript) on every later turn to a model that cannot take the media."""
    cached = (_item_metadata(content) or {}).get(CONVERSION_CACHE_KEY)
    if not isinstance(cached, dict) or not isinstance(cached.get("text"), str) or not cached["text"]:
        return None
    meta = cached.get("metadata")
    return TextContent(text=cached["text"], metadata=dict(meta) if isinstance(meta, dict) else {})


def _remember_conversion(content: Any, result: ResolverResult) -> None:
    """Write the conversion onto the item (in place: the message object stays the same one, so
    the turn barrier still finds its trigger) and mark it announced."""
    metadata = _item_metadata(content)
    if metadata is None:
        return
    metadata[CONVERSION_SAID_KEY] = True
    replacement = result.replacement
    if replacement is None or not replacement.text:
        return
    rmeta = dict(replacement.metadata or {})
    if rmeta.get("conversion") == "described":
        return  # names the model that could not see it; cheap, so recomputed per model
    metadata[CONVERSION_CACHE_KEY] = {"text": replacement.text, "metadata": rmeta}


async def _emit_and_log(
    result: ResolverResult,
    container: MediaContainer,
    ctx: MediaResolveContext,
    *,
    announce: bool = True,
) -> None:
    color = "green" if result.replacement is not None else "yellow"
    vcprint(
        data={
            "media_kind": container.value,
            "action": result.action,
            "model": ctx.model_name,
            "endpoint": ctx.endpoint,
        },
        title=f"📎 MEDIA {result.action.upper()} [{ctx.endpoint}]: {result.system_message or result.user_message}",
        color=color,
        verbose=True,
    )
    stage_media_notice(
        {
            "media_kind": container.value,
            "action": result.action,
            "user_message": result.user_message,
            "system_message": result.system_message,
            "provider": ctx.endpoint,
            "model": ctx.model_name,
        }
    )
    try:
        from matrx_connect import try_get_app_context
        from matrx_connect.context.data_types import MediaNoticeData

        app_ctx = try_get_app_context()
        if app_ctx is not None and app_ctx.emitter is not None:
            await app_ctx.emitter.send_data(
                MediaNoticeData(
                    media_kind=container.value,
                    action=result.action,  # type: ignore[arg-type]
                    user_message=result.user_message,
                    system_message=result.system_message,
                    provider=ctx.endpoint,
                    model=ctx.model_name,
                )
            )
    except Exception as exc:  # noqa: BLE001 — emitting a notice must never break dispatch
        vcprint(f"[media_fallback] failed to emit media notice: {exc}", color="yellow")
    if (
        announce
        and result.replacement is not None
        and result.user_message
        and _first_time_this_request(result.user_message)
    ):
        # The person's ONE line (one-chat C2: an image to a model that cannot see it). The
        # ``media_notice`` data event above has no chat renderer; a warning is drawn live and
        # saved on the answer (``metadata.warnings``), so a reload still says it.
        from matrx_connect.context.events import WarningPayload

        from matrx_ai.providers.outbound_params import send_client_warning

        send_client_warning(
            WarningPayload(
                code=MEDIA_CONVERTED_CODE,
                system_message=result.system_message or result.user_message,
                user_message=result.user_message,
                level="medium",
                recoverable=True,
                metadata={"media_kind": container.value, "action": result.action, "model": ctx.model_name},
            ),
            name="media_fallback_notice",
        )


#: The warning code of the line a converted media item shows in the chat (promoted to a visible
#: line by @ai-matrx/chat ``PROMOTED_WARNING_CODES``).
MEDIA_CONVERTED_CODE = "media_converted"


def _first_time_this_request(line: str) -> bool:
    """A loop converts the same item on every provider call; the person reads its line once
    (the request holder: with or without an app context, never "say it again")."""
    from matrx_ai.context.request_once import first_time_this_request

    return first_time_this_request("media_converted", line)


async def _persist_conversion_on_saved_message(message: Any) -> None:
    """A message saved on an EARLIER turn (it carries its row id and position) gets the conversion
    written onto its stored row, so a fresh server load reads the cached text and the "said" mark
    instead of converting and announcing again. A message new this turn needs nothing: the turn
    barrier writes it, item metadata included. keep_fresh blocks are never stored (re-fetched each
    turn), so they are left out here as the finalize leaves them out."""
    row_id = getattr(message, "id", None)
    if not row_id or getattr(message, "position", None) is None:
        return
    try:
        import copy

        from matrx_ai.config.structured_input_config import _StructuredInputBase
        from matrx_ai.persistence.queue_helpers import queue_message_update
        from matrx_ai.persistence.sealed import stored_message_content

        stored = copy.copy(message)
        stored.content = [
            item
            for item in (getattr(message, "content", None) or [])
            if not (isinstance(item, _StructuredInputBase) and getattr(item, "keep_fresh", False))
        ]
        content = await stored_message_content(stored.to_storage_dict().get("content") or [])
        queue_message_update(str(row_id), content=content)
    except Exception as exc:  # noqa: BLE001 — the conversion still went to the model; said in the log
        vcprint(
            f"[media_fallback] conversion not stored on message {row_id} ({type(exc).__name__}: {exc}); "
            "a later turn converts it again",
            color="yellow",
        )


def _collect_user_text(messages: MessageList) -> str:
    parts: list[str] = []
    try:
        for message in messages.to_list():
            if getattr(message, "role", None) != "user":
                continue
            for content in getattr(message, "content", None) or []:
                text = getattr(content, "text", None)
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
    except Exception:  # noqa: BLE001
        return ""
    return "\n".join(parts[-4:])  # the most recent user text is the best hint


def has_unsupported_media(
    messages: MessageList,
    endpoint: str | None,
    *,
    model_supports_vision: bool | None = None,
) -> bool:
    return bool(
        find_unsupported_media(
            messages,
            endpoint,
            model_supports_vision=model_supports_vision,
        )
    )


async def _name_media_by_file_id(messages: MessageList) -> None:
    """Give every media item its file's own name (``metadata.file_name``) before dispatch.

    The boundary usually carries it from resolution; any item still nameless is named by ONE
    batched host read for the whole message list, as the person (``source_name_resolver``,
    kind ``file``). A name that cannot be read stays absent and the serializer's identity part
    says ``name_unavailable`` (PB-05 defect 54)."""
    nameless: list[Any] = []
    try:
        for message in messages.to_list():
            for content in getattr(message, "content", None) or []:
                if container_for_content(content) is None or not getattr(content, "file_id", None):
                    continue
                # Only media the files access gate already released for this request
                # (bytes or a minted url, no resolver error) — the name read rides that decision.
                released = getattr(content, "base64_data", None) or getattr(content, "resolved_url", None)
                if not released or getattr(content, "resolver_error", None):
                    continue
                metadata = getattr(content, "metadata", None)
                if isinstance(metadata, dict) and not metadata.get("file_name"):
                    nameless.append(content)
    except Exception:  # noqa: BLE001 — naming must never break dispatch
        return
    if not nameless:
        return
    from matrx_ai.config.structured_input_config import _source_names

    names, _reason = await _source_names([("file", str(c.file_id)) for c in nameless])
    for content in nameless:
        name = names.get(("file", str(content.file_id)))
        if name:
            content.metadata["file_name"] = name


def _set_off_converted_text(parts: list[Any], converted_at: list[int]) -> None:
    """Put a blank line between a converted attachment and the parts beside it.

    Chat-Completions translators join a message's text parts with ``""``: an extracted file
    landed glued to the person's question ("...the word.[Document extracted...") and a text-only
    model did not see it as the attachment (live, gpt-oss-20b, 3 of 4 runs). The boundary is
    decided HERE, once, by position, so every provider style and every resolver (document,
    video, YouTube) inherits it; block-per-part providers just get surrounding whitespace.
    """
    for index in converted_at:
        part = parts[index]
        text = getattr(part, "text", None)
        if not isinstance(text, str):
            continue
        core = text.strip("\n")
        before = "\n\n" if index > 0 else ""
        after = "\n\n" if index < len(parts) - 1 else ""
        parts[index] = TextContent(text=f"{before}{core}{after}", metadata=getattr(part, "metadata", None) or {})


def _open_with_source_label(original: Any, replacement: TextContent, role: Any) -> TextContent:
    """Open converted text with the ORIGINAL item's ``<attachment kind name id converted_to/>``.

    The serializers label only media parts, so a conversion used to drop the file's kind and id:
    PB-05 (2026-11-08) sent four attachments behind their label and the converted .docx as bare
    text. Applied here, once, to fresh and reused conversions alike, so every provider style and
    every resolver inherits it. The cache keeps the unlabelled text; the label is added per use.
    """
    from matrx_ai.config.message_config import _media_identity_label

    text = replacement.text or ""
    if text.lstrip().startswith("<attachment "):
        return replacement
    if not (getattr(original, "file_id", None) or getattr(original, "url", None)):
        return replacement  # no identity to carry; the "[Attached file: name]" header names it
    label = _media_identity_label(original, role, converted_to="text")
    if not label:
        return replacement
    return TextContent(text=f"{label}\n{text}", metadata=dict(replacement.metadata or {}))


def _skip_automatic_pictures(messages: MessageList, model_name: str) -> MessageList:
    """A model that cannot read images never receives an AUTOMATIC picture (one a tool attached
    without being asked: ``ImageContent.metadata.auto_picture``) nor a paid or OCR conversion of
    it: each becomes one line saying it was skipped and why. Copy-on-write: the saved history and
    any cached message keep the picture, so a later turn on a model that sees gets it."""
    from dataclasses import replace

    def _is_auto(block: Any) -> bool:
        return container_for_content(block) is MediaContainer.IMAGE and bool(
            (_item_metadata(block) or {}).get("auto_picture")
        )

    note = TextContent(
        text=(
            f"[Picture skipped: {model_name} cannot read images. Read the page as text or as its "
            "element list instead.]"
        )
    )
    changed = False
    out: list[UnifiedMessage] = []
    # Same tolerance as ``_collect_user_text`` / ``_name_media_by_file_id`` beside it: a caller
    # holding a plain list of messages (not yet a MessageList) is read, never crashed on.
    for message in (messages.to_list() if hasattr(messages, "to_list") else list(messages)):
        parts = list(getattr(message, "content", None) or [])
        new_parts: list[Any] = []
        touched = False
        for part in parts:
            inner = getattr(part, "content", None)
            if getattr(part, "type", None) == "tool_result" and isinstance(inner, list) and any(
                _is_auto(b) for b in inner
            ):
                new_parts.append(replace(part, content=[note if _is_auto(b) else b for b in inner]))
                touched = True
            else:
                new_parts.append(part)
        if touched:
            changed = True
            out.append(
                UnifiedMessage(
                    role=message.role,
                    content=new_parts,
                    id=getattr(message, "id", None),
                    name=getattr(message, "name", None),
                    timestamp=getattr(message, "timestamp", None),
                    metadata=getattr(message, "metadata", None) or {},
                )
            )
        else:
            out.append(message)
    return MessageList(_messages=out) if changed else messages


async def preprocess_unsupported_media(
    messages: MessageList,
    endpoint: str | None,
    *,
    model_name: str,
    model_supports_vision: bool | None = None,
    debug: bool = False,
) -> tuple[MessageList, list[TokenUsage]]:
    """Convert every unsupported media item or raise before provider dispatch."""
    if model_supports_vision is False:
        messages = _skip_automatic_pictures(messages, model_name)
    await _name_media_by_file_id(messages)
    unsupported = find_unsupported_media(
        messages,
        endpoint,
        model_supports_vision=model_supports_vision,
    )
    if not unsupported:
        return messages, []

    ctx = MediaResolveContext(
        endpoint=endpoint,
        model_name=model_name,
        user_text_hint=_collect_user_text(messages),
        debug=debug,
    )
    processed: list[UnifiedMessage] = []
    all_usage: list[TokenUsage] = []
    for message in messages.to_list():
        new_content: list[Any] = []
        converted_at: list[int] = []
        remembered = False
        source_content = list(getattr(message, "content", None) or [])
        for content in source_content:
            container = container_for_content(content)
            if container is not None and content_needs_fallback(
                content,
                endpoint,
                model_supports_vision=model_supports_vision,
                role=getattr(message, "role", None),
            ):
                cached = _cached_replacement(content)
                if cached is not None:
                    # Converted on an earlier turn: reuse the stored text, say nothing again.
                    new_content.append(_open_with_source_label(content, cached, message.role))
                    converted_at.append(len(new_content) - 1)
                    continue
                result = await _safe_resolve(container, content, ctx)
                said = bool((_item_metadata(content) or {}).get(CONVERSION_SAID_KEY))
                await _emit_and_log(result, container, ctx, announce=not said)
                if result.replacement is None:
                    raise MediaFallbackResolutionError(
                        container,
                        model_name=ctx.model_name,
                        endpoint=ctx.endpoint,
                        detail=result.system_message or result.user_message,
                    )
                _remember_conversion(content, result)
                remembered = True
                new_content.append(_open_with_source_label(content, result.replacement, message.role))
                all_usage.extend(result.usage)
                converted_at.append(len(new_content) - 1)
            else:
                new_content.append(content)
        _set_off_converted_text(new_content, converted_at)
        if remembered:
            await _persist_conversion_on_saved_message(message)
        processed.append(
            UnifiedMessage(
                role=message.role,
                content=new_content,
                id=getattr(message, "id", None),
                name=getattr(message, "name", None),
                timestamp=getattr(message, "timestamp", None),
                metadata=getattr(message, "metadata", None) or {},
            )
        )
    return MessageList(_messages=processed), all_usage


__all__ = [
    "SNAPSHOT_FIELD",
    "stage_media_notice",
    "MediaResolveContext",
    "ResolverResult",
    "register_media_resolver",
    "has_unsupported_media",
    "preprocess_unsupported_media",
]

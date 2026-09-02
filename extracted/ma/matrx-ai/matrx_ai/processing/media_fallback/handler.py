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
        return ResolverResult(
            replacement=None,
            action="dropped",
            user_message=_DEFAULT_DROP_MESSAGES.get(
                container, f"{container.value.capitalize()} removed — couldn't be processed."
            ),
            system_message=f"resolver for {container.value} raised: {exc!r} — dropped.",
        )


async def _emit_and_log(
    result: ResolverResult, container: MediaContainer, ctx: MediaResolveContext
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


async def preprocess_unsupported_media(
    messages: MessageList,
    endpoint: str | None,
    *,
    model_name: str,
    model_supports_vision: bool | None = None,
    debug: bool = False,
) -> tuple[MessageList, list[TokenUsage]]:
    """Convert every unsupported media item or raise before provider dispatch."""
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
        for content in getattr(message, "content", None) or []:
            container = container_for_content(content)
            if container is not None and container in unsupported:
                result = await _safe_resolve(container, content, ctx)
                await _emit_and_log(result, container, ctx)
                if result.replacement is None:
                    raise MediaFallbackResolutionError(
                        container,
                        model_name=ctx.model_name,
                        endpoint=ctx.endpoint,
                        detail=result.system_message or result.user_message,
                    )
                new_content.append(result.replacement)
                all_usage.extend(result.usage)
            else:
                new_content.append(content)
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
    "MediaResolveContext",
    "ResolverResult",
    "register_media_resolver",
    "has_unsupported_media",
    "preprocess_unsupported_media",
]

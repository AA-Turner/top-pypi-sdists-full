import dataclasses
import re
from dataclasses import dataclass, field
from typing import Any, Literal, Optional
from urllib.parse import parse_qs, urlparse

from google.genai.types import Part
from matrx_utils import vcprint

from matrx_ai.media import detect_mime_type

# Unified storage kind discriminator for all media types
MediaKind = Literal["image", "audio", "video", "document", "youtube"]


def reconcile_media_kind(
    kind: str | None,
    mime_type: str | None,
) -> str | None:
    """Return the truthful media kind when a definitive MIME disagrees.

    Frontends and historical rows can carry a generic ``document`` kind for
    an image/audio/video attachment. Provider routing must follow the bytes,
    not that stale presentation label. YouTube remains URL-specialized and is
    never reclassified by MIME.
    """
    if kind not in {"image", "audio", "video", "document"} or not mime_type:
        return kind

    base_mime = mime_type.split(";", 1)[0].strip().lower()
    inferred: MediaKind | None = None
    if base_mime.startswith("image/"):
        inferred = "image"
    elif base_mime.startswith("audio/"):
        inferred = "audio"
    elif base_mime.startswith("video/"):
        inferred = "video"
    elif base_mime == "application/pdf":
        inferred = "document"

    return inferred or kind


# ----------------------------------------------------------------------
# YouTube URL canonicalisation
# ----------------------------------------------------------------------
#
# The frontend frequently sends a YouTube reference as a bare 11-char
# video ID (e.g. "5WY8Gv_QCDU") or a short-link with tracking params
# (e.g. "https://youtu.be/5WY8Gv_QCDU?si=..."). Google's API only
# accepts a File API URI, a canonical watch URL
# (https://www.youtube.com/watch?v=<id>), or an https:// URL — passing a
# bare ID yields a 400 "Unsupported file URI type". This helper coerces
# any of the common shapes into the canonical watch URL Google accepts.
_YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def normalize_youtube_url(value: str) -> str:
    """Coerce a YouTube reference (bare id, youtu.be, shorts, embed, or a
    full watch URL with tracking params) into the canonical
    ``https://www.youtube.com/watch?v=<id>`` form Google requires.

    Returns the input unchanged when it doesn't look like a YouTube
    reference we recognize (e.g. a File API URI or arbitrary https URL),
    so non-YouTube inputs pass through untouched.
    """
    if not value:
        return value

    raw = value.strip()

    # Bare video ID (no scheme, no slash) → canonical watch URL.
    if "/" not in raw and "." not in raw and _YOUTUBE_ID_RE.match(raw):
        return f"https://www.youtube.com/watch?v={raw}"

    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = (parsed.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]

    video_id: str | None = None
    if host == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0] or None
    elif host in ("youtube.com", "m.youtube.com", "music.youtube.com"):
        path = parsed.path or ""
        if path == "/watch":
            video_id = (parse_qs(parsed.query).get("v") or [None])[0]
        elif path.startswith(("/shorts/", "/embed/", "/v/", "/live/")):
            video_id = path.split("/")[2] if len(path.split("/")) > 2 else None

    if video_id and _YOUTUBE_ID_RE.match(video_id):
        return f"https://www.youtube.com/watch?v={video_id}"

    # Unrecognized shape — leave it for Google to accept/reject.
    return raw


# ----------------------------------------------------------------------
# Variable substitution helper for media content blocks
# ----------------------------------------------------------------------
#
# Agent message templates can embed `{{variable_name}}` patterns inside
# media content fields, e.g.:
#   {"type": "image", "url": "{{my_start_image}}", "metadata": {"role": "start_image"}}
#
# When the agent runs with a `variables` dict, these templates get
# substituted. The user's value can be any of:
#   - a UUID file_id (e.g. "a1b2c3d4-...-...")
#   - a cloud URI (s3:// or gs://)
#   - a URL we issued (cld_files share link, /files/{id}/url, etc.)
#   - an external https:// URL
#   - an empty string (user opted out of an optional media slot)
#
# This helper substitutes into the relevant string fields, then routes
# the result through `coerce_to_media_ref` so the final shape is canonical
# (file_id ↔ url ↔ file_uri exactly-one-set per the MediaRef contract).
# Returns True when the block should be DROPPED (e.g. user supplied
# nothing for an optional slot).
def _substitute_and_coerce_media_fields(content: Any, variables: dict[str, Any]) -> bool:
    """Substitute {{var}} into url/file_id/file_uri/base64_data fields on a
    media content block. Re-routes the value to the right field per
    MediaRef contract. Returns True iff the block should be dropped from
    the message content list (no usable identifier survived).
    """
    from matrx_files.cloud_sync.media_ref import (
        coerce_to_media_ref,
    )

    # Track which fields originally carried a template — those are the
    # ones the user "intended to fill". Empty result on any of them means
    # the user opted out of an optional slot → caller should drop block.
    templated_fields: list[str] = []
    for field_name in ("url", "file_id", "file_uri", "base64_data"):
        current = getattr(content, field_name, None)
        if isinstance(current, str) and "{{" in current and "}}" in current:
            templated_fields.append(field_name)

    # Substitute in any string field.
    for field_name in ("url", "file_id", "file_uri", "base64_data"):
        current = getattr(content, field_name, None)
        if not current or not isinstance(current, str):
            continue
        substituted = current
        for var_name, var_value in variables.items():
            substituted = substituted.replace(
                f"{{{{{var_name}}}}}",
                "" if var_value is None else str(var_value),
            )
        # Trim — variable value can include leading/trailing whitespace.
        if substituted != current:
            substituted = substituted.strip()
        setattr(content, field_name, substituted or None)

    # If a templated field came back empty AND the block has no other
    # usable identifier, drop the block.
    has_any_id = bool(
        getattr(content, "file_id", None)
        or getattr(content, "url", None)
        or getattr(content, "file_uri", None)
        or getattr(content, "base64_data", None)
    )
    if templated_fields and not has_any_id:
        return True

    # Re-route the `url` field if it now looks like a UUID or a cloud
    # URI — MediaRef contract is exactly-one-of. Only re-route when the
    # content class actually has the target field declared (e.g. YouTube
    # content has only `url`, no file_id/file_uri — leave its URL alone).
    url_val = getattr(content, "url", None)
    has_other_id = bool(getattr(content, "file_id", None) or getattr(content, "file_uri", None))
    if isinstance(url_val, str) and url_val and not has_other_id:
        ref = coerce_to_media_ref(url_val)
        if ref is None:
            return True
        if ref.file_id and hasattr(content, "file_id"):
            content.url = None
            content.file_id = ref.file_id
        elif ref.file_uri and hasattr(content, "file_uri"):
            content.url = None
            content.file_uri = ref.file_uri
        # else: keep as url (already correct OR class doesn't support reroute)

    return False


# ---------------------------------------------------------------------------
# THE OUTPUT RULE for media content
# ---------------------------------------------------------------------------
# ``get_output()`` flattens a message into TEXT. That text becomes
# ``result.output`` → an agent's answer → an ``agent_call`` tool result → and is
# ultimately PERSISTED (``chat.message.content``, ``raw_response``, workflow node
# outputs, checkpoints).
#
# A signed URL must never enter that channel. A signed URL is a temporary grant
# handed to a third party at the moment of use — it is not an identifier, and the
# instant it is stored it becomes a link that dies. Internally we pass the
# reference (``file_id``) exactly like a row id; whoever needs bytes or a URL
# mints a fresh one from the id (``FileManager.resolve_media_async``, which the
# provider path already runs before EVERY call).
#
# So the order is: a DURABLE url (CDN/public/genuinely-external) → the ``file_id``
# → inline bytes → a storage uri. An expiring url is skipped entirely; if that is
# all we have, the ``file_id`` beside it is the answer.
#
# This is the boundary that kept manufacturing signed URLs after the rest of the
# platform was converted to ids, and it is why an expiring S3 link ended up frozen
# in chat history. Guard: packages/matrx-ai/tests/test_media_output_durability.py


def _durable_media_output(item: "object") -> str | None:
    """Most durable text handle for a media block, or None when it has none."""
    from matrx_files import is_durable_media_url

    url = getattr(item, "url", None)
    if url and is_durable_media_url(url):
        return url

    file_id = getattr(item, "file_id", None)
    if file_id:
        return str(file_id)

    # A signed url with no file_id on the block. If it is OURS the id is
    # recoverable from the path (`…/{owner}/{file_id}?…`) — use it.
    if url:
        recovered = _our_file_id_from_url(url)
        if recovered:
            return recovered
        # Not ours: a third party's own expiring link (Azure SAS from DALL-E, a
        # googlevideo url). We cannot re-mint it and we have no id for it, so the
        # url IS the only handle — dropping it would be silent content loss. It
        # was never ours to keep durable in the first place.
        return url

    # Nothing at all: fall through to the caller's base64 / file_uri handling.
    return None


_OUR_FILE_URL_RE = re.compile(
    r"(^|\.)matrx-user-files\.s3|s3[.-][^/]*amazonaws\.com", re.IGNORECASE
)
_UUID_SEGMENT_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


def _our_file_id_from_url(url: str) -> str | None:
    """Recover OUR cld_files id from our own user-files URL (`…/{owner}/{file_id}`)."""
    no_query = url.split("?", 1)[0]
    _, _, after_scheme = no_query.partition("://")
    host, _, path = after_scheme.partition("/")
    if not _OUR_FILE_URL_RE.search(host):
        return None
    uuids = [seg for seg in path.split("/") if _UUID_SEGMENT_RE.match(seg)]
    if not uuids:
        return None
    return uuids[1] if len(uuids) >= 2 else uuids[0]


@dataclass
class ImageContent:
    """Image media item.

    Carries the canonical media-reference fields (``file_id``, ``url``,
    ``file_uri``, ``mime_type``, ``base64_data``, ``is_resolved``) so the
    AI Dream boundary normaliser can resolve it through
    ``FileManager.resolve_media_async``. Don't add new media-reference
    fields here — extend ``MediaRef`` in matrx-utils instead.
    """

    type: Literal["image", "input_image"] = "image"
    url: str | None = None
    base64_data: str | None = None
    file_uri: str | None = None
    file_id: str | None = None  # Cloud-files UUID; preferred when known.
    mime_type: str | None = None
    media_resolution: str | None = None
    alt: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    # Phase 3b: intrinsic dimensions persisted into cx_message storage
    # so FE chat-message reads don't need a follow-up GET /assets/{id}.
    width: int | None = None
    height: int | None = None

    # Vision-class hint — when set, the boundary resolver will render (or
    # cache-hit on) a derived variant of the master file before populating
    # the resolved-state fields. Names come from the matrx-ai vision
    # registry (``packages/matrx-ai/matrx_ai/processing/vision``).
    vision_class: str | None = None

    # === Resolved-state fields (populated by the boundary normaliser) ===
    resolved_url: str | None = None
    file_size: int | None = None
    owner_id: str | None = None
    is_ours: bool = False
    is_resolved: bool = False
    resolver_error: str | None = None

    def __post_init__(self):
        """Normalise mime_type from multiple legacy locations, then auto-detect."""
        # Frontend convenience: pull mime from metadata if the top-level
        # mime_type wasn't set. The cloud-files /files/upload response and
        # historical object listings surface MIME under metadata.{mimetype,
        # mime_type, contentType, content_type}; honor any of them.
        if not self.mime_type and self.metadata:
            for key in ("mime_type", "mimetype", "content_type", "contentType", "mimeType", "type"):
                v = self.metadata.get(key)
                if isinstance(v, str) and "/" in v and v != "image":
                    self.mime_type = v
                    break
        if not self.file_id and self.metadata:
            for key in ("file_id", "fileId", "id"):
                v = self.metadata.get(key)
                if isinstance(v, str):
                    self.file_id = v
                    break
        if self.mime_type is None:
            self.mime_type = detect_mime_type(
                url=self.url, base64_data=self.base64_data, file_uri=self.file_uri
            )
        if self.alt is not None:
            self.metadata["alt"] = self.alt
            self.alt = None
        vcprint(f"--> ImageContent MIME Type: {self.mime_type}, file_id={self.file_id}")

    def get_output(self) -> str | None:
        """Durable handle only — see THE OUTPUT RULE above. Never a signed URL."""
        durable = _durable_media_output(self)
        if durable:
            return durable
        if self.base64_data:
            return self.base64_data
        if self.file_uri:
            return self.file_uri
        return None

    def replace_variables(self, variables: dict[str, Any]) -> bool:
        """Substitute {{var}} patterns in identifier fields and re-route to
        the canonical MediaRef field. Returns True iff this block should be
        dropped from the message (e.g. an optional media slot the user left
        unfilled). See ``_substitute_and_coerce_media_fields``."""
        return _substitute_and_coerce_media_fields(self, variables)

    def to_google(self) -> dict[str, Any] | None:
        """Convert to Google Gemini format.

        URL / file_id resolution does NOT happen here — it happens once at
        the AI Dream boundary via ``normalize_request_body``
        (``aidream/services/media_resolvers/request_normalizer.py``). That
        central pass converts every cloud_files URL into ``base64_data`` so
        this method only ever sees one of: file_uri (gs://), base64_data, or
        a truly external url that the provider can fetch itself.
        """
        if self.file_uri and self.file_uri.startswith("gs://"):
            part = {"fileData": {"fileUri": self.file_uri, "mimeType": self.mime_type}}
        elif self.base64_data:
            part = {
                "inlineData": {
                    "data": self.base64_data,
                    "mimeType": self.mime_type or "application/octet-stream",
                }
            }
        else:
            # No usable representation. The boundary normaliser at AI
            # Dream pre-fetches BOTH our cloud_files refs AND external
            # URLs into base64_data, so we never need a sync HTTP fallback
            # here (which would block the event loop). If we land in this
            # branch the boundary either wasn't wired or the fetch failed
            # — in both cases dropping is correct (matrx-ai logs it).
            vcprint(
                self.to_dict(),
                "ImageContent to_google MediaItem has no resolvable content\n\n Temporarily not raising an error, but dropping the media item",
                color="red",
            )
            return None
        if self.media_resolution:
            part["mediaResolution"] = {"level": self.media_resolution}
        return part

    def to_openai(self) -> dict[str, Any] | None:
        """Convert to OpenAI format. URL resolution happens centrally.

        Resolved bytes / presigned URL win over the raw client ``url``: the
        boundary resolver fetches one of OUR cloud-files refs into
        ``base64_data`` (or mints a fresh presigned ``resolved_url``) but leaves
        the original ``url`` in place. Emitting that raw ``url`` would have the
        provider FETCH a share-link / expired-signed URL itself (scraping HTML
        for our links). Prefer the resolved form; fall back to a genuinely-
        external ``url`` only when the boundary produced nothing.
        """
        if self.base64_data:
            # Responses API ``input_image`` takes ``image_url`` as a string —
            # either an https URL or a base64 data URI. The ``{"image":
            # {"data", "mime_type"}}`` shape is Google GenAI's inline-data form
            # and is NOT accepted here (it 400s as an unknown content param).
            mime = self.mime_type or "image/png"
            return {
                "type": "input_image",
                "image_url": f"data:{mime};base64,{self.base64_data}",
            }
        resolved_url = getattr(self, "resolved_url", None)
        if resolved_url or self.url:
            return {"type": "input_image", "image_url": resolved_url or self.url}
        vcprint(
            self.to_dict(),
            "ImageContent to_openai MediaItem has no resolvable content\n\n Temporarily not raising an error, but dropping the media item",
            color="red",
        )
        return None

    def to_openai_chat(self) -> dict[str, Any] | None:
        """Convert to OpenAI Chat Completions content-array entry
        (``{"type": "image_url", "image_url": {"url": ...}}``).

        This is the shape consumed by every OpenAI-compatible Chat
        Completions endpoint — Cerebras, Groq, xAI, Together,
        llama-server, vLLM, Ollama, LocalAI — and is distinct from the
        Responses API ``input_image`` shape returned by ``to_openai()``.

        Returns ``None`` when there's no usable representation; the
        caller drops it (matches the drop-on-unresolvable contract
        used by ``to_openai`` / ``to_anthropic``).

        Resolved bytes / presigned URL win over the raw client ``url`` — see
        ``to_openai`` for why (these providers FETCH the URL we hand them, so a
        raw share-link would be scraped instead of read from S3).
        """
        if self.base64_data:
            mime = self.mime_type or "image/png"
            data_uri = f"data:{mime};base64,{self.base64_data}"
            return {"type": "image_url", "image_url": {"url": data_uri}}
        resolved_url = getattr(self, "resolved_url", None)
        if resolved_url or self.url:
            return {"type": "image_url", "image_url": {"url": resolved_url or self.url}}
        vcprint(
            self.to_dict(),
            "ImageContent to_openai_chat MediaItem has no resolvable url/base64_data; dropping.",
            color="red",
        )
        return None

    def to_moonshot_chat(self) -> dict[str, Any]:
        """Serialize resolved image bytes for Moonshot's Chat Completions API."""
        if not self.base64_data:
            raise ValueError(
                "Moonshot image input requires resolved base64 data; resolve the MediaRef "
                "at the API boundary before dispatch."
            )
        mime = self.mime_type or "image/png"
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{self.base64_data}"},
        }

    def to_anthropic(self) -> dict[str, Any] | None:
        """Convert to Anthropic format. URL resolution happens centrally.

        Resolved bytes win over the raw client ``url``: the boundary resolver
        inlines one of OUR cloud-files refs into ``base64_data`` but leaves the
        original ``url`` in place. Emitting that raw ``url`` as a url-source
        would have Anthropic FETCH a share-link / expired-signed URL itself
        (scraping HTML for our links). Prefer base64, then a fresh presigned
        ``resolved_url``, then a genuinely-external ``url``.
        """
        if self.base64_data:
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": self.mime_type,
                    "data": self.base64_data,
                },
            }
        resolved_url = getattr(self, "resolved_url", None)
        if resolved_url or self.url:
            return {"type": "image", "source": {"type": "url", "url": resolved_url or self.url}}
        vcprint(
            self.to_dict(),
            "ImageContent to_anthropic MediaItem has no resolvable content\n\n Temporarily not raising an error, but dropping the media item",
            color="red",
        )
        return None

    @classmethod
    def from_google(cls, part: Part) -> Optional["ImageContent"]:
        """Create ImageContent from an EXTERNAL Google ``file_data`` URI.

        Inline bytes do NOT belong here: persisting them synchronously yields a
        signed url with no ``file_id``, and this content is written into
        ``chat.message``. Inline parts go through :meth:`from_google_async`,
        which returns a ``file_id``.
        """
        if part.file_data:
            # File URI is already external and persistent, just use it
            return cls(file_uri=part.file_data.file_uri, mime_type=part.file_data.mime_type)
        vcprint(
            {"part_type": type(part).__name__, "part_repr": repr(part)},
            "ImageContent from_google: Part has no file_data (inline bytes belong on from_google_async)\n\n Dropping the media item",
            color="red",
        )
        return None

    @classmethod
    async def from_google_async(cls, part: Part) -> Optional["ImageContent"]:
        """Async/canonical Google → ImageContent conversion (Phase 2c).

        Persists inline_data via ``save_media_envelope_async`` so the
        returned content carries ``file_id`` + ``file_uri`` +
        ``size_bytes`` + ``width``/``height`` (from probe) AND the
        Phase 1 SOCIAL_BASELINE variants + Phase 1c kind-specific
        variants render automatically as part of the envelope path.
        Stamps generation metadata under ``metadata.generation`` for
        the standard Phase 2 audit / re-generation UX.

        file_data parts go to the legacy shape (file URI is already
        persistent at Google's end — no envelope to create).
        """
        from matrx_ai.media import save_media_envelope_async
        from matrx_ai.media.generation_metadata import build_default_metadata

        if part.inline_data:
            gen_meta = build_default_metadata(
                kind="image",
                provider="google",
                model="gemini-multi-modal",
                prompt="",
                n_returned=1,
            )
            try:
                envelope = await save_media_envelope_async(
                    content=part.inline_data.data,
                    mime_type=part.inline_data.mime_type,
                    provider="google",
                    feature="ai_images",
                    extra_metadata={"generation": gen_meta.model_dump(exclude_none=True)},
                )
            except Exception as e:
                # NO fallback: the sync path persists via ``save_media``, which
                # returns a SIGNED url and no ``file_id`` — and this content is
                # written into ``chat.message``, where a frozen expiring link has
                # nothing to re-mint from. Drop the item loudly instead.
                vcprint(
                    f"ImageContent.from_google_async: envelope save failed ({e!r}); "
                    f"dropping the image — no file_id means no durable identity",
                    color="red",
                )
                return None
            return cls(
                url=envelope.url,
                file_id=envelope.file_id,
                mime_type=envelope.mime_type or part.inline_data.mime_type,
                file_size=envelope.size_bytes,
                width=envelope.width,
                height=envelope.height,
                metadata={"generation": gen_meta.model_dump(exclude_none=True)},
            )
        elif part.file_data:
            return cls(file_uri=part.file_data.file_uri, mime_type=part.file_data.mime_type)
        vcprint(
            {"part_type": type(part).__name__, "part_repr": repr(part)},
            "ImageContent from_google_async: Part has neither inline_data nor file_data\n\n Temporarily not raising an error, but dropping the media item",
            color="red",
        )
        return None

    def to_dict(self, truncate_base64: bool = True) -> dict[str, Any]:
        """Convert to dict with optional base64 truncation"""
        result = dataclasses.asdict(self)
        if truncate_base64 and result.get("base64_data"):
            result["base64_data"] = f"<{len(self.base64_data)} chars>"
        return result

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to unified media storage format for database persistence.

        Phase 3a: adds the UnifiedMediaBlock canonical fields (file_id,
        size_bytes, origin) so cx_message.content[] readers can re-resolve
        signed URLs via the file_id without the previous N+1 dance.
        """
        origin = "matrx" if self.file_id else "external"
        result: dict[str, Any] = {
            "type": "media",
            "kind": "image",
            "origin": origin,
        }
        if self.file_id:
            result["file_id"] = self.file_id
        if self.url:
            result["url"] = self.url
        if self.base64_data:
            result["base64_data"] = self.base64_data
        if self.file_uri:
            result["file_uri"] = self.file_uri
        if self.mime_type:
            result["mime_type"] = self.mime_type
        if self.file_size is not None:
            result["size_bytes"] = self.file_size
        # Phase 3b: persist intrinsic dimensions so the FE doesn't need
        # a follow-up GET /assets/{id} for chat-message reads.
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        # Kind-specific extras go into metadata
        storage_metadata = {**self.metadata}
        if self.media_resolution:
            storage_metadata["media_resolution"] = self.media_resolution
        if self.vision_class:
            storage_metadata["vision_class"] = self.vision_class
        if self.alt:
            storage_metadata["alt"] = self.alt
        if storage_metadata:
            result["metadata"] = storage_metadata
        return result

    def __repr__(self) -> str:
        """Custom repr that only truncates base64_data"""
        base64_display = f"<{len(self.base64_data)} chars>" if self.base64_data else None
        return (
            f"ImageContent("
            f"type={self.type!r}, "
            f"url={self.url!r}, "
            f"base64_data={base64_display}, "
            f"file_uri={self.file_uri!r}, "
            f"mime_type={self.mime_type!r}, "
            f"media_resolution={self.media_resolution!r}, "
            f"alt={self.alt!r}, "
            f"metadata={self.metadata!r}"
        )


@dataclass
class AudioContent:
    type: Literal["audio", "input_audio"] = "audio"
    url: str | None = None
    base64_data: str | None = None
    file_uri: str | None = None
    file_id: str | None = None  # Cloud-files UUID
    mime_type: str | None = None

    # === Resolved-state fields (populated by the boundary normaliser) ===
    resolved_url: str | None = None
    file_size: int | None = None
    owner_id: str | None = None
    is_ours: bool = False
    is_resolved: bool = False
    resolver_error: str | None = None

    # Transcription settings
    auto_transcribe: bool = False
    """If True, automatically transcribe audio through the catalog STT route."""

    transcription_model: str = "stt-default"
    """Catalog model or alias whose offering uses an STT translator."""

    # Phase 3b: intrinsic duration persisted into cx_message storage.
    duration_ms: int | None = None

    transcription_language: str | None = None
    """Language of the audio (ISO-639-1 format like 'en', 'es'). Auto-detected if None."""

    transcription_result: str | None = None
    """Cached transcription result (set after transcription)"""

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Auto-detect mime_type if not provided"""
        if self.mime_type is None:
            self.mime_type = detect_mime_type(
                url=self.url, base64_data=self.base64_data, file_uri=self.file_uri
            )

    def get_output(self) -> str | None:
        """Transcript when we have one, else a durable handle — never a signed URL.

        See THE OUTPUT RULE above.
        """
        if self.transcription_result:
            return self.transcription_result
        durable = _durable_media_output(self)
        if durable:
            return durable
        if self.base64_data:
            return self.base64_data
        if self.file_uri:
            return self.file_uri
        return None

    def replace_variables(self, variables: dict[str, Any]) -> bool:
        """See ImageContent.replace_variables."""
        return _substitute_and_coerce_media_fields(self, variables)

    def get_transcription(self, force_refresh: bool = False) -> str | None:
        """Synchronous compatibility wrapper around catalog-dispatched STT.

        Async application code must call :meth:`get_transcription_async`.
        """
        import asyncio

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.get_transcription_async(force_refresh=force_refresh))
        raise RuntimeError(
            "AudioContent.get_transcription() cannot run inside an event loop; "
            "await get_transcription_async() instead."
        )

    async def get_transcription_async(self, force_refresh: bool = False) -> str | None:
        """
        Get transcription of the audio content through the model catalog.

        Uses a global cache to avoid re-transcribing the same audio across
        different requests. Cache is keyed by (audio_source, model, language).

        Args:
            force_refresh: If True, re-transcribe even if cached result exists

        Returns:
            Transcribed text or None if transcription fails
        """
        # Return cached result from instance if available and not forcing refresh
        if self.transcription_result and not force_refresh:
            return self.transcription_result

        # Determine audio source
        audio_source = self.url or self.file_uri or self.base64_data
        if not audio_source:
            vcprint("No audio source available for transcription", color="yellow")
            return None

        # Check global cache (unless forcing refresh)
        if not force_refresh:
            from matrx_ai.processing.audio.transcription_cache import get_cache

            cache = get_cache()
            cached = cache.get(
                audio_source=audio_source,
                model=self.transcription_model,
                language=self.transcription_language,
            )

            if cached:
                # Use cached transcription
                self.transcription_result = cached.text
                self.metadata["transcription"] = cached.metadata
                self.metadata["transcription"]["from_cache"] = True

                vcprint(
                    f"Using cached transcription for audio ({len(cached.text)} characters)",
                    "Audio Transcription",
                    color="green",
                )
                return self.transcription_result

        # Perform transcription
        try:
            from matrx_ai.processing.audio.stt import STTRequest, execute_stt
            from matrx_ai.processing.audio.transcription_cache import get_cache

            result = await execute_stt(
                STTRequest(
                    audio_source=audio_source,
                    model=self.transcription_model,
                    language=self.transcription_language,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"],
                )
            )

            # Cache result in instance
            self.transcription_result = result.text

            # Store usage metadata
            metadata = {
                "usage": result.usage.to_dict(),
                "quality_metrics": result.quality_metrics,
                "language": result.language,
                "duration": result.duration,
                "from_cache": False,
            }
            self.metadata["transcription"] = metadata

            # Store in global cache
            cache = get_cache()
            cache.set(
                audio_source=audio_source,
                model=self.transcription_model,
                language=self.transcription_language,
                text=result.text,
                metadata=metadata,
            )

            return self.transcription_result

        except Exception as e:
            vcprint(
                f"Transcription failed: {str(e)}",
                "Audio Transcription Error",
                color="red",
            )
            return None

    def to_dict(self, truncate_base64: bool = True) -> dict[str, Any]:
        """Convert to dict with optional base64 truncation"""
        result = dataclasses.asdict(self)
        if truncate_base64 and result.get("base64_data"):
            result["base64_data"] = f"<{len(self.base64_data)} chars>"
        return result

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to unified media storage format. Phase 3a adds
        UnifiedMediaBlock canonical fields (file_id, size_bytes, origin)."""
        origin = "matrx" if self.file_id else "external"
        result: dict[str, Any] = {
            "type": "media",
            "kind": "audio",
            "origin": origin,
        }
        if self.file_id:
            result["file_id"] = self.file_id
        if self.url:
            result["url"] = self.url
        if self.base64_data:
            result["base64_data"] = self.base64_data
        if self.file_uri:
            result["file_uri"] = self.file_uri
        if self.mime_type:
            result["mime_type"] = self.mime_type
        if self.file_size is not None:
            result["size_bytes"] = self.file_size
        # Phase 3b: persist duration so AudioBlock.duration_ms hydrates
        # straight from cx_message reads.
        if self.duration_ms is not None:
            result["duration_ms"] = self.duration_ms
        # Kind-specific extras go into metadata
        storage_metadata = {**self.metadata}
        if self.auto_transcribe:
            storage_metadata["auto_transcribe"] = self.auto_transcribe
        if self.transcription_model != "stt-default":
            storage_metadata["transcription_model"] = self.transcription_model
        if self.transcription_language:
            storage_metadata["transcription_language"] = self.transcription_language
        if self.transcription_result:
            storage_metadata["transcription_result"] = self.transcription_result
        if storage_metadata:
            result["metadata"] = storage_metadata
        return result

    def __repr__(self) -> str:
        """Custom repr that only truncates base64_data"""
        base64_display = f"<{len(self.base64_data)} chars>" if self.base64_data else None
        return (
            f"AudioContent("
            f"type={self.type!r}, "
            f"url={self.url!r}, "
            f"base64_data={base64_display}, "
            f"file_uri={self.file_uri!r}, "
            f"mime_type={self.mime_type!r}, "
            f"auto_transcribe={self.auto_transcribe!r}, "
            f"transcription_model={self.transcription_model!r}, "
            f"transcription_language={self.transcription_language!r}, "
            f"transcription_result={self.transcription_result!r}, "
            f"metadata={self.metadata!r})"
        )

    def to_google(self) -> dict[str, Any] | None:
        """Convert to Google Gemini format.

        Sync — never does I/O. The boundary normaliser at AI Dream
        pre-fetches every URL (ours and external) into ``base64_data``,
        so this method only consumes already-resolved data. If we land
        in the no-data branch, the boundary either was not wired or the
        fetch failed; dropping (with matrx-ai's logging) is correct.
        """
        if self.file_uri:
            return {
                "fileData": {
                    "fileUri": self.file_uri,
                    "mimeType": self.mime_type,
                }
            }
        elif self.base64_data:
            return {
                "inlineData": {
                    "data": self.base64_data,
                    "mimeType": self.mime_type,
                }
            }
        vcprint(
            self.to_dict(),
            "AudioContent to_google MediaItem has no resolvable content\n\n Temporarily not raising an error, but dropping the media item",
            color="red",
        )
        return None

    def to_openai(self) -> dict[str, Any] | None:
        """Convert to OpenAI format - not yet supported"""
        # OpenAI doesn't have audio input in Responses API yet
        vcprint(
            self.to_dict(),
            "AudioContent to_openai: audio input is not yet supported by OpenAI — dropping the media item",
            color="yellow",
        )
        return None

    def to_anthropic(self) -> dict[str, Any] | None:
        """Convert to Anthropic format - not yet supported"""
        # Anthropic doesn't support audio input yet
        vcprint(
            self.to_dict(),
            "AudioContent to_anthropic: audio input is not yet supported by Anthropic — dropping the media item",
            color="yellow",
        )
        return None

    @classmethod
    def from_google(cls, part: Part, audio_format: str | None = None) -> Optional["AudioContent"]:
        """Create AudioContent from an EXTERNAL Google ``file_data`` URI.

        Inline bytes do NOT belong here: persisting them synchronously yields a
        signed url with no ``file_id``, and this content is written into
        ``chat.message``. Inline parts go through :meth:`from_google_async`,
        which returns a ``file_id``.

        ``audio_format`` is accepted so the call site stays uniform with the
        async twin; an external URI is never transcoded.
        """
        if hasattr(part, "file_data") and part.file_data:
            return cls(file_uri=part.file_data.file_uri, mime_type=part.file_data.mime_type)
        vcprint(
            {"part_type": type(part).__name__, "part_repr": repr(part)},
            "AudioContent from_google: Part has no file_data (inline bytes belong on from_google_async)\n\n Dropping the media item",
            color="red",
        )
        return None

    @classmethod
    async def from_raw_audio_async(
        cls, raw_bytes: bytes, raw_mime: str, audio_format: str | None = None
    ) -> Optional["AudioContent"]:
        """Persist already-extracted raw audio bytes as ONE canonical file.

        This is the single envelope-save path for inline audio. Streaming TTS
        yields many raw-PCM segments that must be concatenated into one buffer
        BEFORE saving (saving each segment separately produced N truncated
        files — the latent multi-chunk bug). Callers concatenate first, then
        hand the whole buffer here. ``from_google_async`` delegates to this for
        the single-part case.

        Raw PCM (``audio/L16`` / ``audio/pcm``) is normalized to WAV by the
        media handler; ``audio_format`` optionally transcodes the result.
        """
        from matrx_ai.media import save_media_envelope_async
        from matrx_ai.media.generation_metadata import map_tts_audio_response
        from matrx_ai.media.media_persistence import AIMediaHandler

        _, wav_mime = AIMediaHandler.get_instance()._normalize_audio(b"", raw_mime)
        if audio_format:
            format_to_mime = {"wav": "audio/wav", "mp3": "audio/mpeg", "ogg": "audio/ogg"}
            effective_mime = format_to_mime.get(audio_format.lower(), wav_mime)
        else:
            effective_mime = wav_mime

        gen_meta = map_tts_audio_response(
            provider="google",
            model="gemini-multi-modal",
            prompt="",
            audio_format=audio_format,
        )
        envelope = await save_media_envelope_async(
            content=raw_bytes,
            mime_type=raw_mime,
            audio_format=audio_format,
            provider="google",
            feature="ai_audio",
            extra_metadata={"generation": gen_meta.model_dump(exclude_none=True)},
        )
        return cls(
            url=envelope.url,
            file_id=envelope.file_id,
            mime_type=effective_mime,
            file_size=envelope.size_bytes,
            duration_ms=envelope.duration_ms,
            metadata={"generation": gen_meta.model_dump(exclude_none=True)},
        )

    @classmethod
    async def from_google_async(
        cls, part: Part, audio_format: str | None = None
    ) -> Optional["AudioContent"]:
        """Async/canonical Google → AudioContent conversion (Phase 2c).

        Persists inline_data via ``save_media_envelope_async`` so the
        returned content carries ``file_id`` + ``file_uri`` +
        ``size_bytes`` + ``duration_ms`` (from probe). The Phase 1
        SOCIAL_BASELINE variants (waveform-based since Phase 1d) render
        automatically as part of the envelope path. Stamps generation
        metadata under ``metadata.generation`` for audit + re-gen UX.

        Closes the last "external origin audio" surface — Google audio
        previously emitted blocks with ``origin="external"`` because
        the sync from_google only returned a URL.
        """
        if hasattr(part, "inline_data") and part.inline_data:
            raw_mime = part.inline_data.mime_type or ""
            try:
                return await cls.from_raw_audio_async(
                    part.inline_data.data, raw_mime, audio_format=audio_format
                )
            except Exception as e:
                # NO fallback: the sync path persists via ``save_media``, which
                # returns a SIGNED url and no ``file_id`` — and this content is
                # written into ``chat.message``, where a frozen expiring link has
                # nothing to re-mint from. Drop the item loudly instead.
                vcprint(
                    f"AudioContent.from_google_async: envelope save failed ({e!r}); "
                    f"dropping the audio — no file_id means no durable identity",
                    color="red",
                )
                return None
        elif hasattr(part, "file_data") and part.file_data:
            return cls(file_uri=part.file_data.file_uri, mime_type=part.file_data.mime_type)
        vcprint(
            {"part_type": type(part).__name__, "part_repr": repr(part)},
            "AudioContent from_google_async: Part has neither inline_data nor file_data\n\n Temporarily not raising an error, but dropping the media item",
            color="red",
        )
        return None


@dataclass
class VideoContent:
    type: Literal["video", "input_video"] = "video"
    url: str | None = None
    base64_data: str | None = None
    file_uri: str | None = None
    file_id: str | None = None  # Cloud-files UUID
    mime_type: str | None = None
    video_metadata: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # Phase 3b: intrinsic dims + duration persisted into cx_message storage.
    width: int | None = None
    height: int | None = None
    duration_ms: int | None = None

    # === Resolved-state fields (populated by the boundary normaliser) ===
    resolved_url: str | None = None
    file_size: int | None = None
    owner_id: str | None = None
    is_ours: bool = False
    is_resolved: bool = False
    resolver_error: str | None = None

    def __post_init__(self):
        """Auto-detect mime_type if not provided"""
        if self.mime_type is None:
            self.mime_type = detect_mime_type(
                url=self.url, base64_data=self.base64_data, file_uri=self.file_uri
            )

    def get_output(self) -> str | None:
        """Durable handle only — see THE OUTPUT RULE above. Never a signed URL."""
        durable = _durable_media_output(self)
        if durable:
            return durable
        if self.base64_data:
            return self.base64_data
        if self.file_uri:
            return self.file_uri
        return None

    def replace_variables(self, variables: dict[str, Any]) -> bool:
        """See ImageContent.replace_variables."""
        return _substitute_and_coerce_media_fields(self, variables)

    def to_dict(self, truncate_base64: bool = True) -> dict[str, Any]:
        """Convert to dict with optional base64 truncation"""
        result = dataclasses.asdict(self)
        if truncate_base64 and result.get("base64_data"):
            result["base64_data"] = f"<{len(self.base64_data)} chars>"
        return result

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to unified media storage format. Phase 3a adds
        UnifiedMediaBlock canonical fields (file_id, size_bytes, origin)."""
        origin = "matrx" if self.file_id else "external"
        result: dict[str, Any] = {
            "type": "media",
            "kind": "video",
            "origin": origin,
        }
        if self.file_id:
            result["file_id"] = self.file_id
        if self.url:
            result["url"] = self.url
        if self.base64_data:
            result["base64_data"] = self.base64_data
        if self.file_uri:
            result["file_uri"] = self.file_uri
        if self.mime_type:
            result["mime_type"] = self.mime_type
        if self.file_size is not None:
            result["size_bytes"] = self.file_size
        # Phase 3b: dims + duration persisted into cx_message storage.
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        if self.duration_ms is not None:
            result["duration_ms"] = self.duration_ms
        # Kind-specific extras go into metadata
        storage_metadata = {**self.metadata}
        if self.video_metadata:
            storage_metadata["video_metadata"] = self.video_metadata
        if storage_metadata:
            result["metadata"] = storage_metadata
        return result

    def __repr__(self) -> str:
        """Custom repr that only truncates base64_data"""
        base64_display = f"<{len(self.base64_data)} chars>" if self.base64_data else None
        return (
            f"VideoContent("
            f"type={self.type!r}, "
            f"url={self.url!r}, "
            f"base64_data={base64_display}, "
            f"file_uri={self.file_uri!r}, "
            f"mime_type={self.mime_type!r}, "
            f"video_metadata={self.video_metadata!r}, "
            f"metadata={self.metadata!r})"
        )

    def to_google(self) -> dict[str, Any] | None:
        """Convert to Google Gemini format.

        Sync — never does I/O. The boundary normaliser at AI Dream
        pre-fetches every URL (ours and external) into ``base64_data``,
        so this method only consumes already-resolved data.
        """
        if self.file_uri:
            part = {
                "fileData": {
                    "fileUri": self.file_uri,
                    "mimeType": self.mime_type,
                }
            }
        elif self.base64_data:
            part = {
                "inlineData": {
                    "data": self.base64_data,
                    "mimeType": self.mime_type,
                }
            }
        else:
            vcprint(
                self.to_dict(),
                "VideoContent to_google MediaItem has no resolvable content\n\n Temporarily not raising an error, but dropping the media item",
                color="red",
            )
            return None

        if self.video_metadata:
            part["videoMetadata"] = self.video_metadata
        return part

    def to_openai(self) -> dict[str, Any] | None:
        """Convert to OpenAI format - not yet supported"""
        # OpenAI doesn't support video input yet
        vcprint(
            self.to_dict(),
            "VideoContent to_openai: video input is not yet supported by OpenAI — dropping the media item",
            color="yellow",
        )
        return None

    def to_moonshot_chat(self) -> dict[str, Any]:
        """Serialize resolved video bytes for Moonshot's Chat Completions API."""
        if not self.base64_data:
            raise ValueError(
                "Moonshot video input requires resolved base64 data; resolve the MediaRef "
                "at the API boundary before dispatch."
            )
        if not self.mime_type:
            raise ValueError(
                "Moonshot video input requires a MIME type; resolve the MediaRef "
                "at the API boundary before dispatch."
            )
        return {
            "type": "video_url",
            "video_url": {"url": f"data:{self.mime_type};base64,{self.base64_data}"},
        }

    def to_anthropic(self) -> dict[str, Any] | None:
        """Convert to Anthropic format - not yet supported"""
        # Anthropic doesn't support video input yet
        vcprint(
            self.to_dict(),
            "VideoContent to_anthropic: video input is not yet supported by Anthropic — dropping the media item",
            color="yellow",
        )
        return None

    @classmethod
    def from_google(cls, part: Part) -> Optional["VideoContent"]:
        """Create VideoContent from an EXTERNAL Google ``file_data`` URI.

        Inline bytes do NOT belong here: persisting them synchronously yields a
        signed url with no ``file_id``, and this content is written into
        ``chat.message``. Inline parts go through :meth:`from_google_async`,
        which returns a ``file_id``.
        """
        video_metadata = None
        if hasattr(part, "video_metadata") and part.video_metadata:
            video_metadata = {
                "start_offset": getattr(part.video_metadata, "start_offset", None),
                "end_offset": getattr(part.video_metadata, "end_offset", None),
                "fps": getattr(part.video_metadata, "fps", None),
            }

        if hasattr(part, "file_data") and part.file_data:
            # File URI is already external and persistent
            return cls(
                file_uri=part.file_data.file_uri,
                mime_type=part.file_data.mime_type,
                video_metadata=video_metadata,
            )
        vcprint(
            {"part_type": type(part).__name__, "part_repr": repr(part)},
            "VideoContent from_google: Part has no file_data (inline bytes belong on from_google_async)\n\n Dropping the media item",
            color="red",
        )
        return None

    @classmethod
    async def from_google_async(cls, part: Part) -> Optional["VideoContent"]:
        """Async/canonical Google → VideoContent conversion (Phase 2c).

        Same pattern as AudioContent.from_google_async — envelope path
        for inline_data so the returned content carries file_id + dims
        + duration_ms; file_data path stays legacy since the URI is
        already external/persistent.
        """
        from matrx_ai.media import save_media_envelope_async
        from matrx_ai.media.generation_metadata import build_default_metadata

        video_metadata = None
        if hasattr(part, "video_metadata") and part.video_metadata:
            video_metadata = {
                "start_offset": getattr(part.video_metadata, "start_offset", None),
                "end_offset": getattr(part.video_metadata, "end_offset", None),
                "fps": getattr(part.video_metadata, "fps", None),
            }

        if hasattr(part, "inline_data") and part.inline_data:
            gen_meta = build_default_metadata(
                kind="video",
                provider="google",
                model="gemini-multi-modal",
                prompt="",
                n_returned=1,
            )
            try:
                envelope = await save_media_envelope_async(
                    content=part.inline_data.data,
                    mime_type=part.inline_data.mime_type,
                    provider="google",
                    feature="ai_video",
                    extra_metadata={"generation": gen_meta.model_dump(exclude_none=True)},
                )
            except Exception as e:
                # NO fallback: the sync path persists via ``save_media``, which
                # returns a SIGNED url and no ``file_id`` — and this content is
                # written into ``chat.message``, where a frozen expiring link has
                # nothing to re-mint from. Drop the item loudly instead.
                vcprint(
                    f"VideoContent.from_google_async: envelope save failed ({e!r}); "
                    f"dropping the video — no file_id means no durable identity",
                    color="red",
                )
                return None
            return cls(
                url=envelope.url,
                file_id=envelope.file_id,
                mime_type=envelope.mime_type or part.inline_data.mime_type,
                file_size=envelope.size_bytes,
                width=envelope.width,
                height=envelope.height,
                duration_ms=envelope.duration_ms,
                video_metadata=video_metadata,
                metadata={"generation": gen_meta.model_dump(exclude_none=True)},
            )
        elif hasattr(part, "file_data") and part.file_data:
            return cls(
                file_uri=part.file_data.file_uri,
                mime_type=part.file_data.mime_type,
                video_metadata=video_metadata,
            )
        vcprint(
            {"part_type": type(part).__name__, "part_repr": repr(part)},
            "VideoContent from_google_async: Part has neither inline_data nor file_data\n\n Temporarily not raising an error, but dropping the media item",
            color="red",
        )
        return None


@dataclass
class YouTubeVideoContent:
    """
    YouTube video content that can ONLY be processed by Google Gemini.

    Google Gemini accepts YouTube URLs directly via fileData.fileUri.
    All other providers will skip this content with a warning.

    Example YouTube URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """

    type: Literal["youtube_video"] = "youtube_video"
    url: str = ""
    video_metadata: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_output(self) -> str:
        """Get the output of the YouTube video."""
        return self.url

    def replace_variables(self, variables: dict[str, Any]) -> bool:
        """See ImageContent.replace_variables. YouTube content only has a
        `url` field — substitution applies, but URL → file_id/file_uri
        re-routing is a no-op (the helper guards on hasattr)."""
        return _substitute_and_coerce_media_fields(self, variables)

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to unified media storage format. Phase 3a: YouTube
        is always external (no cld_files file_id)."""
        result: dict[str, Any] = {
            "type": "media",
            "kind": "youtube",
            "origin": "external",
            "url": self.url,
            "external_url": self.url,
        }
        # Kind-specific extras go into metadata
        storage_metadata = {**self.metadata}
        if self.video_metadata:
            storage_metadata["video_metadata"] = self.video_metadata
        if storage_metadata:
            result["metadata"] = storage_metadata
        return result

    def to_google(self) -> dict[str, Any] | None:
        """Convert to Google Gemini format - YouTube URLs supported via fileData"""
        if not self.url:
            vcprint(
                {
                    "type": self.type,
                    "video_metadata": self.video_metadata,
                    "metadata": self.metadata,
                },
                "YouTubeVideoContent to_google: no URL present on YouTube content item\n\n Temporarily not raising an error, but dropping the media item",
                color="red",
            )
            return None

        # The FE often sends a bare video ID or a youtu.be short-link;
        # Google only accepts a canonical watch URL / File API URI, so
        # coerce to the form it understands before building the part.
        file_uri = normalize_youtube_url(self.url)

        # Google accepts YouTube URLs directly in fileUri
        part = {
            "fileData": {
                "fileUri": file_uri,
            }
        }

        if self.video_metadata:
            part["videoMetadata"] = self.video_metadata

        return part

    def to_openai(self) -> dict[str, Any] | None:
        """OpenAI doesn't support YouTube URLs - skip with warning"""
        from matrx_utils import vcprint

        vcprint(
            f"YouTube URL '{self.url}' is not supported by OpenAI models and will be skipped.",
            "YouTube URL Warning",
            color="yellow",
        )
        return None

    def to_anthropic(self) -> dict[str, Any] | None:
        """Anthropic doesn't support YouTube URLs - skip with warning"""
        from matrx_utils import vcprint

        vcprint(
            f"YouTube URL '{self.url}' is not supported by Anthropic models and will be skipped.",
            "YouTube URL Warning",
            color="yellow",
        )
        return None

    @classmethod
    def from_google(cls, part: Part) -> Optional["YouTubeVideoContent"]:
        """
        Create YouTubeVideoContent from Google Part object.

        Only creates if the file_uri is a YouTube URL.
        """
        if not hasattr(part, "file_data") or not part.file_data:
            return None

        file_uri = getattr(part.file_data, "file_uri", "")

        # Check if it's a YouTube URL
        if not file_uri or not ("youtube.com" in file_uri or "youtu.be" in file_uri):
            return None

        video_metadata = None
        if hasattr(part, "video_metadata") and part.video_metadata:
            video_metadata = {
                "start_offset": getattr(part.video_metadata, "start_offset", None),
                "end_offset": getattr(part.video_metadata, "end_offset", None),
                "fps": getattr(part.video_metadata, "fps", None),
            }

        return cls(
            url=file_uri,
            video_metadata=video_metadata,
        )


# ----------------------------------------------------------------------
# Text-document handling for providers whose base64 "document" slot is
# PDF-only.
# ----------------------------------------------------------------------
#
# Anthropic's ``document.source.type="base64"`` accepts EXACTLY
# ``media_type="application/pdf"``, and OpenAI's ``input_file`` is likewise
# PDF-oriented. A text file (markdown, plaintext, csv, json, …) attached as
# a DocumentContent therefore 400s the ENTIRE request if shipped as base64
# with its real mime (live incident 2026-06-29: a text/markdown attachment
# returned ``media_type: Input should be 'application/pdf'`` and killed the
# turn). Text documents must instead be decoded and delivered as text:
#   - Anthropic: a document block with ``source.type="text"``,
#     ``media_type="text/plain"``, ``data=<raw decoded text>``.
#   - OpenAI:    an ``input_text`` part carrying the decoded text.
_TEXT_DOCUMENT_MIME_PREFIXES = ("text/",)
_TEXT_DOCUMENT_MIME_EXACT = frozenset(
    {
        "application/json",
        "application/xml",
        "application/x-yaml",
        "application/yaml",
        "application/x-ndjson",
        "application/toml",
        "application/x-sh",
    }
)


def _base_mime(mime: str | None) -> str:
    return (mime or "").split(";")[0].strip().lower()


def is_pdf_mime(mime: str | None) -> bool:
    return _base_mime(mime) == "application/pdf"


def is_text_document_mime(mime: str | None) -> bool:
    base = _base_mime(mime)
    if not base:
        return False
    if base.startswith(_TEXT_DOCUMENT_MIME_PREFIXES):
        return True
    return base in _TEXT_DOCUMENT_MIME_EXACT


def decode_document_text(base64_data: str) -> str | None:
    """Decode base64 document bytes to UTF-8 text. Returns ``None`` when the
    bytes are not valid UTF-8 (a binary file mislabeled as text) so callers
    can drop loudly rather than ship a malformed provider payload."""
    import base64 as _b64

    try:
        raw = _b64.b64decode(base64_data)
    except (ValueError, TypeError):
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


@dataclass
class DocumentContent:
    type: Literal["document", "input_document"] = "document"
    url: str | None = None
    base64_data: str | None = None
    file_uri: str | None = None
    file_id: str | None = None  # Cloud-files UUID
    mime_type: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # Phase 3b: intrinsic dims + page count persisted into cx_message storage.
    width: int | None = None
    height: int | None = None
    page_count: int | None = None

    # === Resolved-state fields (populated by the boundary normaliser) ===
    resolved_url: str | None = None
    file_size: int | None = None
    owner_id: str | None = None
    is_ours: bool = False
    is_resolved: bool = False
    resolver_error: str | None = None

    def __post_init__(self):
        """Pull mime + file_id from metadata fallbacks, then auto-detect."""
        if not self.mime_type and self.metadata:
            for key in ("mime_type", "mimetype", "content_type", "contentType", "mimeType", "type"):
                v = self.metadata.get(key)
                if isinstance(v, str) and "/" in v:
                    self.mime_type = v
                    break
        if not self.file_id and self.metadata:
            for key in ("file_id", "fileId", "id"):
                v = self.metadata.get(key)
                if isinstance(v, str):
                    self.file_id = v
                    break
        if self.mime_type is None:
            self.mime_type = detect_mime_type(
                url=self.url, base64_data=self.base64_data, file_uri=self.file_uri
            )

    def get_output(self) -> str | None:
        """Durable handle only — see THE OUTPUT RULE above. Never a signed URL."""
        durable = _durable_media_output(self)
        if durable:
            return durable
        if self.base64_data:
            return self.base64_data
        if self.file_uri:
            return self.file_uri
        return None

    def replace_variables(self, variables: dict[str, Any]) -> bool:
        """See ImageContent.replace_variables."""
        return _substitute_and_coerce_media_fields(self, variables)

    def to_dict(self, truncate_base64: bool = True) -> dict[str, Any]:
        """Convert to dict with optional base64 truncation"""
        result = dataclasses.asdict(self)
        if truncate_base64 and result.get("base64_data"):
            result["base64_data"] = f"<{len(self.base64_data)} chars>"
        return result

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to unified media storage format. Phase 3a adds
        UnifiedMediaBlock canonical fields (file_id, size_bytes, origin)."""
        origin = "matrx" if self.file_id else "external"
        result: dict[str, Any] = {
            "type": "media",
            "kind": "document",
            "origin": origin,
        }
        if self.file_id:
            result["file_id"] = self.file_id
        if self.url:
            result["url"] = self.url
        if self.base64_data:
            result["base64_data"] = self.base64_data
        if self.file_uri:
            result["file_uri"] = self.file_uri
        if self.mime_type:
            result["mime_type"] = self.mime_type
        if self.file_size is not None:
            result["size_bytes"] = self.file_size
        # Phase 3b: dims + page_count persisted into cx_message storage.
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        if self.page_count is not None:
            result["page_count"] = self.page_count
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result

    def __repr__(self) -> str:
        """Custom repr that only truncates base64_data"""
        base64_display = f"<{len(self.base64_data)} chars>" if self.base64_data else None
        return (
            f"DocumentContent("
            f"type={self.type!r}, "
            f"url={self.url!r}, "
            f"base64_data={base64_display}, "
            f"file_uri={self.file_uri!r}, "
            f"mime_type={self.mime_type!r}, "
            f"metadata={self.metadata!r})"
        )

    def to_google(self) -> dict[str, Any] | None:
        """Convert to Google Gemini format.

        Sync — never does I/O. The boundary normaliser at AI Dream
        pre-fetches every URL (ours and external) into ``base64_data``,
        so this method only consumes already-resolved data. If we land
        in the no-data branch the boundary either was not wired or the
        fetch failed; dropping (with matrx-ai's logging) is correct.
        """
        if self.file_uri and self.file_uri.startswith("gs://"):
            return {"fileData": {"fileUri": self.file_uri, "mimeType": self.mime_type}}
        if self.base64_data:
            return {
                "inlineData": {
                    "data": self.base64_data,
                    "mimeType": self.mime_type or "application/octet-stream",
                }
            }
        vcprint(
            self.to_dict(),
            "DocumentContent to_google MediaItem has no resolvable content\n\n Temporarily not raising an error, but dropping the media item",
            color="red",
        )
        return None

    def to_openai(self) -> dict[str, Any] | None:
        """Convert to OpenAI format. URL resolution happens centrally."""
        # Prefer base64 (boundary normalizer populates it for cld_files);
        # fall back to URL only when both `base64_data` and `file_uri` are
        # absent. Validate at least one usable representation exists rather
        # than silently emitting {"file_url": None}.
        if getattr(self, "base64_data", None):
            # OpenAI's input_file is PDF-oriented; a text document must be
            # delivered DECODED as an input_text part, else the request is
            # rejected (mirrors the Anthropic text-document path).
            if not is_pdf_mime(self.mime_type):
                text = decode_document_text(self.base64_data)
                if text is not None:
                    return {"type": "input_text", "text": text}
                vcprint(
                    self.to_dict(),
                    f"DocumentContent to_openai: non-PDF, non-text document "
                    f"(mime={self.mime_type!r}) has no OpenAI representation — dropping the media item",
                    color="red",
                )
                return None
            return {
                "type": "input_file",
                "filename": getattr(self, "file_name", None) or "document",
                "file_data": (
                    f"data:{self.mime_type or 'application/pdf'};base64,{self.base64_data}"
                ),
            }
        url = getattr(self, "resolved_url", None) or self.url
        if url:
            return {"type": "input_file", "file_url": url}
        vcprint(
            self.to_dict(),
            "DocumentContent to_openai MediaItem has no resolvable content "
            "(no base64_data, resolved_url, or url) — boundary normalizer "
            "failed to pre-fetch. Dropping the media item.",
            color="red",
        )
        return None

    def _anthropic_citation_fields(self) -> dict[str, Any]:
        """Citations enable + title/context — shared by every Anthropic doc shape.

        Citations are DEFAULT-ON (ratified 2026-07-17): every document sent to
        Anthropic is citable unless this specific document was explicitly
        opted out via ``metadata["citations_enabled"]=False`` — and that
        exclusion is LOUD, never silent. The request-level machine-run gate
        (structured-output / pipeline opt-out) lives in the Anthropic
        translator, which knows the UnifiedConfig.

        ``title`` makes citations meaningful (document_title in the returned
        citation objects); ``context`` is extra grounding text Anthropic reads
        but never cites.
        """
        if self.metadata.get("citations_enabled") is False:
            from matrx_ai.config.citations import log_citations_disabled

            log_citations_disabled(
                f"document metadata['citations_enabled']=False (file_id={self.file_id!r})",
                1,
            )
            return {}
        fields: dict[str, Any] = {"citations": {"enabled": True}}
        title = None
        for key in ("title", "file_name", "filename", "name", "original_name"):
            value = self.metadata.get(key)
            if isinstance(value, str) and value.strip():
                title = value.strip()
                break
        if title is None:
            attr_name = getattr(self, "file_name", None)
            if isinstance(attr_name, str) and attr_name.strip():
                title = attr_name.strip()
        if title:
            fields["title"] = title
        context = self.metadata.get("citation_context")
        if isinstance(context, str) and context.strip():
            fields["context"] = context.strip()
        return fields

    def to_anthropic(self) -> dict[str, Any] | None:
        """Convert to Anthropic format.

        Resolved bytes win over the raw client ``url`` (the boundary inlines
        our cld_files refs into ``base64_data`` but leaves ``url`` set);
        emitting that raw ``url`` as a url-source would have Anthropic FETCH a
        share-link / expired-signed URL itself. Prefer base64, then a fresh
        presigned ``resolved_url``, then a genuinely-external ``url`` — mirrors
        ``to_openai``.

        Every shape carries ``citations: {enabled: true}`` (+ title/context
        when known) — see ``_anthropic_citation_fields``.
        """
        citation_fields = self._anthropic_citation_fields()
        if self.base64_data:
            # Anthropic's base64 document source accepts ONLY
            # application/pdf. A text document (markdown, plaintext, csv,
            # json, …) must be delivered DECODED as a text source, else the
            # whole request 400s on media_type.
            if not is_pdf_mime(self.mime_type):
                text = decode_document_text(self.base64_data)
                if text is not None:
                    return {
                        "type": "document",
                        "source": {
                            "type": "text",
                            "media_type": "text/plain",
                            "data": text,
                        },
                        **citation_fields,
                    }
                # Non-PDF that isn't decodable UTF-8 text has no Anthropic
                # representation — drop loudly instead of 400-ing the turn.
                vcprint(
                    self.to_dict(),
                    f"DocumentContent to_anthropic: non-PDF, non-text document "
                    f"(mime={self.mime_type!r}) has no Anthropic representation — dropping the media item",
                    color="red",
                )
                return None
            return {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": self.mime_type,
                    "data": self.base64_data,
                },
                **citation_fields,
            }
        url = getattr(self, "resolved_url", None) or self.url
        if url:
            return {
                "type": "document",
                "source": {"type": "url", "url": url},
                **citation_fields,
            }
        vcprint(
            self.to_dict(),
            "DocumentContent to_anthropic MediaItem has no resolvable content\n\n Temporarily not raising an error, but dropping the media item",
            color="red",
        )
        return None

    @classmethod
    def from_google(cls, part: Part) -> Optional["DocumentContent"]:
        """Create DocumentContent from an EXTERNAL Google ``file_data`` URI.

        Inline bytes do NOT belong here: persisting them synchronously yields a
        signed url with no ``file_id``, and this content is written into
        ``chat.message``. Inline parts go through
        :meth:`from_google_async`, which returns a ``file_id``.
        """
        if hasattr(part, "file_data") and part.file_data:
            # File URI is already persistent
            return cls(file_uri=part.file_data.file_uri, mime_type=part.file_data.mime_type)
        vcprint(
            {"part_type": type(part).__name__, "part_repr": repr(part)},
            "DocumentContent from_google: Part has no file_data (inline bytes belong on from_google_async)\n\n Dropping the media item",
            color="red",
        )
        return None

    @classmethod
    async def from_google_async(cls, part: Part) -> Optional["DocumentContent"]:
        """Async/canonical Google → DocumentContent conversion.

        Inline document bytes go through ``save_media_envelope_async`` so the
        returned content carries ``file_id`` — the durable identity. The
        ``file_data`` branch stays as-is: that URI is already external and
        persistent, so there is nothing of ours to persist or to expire.
        """
        from matrx_ai.media import save_media_envelope_async

        if hasattr(part, "inline_data") and part.inline_data:
            try:
                envelope = await save_media_envelope_async(
                    content=part.inline_data.data,
                    mime_type=part.inline_data.mime_type,
                    provider="google",
                    feature="ai_documents",
                )
            except Exception as e:
                # NO fallback to a sync save: it returns a SIGNED url and no
                # ``file_id``, and this content is written into
                # ``chat.message``, where a frozen expiring link has nothing to
                # re-mint from. Drop the item loudly instead.
                vcprint(
                    f"DocumentContent.from_google_async: envelope save failed ({e!r}); "
                    f"dropping the document — no file_id means no durable identity",
                    color="red",
                )
                return None
            return cls(
                url=envelope.url,
                file_id=envelope.file_id,
                mime_type=envelope.mime_type or part.inline_data.mime_type,
                file_size=envelope.size_bytes,
            )
        elif hasattr(part, "file_data") and part.file_data:
            return cls(file_uri=part.file_data.file_uri, mime_type=part.file_data.mime_type)
        vcprint(
            {"part_type": type(part).__name__, "part_repr": repr(part)},
            "DocumentContent from_google_async: Part has neither inline_data nor file_data\n\n Dropping the media item",
            color="red",
        )
        return None


# ============================================================================
# UNIFIED MEDIA STORAGE RECONSTRUCTION
# ============================================================================

# Union of all media content types
MediaContent = ImageContent | AudioContent | VideoContent | YouTubeVideoContent | DocumentContent


def _single_locator(block: dict[str, Any]) -> dict[str, Any]:
    """Return EXACTLY ONE wire identifier for a stored media block — identity first.

    ``MediaRef`` accepts exactly one of ``file_id`` / ``url`` / ``file_uri``, and a
    stored media part routinely carries BOTH a ``file_id`` and whatever ``url`` was
    visible when the row was written. Forwarding both raised
    ``MediaRef accepts exactly one of ...`` and killed the turn — the server
    refusing history the server itself had written, which made every conversation
    that had ever produced media permanently unusable.

    ``file_id`` is the identity: it re-resolves forever, through the access gate,
    with a URL minted (or not) at the moment of use. A stored ``url`` is a snapshot;
    for one of our own files it is at best redundant and at worst a dead signed
    link. So identity wins and the rest are dropped. A block with NO ``file_id`` is
    a genuinely external reference (a web image the model was shown, a YouTube link)
    and keeps its ``url``.

    See ``collect_media_refs`` below, which states the same law for the outbound
    direction: identity only, never a URL.
    """
    file_id = block.get("file_id") or None
    if file_id:
        return {"file_id": file_id, "url": None, "file_uri": None}
    url = block.get("url") or None
    if url:
        return {"file_id": None, "url": url, "file_uri": None}
    return {"file_id": None, "url": None, "file_uri": block.get("file_uri") or None}


def reconstruct_media_content(
    block: dict[str, Any],
) -> MediaContent | None:
    """
    Reconstruct the correct media content class from a unified storage dict.

    Reads the 'kind' field from a block with type="media" and constructs the
    appropriate original class (ImageContent, AudioContent, etc.).

    This is the deserialization counterpart to each class's to_storage_dict() method.

    Phase 3a back-compat: handles both the legacy storage shape (no
    file_id / origin / size_bytes at top level) and the new
    UnifiedMediaBlock-aligned shape. New fields are picked up when
    present; old shapes still load cleanly (file_id stays None and the
    FE re-resolves via /assets/{file_id} or its existing fallback).

    Args:
        block: Dict with type="media", kind=<MediaKind>, and common/kind-specific fields.

    Returns:
        The appropriate media content instance, or None if kind is unknown.
    """
    claimed_kind = block.get("kind")
    meta = block.get("metadata", {})
    mime_type = block.get("mime_type")
    if not mime_type and isinstance(meta, dict):
        for key in ("mime_type", "mimetype", "content_type", "contentType", "mimeType"):
            candidate = meta.get(key)
            if isinstance(candidate, str) and "/" in candidate:
                mime_type = candidate
                break
    kind = reconcile_media_kind(claimed_kind, mime_type)
    if kind != claimed_kind:
        vcprint(
            data={
                "claimed_kind": claimed_kind,
                "reconciled_kind": kind,
                "mime_type": mime_type,
                "file_id": block.get("file_id"),
                "url": block.get("url"),
            },
            title="🚨 Recovered mismatched media kind from definitive MIME",
            color="red",
        )
    # Phase 3a additions — all optional, fall back to None on legacy reads.
    # ONE identifier reaches the MediaRef, and it is the file_id whenever we
    # have one (see _single_locator).
    locator = _single_locator(block)
    file_size = block.get("size_bytes", block.get("file_size"))

    # Phase 3b additions — dimensions/duration/page_count.
    width = block.get("width")
    height = block.get("height")
    duration_ms = block.get("duration_ms")
    page_count = block.get("page_count")

    if kind == "image":
        return ImageContent(
            **locator,
            base64_data=block.get("base64_data"),
            mime_type=mime_type,
            media_resolution=meta.get("media_resolution"),
            alt=meta.get("alt"),
            vision_class=meta.get("vision_class"),
            file_size=file_size,
            width=width,
            height=height,
            metadata=meta,
        )
    elif kind == "audio":
        return AudioContent(
            **locator,
            base64_data=block.get("base64_data"),
            mime_type=mime_type,
            auto_transcribe=meta.get("auto_transcribe", False),
            transcription_model=meta.get("transcription_model", "stt-default"),
            transcription_language=meta.get("transcription_language"),
            transcription_result=meta.get("transcription_result"),
            file_size=file_size,
            duration_ms=duration_ms,
            metadata=meta,
        )
    elif kind == "video":
        return VideoContent(
            **locator,
            base64_data=block.get("base64_data"),
            mime_type=mime_type,
            video_metadata=meta.get("video_metadata"),
            file_size=file_size,
            width=width,
            height=height,
            duration_ms=duration_ms,
            metadata=meta,
        )
    elif kind == "youtube":
        return YouTubeVideoContent(
            url=block.get("url") or block.get("external_url", ""),
            video_metadata=meta.get("video_metadata"),
            metadata=meta,
        )
    elif kind == "document":
        return DocumentContent(
            **locator,
            base64_data=block.get("base64_data"),
            mime_type=mime_type,
            file_size=file_size,
            width=width,
            height=height,
            page_count=page_count,
            metadata=meta,
        )
    else:
        vcprint(
            block,
            f"WARNING: Unknown media kind: {kind}",
            color="red",
        )
        return None


def collect_media_refs(message: "object") -> list[dict]:
    """Durable references to every media block a message PRODUCED.

    Returns ``[{"file_id", "mime_type", "kind"}]`` — identity only, never a URL.
    A block with no ``file_id`` (an external image the model was shown, a failed
    upload) is skipped: there is nothing durable to hand on, and inventing a URL
    here is the exact bug this whole path exists to kill.

    Consumed by ``AgentRunResult.media`` → ``agent_call``, so a calling agent
    receives a real image block it can SEE rather than a link it can only repeat.
    """
    if message is None:
        return []
    kinds = {
        "ImageContent": "image",
        "AudioContent": "audio",
        "VideoContent": "video",
        "DocumentContent": "document",
    }
    refs: list[dict] = []
    seen: set[str] = set()
    for item in getattr(message, "content", None) or []:
        kind = kinds.get(type(item).__name__)
        if kind is None:
            continue
        file_id = getattr(item, "file_id", None)
        if not file_id or str(file_id) in seen:
            continue
        seen.add(str(file_id))
        refs.append(
            {
                "file_id": str(file_id),
                "mime_type": getattr(item, "mime_type", None),
                "kind": kind,
            }
        )
    return refs

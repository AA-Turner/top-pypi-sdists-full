"""Canonical wire format for ANY user-supplied media reference.

This is THE shape every API in the system accepts when a client wants
the backend to operate on a file. AI requests, PDF processing, scraper,
podcast generation, sandbox bridge, workflow nodes — they all parse
incoming media as ``MediaRef`` (or a subclass), then run it through
``FileManager.resolve_media_async`` exactly once at the API boundary.

Three guarantees:

1. **Exactly one identifier on the wire** (``file_id`` / ``url`` /
   ``file_uri``). The Pydantic validator rejects malformed payloads at
   parse time so handlers never see ambiguous input.

2. **Resolved state is in-band.** After the boundary normalizer runs,
   the fields ``base64_data`` / ``resolved_url`` / canonical
   ``mime_type`` / ``file_size`` / ``owner_id`` / ``is_ours`` are
   populated and ``_resolved`` is set to True. Downstream packages
   read those fields directly; they never need a second DB or S3 trip.

3. **Idempotency.** ``FileManager.resolve_media_async`` checks
   ``_resolved`` and returns the input untouched when it's already
   normalized. Defense-in-depth calls are free.

Inheritance pattern: ``ImageContent``, ``DocumentContent``,
``AudioContent``, ``VideoContent`` (in matrx-ai), and any new media
content type, MUST subclass ``MediaRef`` and add only their
provider-display fields. Do NOT redeclare the canonical identifiers.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator


logger = logging.getLogger(__name__)


# Map of common bare-family MIME hints we'll accept-and-warn (because the
# real subtype gets pulled from cld_files at resolve time anyway). Keeping
# this list small & explicit so we don't silently let truly garbage data
# through. "image" -> coerced to None and logged; resolver will fill the
# canonical mime_type from the DB record.
_BARE_FAMILY_HINTS: frozenset[str] = frozenset(
    {
        "image",
        "audio",
        "video",
        "document",
        "file",
        "application",
        "text",
    }
)


def _looks_like_uuid(text: str) -> bool:
    """A cld_files id is a UUID; anything else is a URL-ish reference."""
    parts = text.split("-")
    if len(parts) != 5 or len(text) != 36:
        return False
    try:
        int(text.replace("-", ""), 16)
    except ValueError:
        return False
    return True


class MediaRef(BaseModel):
    """Canonical media reference shared across every API that takes media."""

    model_config = ConfigDict(
        # Allow extra fields so subclasses can carry provider-display data
        # without redeclaring it here.
        extra="allow",
        # Allow assignment after validation so the boundary normalizer can
        # set base64_data / resolved_url / mime_type in place.
        validate_assignment=False,
        # Open BY DESIGN: subclasses (ImageContent / DocumentContent /
        # AudioContent / VideoContent in matrx-ai) carry provider-display
        # fields as extras rather than redeclaring the canonical identifiers.
        # Acknowledged to the type-contract audit so it reports DYNAMIC, not
        # debt — never "fix" this by closing the shape.
        json_schema_extra={
            "x-contract-dynamic": (
                "subclasses carry provider-display fields as extras; the "
                "canonical identifiers stay declared here"
            )
        },
    )

    # ------------------------------------------------------------------
    # Wire identifiers — exactly one must be set when the client sends.
    # ------------------------------------------------------------------
    file_id: str | None = Field(
        default=None,
        description="cld_files UUID. Preferred form; returned by POST /files/upload.",
    )
    url: str | None = Field(
        default=None,
        description=(
            "Any URL we issued (share link, /files/{id}/url, /files/{id}/download, "
            "raw S3 URL) or a truly external https://. The server recognizes ours "
            "and resolves to bytes; external URLs are passed through to providers "
            "that fetch them, or downloaded as a last resort."
        ),
    )
    file_uri: str | None = Field(
        default=None,
        description="Native cloud URI: s3://bucket/key, gs://..., azure://...",
    )

    # ------------------------------------------------------------------
    # Hints (server overrides with canonical when the file is ours)
    # ------------------------------------------------------------------
    mime_type: str | None = Field(
        default=None,
        description=(
            "Hint from the client. Server REPLACES with the canonical "
            "cld_files.mime_type when the reference resolves to one of our files."
        ),
    )
    metadata: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Free-form per-API metadata. Opaque to the resolver.",
    )

    # ------------------------------------------------------------------
    # Variant hint — when set, the resolver renders (or hits the cache
    # for) a derived variant of the master file before populating the
    # resolved-state fields. Wire-stable; defaults to None. The set of
    # legal values is owned by the encoder family registered with
    # ``cloud_sync.variants.register_variant_encoder``.
    # ------------------------------------------------------------------
    vision_class: str | None = Field(
        default=None,
        description=(
            "Optional name of a registered vision class (e.g. "
            "'anthropic_opus_hires', 'gemini3_high'). When set, resolution "
            "produces a derived variant of the master file using the "
            "host-registered encoder for the 'vision' family. Wire-stable: "
            "frontends and tools may pin a specific variant; otherwise the "
            "unified client annotates this field based on the target model."
        ),
    )

    # ------------------------------------------------------------------
    # Resolved state — populated by FileManager.resolve_media_async.
    # Clients must not set these on the wire (they will be overwritten).
    # ------------------------------------------------------------------
    base64_data: str | None = Field(
        default=None,
        repr=False,
        description="Inline bytes (base64). Set by resolver when needs_bytes=True.",
    )
    resolved_url: str | None = Field(
        default=None,
        description="Fresh presigned URL the resolver minted (provider-fetchable).",
    )
    file_size: int | None = Field(
        default=None,
        description="Resolved byte size from the canonical file row or downloaded content.",
    )
    owner_id: str | None = Field(
        default=None,
        description="Owner user id loaded from the canonical file row during resolution.",
    )
    is_ours: bool = Field(
        default=False,
        description="True iff the resolver matched the reference to a cld_files row.",
    )
    resolver_error: str | None = Field(
        default=None,
        description="Set when resolution failed; surface to the caller for logging.",
    )

    # Private idempotency marker. Pydantic v2 treats leading-underscore
    # fields as private (PrivateAttr would be cleaner but breaks
    # serialisation; we want this to round-trip through model_dump for
    # the per-provider serializers).
    is_resolved: bool = Field(
        default=False,
        description=(
            "Set to True by the boundary normalizer. Resolvers short-circuit "
            "when this is True (idempotency). Internal — clients do not set."
        ),
    )

    # ------------------------------------------------------------------
    # Validation: mime_type must be canonical "type/subtype". We warn
    # and coerce bare family hints ("image", "audio") to None so the
    # resolver fills the real mime_type from cld_files. Anything else
    # malformed is rejected at parse time — the route returns 422.
    # ------------------------------------------------------------------
    @field_validator("mime_type", mode="before")
    @classmethod
    def _normalise_mime_type(cls, v: Any) -> Any:
        if v is None or v == "":
            return None
        if not isinstance(v, str):
            raise ValueError(
                f"mime_type must be a string in 'type/subtype' form (got {type(v).__name__})."
            )
        normalised = v.strip().lower()
        if normalised in _BARE_FAMILY_HINTS:
            logger.warning(
                "[MediaRef] received bare mime_type=%r (no subtype). "
                "This is a client bug — send 'image/png', 'application/pdf', etc. "
                "Coercing to None; the resolver will fill the canonical mime_type "
                "from the cld_files record.",
                v,
            )
            return None
        if "/" not in normalised:
            raise ValueError(
                f"mime_type must be 'type/subtype' (got {v!r}). "
                "Examples: image/png, application/pdf, audio/mpeg, video/mp4."
            )
        if normalised.startswith("/") or normalised.endswith("/"):
            raise ValueError(
                f"mime_type {v!r} is malformed: missing type or subtype around the slash."
            )
        return normalised

    # ------------------------------------------------------------------
    # A bare string IS a reference (2026-09-11). Workflow edges, templates
    # and agents hand media around as plain strings — a link, a cloud URI,
    # or a cld_files id. The reverse-image node refused an Expert's image
    # link with "should be a valid dictionary or instance of MediaRef" and
    # the run died. The wire form stays the one-identifier record; a
    # string is coerced INTO it, never rejected.
    # ------------------------------------------------------------------
    @model_validator(mode="before")
    @classmethod
    def _coerce_bare_reference(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value
        text = value.strip()
        if not text:
            return value  # the after-validator reports the empty reference
        lowered = text.lower()
        if lowered.startswith(("s3://", "gs://", "azure://")):
            return {"file_uri": text}
        if lowered.startswith(("http://", "https://")):
            return {"url": text}
        if _looks_like_uuid(text):
            return {"file_id": text}
        return {"url": text}

    # ------------------------------------------------------------------
    # Validation: exactly one wire identifier (only checked pre-resolution)
    # ------------------------------------------------------------------
    @model_validator(mode="after")
    def _exactly_one_identifier(self) -> MediaRef:
        # If the resolver has already populated this object, the wire-shape
        # rule no longer applies (e.g., is_resolved=True with both file_id
        # and resolved_url set).
        if self.is_resolved:
            return self
        ids = [x for x in (self.file_id, self.url, self.file_uri) if x]
        if len(ids) == 0:
            # Allow empty during construction (subclasses may populate later
            # via model_validate). Re-validation occurs at request parse.
            return self
        if len(ids) > 1:
            raise ValueError(
                "MediaRef accepts exactly one of: file_id, url, file_uri "
                f"(got {len(ids)}: "
                + ", ".join(
                    name
                    for name, val in [
                        ("file_id", self.file_id),
                        ("url", self.url),
                        ("file_uri", self.file_uri),
                    ]
                    if val
                )
                + ")"
            )
        return self

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------
    def has_identifier(self) -> bool:
        return bool(self.file_id or self.url or self.file_uri)

    def has_resolved_payload(self) -> bool:
        """True iff the resolver populated something a provider can use."""
        return bool(self.base64_data or self.resolved_url)


# ---------------------------------------------------------------------------
# String → MediaRef coercion
# ---------------------------------------------------------------------------
#
# Used when a media value reaches the system as a bare string (e.g. a user
# supplied a value for a `{{my_image}}` template variable; the substituted
# string could be a UUID, one of our share links, an s3:// URI, or an
# external https URL). The detection rules mirror what FileManager's
# resolver expects:
#
#   - 36-char UUID  → file_id
#   - s3://, gs://, azure://  → file_uri
#   - everything else → url (the resolver will recognize our share-link /
#     /files/{id}/url / /files/{id}/download patterns and fetch from cld_files,
#     or fall back to fetching as an external URL)
#
# Returns None when the value is None / empty / whitespace-only — the caller
# should drop the surrounding content block in that case.

_UUID_RE = __import__("re").compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    __import__("re").IGNORECASE,
)
_CLOUD_URI_PREFIXES: tuple[str, ...] = ("s3://", "gs://", "azure://")


def classify_media_string(value: str) -> tuple[str, str] | None:
    """Classify a non-empty trimmed string as one of MediaRef's identifier
    fields. Returns (field_name, value) or None if the string is empty.
    """
    if not value:
        return None
    v = value.strip()
    if not v:
        return None
    if _UUID_RE.match(v):
        return ("file_id", v)
    lower = v.lower()
    for prefix in _CLOUD_URI_PREFIXES:
        if lower.startswith(prefix):
            return ("file_uri", v)
    return ("url", v)


def coerce_to_media_ref(
    value: Any,
    *,
    mime_type_hint: str | None = None,
) -> MediaRef | None:
    """Convert a heterogeneous media value into a canonical MediaRef.

    Accepts:
      - None or empty string → returns None (caller should drop the block)
      - An existing MediaRef → returned untouched
      - A dict with at least one identifier (file_id / url / file_uri) →
        constructed via MediaRef(**value)
      - A bare string → classified by ``classify_media_string`` and
        constructed with the inferred identifier field set.

    The optional ``mime_type_hint`` is a fallback when the input doesn't
    carry one. The boundary normalizer will overwrite with the canonical
    cld_files mime_type for owned files.
    """
    if value is None:
        return None
    if isinstance(value, MediaRef):
        return value
    if isinstance(value, dict):
        has_id = bool(value.get("file_id") or value.get("url") or value.get("file_uri"))
        if not has_id:
            return None
        kwargs = {**value}
        if mime_type_hint and not kwargs.get("mime_type"):
            kwargs["mime_type"] = mime_type_hint
        return MediaRef(**kwargs)
    if isinstance(value, str):
        classified = classify_media_string(value)
        if classified is None:
            return None
        field, cleaned = classified
        kwargs: dict[str, Any] = {field: cleaned}
        if mime_type_hint:
            kwargs["mime_type"] = mime_type_hint
        return MediaRef(**kwargs)
    raise TypeError(
        f"coerce_to_media_ref accepts None / MediaRef / dict / str; got {type(value).__name__}"
    )


__all__ = ["MediaRef", "coerce_to_media_ref", "classify_media_string"]

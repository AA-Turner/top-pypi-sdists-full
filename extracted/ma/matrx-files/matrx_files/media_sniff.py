"""MIME-type sniff-and-rewrite at the upload boundary.

Every endpoint that accepts a user-uploaded file SHOULD route the bytes
through ``sniff_mime_type`` before writing. The rules:

1. Reject ``application/octet-stream`` from the client claim — try to
   produce a real type via magic-byte + filename guess.
2. Detect HTML / SVG bytes uploaded under a benign image MIME and coerce
   to ``application/octet-stream`` (forces download — prevents XSS via
   uploaded "image").
3. Fall back to filename-extension guess when the claim is missing.
4. Final fallback is ``application/octet-stream`` so the engine still
   accepts the bytes; downstream callers can decide whether to reject.

The function is platform-level (not specific to images) so the asset
endpoint, the file-upload endpoint, and any future media endpoint share
the same coercion logic. Ships in matrx-utils so every host that runs
cloud-sync gets the same MIME canonicalisation behavior for free.
"""

from __future__ import annotations

import mimetypes
from typing import Final, Literal

# How many leading bytes a caller should hand to ``sniff_mime_type``.
# The cheap magic-byte sniff only reads the first 32 bytes, but the
# audio-vs-video track probe (``detect_av_track_kind``) needs to reach the
# container's track/codec headers, which for a ``MediaRecorder`` WebM/MP4
# sit a few KB in. 64 KB is comfortably past them for every real-world
# recording while staying a trivial slice of bytes already held in memory.
SNIFF_HEAD_BYTES: Final[int] = 65536

# MIME types that browsers will execute or render as HTML — never echo
# the client claim for these; force ``application/octet-stream``.
DANGEROUS_INLINE_MIMES: Final[frozenset[str]] = frozenset(
    {
        "text/html",
        "application/xhtml+xml",
        "application/xml",
        "image/svg+xml",
        "application/javascript",
        "text/javascript",
    }
)

# Mapping for filename-guess fallback. We let mimetypes handle the bulk
# and override only the ambiguous cases.
_EXTRA_EXT_TO_MIME: Final[dict[str, str]] = {
    ".heic": "image/heic",
    ".heif": "image/heif",
    ".avif": "image/avif",
    ".webp": "image/webp",
    ".m4a": "audio/mp4",
    ".m4v": "video/mp4",
    # The host MIME database disagrees about `.ts`/`.mts` (Ubuntu can call
    # them Qt Linguist). TypeScript source is recognized from text evidence
    # before this fallback; ambiguous remaining uploads default to MPEG-TS.
    ".ts": "video/mp2t",
    ".mts": "video/mp2t",
}

# Python's platform MIME database treats ``.ts`` and ``.mts`` as MPEG
# transport streams. Those suffixes are also standard TypeScript source
# suffixes, so filename-first normalization can turn source code into video.
# ``.tsx``/``.cts`` are unambiguous; ``.ts``/``.mts`` require text evidence.
_TYPESCRIPT_EXTENSIONS: Final[frozenset[str]] = frozenset({".ts", ".tsx", ".mts", ".cts"})
_AMBIGUOUS_TRANSPORT_STREAM_EXTENSIONS: Final[frozenset[str]] = frozenset({".ts", ".mts"})
_TYPESCRIPT_CLAIMS: Final[frozenset[str]] = frozenset(
    {
        "application/typescript",
        "application/x-typescript",
        "text/typescript",
    }
)

# Container formats where the file extension alone cannot disambiguate
# audio-only vs video. WebM, Ogg, MP4 (and its variants), Matroska, and
# 3GP all legitimately hold either. Python's stdlib ``mimetypes`` only
# knows the ``video/*`` variant for these, so a `MediaRecorder` upload
# of an audio-only WebM with `Content-Type: audio/webm` would otherwise
# be coerced to ``video/webm`` by the filename guess. For these
# containers we prefer the client's claim when it explicitly says
# ``audio/*`` or ``video/*`` and names the same container.
_AV_AMBIGUOUS_CONTAINERS: Final[frozenset[str]] = frozenset(
    {
        "webm",
        "ogg",
        "mp4",
        "x-matroska",
        "matroska",
        "3gpp",
        "3gpp2",
    }
)


def _container_subtype(mime: str) -> str | None:
    """Return the bare container subtype for an ``audio/`` or ``video/`` MIME.

    ``audio/webm;codecs=opus`` → ``"webm"``; anything else → ``None``.
    """
    if "/" not in mime:
        return None
    prefix, _, sub = mime.partition("/")
    if prefix not in ("audio", "video"):
        return None
    sub = sub.split(";", 1)[0].strip().lower()
    return sub or None


# Matroska/WebM CodecID payloads (ASCII), carried by the 0x86 CodecID
# element inside each TrackEntry. These tokens are distinctive enough that
# a substring scan over the head has effectively zero false-positive rate,
# yet they unambiguously reveal whether a video track is present.
_WEBM_VIDEO_CODECS: Final[tuple[bytes, ...]] = (
    b"V_VP8",
    b"V_VP9",
    b"V_AV1",
    b"V_MPEG",
    b"V_MPEGH",
    b"V_MS",
    b"V_THEORA",
)
_WEBM_AUDIO_CODECS: Final[tuple[bytes, ...]] = (
    b"A_OPUS",
    b"A_VORBIS",
    b"A_AAC",
    b"A_MPEG",
    b"A_PCM",
    b"A_FLAC",
)


def detect_av_track_kind(data: bytes) -> Literal["audio", "video"] | None:
    """Inspect raw container bytes for the presence of a video track.

    Returns ``"video"`` when a video track is positively detected,
    ``"audio"`` when at least one audio track is present and no video
    track is, and ``None`` when the bytes are inconclusive (e.g. an MP4
    whose ``moov`` box sits at the end, beyond the supplied head).

    Covers the containers that legitimately hold either audio or video and
    that browsers / encoders mislabel: WebM/Matroska (EBML CodecID scan),
    MP4/ISO-BMFF (``hdlr`` handler-type scan), and Ogg (codec magic).
    The scan is evidence-only — it never guesses; an undetermined result
    falls back to the caller's claim/extension heuristics.
    """
    if not data:
        return None

    # --- MP4 / ISO-BMFF: look at hdlr handler types (vide / soun) ---
    # ``hdlr`` boxes name each track's media type. ``vide`` => video,
    # ``soun`` => audio. Present near moov, which faststart files keep at
    # the front; non-faststart files may push it past the head (-> None).
    if b"ftyp" in data[:16] or b"moov" in data:
        has_video = b"vide" in data
        has_audio = b"soun" in data
        if has_video:
            return "video"
        if has_audio:
            return "audio"
        return None

    # --- WebM / Matroska: scan EBML CodecID tokens ---
    if data[:4] == b"\x1a\x45\xdf\xa3":
        if any(c in data for c in _WEBM_VIDEO_CODECS):
            return "video"
        if any(c in data for c in _WEBM_AUDIO_CODECS):
            return "audio"
        return None

    # --- Ogg: page magic 'OggS', then codec identification headers ---
    if data[:4] == b"OggS":
        if b"\x80theora" in data or b"OVP80" in data:
            return "video"
        if b"\x01vorbis" in data or b"OpusHead" in data or b"\x7fFLAC" in data:
            return "audio"
        return None

    return None


def _magic_byte_sniff(head: bytes) -> str | None:
    """Cheap magic-byte sniff for the few types that matter most.

    Covers active-content types (HTML, SVG, JS) plus the common image /
    PDF magic numbers. Returns the canonical MIME or ``None`` when no
    confident match.
    """
    if not head:
        return None
    h = head[:32].lstrip()
    lower = h.lower()
    # Active content
    if lower.startswith(b"<?xml") and b"<svg" in lower:
        return "image/svg+xml"
    if lower.startswith((b"<svg", b"<svg ")):
        return "image/svg+xml"
    if lower.startswith((b"<!doctype html", b"<html")):
        return "text/html"
    if lower.startswith(b"<?xml"):
        return "application/xml"
    # Images
    if h.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if h.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if h.startswith(b"GIF87a") or h.startswith(b"GIF89a"):
        return "image/gif"
    if h[:4] == b"RIFF" and h[8:12] == b"WEBP":
        return "image/webp"
    # AVIF / HEIC ISO-BMFF: bytes 4..12 = "ftypHEIC" / "ftypheic" / "ftypavif" / "ftypheix" / "ftypmif1" / "ftypmsf1"
    if h[4:8] == b"ftyp":
        brand = h[8:12]
        if brand in (b"avif", b"avis"):
            return "image/avif"
        if brand in (b"heic", b"heix", b"hevc", b"hevx"):
            return "image/heic"
        if brand in (b"mif1", b"msf1"):
            return "image/heif"
        if brand in (b"mp42", b"isom", b"iso2", b"M4V "):
            return "video/mp4"
    # PDF
    if h.startswith(b"%PDF-"):
        return "application/pdf"
    return None


def _guess_from_filename(filename: str | None) -> str | None:
    if not filename:
        return None
    lower = filename.lower()
    for ext, mime in _EXTRA_EXT_TO_MIME.items():
        if lower.endswith(ext):
            return mime
    guessed, _ = mimetypes.guess_type(lower)
    return guessed


def _typescript_source_mime(
    *, claimed: str | None, head_bytes: bytes, filename: str | None
) -> str | None:
    """Identify TypeScript without stealing real MPEG transport streams."""
    if not filename:
        return None
    lower = filename.lower()
    extension = next((ext for ext in _TYPESCRIPT_EXTENSIONS if lower.endswith(ext)), None)
    if extension is None:
        return None
    if extension not in _AMBIGUOUS_TRANSPORT_STREAM_EXTENSIONS:
        return "text/typescript"
    # MPEG-TS packets are 188 bytes and begin with sync byte 0x47. Check the
    # structure before the UTF-8 heuristic so an all-ASCII transport payload
    # cannot masquerade as TypeScript.
    if len(head_bytes) >= 376 and head_bytes[0] == 0x47 and head_bytes[188] == 0x47:
        return None
    if claimed in _TYPESCRIPT_CLAIMS or (claimed or "").startswith("text/"):
        return "text/typescript"
    if not head_bytes:
        return None
    try:
        decoded = head_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if "\x00" in decoded:
        return None
    control_chars = sum(1 for char in decoded if ord(char) < 32 and char not in "\t\n\r\f\b")
    if control_chars > max(1, len(decoded) // 100):
        return None
    return "text/typescript"


def sniff_mime_type(
    *,
    claimed: str | None,
    head_bytes: bytes,
    filename: str | None,
) -> str:
    """Return the canonical MIME type for an uploaded file.

    Priority:
        1. Magic-byte sniff says "active content" while the claim is a
           benign image → return ``application/octet-stream``.
        2. Magic-byte sniff returns a confident type → use it.
        3. Filename extension guess → use it.
        4. Client claim if non-octet-stream → use it.
        5. Fallback to ``application/octet-stream``.

    The function never raises and never returns ``None`` — there is
    always a string. Callers may still decide to reject the upload
    based on the returned type, but the sniff itself is purely
    advisory normalization.
    """
    claim = (claimed or "").lower().strip() or None
    sniffed = _magic_byte_sniff(head_bytes)

    # Anti-XSS coercion: client claimed image/* but bytes are active content.
    if (
        sniffed in DANGEROUS_INLINE_MIMES
        and claim is not None
        and claim.startswith("image/")
        and claim != "image/svg+xml"
    ):
        return "application/octet-stream"

    typescript_source = _typescript_source_mime(
        claimed=claim, head_bytes=head_bytes, filename=filename
    )
    guessed = _guess_from_filename(filename)

    # Audio-vs-video container disambiguation — evidence first, claim second.
    # WebM, MP4, Ogg, MKV, and 3GP all legitimately carry audio-only OR
    # video. Browsers (``MediaRecorder``) and ``mimetypes`` routinely label
    # an audio-only recording ``video/<container>``; this is the single
    # most common real-world misclassification (voice notes stored as
    # "video"). For these containers we:
    #   1. PROBE the actual track headers — a positive audio-only / video
    #      result is authoritative and overrides everything, including the
    #      ``video/mp4`` magic-byte guess.
    #   2. Failing a conclusive probe, trust an explicit ``audio/*`` ||
    #      ``video/*`` client claim that names the same container.
    # Anything inconclusive falls through to the original priority order.
    av_container = (
        _container_subtype(sniffed or "")
        or _container_subtype(claim or "")
        or _container_subtype(guessed or "")
    )
    if av_container in _AV_AMBIGUOUS_CONTAINERS:
        probed = detect_av_track_kind(head_bytes)
        if probed == "audio":
            return f"audio/{av_container}"
        if probed == "video":
            return f"video/{av_container}"
        if claim and _container_subtype(claim) == av_container:
            return claim

    if sniffed:
        return sniffed

    if typescript_source:
        return typescript_source

    if guessed:
        return guessed
    if claim and claim != "application/octet-stream":
        return claim
    return "application/octet-stream"


def is_dangerous_inline_mime(mime: str | None) -> bool:
    return (mime or "").lower() in DANGEROUS_INLINE_MIMES


__all__ = [
    "DANGEROUS_INLINE_MIMES",
    "SNIFF_HEAD_BYTES",
    "sniff_mime_type",
    "detect_av_track_kind",
    "is_dangerous_inline_mime",
]

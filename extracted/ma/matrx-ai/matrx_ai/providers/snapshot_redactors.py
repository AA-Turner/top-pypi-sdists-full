"""Snapshot Redactors — replace inline FILE DATA (never text) with recoverable markers.

OWNER RULING 2026-10-05: the stored request must let us recreate the exact
request. Text is NEVER cut at any size. Only base64/data-URI file payloads may
be replaced, and the marker carries file_id/url when the request names one.

Why this module exists
======================
For every persisted run (capture is on by default — see
``REQUEST_SNAPSHOT_CAPTURE_DEFAULT``), we persist the *exact provider request
payload* (and best-effort response) to ``cx_request_snapshot`` so we can
reproduce what the model saw. Raw provider payloads can legitimately contain
multi-megabyte base64 blobs (inline PDFs, images, audio). Writing a 10 MB
jsonb row during an active stream saturates the DB write pool and the
snapshot write times out (seen in production 2026-04-21).

This module solves **only** that narrow problem — making the payload small
enough to write reliably — while giving up **as little fidelity as possible**.
Every byte removed is accounted for by an inline fingerprint.

Design rules (non-negotiable)
=============================
1. **Single purpose per class.** Each redactor has ONE narrowly-defined
   transformation it is allowed to perform. No redactor is allowed to do
   "whatever seems convenient". Adding a new behavior requires a new class
   with its own clear name, docstring, and reason_code.

2. **Structure is sacred.** Redactors never add, remove, rename, reorder, or
   retype keys. If the input is a dict, the output dict has identical keys in
   identical order. If a value is a string, its replacement is a string —
   not a dict, not None, not a summary object. Dict-in, dict-out;
   string-in, string-out; always.

3. **Self-describing fingerprint.** Every redacted value embeds an inline
   text marker identifying:
       - which redactor class did it
       - exactly what kind of redaction (reason_code)
       - how much (byte count + sha256 of the original)
       - the JSON path of the field
       - where to find the source code for more detail
   No "soft" redactions. No truncation without a marker.

4. **Preserve head and tail.** When shortening a long string, keep the first
   N and last N characters of the original verbatim. This lets a human
   reader visually recognize what kind of data used to be there:
       - "%PDF-1.4…"      → a PDF was here
       - "/9j/4AAQSk…"    → a JPEG was here
       - "data:image/png;base64,iVBORw0KGgo…" → PNG data URL was here
       - "<html><head>…"  → HTML was here
   The head/tail is NOT a summary — it's a verbatim slice of the original.

5. **Explicit pipeline, explicit order.** Redactors are applied by explicit
   registration order via ``apply_redactors()``. There is no hidden
   composition. There are no magic defaults baked into data structures. If
   a redactor didn't fire, it isn't in the list.

6. **Idempotent.** Running a redacted payload back through the pipeline is a
   no-op. Redactors detect their own previous work via the marker and skip.

7. **Clarity over performance.** This runs at most once per iteration on the
   write path. Correctness, readability, and auditability win every
   trade-off against micro-optimization.

8. **The AI's answer is never shortened** (decision 2026-09-14, KI-049). A
   platform that records AI calls keeps what the AI said. In the RESPONSE
   payload, an assistant ``type="text"`` block's ``text`` is kept verbatim via
   ``apply_response_redactors()``; blobs are still redacted everywhere,
   including inside assistant content. Size is never a reason to cut an
   answer: above the ``agents.request_snapshot.assistant_text_announce_bytes``
   knob it is stored in full and announced. Full reasoning: the decision block
   above ``apply_response_redactors``.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import logging
import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Marker format
# ---------------------------------------------------------------------------
# The marker is a single-line, greppable sentinel that begins with
# MARKER_OPEN and ends with MARKER_CLOSE. Fields are space-separated
# key=value pairs. String values are double-quoted; numeric values are bare.
# Example (single line; wrapped here for readability):
#
#     <<<MATRX_SNAPSHOT_REDACTION
#         redactor="LargeBinaryStringRedactor"
#         reason="string_over_max_bytes"
#         original_bytes=7577567
#         original_sha256="1f3a…"
#         head_chars_preserved=128
#         tail_chars_preserved=128
#         path="$.contents[0].parts[1].inline_data.data"
#         source="matrx_ai.providers.snapshot_redactors"
#     >>>
#
# The redacted string has the shape:
#     <head_verbatim>\n<marker>\n<tail_verbatim>
# so the marker visually sits between the surviving real data.

MARKER_OPEN = "<<<MATRX_SNAPSHOT_REDACTION"
MARKER_CLOSE = ">>>"


def _fmt_marker(**fields: Any) -> str:
    """Build the inline redaction marker.

    All fields passed in are included, in insertion order. Strings are
    double-quoted with embedded quotes backslash-escaped; numbers are bare.
    """
    parts: list[str] = [MARKER_OPEN]
    for key, val in fields.items():
        if isinstance(val, bool):
            parts.append(f'{key}={"true" if val else "false"}')
        elif isinstance(val, (int, float)):
            parts.append(f"{key}={val}")
        else:
            escaped = str(val).replace("\\", "\\\\").replace('"', '\\"')
            parts.append(f'{key}="{escaped}"')
    parts.append(MARKER_CLOSE)
    return " ".join(parts)


def contains_redaction_marker(value: Any) -> bool:
    """True if ``value`` is a string already carrying a redaction marker.

    Used by redactors to guarantee idempotency — re-running the pipeline on
    an already-redacted payload is a no-op.
    """
    return isinstance(value, str) and MARKER_OPEN in value


# ---------------------------------------------------------------------------
# Redactor protocol
# ---------------------------------------------------------------------------

@runtime_checkable
class Redactor(Protocol):
    """Contract every redactor must implement.

    Implementations MUST:
      - Set ``name`` to the class name (for traceability in the marker).
      - Set ``reason_code`` to a stable, grep-friendly snake_case identifier.
      - Return the input unchanged if ``applies_to`` is False.
      - Never modify structure. Leaf-value substitutions only.
    """

    name: str
    reason_code: str

    def applies_to(self, value: Any, path: str = "", siblings: dict[str, Any] | None = None) -> bool: ...
    def redact(self, value: Any, path: str, siblings: dict[str, Any] | None = None) -> Any: ...


# ---------------------------------------------------------------------------
# LargeBinaryStringRedactor
# ---------------------------------------------------------------------------

#: Keys at which provider formats put inline file data (Anthropic
#: ``source.data``, OpenAI ``image_url.url`` / ``input_audio.data`` /
#: ``file_data``, Google ``inline_data.data`` / ``inlineData.data``, the
#: unified ``base64_data``).
_BLOB_KEYS = frozenset(
    {"data", "base64_data", "base64", "b64_json", "bytes", "file_data", "url", "image_url", "audio", "image"}
)
#: Sibling keys that name the same file elsewhere (unified media blocks).
_REFERENCE_KEYS = ("file_id", "file_uri", "url", "resolved_url")
_MIME_KEYS = ("mime_type", "media_type", "mime")

_STRICT_BASE64 = re.compile(r"[A-Za-z0-9+/_\-]+={0,2}")

#: Magic prefixes of the file kinds that travel inline, as BASE64 text.
_BASE64_MAGIC = (
    "JVBERi",  # %PDF
    "iVBOR",  # PNG
    "/9j/",  # JPEG
    "R0lGOD",  # GIF
    "UklGR",  # RIFF (WEBP/WAV)
    "SUQz",  # ID3 (MP3)
    "T2dnUw",  # Ogg
    "//uQ", "//sQ", "//tQ", "//vQ",  # MPEG audio frame sync
    "UEsDB",  # zip (docx/xlsx/pptx)
    "AAAA",  # mp4/mov ftyp box / ico
    "GkXfo",  # webm/mkv
)


_MAGIC_MIME = (
    ("JVBERi", "application/pdf"),
    ("iVBOR", "image/png"),
    ("/9j/", "image/jpeg"),
    ("R0lGOD", "image/gif"),
    ("UklGR", "application/octet-stream"),
    ("SUQz", "audio/mpeg"),
    ("T2dnUw", "audio/ogg"),
    ("UEsDB", "application/zip"),
)


def _sniff_mime(b64: str) -> str:
    return next((m for prefix, m in _MAGIC_MIME if b64.startswith(prefix)), "")


def _leaf_key(path: str) -> str:
    return re.sub(r"\[\d+\]$", "", path.rsplit(".", 1)[-1])


def _is_strict_base64(text: str) -> bool:
    """Base64 alphabet only (no whitespace, no prose), valid padding length."""
    if not text or len(text) % 4 == 1:
        return False
    return _STRICT_BASE64.fullmatch(text) is not None


def _data_uri_parts(value: str) -> tuple[str, str] | None:
    """``(mime, base64_payload)`` when ``value`` is a ``data:…;base64,<strict b64>`` URI."""
    if not value.startswith("data:"):
        return None
    comma = value.find(",", 5, 512)
    if comma < 0 or not value[:comma].endswith(";base64"):
        return None
    payload = value[comma + 1 :]
    if not _is_strict_base64(payload):
        return None
    return value[5 : comma - 7].split(";", 1)[0], payload


def sibling_file_refs(siblings: dict[str, Any] | None, value: str) -> dict[str, str]:
    """File references a media block already carries beside its inline data."""
    siblings = siblings or {}
    return {
        k: siblings[k]
        for k in _REFERENCE_KEYS
        if isinstance(siblings.get(k), str)
        and siblings[k]
        and siblings[k] is not value
        and not contains_redaction_marker(siblings[k])
        and not siblings[k].startswith("data:")
    }


@dataclass
class LargeBinaryStringRedactor:
    """Replaces INLINE FILE DATA (base64 images/PDFs/audio) too large to persist.

    THE RULE (owner ruling 2026-10-05): the stored copy of an AI request must
    let us recreate the exact request. TEXT IS NEVER CUT, at any size. Only a
    real file's bytes may be replaced, and only by a marker that lets the file
    be recovered.

    WHAT IT TOUCHES
    ---------------
    A string over ``max_bytes`` that is BOTH
      * structurally binary — a ``data:…;base64,`` URI whose payload is strict
        base64, OR a strict-base64 string (alphabet only, no whitespace/prose)
        — AND
      * positioned like inline data — its key is one of ``_BLOB_KEYS`` (the
        keys the provider formats use), or its decoded head carries a known
        file magic (PDF/PNG/JPEG/GIF/WEBP/audio/zip/…).
    Prompts, JSON-in-a-string, code and markdown carry spaces/quotes/braces,
    so they can never match, however large.

    WHAT THE MARKER CARRIES
    -----------------------
    redactor, reason, original_bytes, original_sha256, mime, path, and the
    reference to recover the file: ``file_id`` / ``file_uri`` / ``url`` /
    ``resolved_url`` read from the SIBLING keys of the same media block (the
    unified payload keeps them beside ``base64_data``). When the block names
    no file (raw base64 pasted by a caller, or the provider-shaped payload,
    which has no sibling refs), ``reference="none_sha256_only"`` says so —
    the bytes are then not recoverable from the snapshot.

    Structure is preserved (string-in, string-out); head/tail 128 chars of the
    original stay verbatim around the marker.
    """

    max_bytes: int = 65536
    head_chars: int = 128
    tail_chars: int = 128

    name: str = "LargeBinaryStringRedactor"
    reason_code: str = "inline_file_data_over_max_bytes"
    #: path -> (file_id, sha256 of the DECODED bytes) for blobs the host store
    #: already saved (see ``redactors_with_stored_blobs``).
    stored_refs: dict[str, tuple[str, str]] = field(default_factory=dict)

    def _classify(self, value: Any, path: str) -> tuple[str, str] | None:
        """``(mime, base64_payload)`` when this leaf is inline file data to replace."""
        if not isinstance(value, str) or len(value) <= self.max_bytes:
            return None
        if contains_redaction_marker(value):
            return None
        uri = _data_uri_parts(value)
        if uri is not None:
            return uri
        if _leaf_key(path) in _BLOB_KEYS and _is_strict_base64(value):
            return "", value
        if _is_strict_base64(value) and value.startswith(_BASE64_MAGIC):
            return "", value
        return None

    def applies_to(self, value: Any, path: str = "", siblings: dict[str, Any] | None = None) -> bool:
        return self._classify(value, path) is not None

    def redact(self, value: str, path: str, siblings: dict[str, Any] | None = None) -> str:
        found = self._classify(value, path)
        uri_mime = found[0] if found else ""
        siblings = siblings or {}
        refs = sibling_file_refs(siblings, value)
        mime = (
            uri_mime
            or next((siblings[k] for k in _MIME_KEYS if isinstance(siblings.get(k), str)), "")
            or _sniff_mime(value)
        )
        raw_bytes = value.encode("utf-8", errors="replace")
        head = value[: self.head_chars]
        tail = value[-self.tail_chars :] if self.tail_chars > 0 else ""
        fields: dict[str, Any] = {
            "redactor": self.name,
            "reason": self.reason_code,
            "original_bytes": len(raw_bytes),
            "original_sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "mime": mime or "unknown",
        }
        stored = self.stored_refs.get(path)
        if refs:
            fields["reference"] = "file_ref"
            fields.update({f"ref_{k}": v for k, v in refs.items()})
        elif stored:
            fields["reference"] = "file_ref"
            fields["ref_file_id"] = stored[0]
            fields["file_sha256"] = stored[1]
            fields["stored_by"] = "snapshot_blob_store"
        else:
            fields["reference"] = "none_sha256_only"
        fields.update(
            head_chars_preserved=len(head),
            tail_chars_preserved=len(tail),
            path=path,
            source="matrx_ai.providers.snapshot_redactors",
        )
        return f"{head}\n{_fmt_marker(**fields)}\n{tail}"


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def apply_redactors(
    value: Any,
    redactors: list[Redactor],
    *,
    path: str = "$",
) -> Any:
    """Walk a JSON-safe tree and apply each redactor to every leaf.

    Structure preservation is enforced by the walker itself:
      - dict keys are copied verbatim in original order
      - list items are copied verbatim in original order
      - only *leaf* values are offered to redactors
      - redactors receive the full JSON-path of the value they're inspecting

    Redactors run in registration order. Each redactor sees the value after
    any earlier redactor has transformed it. In practice we design redactors
    to be independent, but the pipeline ordering is explicit and stable so
    future composition is predictable.

    Parameters
    ----------
    value : Any
        A JSON-safe Python value (dict / list / str / int / float / bool /
        None). Non-JSON-safe values should have already been coerced by
        ``_json_safe`` upstream; this function does not coerce types.
    redactors : list[Redactor]
        Explicitly ordered list of redactors to apply. An empty list is a
        no-op copy of the input.
    path : str
        JSON-path of ``value`` relative to the document root. Defaults to
        "$" for the root invocation. Redactors see this path in their marker
        output.

    Returns
    -------
    Any
        A new value tree with the same shape, keys, order, and types as the
        input, with leaf strings possibly replaced via the configured
        redactors. Dicts and lists are fresh instances; unchanged leaves are
        returned by identity.
    """
    if isinstance(value, dict):
        return {k: _apply_leaf(v, redactors, f"{path}.{k}", value) for k, v in value.items()}
    if isinstance(value, list):
        return [
            apply_redactors(item, redactors, path=f"{path}[{i}]")
            for i, item in enumerate(value)
        ]
    return _apply_leaf(value, redactors, path, None)


def _apply_leaf(
    value: Any, redactors: list[Redactor], path: str, siblings: dict[str, Any] | None
) -> Any:
    """Offer one leaf to each redactor, with the dict it sits in (for references)."""
    if isinstance(value, (dict, list)):
        return apply_redactors(value, redactors, path=path)
    out = value
    for r in redactors:
        if r.applies_to(out, path, siblings):
            out = r.redact(out, path, siblings)
    return out


# ---------------------------------------------------------------------------
# Default pipeline
# ---------------------------------------------------------------------------
# Owner ruling 2026-10-05: text is never cut; only inline file data is replaced,
# by a marker carrying the file reference (see LargeBinaryStringRedactor).
# The single source of truth for what the snapshot system is allowed to
# modify. Changing this list is a deliberate act — not a quiet one-liner
# tucked into an unrelated PR.

DEFAULT_SNAPSHOT_REDACTORS: list[Redactor] = [
    LargeBinaryStringRedactor(max_bytes=65536, head_chars=128, tail_chars=128),
]


# ---------------------------------------------------------------------------
# The AI's answer is recorded IN FULL (decision 2026-09-14, KI-049)
# ---------------------------------------------------------------------------
# DECISION. A platform that records AI calls keeps what the AI said. The blob
# redactor above exists to stop multi-MB inline files saturating the write
# pool; it was never meant to shorten an answer. But it walked EVERY leaf, so a
# ~73 KB structured answer (the SEO keyword classifier's) was stored as 128
# chars + marker + 128 chars — live, 78 of 415 Run history outputs in the 30
# days to 2026-09-14 — and the rest of what the model said was gone.
#
# RULE. In the RESPONSE payload, an assistant message's ``type="text"`` block
# keeps its ``text`` verbatim. Everything else still goes through the pipeline:
# every other key of that block, every other block type (``image.base64_data``,
# ``tool_call.arguments``, ``thinking``), user/system messages, ``raw_response``,
# and the request/unified payloads. A ``text`` that is itself an encoded blob
# (base64 alphabet only, or a ``data:…;base64,`` URL) is still redacted — base64
# does not become safe by arriving inside assistant content.
#
# BOUND. There is no size at which the answer is cut. Above the knob
# ``agents.request_snapshot.assistant_text_announce_bytes`` (start 4 MiB,
# review due 2026-12-14) it is STILL stored in full and the writer logs a
# warning naming the size — loud, never a silent truncation.
#
# Guard: packages/matrx-ai/tests/test_request_snapshot_assistant_text_full.py.

KNOB_FEATURE = "agents.request_snapshot"
ASSISTANT_TEXT_ANNOUNCE_BYTES_KEY = "assistant_text_announce_bytes"
#: KNOB MIRROR of platform.feature_knob "agents.request_snapshot" "assistant_text_announce_bytes"
ASSISTANT_TEXT_ANNOUNCE_BYTES_MIRROR = 4_194_304

_knob_reader: Callable[[str], Any] | None = None
_knob_announced = False


def configure_snapshot_knobs(reader: Callable[[str], Any] | None) -> None:
    """Bind the host's reader (``key -> value`` for feature ``agents.request_snapshot``).
    ``None`` unbinds it, restoring the standalone posture."""
    global _knob_reader, _knob_announced
    _knob_reader = reader
    _knob_announced = False


def assistant_text_announce_bytes() -> int:
    """The live announce threshold, or the declared mirror when no host is bound
    or the read fails (announced once — a knob read never breaks a snapshot)."""
    global _knob_announced
    raw: Any = ASSISTANT_TEXT_ANNOUNCE_BYTES_MIRROR
    if _knob_reader is None:
        if not _knob_announced:
            _knob_announced = True
            logger.warning(
                "[matrx_ai] no host knob reader bound for %r; using the mirrored "
                "%s=%d (bind one with configure_snapshot_knobs())",
                KNOB_FEATURE, ASSISTANT_TEXT_ANNOUNCE_BYTES_KEY, ASSISTANT_TEXT_ANNOUNCE_BYTES_MIRROR,
            )
    else:
        try:
            raw = _knob_reader(ASSISTANT_TEXT_ANNOUNCE_BYTES_KEY)
        except Exception as exc:  # noqa: BLE001 — announced, never a crashed snapshot
            if not _knob_announced:
                _knob_announced = True
                logger.warning(
                    "[matrx_ai] knob read failed for %r.%r: %r; using the mirrored %d",
                    KNOB_FEATURE, ASSISTANT_TEXT_ANNOUNCE_BYTES_KEY, exc,
                    ASSISTANT_TEXT_ANNOUNCE_BYTES_MIRROR,
                )
    try:
        value = int(str(raw).strip().strip('"'))
    except (TypeError, ValueError):
        return ASSISTANT_TEXT_ANNOUNCE_BYTES_MIRROR
    return value if value > 0 else ASSISTANT_TEXT_ANNOUNCE_BYTES_MIRROR


_BASE64_ONLY = re.compile(r"[A-Za-z0-9+/=_\-\r\n]+")


def looks_like_encoded_blob(value: str) -> bool:
    """True for a string that is an encoded file rather than language: a
    ``data:…;base64,`` URL, or a run made only of the base64 alphabet. Prose and
    JSON always carry spaces, quotes or braces, so an answer never matches."""
    head = value.lstrip()[:8192]
    if not head:
        return False
    if head.startswith("data:") and ";base64," in head[:512]:
        return True
    return _BASE64_ONLY.fullmatch(head) is not None


def _keep_assistant_text(block: Any) -> bool:
    return (
        isinstance(block, dict)
        and block.get("type") == "text"
        and isinstance(block.get("text"), str)
        and not looks_like_encoded_blob(block["text"])
    )


def _announce_if_huge(text: str, path: str) -> None:
    if len(text) <= 65536:  # cheap pre-check: bytes >= chars
        return
    size = len(text.encode("utf-8", errors="replace"))
    ceiling = assistant_text_announce_bytes()
    if size > ceiling:
        logger.warning(
            "[matrx_ai] request snapshot: assistant answer at %s is %d bytes, over "
            "%s.assistant_text_announce_bytes=%d — stored IN FULL (answers are never "
            "truncated); raise the knob if answers this size are normal",
            path, size, KNOB_FEATURE, ceiling,
        )


def _redact_assistant_block(block: Any, redactors: list[Redactor], path: str) -> Any:
    if not _keep_assistant_text(block):
        return apply_redactors(block, redactors, path=path)
    out: dict[str, Any] = {}
    for key, val in block.items():
        key_path = f"{path}.{key}"
        if key == "text":
            _announce_if_huge(val, key_path)
            out[key] = val
        else:
            out[key] = apply_redactors(val, redactors, path=key_path)
    return out


def _redact_response_message(message: Any, redactors: list[Redactor], path: str) -> Any:
    if not (
        isinstance(message, dict)
        and message.get("role") == "assistant"
        and isinstance(message.get("content"), list)
    ):
        return apply_redactors(message, redactors, path=path)
    out: dict[str, Any] = {}
    for key, val in message.items():
        key_path = f"{path}.{key}"
        if key == "content":
            out[key] = [
                _redact_assistant_block(block, redactors, f"{key_path}[{i}]")
                for i, block in enumerate(val)
            ]
        else:
            out[key] = apply_redactors(val, redactors, path=key_path)
    return out


def apply_response_redactors(
    response: Any,
    redactors: list[Redactor],
    *,
    path: str = "$",
) -> Any:
    """``apply_redactors`` for the RESPONSE payload, keeping the assistant's
    answer text verbatim (see the decision block above). Same structure
    guarantees: keys, order and types are preserved; only leaves change."""
    if not isinstance(response, dict):
        return apply_redactors(response, redactors, path=path)
    out: dict[str, Any] = {}
    for key, val in response.items():
        key_path = f"{path}.{key}"
        if key == "messages" and isinstance(val, list):
            out[key] = [
                _redact_response_message(message, redactors, f"{key_path}[{i}]")
                for i, message in enumerate(val)
            ]
        else:
            out[key] = apply_redactors(val, redactors, path=key_path)
    return out


# ---------------------------------------------------------------------------
# Blob store seam — every replaced blob stays recoverable
# ---------------------------------------------------------------------------
# Arman ruled (2026-10-05): large files are stored BY FILE REFERENCE. A blob the
# request does not already name by file_id/url (raw base64 a caller pasted, or
# bytes a tool produced) is saved ONCE through a host-injected store and the
# redaction marker carries the new file_id. matrx-ai never picks the storage,
# the owner or the organization — the host does (aidream wires matrx-files in
# aidream/package_integration.py). A failed save NEVER perturbs the request:
# it is reported through ``on_error`` and the marker keeps the sha256-only form.

#: ``async (raw_bytes, mime, sha256_hex, *, user_id, organization_id) -> file_id``
SnapshotBlobStore = Callable[..., Awaitable[str]]

_blob_store: SnapshotBlobStore | None = None


def configure_snapshot_blob_store(store: SnapshotBlobStore | None) -> None:
    """Bind the host's blob saver. ``None`` unbinds it (sha256-only markers)."""
    global _blob_store
    _blob_store = store


def get_snapshot_blob_store() -> SnapshotBlobStore | None:
    return _blob_store


def _decode_b64(payload: str) -> bytes:
    pad = "=" * (-len(payload) % 4)
    try:
        return base64.b64decode(payload + pad, altchars=b"-_" if ("-" in payload or "_" in payload) else None)
    except (binascii.Error, ValueError):
        return b""


async def redactors_with_stored_blobs(
    tree: Any,
    *,
    user_id: str | None = None,
    organization_id: str | None = None,
    on_error: Callable[[BaseException, dict[str, Any]], Awaitable[None]] | None = None,
    store: SnapshotBlobStore | None = None,
) -> list[Redactor]:
    """The default redactors, with every unreferenced blob in ``tree`` saved first.

    Walks ``tree`` (the same walk ``apply_redactors`` does), and for each inline
    blob the redactor will replace and that names no file, decodes it and awaits
    the host store ``(bytes, mime, sha256) -> file_id``. Equal bytes are saved
    once per call. Never raises; returns the stock list when no store is bound.
    """
    store = store or _blob_store
    if store is None:
        return DEFAULT_SNAPSHOT_REDACTORS
    base = next((r for r in DEFAULT_SNAPSHOT_REDACTORS if isinstance(r, LargeBinaryStringRedactor)), None)
    if base is None:
        return DEFAULT_SNAPSHOT_REDACTORS
    refs: dict[str, tuple[str, str]] = {}
    by_sha: dict[str, str] = {}

    async def _visit(value: Any, path: str, siblings: dict[str, Any] | None) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                await _visit(v, f"{path}.{k}", value)
            return
        if isinstance(value, list):
            for i, item in enumerate(value):
                await _visit(item, f"{path}[{i}]", None)
            return
        found = base._classify(value, path)
        if found is None or sibling_file_refs(siblings, value):
            return
        mime, payload = found
        try:
            raw = _decode_b64(payload)
            if not raw:
                return
            sha = hashlib.sha256(raw).hexdigest()
            if sha not in by_sha:
                mime = mime or _sniff_mime(payload) or next(
                    (siblings[k] for k in _MIME_KEYS if siblings and isinstance(siblings.get(k), str)), ""
                )
                by_sha[sha] = await store(
                    raw, mime or "application/octet-stream", sha,
                    user_id=user_id, organization_id=organization_id,
                )
            refs[path] = (by_sha[sha], sha)
        except Exception as exc:  # noqa: BLE001 — a failed save never perturbs the request
            logger.warning("[matrx_ai] snapshot blob store failed at %s: %r", path, exc)
            if on_error is not None:
                try:
                    await on_error(exc, {"path": path, "stage": "snapshot_blob_store"})
                except Exception:  # noqa: BLE001
                    pass

    await _visit(tree, "$", None)
    if not refs:
        return DEFAULT_SNAPSHOT_REDACTORS
    out: list[Redactor] = [
        LargeBinaryStringRedactor(
            max_bytes=base.max_bytes, head_chars=base.head_chars, tail_chars=base.tail_chars,
            stored_refs=refs,
        )
    ]
    return out

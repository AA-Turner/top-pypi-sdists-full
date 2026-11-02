"""Reversible redaction — mask with mapping + restore on return path.

**Encryption model — caller-held per-session keys**:
  * mask_with_mapping generates a FRESH AES-256-GCM key per session.
  * The key is returned to the caller in the MaskResult — ONCE.
  * Each mapping record carries its own ciphertext + nonce.
  * The store NEVER sees plaintext. The DB has no system-wide secret.
  * To restore, the caller passes session_id + the key back.

If the caller loses the key, the originals are gone. That's intentional —
it means a server-side compromise yields zero plaintext, and the caller
controls the cryptographic boundary completely.

Two non-reversible modes are also supported:
  - destructive: same as the legacy engine but produces no mapping rows.
  - annotation: detect spans, persist mapping rows for audit, but DO NOT
    modify the file — useful when the user just wants to flag risks.
"""

from __future__ import annotations

import base64
import os
import re
import uuid
from typing import Any, Literal

from pydantic import BaseModel, Field

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from .engine import _apply_redact_annots
from .mapping_store import MappingRecord, MappingStoreProtocol
from .models import RedactionRegion
from .substitutes import format_substitute


Mode = Literal["reversible", "destructive", "annotation"]

CIPHER_ID = "aes-256-gcm-v1"


class RedactionCandidate(BaseModel):
    """A single span discovered by the pattern_candidates detector."""

    pattern_id: str
    category: str = "pii"
    page_number: int = Field(ge=1)
    bbox: dict[str, float]
    char_start: int = 0
    char_end: int = 0
    original_text: str
    """REQUIRED for reversible / annotation modes. The caller never sees it
    again after this call — it's encrypted at rest with the session key."""
    confidence_tier: str = "n/a"


class MaskResult(BaseModel):
    file_bytes: bytes = Field(repr=False)
    session_id: str
    mode: Mode
    mapping_count: int
    session_key_b64: str | None = None
    """Base64-encoded AES-256-GCM key. SET ONLY when mode in
    ('reversible','annotation'). Caller MUST store this somewhere safe — it
    is returned exactly once and never persisted server-side. None for
    destructive mode (no key needed)."""
    notes: list[str] = Field(default_factory=list)


# ── AES-GCM helpers ──────────────────────────────────────────────────────────

def _new_session_key() -> bytes:
    """Generate a fresh 256-bit key."""
    return os.urandom(32)


def _new_nonce() -> bytes:
    """Generate a fresh 96-bit nonce. AES-GCM requires uniqueness per (key, nonce)."""
    return os.urandom(12)


def _aesgcm_encrypt(key: bytes, plaintext: str) -> tuple[bytes, bytes]:
    """Returns (ciphertext_with_tag, nonce). Imports cryptography lazily."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aes = AESGCM(key)
    nonce = _new_nonce()
    ct = aes.encrypt(nonce, plaintext.encode("utf-8"), associated_data=None)
    return ct, nonce


def _aesgcm_decrypt(key: bytes, ciphertext: bytes, nonce: bytes) -> str:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aes = AESGCM(key)
    pt = aes.decrypt(nonce, ciphertext, associated_data=None)
    return pt.decode("utf-8")


def _bbox_to_region(bbox: dict[str, float], page_number: int) -> RedactionRegion:
    return RedactionRegion(
        page_number=page_number,
        x0=float(bbox["x0"]),
        y0=float(bbox["y0"]),
        x1=float(bbox["x1"]),
        y1=float(bbox["y1"]),
        replacement="BLOCK",
    )


async def mask_with_mapping(
    pdf_bytes: bytes,
    spans: list[RedactionCandidate],
    *,
    file_id: str,
    redacted_by: str,
    mapping_store: MappingStoreProtocol,
    mode: Mode = "reversible",
    substitute_style: str = "bracket",
    substitute_formats: dict[str, str] | None = None,
    session_id: str | None = None,
    session_key_b64: str | None = None,
) -> MaskResult:
    """Apply masking + persist mappings (encrypted client-side).

    session_key_b64 is OPTIONAL. When omitted, a fresh AES-256-GCM key is
    generated and returned in the result. When provided (e.g. appending to
    an existing session), the same key is reused so the existing records
    remain decryptable.
    """
    if not spans:
        return MaskResult(
            file_bytes=pdf_bytes,
            session_id=session_id or "",
            mode=mode,
            mapping_count=0,
            notes=["no spans"],
        )

    if session_id is None:
        session_id = await mapping_store.begin_session(
            file_id=file_id, redacted_by=redacted_by, mode=mode,
        )

    # Key management: generate fresh OR reuse caller-supplied.
    session_key: bytes | None = None
    if mode in ("reversible", "annotation"):
        if session_key_b64:
            session_key = base64.b64decode(session_key_b64)
            if len(session_key) != 32:
                raise ValueError("session_key_b64 must decode to 32 bytes (AES-256)")
        else:
            session_key = _new_session_key()

    formats = substitute_formats or {}
    per_pattern_counters: dict[str, int] = {}
    records: list[MappingRecord] = []
    regions: list[RedactionRegion] = []

    for span in spans:
        pid = span.pattern_id
        per_pattern_counters[pid] = per_pattern_counters.get(pid, 0) + 1
        idx = per_pattern_counters[pid]
        template = formats.get(pid)
        substitute = format_substitute(
            pid, idx, template=template, style=substitute_style,
        )
        span_id = f"{pid}-{idx:04d}"

        # Encrypt the original. None for destructive mode.
        ciphertext: bytes | None = None
        nonce: bytes | None = None
        if mode != "destructive" and session_key is not None:
            ciphertext, nonce = _aesgcm_encrypt(session_key, span.original_text)

        records.append(MappingRecord(
            file_id=file_id,
            redacted_by=redacted_by,
            session_id=session_id,
            span_id=span_id,
            detector_kind="redaction_candidates",
            detector_version="v1",
            pattern_id=pid,
            confidence_tier=span.confidence_tier,
            mode=mode,
            ciphertext=ciphertext,
            nonce=nonce,
            cipher=CIPHER_ID,
            substitute_value=substitute,
            location={
                "page": span.page_number,
                "bbox": span.bbox,
                "char_start": span.char_start,
                "char_end": span.char_end,
            },
        ))
        if mode != "annotation":
            region = _bbox_to_region(span.bbox, span.page_number)
            region.text = substitute if mode == "reversible" else ""
            regions.append(region)

    if mode in ("reversible", "annotation"):
        await mapping_store.persist_records(records)

    if mode == "annotation":
        return MaskResult(
            file_bytes=pdf_bytes,
            session_id=session_id,
            mode=mode,
            mapping_count=len(records),
            session_key_b64=base64.b64encode(session_key).decode("ascii") if session_key else None,
            notes=["annotation mode — file returned unchanged"],
        )

    def _apply_sync() -> bytes:
        pymupdf = load_pymupdf()
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
            _apply_redact_annots(doc, regions)
            return doc.tobytes(garbage=4, deflate=True, clean=True)

    out_bytes = await run_in_cpu_executor(_apply_sync)
    return MaskResult(
        file_bytes=out_bytes,
        session_id=session_id,
        mode=mode,
        mapping_count=len(records),
        session_key_b64=base64.b64encode(session_key).decode("ascii") if session_key else None,
    )


# ── restore on return path ───────────────────────────────────────────────────

# Match anything that looks like our default bracket substitute, e.g. [SSN_001].
_BRACKET_RE = re.compile(r"\[[A-Z][A-Z0-9_]*_\d{3,}\]")


async def restore_text_from_response(
    text: str,
    *,
    session_id: str,
    session_key_b64: str,
    mapping_store: MappingStoreProtocol,
    extra_patterns: list[str] | None = None,
) -> str:
    """Decrypt + swap substitute markers back to originals.

    Requires the caller-held per-session key (base64). Without it, decryption
    fails and the substitutes pass through unchanged.

    Never raises — partial restoration is safe by design.
    """
    if not text or not session_key_b64:
        return text

    try:
        key = base64.b64decode(session_key_b64)
        if len(key) != 32:
            return text
    except Exception:
        return text

    records = await mapping_store.fetch_session_records(session_id=session_id)
    if not records:
        return text

    # Build substitute → original map by decrypting each record.
    sub_map: dict[str, str] = {}
    for rec in records:
        if rec.mode == "destructive":
            continue
        if rec.ciphertext is None or rec.nonce is None:
            continue
        try:
            original = _aesgcm_decrypt(key, rec.ciphertext, rec.nonce)
        except Exception:
            # Wrong key or corrupted record — skip.
            continue
        sub_map[rec.substitute_value] = original

    if not sub_map:
        return text

    patterns = [_BRACKET_RE]
    for p in extra_patterns or []:
        try:
            patterns.append(re.compile(p))
        except re.error:
            pass

    found: set[str] = set()
    for pat in patterns:
        for m in pat.finditer(text):
            found.add(m.group(0))

    out = text
    for sub in found:
        original = sub_map.get(sub)
        if original is not None:
            out = out.replace(sub, original)
    return out


__all__ = [
    "Mode",
    "CIPHER_ID",
    "RedactionCandidate",
    "MaskResult",
    "mask_with_mapping",
    "restore_text_from_response",
]

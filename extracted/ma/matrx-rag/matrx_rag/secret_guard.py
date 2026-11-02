"""The RAG side of the platform secret guard.

2026-09-13 incident: ``knowledge_search`` returned, as its TOP hit, a chunk of
a user note that was a raw ``.env`` dump — the snippet handed to the agent
carried live values for ``ADMIN_API_TOKEN`` and several provider keys. The
pipeline had no content-level secret detection anywhere: whatever a resolver
produced was chunked, embedded and stored verbatim, and from then on every
agent holding ``knowledge_search`` could read platform credentials.

The rule this module enforces: **nothing secret-shaped is ever written to a
stored chunk row or sent to an embedding provider.** Redaction happens at two
seams, and because :func:`matrx_utils.redact_secrets` is idempotent, running
both is free and the second one finding zero is evidence the first worked:

1. :func:`matrx_rag.sources.resolve` — the single door every source kind
   (note, cld_file, code_file, repository, transcript, scraped, task,
   project, cx_message, research, library_doc) comes through.
2. :func:`matrx_rag.chunking.chunk_text` / ``chunk_code`` — the last seam
   before a value can become a stored row, covering the callers that build a
   ``ResolvedSource`` themselves (PDF and image pipelines, the ``rag.*``
   workflow actions).

Ingestion is NEVER blocked — a note full of credentials still gets indexed,
minus the credentials, because refusing to index would be a silent, confusing
data loss for the user. But it never happens quietly either: every redaction
raises a WARNING naming the source and the credential NAMES (never values),
and the count rides the run collector into the host's per-run ledger row.
"""

from __future__ import annotations

import logging

from matrx_utils.secret_detection import find_secrets, redact_secrets, secret_name_classes

from matrx_rag._observability import record_secret_redaction

logger = logging.getLogger("matrx_rag.secret_guard")

__all__ = ["guard_text", "secrets_metadata"]


def guard_text(
    text: str,
    *,
    source_kind: str | None = None,
    source_id: str | None = None,
    where: str = "ingest",
) -> tuple[str, int, list[str]]:
    """Redact secret values out of ``text`` before it can be stored.

    Returns ``(clean_text, count, names)``. ``names`` are credential NAMES and
    detector classes only — a value never leaves this function. Never raises:
    a detector bug must not be able to stop ingestion.
    """
    if not text:
        return text, 0, []
    try:
        findings = find_secrets(text)
        if not findings:
            return text, 0, []
        clean, count = redact_secrets(text)
        names = sorted(secret_name_classes(findings))
        logger.warning(
            "SECRET GUARD: redacted %d secret value(s) from %s %s before indexing "
            "at seam=%s. Names/classes found: %s. The values were NOT stored and "
            "were NOT sent to the embedding provider. The original record is "
            "untouched — its owner should rotate these credentials and remove "
            "them from the source.",
            count,
            source_kind or "source",
            source_id or "(unidentified)",
            where,
            ", ".join(names),
        )
        record_secret_redaction(count=count, names=names)
        return clean, count, names
    except Exception:  # noqa: BLE001 — the guard must never break ingest
        logger.exception(
            "SECRET GUARD FAILED on %s %s at seam=%s — text was passed through "
            "UNREDACTED. Treat this as a live leak path.",
            source_kind or "source",
            source_id or "(unidentified)",
            where,
        )
        return text, 0, []


def secrets_metadata(count: int, names: list[str]) -> dict[str, object]:
    """The metadata stamp a source/chunk row carries after a guard pass."""
    if count <= 0:
        return {}
    return {"secrets_redacted": count, "secret_names": names}

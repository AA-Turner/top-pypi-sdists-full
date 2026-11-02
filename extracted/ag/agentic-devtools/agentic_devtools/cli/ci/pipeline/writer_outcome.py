"""Classify writer delivery from commit identities and caller-supplied evidence."""

from __future__ import annotations

import re
from collections.abc import Iterable
from enum import StrEnum


class WriterOutcome(StrEnum):
    """Outcome of a completed writer session."""

    PUSHED_WITH_EVIDENCE = "PUSHED_WITH_EVIDENCE"
    PUSHED_WITHOUT_EVIDENCE = "PUSHED_WITHOUT_EVIDENCE"
    NO_PUSH = "NO_PUSH"
    UNKNOWN = "UNKNOWN"


def classify_writer_outcome(
    *,
    dispatch_head_sha: str,
    current_head_sha: str,
    session_finished: bool,
    evidence_head_shas: Iterable[str],
) -> WriterOutcome:
    """Classify a finished writer without authenticating evidence provenance."""
    evidence = list(evidence_head_shas)
    supplied_shas = [dispatch_head_sha, current_head_sha, *evidence]
    valid_shas = [re.fullmatch(r"[0-9A-Fa-f]{40}", sha) is not None for sha in supplied_shas]
    normalized_shas = [sha.lower() for sha in supplied_shas]
    if not session_finished or not all(valid_shas):
        return WriterOutcome.UNKNOWN
    dispatch_head, current_head, *normalized_evidence = normalized_shas
    if dispatch_head == current_head:
        return WriterOutcome.NO_PUSH
    if current_head in normalized_evidence:
        return WriterOutcome.PUSHED_WITH_EVIDENCE
    return WriterOutcome.PUSHED_WITHOUT_EVIDENCE

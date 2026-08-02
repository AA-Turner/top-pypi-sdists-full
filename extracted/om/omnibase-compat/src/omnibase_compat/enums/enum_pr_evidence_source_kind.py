# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: OMN-14223 — operator-designated canonical home for the
#   OCC stamp schema (placement correction to OMN-14180); not a migration shim.

"""Kind discriminator for a PR OCC evidence source (OMN-14187).

An ``Evidence-Source:`` line in a PR body references either an open OCC PR by
number (``OCC#<n>``) or a merged commit by SHA (a 7-40 char hex string). This
enum captures that binary distinction as the typed discriminator for
``ModelPrEvidenceSource``, replacing the ad-hoc regex branching in
``validator_receipt_gate.py`` (``EVIDENCE_SOURCE_OCC_PR_PATTERN`` vs
``EVIDENCE_SOURCE_SHA_PATTERN``).

Relocated from ``omnibase_core.enums`` to ``omnibase_compat`` under OMN-14223 so
the canonical OCC stamp schema lives in the lowest shared layer (operator
placement correction to OMN-14180).
"""

from __future__ import annotations

from enum import StrEnum


class EnumPrEvidenceSourceKind(StrEnum):
    """Whether a PR evidence source points at an OCC PR or a merged commit."""

    OCC_PR = "occ_pr"
    COMMIT_SHA = "commit_sha"


__all__ = ["EnumPrEvidenceSourceKind"]

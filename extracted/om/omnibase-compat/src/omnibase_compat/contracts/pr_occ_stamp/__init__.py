# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Canonical PR OCC metadata-stamp schema (parent epic OMN-14180).

The single typed vocabulary — models, discriminator enum, and the
deterministic parser/renderer — for the ``Evidence-Source:`` /
``Evidence-Ticket:`` / ``[skip-<gate>:]`` metadata that the receipt-gate and the
omnimarket OCC autobind effect both operate over.

Relocated here from ``omnibase_core`` under OMN-14223 so the schema lives in the
lowest shared layer (``omnibase_compat``), letting every downstream repo consume
one canonical definition (operator placement correction to OMN-14180).
"""

from omnibase_compat.contracts.pr_occ_stamp.model_pr_body_section import (
    ModelPrBodySection,
)
from omnibase_compat.contracts.pr_occ_stamp.model_pr_evidence_source import (
    ModelPrEvidenceSource,
)
from omnibase_compat.contracts.pr_occ_stamp.model_pr_occ_metadata_stamp import (
    ModelPrOccMetadataStamp,
)
from omnibase_compat.contracts.pr_occ_stamp.model_pr_receipt_gate_skip_token import (
    ModelPrReceiptGateSkipToken,
)
from omnibase_compat.contracts.pr_occ_stamp.pr_occ_metadata_stamp import (
    parse_pr_occ_metadata_stamp,
    render_pr_occ_metadata_stamp,
)
from omnibase_compat.enums.enum_pr_evidence_source_kind import EnumPrEvidenceSourceKind

__all__: list[str] = [
    "EnumPrEvidenceSourceKind",
    "ModelPrBodySection",
    "ModelPrEvidenceSource",
    "ModelPrOccMetadataStamp",
    "ModelPrReceiptGateSkipToken",
    "parse_pr_occ_metadata_stamp",
    "render_pr_occ_metadata_stamp",
]

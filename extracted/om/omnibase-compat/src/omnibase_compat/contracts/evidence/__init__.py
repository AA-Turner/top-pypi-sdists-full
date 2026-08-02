# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Temporary evidence contract DTOs for OCC contract storage migration."""

from omnibase_compat.contracts.evidence.model_contract_evidence_proof import (
    ModelContractEvidenceProof,
)
from omnibase_compat.contracts.evidence.model_contract_evidence_spec import (
    ModelContractEvidenceSpec,
)
from omnibase_compat.contracts.evidence.model_evidence_provenance import (
    ModelEvidenceProvenance,
)

__all__: list[str] = [
    "ModelContractEvidenceProof",
    "ModelContractEvidenceSpec",
    "ModelEvidenceProvenance",
]

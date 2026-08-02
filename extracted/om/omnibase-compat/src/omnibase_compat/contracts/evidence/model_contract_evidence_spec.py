# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# COMPAT_MIGRATION_TARGET: omnibase_core.models.contracts.evidence.model_contract_evidence_spec
# COMPAT_REMOVAL_DATE: 2026-10-01

"""ModelContractEvidenceSpec — typed contract evidence storage format."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from omnibase_compat.contracts.evidence.model_contract_evidence_proof import (
    ModelContractEvidenceProof,
)
from omnibase_compat.contracts.evidence.model_evidence_provenance import (
    ModelEvidenceProvenance,
)

_TICKET_ID_RE = re.compile(r"^[A-Z]+-\d+$")


class ModelContractEvidenceSpec(BaseModel):
    """Typed artifact-first replacement for PR-number-bound evidence checks.

    This is a temporary compat model. It lets OCC author new contracts in a
    typed shape while `omnibase_core` becomes the canonical home.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal["1.0.0"] = "1.0.0"
    ticket_id: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    artifact_names: tuple[str, ...] = Field(..., min_length=1)
    repository_surfaces: tuple[str, ...] = Field(..., min_length=1)
    acceptance_criteria: tuple[str, ...] = Field(..., min_length=1)
    stable_proofs: tuple[ModelContractEvidenceProof, ...] = Field(..., min_length=1)
    provenance: tuple[ModelEvidenceProvenance, ...] = Field(default_factory=tuple)
    legacy_contract_path: str | None = Field(default=None, min_length=1)
    migration_ticket_id: str | None = Field(default=None, min_length=1)

    @field_validator("ticket_id", "migration_ticket_id")
    @classmethod
    def _validate_ticket_id(cls, value: str | None) -> str | None:
        if value is not None and not _TICKET_ID_RE.match(value):
            raise ValueError("ticket id must look like OMN-1234")
        return value


__all__: list[str] = ["ModelContractEvidenceSpec"]

from __future__ import annotations
from pydantic import Field
from typing import List
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.schemas.medical_role import MaleoMetadataMedicalRoleSchemas

class MedicalRoleTransfers(
    MaleoMetadataMedicalRoleSchemas.OptionalParentId,
    MaleoMetadataMedicalRoleSchemas.Name,
    MaleoMetadataMedicalRoleSchemas.Key,
    MaleoMetadataMedicalRoleSchemas.Code,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass

class StructuredMedicalRoleTransfers(MedicalRoleTransfers):
    specializations:List["StructuredMedicalRoleTransfers"] = Field(..., description="Role specializations")

# this is required for forward reference resolution
StructuredMedicalRoleTransfers.model_rebuild()
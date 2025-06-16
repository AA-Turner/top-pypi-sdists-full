from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_metadata.enums.medical_role import MaleoMetadataMedicalRoleEnums

class MaleoMetadataMedicalRoleGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralParametersTransfers.GetSingleQuery): pass

    class GetSingle(BaseGeneralParametersTransfers.GetSingle):
        identifier:MaleoMetadataMedicalRoleEnums.IdentifierType = Field(..., description="Identifier")
from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums

class MaleoMetadataSystemRoleGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralParametersTransfers.GetSingleQuery): pass

    class GetSingle(BaseGeneralParametersTransfers.GetSingle):
        identifier:MaleoMetadataSystemRoleEnums.IdentifierType = Field(..., description="Identifier")
from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_metadata.enums.user_type import MaleoMetadataUserTypeEnums

class MaleoMetadataUserTypeGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralParametersTransfers.GetSingleQuery): pass

    class GetSingle(BaseGeneralParametersTransfers.GetSingle):
        identifier:MaleoMetadataUserTypeEnums.IdentifierType = Field(..., description="Identifier")
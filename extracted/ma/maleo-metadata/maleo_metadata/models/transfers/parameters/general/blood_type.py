from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_metadata.enums.blood_type import MaleoMetadataBloodTypeEnums

class MaleoMetadataBloodTypeGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralParametersTransfers.GetSingleQuery): pass

    class GetSingle(BaseGeneralParametersTransfers.GetSingle):
        identifier:MaleoMetadataBloodTypeEnums.IdentifierType = Field(..., description="Identifier")
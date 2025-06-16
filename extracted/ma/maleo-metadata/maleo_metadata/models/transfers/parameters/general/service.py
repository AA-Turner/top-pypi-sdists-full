from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_metadata.enums.service import MaleoMetadataServiceEnums

class MaleoMetadataServiceGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralParametersTransfers.GetSingleQuery): pass

    class GetSingle(BaseGeneralParametersTransfers.GetSingle):
        identifier:MaleoMetadataServiceEnums.IdentifierType = Field(..., description="Identifier")
from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums

class MaleoMetadataOrganizationTypeGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralParametersTransfers.GetSingleQuery): pass

    class GetSingle(BaseGeneralParametersTransfers.GetSingle):
        identifier:MaleoMetadataOrganizationTypeEnums.IdentifierType = Field(..., description="Identifier")
from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums
from maleo_metadata.models.transfers.general.organization_type import OrganizationTypeTransfers

class MaleoMetadataOrganizationTypeResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "MDT-OGT-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoMetadataOrganizationTypeEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "MDT-OGT-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "MDT-OGT-003"
        message:str = "Organization type found"
        description:str = "Requested organization type found in database"
        data:OrganizationTypeTransfers = Field(..., description="Organization type")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "MDT-OGT-004"
        message:str = "Organization types found"
        description:str = "Requested organization types found in database"
        data:list[OrganizationTypeTransfers] = Field(..., description="Organization types")
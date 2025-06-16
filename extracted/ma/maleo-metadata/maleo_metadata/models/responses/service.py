from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_metadata.enums.service import MaleoMetadataServiceEnums
from maleo_metadata.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "MDT-SRV-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoMetadataServiceEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "MDT-SRV-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "MDT-SRV-003"
        message:str = "Service found"
        description:str = "Requested service found in database"
        data:ServiceTransfers = Field(..., description="Service")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "MDT-SRV-004"
        message:str = "Services found"
        description:str = "Requested services found in database"
        data:list[ServiceTransfers] = Field(..., description="Services")
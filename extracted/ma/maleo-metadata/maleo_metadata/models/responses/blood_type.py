from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_metadata.enums.blood_type import MaleoMetadataBloodTypeEnums
from maleo_metadata.models.transfers.general.blood_type import BloodTypeTransfers

class MaleoMetadataBloodTypeResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "MDT-BLT-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoMetadataBloodTypeEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "MDT-BLT-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "MDT-BLT-003"
        message:str = "Blood type found"
        description:str = "Requested blood type found in database"
        data:BloodTypeTransfers = Field(..., description="Blood type")

    class GetMultiple(BaseResponses.UnpaginatedMultipleData):
        code:str = "MDT-BLT-004"
        message:str = "Blood types found"
        description:str = "Requested blood types found in database"
        data:list[BloodTypeTransfers] = Field(..., description="Blood types")
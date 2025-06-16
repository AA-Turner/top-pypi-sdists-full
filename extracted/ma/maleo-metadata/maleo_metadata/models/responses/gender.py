from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_metadata.enums.gender import MaleoMetadataGenderEnums
from maleo_metadata.models.transfers.general.gender import GenderTransfers

class MaleoMetadataGenderResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "MDT-GND-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoMetadataGenderEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "MDT-GND-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "MDT-GND-003"
        message:str = "Gender found"
        description:str = "Requested gender found in database"
        data:GenderTransfers = Field(..., description="Gender")

    class GetMultiple(BaseResponses.UnpaginatedMultipleData):
        code:str = "MDT-GND-004"
        message:str = "Genders found"
        description:str = "Requested genders found in database"
        data:list[GenderTransfers] = Field(..., description="Genders")
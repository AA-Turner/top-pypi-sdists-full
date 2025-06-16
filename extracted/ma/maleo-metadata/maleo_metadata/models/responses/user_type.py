from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_metadata.enums.user_type import MaleoMetadataUserTypeEnums
from maleo_metadata.models.transfers.general.user_type import UserTypeTransfers

class MaleoMetadataUserTypeResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "MDT-UST-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoMetadataUserTypeEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "MDT-UST-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "MDT-UST-003"
        message:str = "User type found"
        description:str = "Requested user type found in database"
        data:UserTypeTransfers = Field(..., description="User type")

    class GetMultiple(BaseResponses.UnpaginatedMultipleData):
        code:str = "MDT-UST-004"
        message:str = "User types found"
        description:str = "Requested user types found in database"
        data:list[UserTypeTransfers] = Field(..., description="User types")
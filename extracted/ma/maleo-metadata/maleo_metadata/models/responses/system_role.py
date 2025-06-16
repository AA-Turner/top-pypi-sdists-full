from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums
from maleo_metadata.models.transfers.general.system_role import SystemRoleTransfers

class MaleoMetadataSystemRoleResponses:
    class InvalidIdentifierRole(BaseResponses.BadRequest):
        code:str = "MDT-SYR-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier roles: {[f'{e.name} ({e.value})' for e in MaleoMetadataSystemRoleEnums.IdentifierType]}"

    class InvalidValueRole(BaseResponses.BadRequest):
        code:str = "MDT-SYR-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "MDT-SYR-003"
        message:str = "System role found"
        description:str = "Requested system role found in database"
        data:SystemRoleTransfers = Field(..., description="System role")

    class GetMultiple(BaseResponses.UnpaginatedMultipleData):
        code:str = "MDT-SYR-004"
        message:str = "System roles found"
        description:str = "Requested system roles found in database"
        data:list[SystemRoleTransfers] = Field(..., description="System roles")
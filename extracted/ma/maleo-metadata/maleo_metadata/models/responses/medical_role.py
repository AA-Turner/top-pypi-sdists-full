from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_metadata.enums.medical_role import MaleoMetadataMedicalRoleEnums
from maleo_metadata.models.transfers.general.medical_role import MedicalRoleTransfers, StructuredMedicalRoleTransfers

class MaleoMetadataMedicalRoleResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "MDT-MRO-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoMetadataMedicalRoleEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "MDT-MRO-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "MDT-MRO-003"
        message:str = "Medical role found"
        description:str = "Requested medical role found in database"
        data:MedicalRoleTransfers = Field(..., description="Medical role")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "MDT-MRO-004"
        message:str = "Medical roles found"
        description:str = "Requested medical roles found in database"
        data:list[MedicalRoleTransfers] = Field(..., description="Medical roles")

    class GetSingleStructured(BaseResponses.SingleData):
        code:str = "MDT-MRO-005"
        message:str = "Structured medical role found"
        description:str = "Requested structured medical role found in database"
        data:StructuredMedicalRoleTransfers = Field(..., description="Structured medical role")

    class GetStructuredMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "MDT-MRO-006"
        message:str = "Structured medical roles found"
        description:str = "Requested structured medical roles found in database"
        data:list[StructuredMedicalRoleTransfers] = Field(..., description="Structured medical roles")
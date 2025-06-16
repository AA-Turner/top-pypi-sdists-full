from pydantic import BaseModel, Field
from maleo_foundation.types import BaseTypes
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.enums.medical_role import MaleoMetadataMedicalRoleEnums

class MaleoMetadataMedicalRoleSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataMedicalRoleEnums.IdentifierType = Field(..., description="Medical role's identifier type")

    class OptionalParentId(BaseModel):
        parent_id:BaseTypes.OptionalInteger = Field(None, ge=1, description="Optional Parent's ID")

    class OptionalListOfParentIds(BaseModel):
        parent_ids:BaseTypes.OptionalListOfIntegers = Field(None, description="Optional Parent's IDs")

    class Code(BaseGeneralSchemas.Code):
        code:str = Field(..., max_length=20, description="Medical role's code")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=255, description="Medical role's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=255, description="Medical role's name")

    class MedicaRoleId(BaseModel):
        medical_role_id:int = Field(..., ge=1, description="Medical role's ID")
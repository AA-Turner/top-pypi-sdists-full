from pydantic import Field
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.enums.user_type import MaleoMetadataUserTypeEnums

class MaleoMetadataUserTypeSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataUserTypeEnums.IdentifierType = Field(..., description="User Type's identifier type")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=20, description="User Type's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=20, description="User Type's name")
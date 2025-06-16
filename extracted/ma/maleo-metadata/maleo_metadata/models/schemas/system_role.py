from pydantic import Field
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums

class MaleoMetadataSystemRoleSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataSystemRoleEnums.IdentifierType = Field(..., description="System Role's identifier type")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=20, description="System Role's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=20, description="System Role's name")
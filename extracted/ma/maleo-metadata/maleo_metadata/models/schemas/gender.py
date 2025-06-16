from pydantic import Field
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.enums.gender import MaleoMetadataGenderEnums

class MaleoMetadataGenderSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataGenderEnums.IdentifierType = Field(..., description="Gender's identifier type")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=20, description="Gender's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=20, description="Gender's name")
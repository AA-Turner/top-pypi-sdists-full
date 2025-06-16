from pydantic import BaseModel, Field
from maleo_foundation.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.enums.service import MaleoMetadataServiceEnums

class MaleoMetadataServiceSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataServiceEnums.IdentifierType = Field(..., description="Service's identifier type")

    class Type(BaseModel):
        type:BaseEnums.ServiceType = Field(..., description="Service's type")

    class Category(BaseModel):
        category:BaseEnums.ServiceCategory = Field(..., description="Service's category")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=20, description="Service's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=20, description="Service's name")
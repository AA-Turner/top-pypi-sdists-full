from pydantic import Field
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.enums.blood_type import MaleoMetadataBloodTypeEnums

class MaleoMetadataBloodTypeSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataBloodTypeEnums.IdentifierType = Field(..., description="Blood Type's identifier type")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=20, description="Blood Type's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=20, description="Blood Type's name")
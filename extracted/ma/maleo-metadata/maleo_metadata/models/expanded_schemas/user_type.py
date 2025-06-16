from pydantic import BaseModel, Field
from maleo_metadata.types.general.user_type import MaleoMetadataUserTypeGeneralTypes

class MaleoMetadataUserTypeExpandedSchemas:
    class SimpleUserType(BaseModel):
        user_type:MaleoMetadataUserTypeGeneralTypes.SimpleUserType = Field(..., description="User type")

    class OptionalSimpleUserType(BaseModel):
        user_type:MaleoMetadataUserTypeGeneralTypes.OptionalSimpleUserType = Field(None, description="User type")

    class ListOfSimpleUserTypes(BaseModel):
        user_types:MaleoMetadataUserTypeGeneralTypes.ListOfSimpleUserTypes = Field([], description="User types")

    class OptionalListOfSimpleUserTypes(BaseModel):
        user_types:MaleoMetadataUserTypeGeneralTypes.OptionalListOfSimpleUserTypes = Field(None, description="User types")

    class ExpandedUserType(BaseModel):
        user_type_details:MaleoMetadataUserTypeGeneralTypes.ExpandedUserType = Field(..., description="User type's details")

    class OptionalExpandedUserType(BaseModel):
        user_type_details:MaleoMetadataUserTypeGeneralTypes.OptionalExpandedUserType = Field(None, description="User type's details")

    class ListOfExpandedUserTypes(BaseModel):
        user_types_details:MaleoMetadataUserTypeGeneralTypes.ListOfExpandedUserTypes = Field([], description="User types's details")

    class OptionalListOfExpandedUserTypes(BaseModel):
        user_types_details:MaleoMetadataUserTypeGeneralTypes.OptionalListOfExpandedUserTypes = Field(None, description="User types's details")
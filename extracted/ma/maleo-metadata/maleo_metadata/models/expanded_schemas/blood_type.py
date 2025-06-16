from pydantic import BaseModel, Field
from maleo_metadata.types.general.blood_type import MaleoMetadataBloodTypeGeneralTypes

class MaleoMetadataBloodTypeExpandedSchemas:
    class SimpleBloodType(BaseModel):
        blood_type:MaleoMetadataBloodTypeGeneralTypes.SimpleBloodType = Field(..., description="Blood type")

    class OptionalSimpleBloodType(BaseModel):
        blood_type:MaleoMetadataBloodTypeGeneralTypes.OptionalSimpleBloodType = Field(None, description="Blood type")

    class ListOfSimpleBloodTypes(BaseModel):
        blood_types:MaleoMetadataBloodTypeGeneralTypes.ListOfSimpleBloodTypes = Field([], description="Blood types")

    class OptionalListOfSimpleBloodTypes(BaseModel):
        blood_types:MaleoMetadataBloodTypeGeneralTypes.OptionalListOfSimpleBloodTypes = Field(None, description="Blood types")

    class ExpandedBloodType(BaseModel):
        blood_type_details:MaleoMetadataBloodTypeGeneralTypes.ExpandedBloodType = Field(..., description="Blood type's details")

    class OptionalExpandedBloodType(BaseModel):
        blood_type_details:MaleoMetadataBloodTypeGeneralTypes.OptionalExpandedBloodType = Field(None, description="Blood type's details")

    class ListOfExpandedBloodTypes(BaseModel):
        blood_types_details:MaleoMetadataBloodTypeGeneralTypes.ListOfExpandedBloodTypes = Field([], description="Blood types's details")

    class OptionalListOfExpandedBloodTypes(BaseModel):
        blood_types_details:MaleoMetadataBloodTypeGeneralTypes.OptionalListOfExpandedBloodTypes = Field(None, description="Blood types's details")
from pydantic import BaseModel, Field
from maleo_metadata.types.general.gender import MaleoMetadataGenderGeneralTypes

class MaleoMetadataGenderExpandedSchemas:
    class SimpleGender(BaseModel):
        gender:MaleoMetadataGenderGeneralTypes.SimpleGender = Field(..., description="Gender")

    class OptionalSimpleGender(BaseModel):
        gender:MaleoMetadataGenderGeneralTypes.OptionalSimpleGender = Field(None, description="Gender")

    class ListOfSimpleGenders(BaseModel):
        genders:MaleoMetadataGenderGeneralTypes.ListOfSimpleGenders = Field([], description="Genders")

    class OptionalListOfSimpleGenders(BaseModel):
        genders:MaleoMetadataGenderGeneralTypes.OptionalListOfSimpleGenders = Field(None, description="Genders")

    class ExpandedGender(BaseModel):
        gender_details:MaleoMetadataGenderGeneralTypes.ExpandedGender = Field(..., description="Gender's details")

    class OptionalExpandedGender(BaseModel):
        gender_details:MaleoMetadataGenderGeneralTypes.OptionalExpandedGender = Field(None, description="Gender's details")

    class ListOfExpandedGenders(BaseModel):
        genders_details:MaleoMetadataGenderGeneralTypes.ListOfExpandedGenders = Field([], description="Genders's details")

    class OptionalListOfExpandedGenders(BaseModel):
        genders_details:MaleoMetadataGenderGeneralTypes.OptionalListOfExpandedGenders = Field(None, description="Genders's details")
from pydantic import BaseModel, Field
from maleo_metadata.types.general.medical_role import MaleoMetadataMedicalRoleGeneralTypes

class MaleoMetadataMedicalRoleExpandedSchemas:
    class SimpleMedicalRole(BaseModel):
        medical_role:MaleoMetadataMedicalRoleGeneralTypes.SimpleMedicalRole = Field(..., description="Medical role")

    class OptionalSimpleMedicalRole(BaseModel):
        medical_role:MaleoMetadataMedicalRoleGeneralTypes.OptionalSimpleMedicalRole = Field(None, description="Medical role")

    class ListOfSimpleMedicalRoles(BaseModel):
        medical_roles:MaleoMetadataMedicalRoleGeneralTypes.ListOfSimpleMedicalRoles = Field([], description="Medical roles")

    class OptionalListOfSimpleMedicalRoles(BaseModel):
        medical_roles:MaleoMetadataMedicalRoleGeneralTypes.OptionalListOfSimpleMedicalRoles = Field(None, description="Medical roles")

    class ExpandedMedicalRole(BaseModel):
        medical_role_details:MaleoMetadataMedicalRoleGeneralTypes.ExpandedMedicalRole = Field(..., description="Medical role's details")

    class OptionalExpandedMedicalRole(BaseModel):
        medical_role_details:MaleoMetadataMedicalRoleGeneralTypes.OptionalExpandedMedicalRole = Field(None, description="Medical role's details")

    class ListOfExpandedMedicalRoles(BaseModel):
        medical_roles_details:MaleoMetadataMedicalRoleGeneralTypes.ListOfExpandedMedicalRoles = Field([], description="Medical roles's details")

    class OptionalListOfExpandedMedicalRoles(BaseModel):
        medical_roles_details:MaleoMetadataMedicalRoleGeneralTypes.OptionalListOfExpandedMedicalRoles = Field(None, description="Medical role's details")

    class StructuredMedicalRole(BaseModel):
        structured_medical_role:MaleoMetadataMedicalRoleGeneralTypes.StructuredMedicalRole = Field(..., description="Medical role")

    class OptionalStructuredMedicalRole(BaseModel):
        structured_medical_role:MaleoMetadataMedicalRoleGeneralTypes.OptionalStructuredMedicalRole = Field(None, description="Medical role")

    class ListOfStructuredMedicalRoles(BaseModel):
        structured_medical_role:MaleoMetadataMedicalRoleGeneralTypes.ListOfStructuredMedicalRoles = Field([], description="Medical roles")

    class OptionalListOfStructuredMedicalRoles(BaseModel):
        structured_medical_role:MaleoMetadataMedicalRoleGeneralTypes.OptionalListOfStructuredMedicalRoles = Field(None, description="Medical roles")
from pydantic import BaseModel, Field
from maleo_metadata.types.general.system_role import MaleoMetadataSystemRoleGeneralTypes

class MaleoMetadataSystemRoleExpandedSchemas:
    class SimpleSystemRole(BaseModel):
        system_role:MaleoMetadataSystemRoleGeneralTypes.SimpleSystemRole = Field(..., description="System role")

    class OptionalSimpleSystemRole(BaseModel):
        system_role:MaleoMetadataSystemRoleGeneralTypes.OptionalSimpleSystemRole = Field(None, description="System role")

    class ListOfSimpleSystemRoles(BaseModel):
        system_roles:MaleoMetadataSystemRoleGeneralTypes.ListOfSimpleSystemRoles = Field([], description="System roles")

    class OptionalListOfSimpleSystemRoles(BaseModel):
        system_roles:MaleoMetadataSystemRoleGeneralTypes.OptionalListOfSimpleSystemRoles = Field(None, description="System roles")

    class ExpandedSystemRole(BaseModel):
        system_role_details:MaleoMetadataSystemRoleGeneralTypes.ExpandedSystemRole = Field(..., description="System role's details")

    class OptionalExpandedSystemRole(BaseModel):
        system_role_details:MaleoMetadataSystemRoleGeneralTypes.OptionalExpandedSystemRole = Field(None, description="System role's details")

    class ListOfExpandedSystemRoles(BaseModel):
        system_roles_details:MaleoMetadataSystemRoleGeneralTypes.ListOfExpandedSystemRoles = Field([], description="System roles's details")

    class OptionalListOfExpandedSystemRoles(BaseModel):
        system_roles_details:MaleoMetadataSystemRoleGeneralTypes.OptionalListOfExpandedSystemRoles = Field(None, description="System role's details")
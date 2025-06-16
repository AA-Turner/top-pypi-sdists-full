from __future__ import annotations
from pydantic import Field
from maleo_foundation.managers.client.base import ClientServices
from maleo_metadata.client.services.blood_type \
    import MaleoMetadataBloodTypeClientService
from maleo_metadata.client.services.gender \
    import MaleoMetadataGenderClientService
from maleo_metadata.client.services.medical_role \
    import MaleoMetadataMedicalRoleClientService
from maleo_metadata.client.services.organization_type \
    import MaleoMetadataOrganizationTypeClientService
from maleo_metadata.client.services.service \
    import MaleoMetadataServiceClientService
from maleo_metadata.client.services.system_role \
    import MaleoMetadataSystemRoleClientService
from maleo_metadata.client.services.user_type \
    import MaleoMetadataUserTypeClientService

class MaleoMetadataServices(ClientServices):
    blood_type:MaleoMetadataBloodTypeClientService = Field(..., description="Blood type's service")
    gender:MaleoMetadataGenderClientService = Field(..., description="Gender's service")
    medical_role:MaleoMetadataMedicalRoleClientService = Field(..., description="Medical role's service")
    organization_type:MaleoMetadataOrganizationTypeClientService = Field(..., description="Organization type's service")
    service:MaleoMetadataServiceClientService = Field(..., description="Service's service")
    system_role:MaleoMetadataSystemRoleClientService = Field(..., description="System role's service")
    user_type:MaleoMetadataUserTypeClientService = Field(..., description="User type's service")
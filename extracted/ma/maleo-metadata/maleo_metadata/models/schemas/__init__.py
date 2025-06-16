from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeSchemas
from .gender import MaleoMetadataGenderSchemas
from .medical_role import MaleoMetadataMedicalRoleSchemas
from .organization_type import MaleoMetadataOrganizationTypeSchemas
from .service import MaleoMetadataServiceSchemas
from .system_role import MaleoMetadataSystemRoleSchemas
from .user_type import MaleoMetadataUserTypeSchemas

class MaleoMetadataSchemas:
    BloodType = MaleoMetadataBloodTypeSchemas
    Gender = MaleoMetadataGenderSchemas
    MedicalRole = MaleoMetadataMedicalRoleSchemas
    OrganizationType = MaleoMetadataOrganizationTypeSchemas
    Service = MaleoMetadataServiceSchemas
    SystemRole = MaleoMetadataSystemRoleSchemas
    UserType = MaleoMetadataUserTypeSchemas
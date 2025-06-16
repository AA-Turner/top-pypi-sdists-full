from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeGeneralTypes
from .gender import MaleoMetadataGenderGeneralTypes
from .medical_role import MaleoMetadataMedicalRoleGeneralTypes
from .organization_type import MaleoMetadataOrganizationTypeGeneralTypes
from .service import MaleoMetadataServiceGeneralTypes
from .system_role import MaleoMetadataSystemRoleGeneralTypes
from .user_type import MaleoMetadataUserTypeGeneralTypes

class MaleoMetadataGeneralTypes:
    BloodType = MaleoMetadataBloodTypeGeneralTypes
    Gender = MaleoMetadataGenderGeneralTypes
    MedicalRole = MaleoMetadataMedicalRoleGeneralTypes
    OrganizationType = MaleoMetadataOrganizationTypeGeneralTypes
    Service = MaleoMetadataServiceGeneralTypes
    SystemRole = MaleoMetadataSystemRoleGeneralTypes
    UserType = MaleoMetadataUserTypeGeneralTypes
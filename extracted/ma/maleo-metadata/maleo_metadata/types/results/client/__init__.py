from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeClientResultsTypes
from .gender import MaleoMetadataGenderClientResultsTypes
from .medical_role import MaleoMetadataMedicalRoleClientResultsTypes
from .organization_type import MaleoMetadataOrganizationTypeClientResultsTypes
from .service import MaleoMetadataServiceClientResultsTypes
from .system_role import MaleoMetadataSystemRoleClientResultsTypes
from .user_type import MaleoMetadataUserTypeClientResultsTypes

class MaleoMetadataClientResultsTypes:
    BloodType = MaleoMetadataBloodTypeClientResultsTypes
    Gender = MaleoMetadataGenderClientResultsTypes
    MedicalRole = MaleoMetadataMedicalRoleClientResultsTypes
    OrganizationType = MaleoMetadataOrganizationTypeClientResultsTypes
    Service = MaleoMetadataServiceClientResultsTypes
    SystemRole = MaleoMetadataSystemRoleClientResultsTypes
    UserType = MaleoMetadataUserTypeClientResultsTypes
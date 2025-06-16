from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeServiceResultsTypes
from .gender import MaleoMetadataGenderServiceResultsTypes
from .medical_role import MaleoMetadataMedicalRoleServiceResultsTypes
from .organization_type import MaleoMetadataOrganizationTypeServiceResultsTypes
from .service import MaleoMetadataServiceServiceResultsTypes
from .system_role import MaleoMetadataSystemRoleServiceResultsTypes
from .user_type import MaleoMetadataUserTypeServiceResultsTypes

class MaleoMetadataServiceResultsTypes:
    BloodType = MaleoMetadataBloodTypeServiceResultsTypes
    Gender = MaleoMetadataGenderServiceResultsTypes
    MedicalRole = MaleoMetadataMedicalRoleServiceResultsTypes
    OrganizationType = MaleoMetadataOrganizationTypeServiceResultsTypes
    Service = MaleoMetadataServiceServiceResultsTypes
    SystemRole = MaleoMetadataSystemRoleServiceResultsTypes
    UserType = MaleoMetadataUserTypeServiceResultsTypes
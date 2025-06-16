from __future__ import annotations
from .blood_type import BloodTypeTransfers
from .gender import GenderTransfers
from .medical_role import MedicalRoleTransfers
from .organization_type import OrganizationTypeTransfers
from .service import ServiceTransfers
from .system_role import SystemRoleTransfers
from .user_type import UserTypeTransfers

class MaleoMetadataGeneralTransfers:
    BloodType = BloodTypeTransfers
    Gender = GenderTransfers
    MedicalRole = MedicalRoleTransfers
    OrganizationType = OrganizationTypeTransfers
    Service = ServiceTransfers
    SystemRole = SystemRoleTransfers
    UserType = UserTypeTransfers
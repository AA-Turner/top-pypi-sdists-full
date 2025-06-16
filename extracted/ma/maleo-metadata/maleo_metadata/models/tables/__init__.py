from __future__ import annotations
from .blood_type import BloodTypesTable
from .gender import GendersTable
from .medical_role import MedicalRolesTable
from .organization_type import OrganizationTypesTable
from .service import ServicesTable
from .system_role import SystemRolesTable
from .user_type import UserTypesTable

class MaleoMetadataTables:
    BloodType = BloodTypesTable
    Genders = GendersTable
    MedicalRoles = MedicalRolesTable
    OrganizationTypes = OrganizationTypesTable
    Services = ServicesTable
    SystemRoles = SystemRolesTable
    UserType = UserTypesTable
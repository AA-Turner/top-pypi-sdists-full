from typing import Dict
from uuid import UUID
from maleo_metadata.enums.medical_role import MaleoMetadataMedicalRoleEnums

class MaleoMetadataMedicalRoleConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoMetadataMedicalRoleEnums.IdentifierType,
        object
    ] = {
        MaleoMetadataMedicalRoleEnums.IdentifierType.ID: int,
        MaleoMetadataMedicalRoleEnums.IdentifierType.UUID: UUID,
        MaleoMetadataMedicalRoleEnums.IdentifierType.CODE: str,
        MaleoMetadataMedicalRoleEnums.IdentifierType.KEY: str,
        MaleoMetadataMedicalRoleEnums.IdentifierType.NAME: str,
    }
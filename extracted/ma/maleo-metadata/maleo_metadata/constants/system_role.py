from typing import Dict
from uuid import UUID
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums

class MaleoMetadataSystemRoleConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoMetadataSystemRoleEnums.IdentifierType,
        object
    ] = {
        MaleoMetadataSystemRoleEnums.IdentifierType.ID: int,
        MaleoMetadataSystemRoleEnums.IdentifierType.UUID: UUID,
        MaleoMetadataSystemRoleEnums.IdentifierType.KEY: str,
        MaleoMetadataSystemRoleEnums.IdentifierType.NAME: str,
    }
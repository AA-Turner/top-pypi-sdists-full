from typing import Dict
from uuid import UUID
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums

class MaleoMetadataOrganizationTypeConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoMetadataOrganizationTypeEnums.IdentifierType,
        object
    ] = {
        MaleoMetadataOrganizationTypeEnums.IdentifierType.ID: int,
        MaleoMetadataOrganizationTypeEnums.IdentifierType.UUID: UUID,
        MaleoMetadataOrganizationTypeEnums.IdentifierType.KEY: str,
        MaleoMetadataOrganizationTypeEnums.IdentifierType.NAME: str,
    }
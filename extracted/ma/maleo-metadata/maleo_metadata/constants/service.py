from typing import Dict
from uuid import UUID
from maleo_metadata.enums.service import MaleoMetadataServiceEnums

class MaleoMetadataServiceConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoMetadataServiceEnums.IdentifierType,
        object
    ] = {
        MaleoMetadataServiceEnums.IdentifierType.ID: int,
        MaleoMetadataServiceEnums.IdentifierType.UUID: UUID,
        MaleoMetadataServiceEnums.IdentifierType.KEY: str,
        MaleoMetadataServiceEnums.IdentifierType.NAME: str,
    }
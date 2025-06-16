from typing import Dict
from uuid import UUID
from maleo_metadata.enums.user_type import MaleoMetadataUserTypeEnums

class MaleoMetadataUserTypeConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoMetadataUserTypeEnums.IdentifierType,
        object
    ] = {
        MaleoMetadataUserTypeEnums.IdentifierType.ID: int,
        MaleoMetadataUserTypeEnums.IdentifierType.UUID: UUID,
        MaleoMetadataUserTypeEnums.IdentifierType.KEY: str,
        MaleoMetadataUserTypeEnums.IdentifierType.NAME: str,
    }
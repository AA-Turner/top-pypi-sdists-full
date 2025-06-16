from typing import Dict
from uuid import UUID
from maleo_metadata.enums.blood_type import MaleoMetadataBloodTypeEnums

class MaleoMetadataBloodTypeConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoMetadataBloodTypeEnums.IdentifierType,
        object
    ] = {
        MaleoMetadataBloodTypeEnums.IdentifierType.ID: int,
        MaleoMetadataBloodTypeEnums.IdentifierType.UUID: UUID,
        MaleoMetadataBloodTypeEnums.IdentifierType.KEY: str,
        MaleoMetadataBloodTypeEnums.IdentifierType.NAME: str,
    }
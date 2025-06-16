from enum import StrEnum

class MaleoMetadataBloodTypeEnums:
    class IdentifierType(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"
        NAME = "name"

    class BloodType(StrEnum):
        A = "a"
        B = "b"
        AB = "ab"
        O = "o"
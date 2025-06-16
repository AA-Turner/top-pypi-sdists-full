from enum import StrEnum

class MaleoMetadataSystemRoleEnums:
    class IdentifierType(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"
        NAME = "name"

    class SystemRole(StrEnum):
        ADMINISTRATOR = "administrator"
        USER = "user"
from enum import Enum


class GetPublicSettingsResponse200DatatableDatatablesAdditionalPropertyDatabaseResourceType(str, Enum):
    INSTANCE = "instance"
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class GetSettingsResponse200DatatableDatatablesAdditionalPropertyDatabaseResourceType(str, Enum):
    INSTANCE = "instance"
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)

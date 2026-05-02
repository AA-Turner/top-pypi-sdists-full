from enum import Enum


class GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalogResourceType(str, Enum):
    INSTANCE = "instance"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)

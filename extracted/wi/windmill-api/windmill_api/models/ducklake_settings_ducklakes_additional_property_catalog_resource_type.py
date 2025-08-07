from enum import Enum


class DucklakeSettingsDucklakesAdditionalPropertyCatalogResourceType(str, Enum):
    INSTANCE = "instance"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)

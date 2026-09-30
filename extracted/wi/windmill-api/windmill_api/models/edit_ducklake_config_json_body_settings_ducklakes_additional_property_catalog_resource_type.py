from enum import Enum


class EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyCatalogResourceType(str, Enum):
    EXTERNAL_INSTANCE = "external_instance"
    INSTANCE = "instance"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)

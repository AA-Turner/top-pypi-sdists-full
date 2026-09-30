from enum import Enum


class EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabaseResourceType(str, Enum):
    EXTERNAL_INSTANCE = "external_instance"
    INSTANCE = "instance"
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)

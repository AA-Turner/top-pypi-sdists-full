from enum import Enum


class ListSchemasSortType0Item(str, Enum):
    LATEST_VERSION_AT = "latest_version_at"
    SCHEMA_NAME = "schema_name"

    def __str__(self) -> str:
        return str(self.value)

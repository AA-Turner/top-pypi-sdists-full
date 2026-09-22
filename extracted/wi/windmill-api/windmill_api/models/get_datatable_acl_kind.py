from enum import Enum


class GetDatatableAclKind(str, Enum):
    DATABASE = "database"
    SCHEMA = "schema"
    TABLE = "table"

    def __str__(self) -> str:
        return str(self.value)

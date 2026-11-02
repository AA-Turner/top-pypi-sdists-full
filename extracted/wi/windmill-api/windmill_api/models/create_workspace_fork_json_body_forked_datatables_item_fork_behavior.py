from enum import Enum


class CreateWorkspaceForkJsonBodyForkedDatatablesItemForkBehavior(str, Enum):
    SCHEMA_AND_DATA = "schema_and_data"
    SCHEMA_ONLY = "schema_only"

    def __str__(self) -> str:
        return str(self.value)

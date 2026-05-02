from enum import Enum


class ImportPgDatabaseJsonBodyForkBehavior(str, Enum):
    KEEP_ORIGINAL = "keep_original"
    SCHEMA_AND_DATA = "schema_and_data"
    SCHEMA_ONLY = "schema_only"

    def __str__(self) -> str:
        return str(self.value)

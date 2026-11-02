from enum import Enum


class ApplyDatatableAclJsonBodyChangeType2Scope(str, Enum):
    ALL_FUNCTIONS = "all_functions"
    ALL_SEQUENCES = "all_sequences"
    ALL_TABLES = "all_tables"
    FUTURE_FUNCTIONS = "future_functions"
    FUTURE_SEQUENCES = "future_sequences"
    FUTURE_TABLES = "future_tables"
    TARGET = "target"

    def __str__(self) -> str:
        return str(self.value)

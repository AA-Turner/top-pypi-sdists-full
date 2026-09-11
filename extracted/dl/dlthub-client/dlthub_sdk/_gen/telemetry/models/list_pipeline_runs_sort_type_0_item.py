from enum import Enum


class ListPipelineRunsSortType0Item(str, Enum):
    DURATION_MS = "duration_ms"
    FINISHED_AT = "finished_at"
    STARTED_AT = "started_at"
    TOTAL_BYTES_LOADED = "total_bytes_loaded"
    TOTAL_ROWS_LOADED = "total_rows_loaded"

    def __str__(self) -> str:
        return str(self.value)

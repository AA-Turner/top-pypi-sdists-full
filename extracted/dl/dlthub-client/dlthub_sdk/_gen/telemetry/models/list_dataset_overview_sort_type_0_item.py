from enum import Enum


class ListDatasetOverviewSortType0Item(str, Enum):
    AVG_DURATION_MS = "avg_duration_ms"
    DATASET_NAME = "dataset_name"
    LATEST_RUN_AT = "latest_run_at"
    SUCCESS_RATE = "success_rate"
    TOTAL_ROWS_LOADED = "total_rows_loaded"
    TOTAL_RUNS = "total_runs"

    def __str__(self) -> str:
        return str(self.value)

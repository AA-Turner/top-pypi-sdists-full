from enum import Enum


class ListDatasetStatsSortType0Item(str, Enum):
    AVERAGE_DURATION_MS = "average_duration_ms"
    DATASET_NAME = "dataset_name"
    LATEST_PIPELINE_RUN_AT = "latest_pipeline_run_at"
    SUCCESS_RATIO = "success_ratio"
    TOTAL_PIPELINE_RUN_COUNT = "total_pipeline_run_count"
    TOTAL_ROWS_LOADED = "total_rows_loaded"

    def __str__(self) -> str:
        return str(self.value)

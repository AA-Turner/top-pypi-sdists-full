from enum import Enum


class ListPipelineStatsSortType0Item(str, Enum):
    AVERAGE_DURATION_MS = "average_duration_ms"
    LATEST_PIPELINE_RUN_AT = "latest_pipeline_run_at"
    PIPELINE_NAME = "pipeline_name"
    SUCCESS_RATIO = "success_ratio"
    TOTAL_PIPELINE_RUN_COUNT = "total_pipeline_run_count"
    TOTAL_ROWS_LOADED = "total_rows_loaded"

    def __str__(self) -> str:
        return str(self.value)

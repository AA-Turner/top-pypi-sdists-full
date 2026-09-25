from enum import Enum


class TJobObjectInputEntityType(str, Enum):
    DATASET = "dataset"
    JOB = "job"
    JOB_RUN = "job-run"
    PIPELINE = "pipeline"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)

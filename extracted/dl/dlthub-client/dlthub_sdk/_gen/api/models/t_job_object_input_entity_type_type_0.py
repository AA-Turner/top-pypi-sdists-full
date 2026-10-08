from enum import Enum


class TJobObjectInputEntityTypeType0(str, Enum):
    DATASET = "dataset"
    JOB = "job"
    JOB_RUNS = "job-runs"
    PIPELINE = "pipeline"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)

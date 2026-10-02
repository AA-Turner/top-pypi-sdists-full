from enum import StrEnum

class EvaluationExportResponseListDtoItemFormatType0Type0(StrEnum):
    DEFAULT = "default"
    HARBOR_BASIC = "harbor-basic"
    HARBOR_JOB = "harbor-job"

    def __str__(self) -> str:
        return str(self.value)

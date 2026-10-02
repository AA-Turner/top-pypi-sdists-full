from enum import StrEnum

class EvaluationExportResponseDtoEvaluationConfigType0Format(StrEnum):
    CSV = "csv"
    HARBOR_BASIC = "harbor-basic"
    JSON = "json"

    def __str__(self) -> str:
        return str(self.value)

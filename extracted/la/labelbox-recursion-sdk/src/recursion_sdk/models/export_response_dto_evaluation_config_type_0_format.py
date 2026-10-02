from enum import StrEnum

class ExportResponseDtoEvaluationConfigType0Format(StrEnum):
    CSV = "csv"
    HARBOR_BASIC = "harbor-basic"
    JSON = "json"

    def __str__(self) -> str:
        return str(self.value)

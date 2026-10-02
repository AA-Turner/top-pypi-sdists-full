from enum import StrEnum

class CreateEvaluationExportBodyDtoFormat(StrEnum):
    CSV = "csv"
    HARBOR_BASIC = "harbor-basic"
    JSON = "json"

    def __str__(self) -> str:
        return str(self.value)

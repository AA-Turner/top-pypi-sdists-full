from enum import StrEnum

class CreateExportBodyDtoIdsFormat(StrEnum):
    DEFAULT = "default"
    HARBOR_BASIC = "harbor-basic"
    HARBOR_JOB = "harbor-job"

    def __str__(self) -> str:
        return str(self.value)

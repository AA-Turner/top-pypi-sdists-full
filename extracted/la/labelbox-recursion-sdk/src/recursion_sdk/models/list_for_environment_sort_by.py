from enum import StrEnum

class ListForEnvironmentSortBy(StrEnum):
    AVGSCORE = "avgScore"
    COST = "cost"
    CREATEDAT = "createdAt"
    EXTERNALID = "externalId"
    LATESTVERSIONCREATEDAT = "latestVersionCreatedAt"
    RUNS = "runs"
    TITLE = "title"
    UPDATEDAT = "updatedAt"

    def __str__(self) -> str:
        return str(self.value)

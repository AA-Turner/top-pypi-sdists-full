from enum import StrEnum

class AutoUpdateUnavailableCode(StrEnum):
    DRAFT = "draft"
    RELEASE_PLEASE = "release_please"

    def __str__(self) -> str:
        return str(self.value)

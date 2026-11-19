from enum import Enum


class GetApprovalStepDetailResponse200Skin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)

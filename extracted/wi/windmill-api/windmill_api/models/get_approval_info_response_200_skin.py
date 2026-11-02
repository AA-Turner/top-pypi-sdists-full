from enum import Enum


class GetApprovalInfoResponse200Skin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class CreateAppRawSourceJsonBodyPolicyExecutionMode(str, Enum):
    ANONYMOUS = "anonymous"
    GUEST = "guest"
    PUBLISHER = "publisher"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)

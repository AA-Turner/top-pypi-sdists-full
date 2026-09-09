from enum import Enum


class GetCredentialOriginResponse200Provider(str, Enum):
    GITLAB = "gitlab"

    def __str__(self) -> str:
        return str(self.value)

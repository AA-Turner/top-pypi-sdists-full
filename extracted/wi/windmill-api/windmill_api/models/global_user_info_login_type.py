from enum import Enum


class GlobalUserInfoLoginType(str, Enum):
    GITHUB = "github"
    PASSWORD = "password"
    SERVICE_ACCOUNT = "service_account"

    def __str__(self) -> str:
        return str(self.value)

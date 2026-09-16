from enum import Enum


class GlobalWhoamiResponse200LoginType(str, Enum):
    GITHUB = "github"
    PASSWORD = "password"
    PENDING_OAUTH = "pending_oauth"
    SERVICE_ACCOUNT = "service_account"

    def __str__(self) -> str:
        return str(self.value)

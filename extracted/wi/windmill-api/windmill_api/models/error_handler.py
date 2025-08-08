from enum import Enum


class ErrorHandler(str, Enum):
    CUSTOM = "custom"
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"

    def __str__(self) -> str:
        return str(self.value)

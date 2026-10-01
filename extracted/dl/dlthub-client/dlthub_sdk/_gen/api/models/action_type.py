from enum import Enum


class ActionType(str, Enum):
    EMAIL_SEND = "email.send"
    SLACK_POST = "slack.post"

    def __str__(self) -> str:
        return str(self.value)

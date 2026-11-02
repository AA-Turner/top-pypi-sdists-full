from enum import StrEnum

class BotRequestAction(StrEnum):
    REBASE = "rebase"
    RECREATE = "recreate"

    def __str__(self) -> str:
        return str(self.value)

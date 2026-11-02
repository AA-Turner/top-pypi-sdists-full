from enum import StrEnum

class BotRequestBot(StrEnum):
    DEPENDABOT = "dependabot"
    RENOVATE = "renovate"

    def __str__(self) -> str:
        return str(self.value)

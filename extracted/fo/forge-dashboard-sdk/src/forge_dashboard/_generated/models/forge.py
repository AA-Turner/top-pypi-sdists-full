from enum import StrEnum

class Forge(StrEnum):
    FORGEJO = "forgejo"
    GITHUB = "github"

    def __str__(self) -> str:
        return str(self.value)

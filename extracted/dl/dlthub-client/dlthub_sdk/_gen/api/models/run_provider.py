from enum import Enum


class RunProvider(str, Enum):
    LOCAL = "local"
    MODAL = "modal"
    TOWER = "tower"

    def __str__(self) -> str:
        return str(self.value)

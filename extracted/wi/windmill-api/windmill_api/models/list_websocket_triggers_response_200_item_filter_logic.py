from enum import Enum


class ListWebsocketTriggersResponse200ItemFilterLogic(str, Enum):
    AND = "and"
    OR = "or"

    def __str__(self) -> str:
        return str(self.value)

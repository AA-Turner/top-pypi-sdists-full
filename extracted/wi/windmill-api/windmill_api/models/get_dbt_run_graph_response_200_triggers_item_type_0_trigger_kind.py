from enum import Enum


class GetDbtRunGraphResponse200TriggersItemType0TriggerKind(str, Enum):
    ASSET = "asset"

    def __str__(self) -> str:
        return str(self.value)

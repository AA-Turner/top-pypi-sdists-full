from enum import Enum


class AssetGraphTriggersItemType0TriggerKind(str, Enum):
    ASSET = "asset"

    def __str__(self) -> str:
        return str(self.value)

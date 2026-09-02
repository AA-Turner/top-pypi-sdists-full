from enum import Enum


class AssetGraphAssetsItemForkMaterialization(str, Enum):
    DEFERRED = "deferred"
    FORK = "fork"

    def __str__(self) -> str:
        return str(self.value)

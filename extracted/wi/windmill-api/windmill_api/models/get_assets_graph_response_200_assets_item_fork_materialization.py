from enum import Enum


class GetAssetsGraphResponse200AssetsItemForkMaterialization(str, Enum):
    DEFERRED = "deferred"
    FORK = "fork"

    def __str__(self) -> str:
        return str(self.value)

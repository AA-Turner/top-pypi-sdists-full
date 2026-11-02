from enum import Enum


class GetDbtRunGraphResponse200AssetsItemForkMaterialization(str, Enum):
    DEFERRED = "deferred"
    FORK = "fork"

    def __str__(self) -> str:
        return str(self.value)

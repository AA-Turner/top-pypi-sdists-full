from enum import StrEnum

class QaJobPageResponseDtoItemsItemKind(StrEnum):
    AGGREGATE = "aggregate"
    INDIVIDUAL = "individual"

    def __str__(self) -> str:
        return str(self.value)

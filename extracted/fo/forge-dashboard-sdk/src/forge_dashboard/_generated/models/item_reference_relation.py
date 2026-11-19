from enum import StrEnum

class ItemReferenceRelation(StrEnum):
    CLOSES = "closes"
    MENTIONS = "mentions"
    REFS = "refs"

    def __str__(self) -> str:
        return str(self.value)

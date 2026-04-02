from enum import Enum


class RelationshipTypeEnum(str, Enum):
    BOARD = "board"
    CONSULTING = "consulting"
    EMPLOYMENT = "employment"
    EQUITY = "equity"
    GIFTS = "gifts"
    OTHER = "other"
    ROYALTIES = "royalties"

    def __str__(self) -> str:
        return str(self.value)

from enum import StrEnum

class ReapedRunConfigPageDtoItemsItemDeletedReasonType0(StrEnum):
    STALE_DRAFT = "stale_draft"
    UNUSED_UNBOUND = "unused_unbound"

    def __str__(self) -> str:
        return str(self.value)

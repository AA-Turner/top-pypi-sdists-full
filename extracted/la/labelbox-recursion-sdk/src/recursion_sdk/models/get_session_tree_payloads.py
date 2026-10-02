from enum import StrEnum

class GetSessionTreePayloads(StrEnum):
    REFS = "refs"

    def __str__(self) -> str:
        return str(self.value)

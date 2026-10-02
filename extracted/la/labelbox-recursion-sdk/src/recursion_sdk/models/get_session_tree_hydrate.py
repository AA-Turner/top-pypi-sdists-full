from enum import StrEnum

class GetSessionTreeHydrate(StrEnum):
    IMAGES = "images"

    def __str__(self) -> str:
        return str(self.value)

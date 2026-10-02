from enum import StrEnum

class ListSessionEventsHydrate(StrEnum):
    IMAGES = "images"

    def __str__(self) -> str:
        return str(self.value)

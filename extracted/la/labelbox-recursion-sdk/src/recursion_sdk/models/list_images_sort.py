from enum import StrEnum

class ListImagesSort(StrEnum):
    NAME = "name"
    RECENT = "recent"
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)

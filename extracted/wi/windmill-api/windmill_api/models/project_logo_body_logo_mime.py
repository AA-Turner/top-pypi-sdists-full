from enum import Enum


class ProjectLogoBodyLogoMime(str, Enum):
    IMAGEPNG = "image/png"
    IMAGESVGXML = "image/svg+xml"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class ChartAnnotationTypeEnum(str, Enum):
    AREA_X = "area_x"
    AREA_Y = "area_y"
    LINE_X = "line_x"
    LINE_Y = "line_y"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class ChartTypeEnum(str, Enum):
    AREA = "area"
    BAR = "bar"
    HEATMAP = "heatmap"
    LINE = "line"
    SCATTER = "scatter"
    STACKED_BAR = "stacked_bar"
    TIMELINE = "timeline"

    def __str__(self) -> str:
        return str(self.value)

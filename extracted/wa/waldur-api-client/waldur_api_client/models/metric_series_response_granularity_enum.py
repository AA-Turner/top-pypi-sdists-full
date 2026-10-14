from enum import Enum


class MetricSeriesResponseGranularityEnum(str, Enum):
    AUTO = "auto"
    DAY = "day"
    HOUR = "hour"
    RAW = "raw"

    def __str__(self) -> str:
        return str(self.value)

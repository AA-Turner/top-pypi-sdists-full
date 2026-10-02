from enum import StrEnum

class JobExecutionsResponseDtoTimeRange(StrEnum):
    VALUE_0 = "1h"
    VALUE_1 = "6h"
    VALUE_2 = "24h"
    VALUE_3 = "7d"

    def __str__(self) -> str:
        return str(self.value)

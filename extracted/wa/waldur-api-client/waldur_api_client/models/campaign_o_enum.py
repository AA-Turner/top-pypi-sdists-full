from enum import Enum


class CampaignOEnum(str, Enum):
    END_DATE = "end_date"
    START_DATE = "start_date"
    VALUE_0 = "-end_date"
    VALUE_1 = "-start_date"

    def __str__(self) -> str:
        return str(self.value)

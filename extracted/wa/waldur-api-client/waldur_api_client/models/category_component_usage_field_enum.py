from enum import Enum


class CategoryComponentUsageFieldEnum(str, Enum):
    CATEGORY_TITLE = "category_title"
    CATEGORY_UUID = "category_uuid"
    DATE = "date"
    FIXED_USAGE = "fixed_usage"
    MEASURED_UNIT = "measured_unit"
    NAME = "name"
    REPORTED_USAGE = "reported_usage"
    SCOPE = "scope"
    TYPE = "type"

    def __str__(self) -> str:
        return str(self.value)

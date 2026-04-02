from enum import Enum


class ProjectCreditOEnum(str, Enum):
    END_DATE = "end_date"
    EXPECTED_CONSUMPTION = "expected_consumption"
    PROJECT_NAME = "project_name"
    VALUE = "value"
    VALUE_0 = "-end_date"
    VALUE_1 = "-expected_consumption"
    VALUE_2 = "-project_name"
    VALUE_3 = "-value"

    def __str__(self) -> str:
        return str(self.value)

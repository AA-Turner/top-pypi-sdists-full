from enum import Enum


class ResourceOEnum(str, Enum):
    CREATED = "created"
    END_DATE = "end_date"
    NAME = "name"
    PROJECT_NAME = "project_name"
    STATE = "state"
    VALUE_0 = "-created"
    VALUE_1 = "-end_date"
    VALUE_2 = "-name"
    VALUE_3 = "-project_name"
    VALUE_4 = "-state"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class CourseAccountOEnum(str, Enum):
    CREATED = "created"
    EMAIL = "email"
    MODIFIED = "modified"
    PROJECT_END_DATE = "project_end_date"
    PROJECT_NAME = "project_name"
    PROJECT_START_DATE = "project_start_date"
    STATE = "state"
    USERNAME = "username"
    VALUE_0 = "-created"
    VALUE_1 = "-email"
    VALUE_2 = "-modified"
    VALUE_3 = "-project_end_date"
    VALUE_4 = "-project_name"
    VALUE_5 = "-project_start_date"
    VALUE_6 = "-state"
    VALUE_7 = "-username"

    def __str__(self) -> str:
        return str(self.value)

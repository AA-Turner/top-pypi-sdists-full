from enum import Enum


class ResourceOEnum(str, Enum):
    BACKEND_ID = "backend_id"
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    END_DATE = "end_date"
    NAME = "name"
    OFFERING_NAME = "offering_name"
    PLAN_NAME = "plan_name"
    PROJECT_NAME = "project_name"
    STATE = "state"
    VALUE_0 = "-backend_id"
    VALUE_1 = "-created"
    VALUE_2 = "-customer_name"
    VALUE_3 = "-end_date"
    VALUE_4 = "-name"
    VALUE_5 = "-offering_name"
    VALUE_6 = "-plan_name"
    VALUE_7 = "-project_name"
    VALUE_8 = "-state"

    def __str__(self) -> str:
        return str(self.value)

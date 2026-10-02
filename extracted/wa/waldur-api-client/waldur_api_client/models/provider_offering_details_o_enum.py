from enum import Enum


class ProviderOfferingDetailsOEnum(str, Enum):
    CREATED = "created"
    NAME = "name"
    STATE = "state"
    TOTAL_COST = "total_cost"
    TOTAL_COST_ESTIMATED = "total_cost_estimated"
    TOTAL_CUSTOMERS = "total_customers"
    TYPE = "type"
    VALUE_0 = "-created"
    VALUE_1 = "-name"
    VALUE_2 = "-state"
    VALUE_3 = "-total_cost"
    VALUE_4 = "-total_cost_estimated"
    VALUE_5 = "-total_customers"
    VALUE_6 = "-type"

    def __str__(self) -> str:
        return str(self.value)

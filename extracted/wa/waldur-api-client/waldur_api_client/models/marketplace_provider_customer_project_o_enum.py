from enum import Enum


class MarketplaceProviderCustomerProjectOEnum(str, Enum):
    CREATED = "created"
    CUSTOMER_ABBREVIATION = "customer_abbreviation"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_NATIVE_NAME = "customer_native_name"
    END_DATE = "end_date"
    ESTIMATED_COST = "estimated_cost"
    NAME = "name"
    START_DATE = "start_date"
    VALUE_0 = "-created"
    VALUE_1 = "-customer_abbreviation"
    VALUE_2 = "-customer_name"
    VALUE_3 = "-customer_native_name"
    VALUE_4 = "-end_date"
    VALUE_5 = "-estimated_cost"
    VALUE_6 = "-name"
    VALUE_7 = "-start_date"

    def __str__(self) -> str:
        return str(self.value)

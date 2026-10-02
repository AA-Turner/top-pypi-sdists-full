from enum import Enum


class CustomerCreditOEnum(str, Enum):
    CUSTOMER_NAME = "customer_name"
    END_DATE = "end_date"
    EXPECTED_CONSUMPTION = "expected_consumption"
    VALUE = "value"
    VALUE_0 = "-customer_name"
    VALUE_1 = "-end_date"
    VALUE_2 = "-expected_consumption"
    VALUE_3 = "-value"

    def __str__(self) -> str:
        return str(self.value)

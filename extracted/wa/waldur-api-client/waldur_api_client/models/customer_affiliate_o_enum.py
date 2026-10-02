from enum import Enum


class CustomerAffiliateOEnum(str, Enum):
    AFFILIATE_NAME = "affiliate_name"
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    VALUE_0 = "-affiliate_name"
    VALUE_1 = "-created"
    VALUE_2 = "-customer_name"

    def __str__(self) -> str:
        return str(self.value)

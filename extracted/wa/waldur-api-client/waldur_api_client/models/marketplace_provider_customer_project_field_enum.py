from enum import Enum


class MarketplaceProviderCustomerProjectFieldEnum(str, Enum):
    BILLING_PRICE_ESTIMATE = "billing_price_estimate"
    DESCRIPTION = "description"
    END_DATE = "end_date"
    NAME = "name"
    RESOURCES_COUNT = "resources_count"
    USERS_COUNT = "users_count"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class MarketplaceProviderCustomerFieldEnum(str, Enum):
    ABBREVIATION = "abbreviation"
    BILLING_PRICE_ESTIMATE = "billing_price_estimate"
    EMAIL = "email"
    NAME = "name"
    PAYMENT_PROFILES = "payment_profiles"
    PHONE_NUMBER = "phone_number"
    PROJECTS = "projects"
    PROJECTS_COUNT = "projects_count"
    SLUG = "slug"
    USERS = "users"
    USERS_COUNT = "users_count"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class ProviderOfferingFieldEnum(str, Enum):
    BILLING_PRICE_ESTIMATE = "billing_price_estimate"
    CATEGORY_TITLE = "category_title"
    COMPONENTS = "components"
    CUSTOMER_UUID = "customer_uuid"
    NAME = "name"
    OPTIONS = "options"
    PLANS = "plans"
    RESOURCES_COUNT = "resources_count"
    RESOURCE_OPTIONS = "resource_options"
    SECRET_OPTIONS = "secret_options"
    SLUG = "slug"
    STATE = "state"
    THUMBNAIL = "thumbnail"
    TYPE = "type"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class ServiceProviderFieldEnum(str, Enum):
    ALLOWED_DOMAINS = "allowed_domains"
    CREATED = "created"
    CUSTOMER = "customer"
    CUSTOMER_ABBREVIATION = "customer_abbreviation"
    CUSTOMER_COUNTRY = "customer_country"
    CUSTOMER_IMAGE = "customer_image"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_NATIVE_NAME = "customer_native_name"
    CUSTOMER_SLUG = "customer_slug"
    CUSTOMER_UUID = "customer_uuid"
    DESCRIPTION = "description"
    ENABLE_NOTIFICATIONS = "enable_notifications"
    IMAGE = "image"
    OFFERING_COUNT = "offering_count"
    ORGANIZATION_GROUPS = "organization_groups"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

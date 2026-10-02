from enum import Enum


class OfferingGroupFieldEnum(str, Enum):
    CREATED = "created"
    CUSTOMER = "customer"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_UUID = "customer_uuid"
    DESCRIPTION = "description"
    ICON = "icon"
    TITLE = "title"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

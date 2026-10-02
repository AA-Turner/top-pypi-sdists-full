from enum import Enum


class ProviderOfferingCustomerFieldEnum(str, Enum):
    ABBREVIATION = "abbreviation"
    EMAIL = "email"
    NAME = "name"
    PHONE_NUMBER = "phone_number"
    SLUG = "slug"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

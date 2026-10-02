from enum import Enum


class OfferingTermsOfServiceOEnum(str, Enum):
    CREATED = "created"
    MODIFIED = "modified"
    VALUE_0 = "-created"
    VALUE_1 = "-modified"
    VALUE_2 = "-version"
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class OfferingReferralOEnum(str, Enum):
    PUBLISHED = "published"
    RELATION_TYPE = "relation_type"
    RESOURCE_TYPE = "resource_type"
    VALUE_0 = "-published"
    VALUE_1 = "-relation_type"
    VALUE_2 = "-resource_type"

    def __str__(self) -> str:
        return str(self.value)

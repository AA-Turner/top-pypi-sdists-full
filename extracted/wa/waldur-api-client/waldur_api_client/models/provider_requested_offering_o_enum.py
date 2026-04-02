from enum import Enum


class ProviderRequestedOfferingOEnum(str, Enum):
    CALL_NAME = "call__name"
    CREATED = "created"
    OFFERING_NAME = "offering__name"
    STATE = "state"
    VALUE_0 = "-call__name"
    VALUE_1 = "-created"
    VALUE_2 = "-offering__name"
    VALUE_3 = "-state"

    def __str__(self) -> str:
        return str(self.value)

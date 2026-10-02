from enum import Enum


class UserRequestedResourceOEnum(str, Enum):
    CALL_NAME = "call__name"
    CREATED = "created"
    OFFERING_NAME = "offering__name"
    PROPOSAL_NAME = "proposal__name"
    PROPOSAL_STATE = "proposal__state"
    RESOURCE_NAME = "resource__name"
    RESOURCE_STATE = "resource__state"
    VALUE_0 = "-call__name"
    VALUE_1 = "-created"
    VALUE_2 = "-offering__name"
    VALUE_3 = "-proposal__name"
    VALUE_4 = "-proposal__state"
    VALUE_5 = "-resource__name"
    VALUE_6 = "-resource__state"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class ProviderRequestedResourceOEnum(str, Enum):
    CREATED = "created"
    OFFERING_NAME = "offering__name"
    PROPOSAL_NAME = "proposal__name"
    RESOURCE_NAME = "resource__name"
    VALUE_0 = "-created"
    VALUE_1 = "-offering__name"
    VALUE_2 = "-proposal__name"
    VALUE_3 = "-resource__name"

    def __str__(self) -> str:
        return str(self.value)

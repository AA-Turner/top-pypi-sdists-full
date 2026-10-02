from enum import Enum


class AccessSubnetImpactAddressSourceEnum(str, Enum):
    ORGANIZATION = "organization"
    PROVIDER_DEFAULT = "provider_default"

    def __str__(self) -> str:
        return str(self.value)

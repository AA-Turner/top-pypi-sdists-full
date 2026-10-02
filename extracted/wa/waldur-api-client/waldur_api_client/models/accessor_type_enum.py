from enum import Enum


class AccessorTypeEnum(str, Enum):
    ORGANIZATION_MEMBER = "organization_member"
    SELF = "self"
    SERVICE_PROVIDER = "service_provider"
    STAFF = "staff"
    SUPPORT = "support"

    def __str__(self) -> str:
        return str(self.value)

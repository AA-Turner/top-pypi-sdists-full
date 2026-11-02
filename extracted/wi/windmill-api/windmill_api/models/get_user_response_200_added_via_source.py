from enum import Enum


class GetUserResponse200AddedViaSource(str, Enum):
    DOMAIN = "domain"
    INSTANCE_GROUP = "instance_group"
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)

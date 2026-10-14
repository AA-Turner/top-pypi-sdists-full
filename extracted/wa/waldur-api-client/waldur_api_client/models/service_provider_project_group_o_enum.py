from enum import Enum


class ServiceProviderProjectGroupOEnum(str, Enum):
    CREATED = "created"
    GID = "gid"
    MODIFIED = "modified"
    NAME = "name"
    VALUE_0 = "-created"
    VALUE_1 = "-gid"
    VALUE_2 = "-modified"
    VALUE_3 = "-name"

    def __str__(self) -> str:
        return str(self.value)

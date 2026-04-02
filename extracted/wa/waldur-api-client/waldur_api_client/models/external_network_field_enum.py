from enum import Enum


class ExternalNetworkFieldEnum(str, Enum):
    BACKEND_ID = "backend_id"
    DESCRIPTION = "description"
    IS_DEFAULT = "is_default"
    IS_SHARED = "is_shared"
    NAME = "name"
    SETTINGS = "settings"
    STATUS = "status"
    SUBNETS = "subnets"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

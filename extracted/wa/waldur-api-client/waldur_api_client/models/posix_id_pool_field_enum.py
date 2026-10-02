from enum import Enum


class PosixIdPoolFieldEnum(str, Enum):
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_UUID = "customer_uuid"
    DESCRIPTION = "description"
    GID_USED = "gid_used"
    GID_UTILIZATION = "gid_utilization"
    MAX_GID = "max_gid"
    MAX_UID = "max_uid"
    MIN_GID = "min_gid"
    MIN_UID = "min_uid"
    NEXT_GID = "next_gid"
    NEXT_UID = "next_uid"
    OFFERING = "offering"
    SCOPE = "scope"
    SERVICE_PROVIDER = "service_provider"
    UID_USED = "uid_used"
    UID_UTILIZATION = "uid_utilization"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

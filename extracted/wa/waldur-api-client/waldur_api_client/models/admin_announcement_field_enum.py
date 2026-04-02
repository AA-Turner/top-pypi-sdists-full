from enum import Enum


class AdminAnnouncementFieldEnum(str, Enum):
    ACTIVE_FROM = "active_from"
    ACTIVE_TO = "active_to"
    CREATED = "created"
    DESCRIPTION = "description"
    IS_ACTIVE = "is_active"
    MAINTENANCE_AFFECTED_OFFERINGS = "maintenance_affected_offerings"
    MAINTENANCE_EXTERNAL_REFERENCE_URL = "maintenance_external_reference_url"
    MAINTENANCE_NAME = "maintenance_name"
    MAINTENANCE_SCHEDULED_END = "maintenance_scheduled_end"
    MAINTENANCE_SCHEDULED_START = "maintenance_scheduled_start"
    MAINTENANCE_SERVICE_PROVIDER = "maintenance_service_provider"
    MAINTENANCE_STATE = "maintenance_state"
    MAINTENANCE_TYPE = "maintenance_type"
    MAINTENANCE_UUID = "maintenance_uuid"
    TYPE = "type"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

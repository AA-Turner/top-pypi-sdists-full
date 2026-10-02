from enum import Enum


class RobotAccountDetailsFieldEnum(str, Enum):
    BACKEND_ID = "backend_id"
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_UUID = "customer_uuid"
    DESCRIPTION = "description"
    ERROR_MESSAGE = "error_message"
    ERROR_TRACEBACK = "error_traceback"
    FINGERPRINTS = "fingerprints"
    KEYS = "keys"
    MODIFIED = "modified"
    OFFERING_PLUGIN_OPTIONS = "offering_plugin_options"
    PROJECT_NAME = "project_name"
    PROJECT_UUID = "project_uuid"
    PROVIDER_NAME = "provider_name"
    PROVIDER_UUID = "provider_uuid"
    RESOURCE = "resource"
    RESOURCE_NAME = "resource_name"
    RESOURCE_UUID = "resource_uuid"
    RESPONSIBLE_USER = "responsible_user"
    STATE = "state"
    TYPE = "type"
    URL = "url"
    USERNAME = "username"
    USERS = "users"
    USER_KEYS = "user_keys"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

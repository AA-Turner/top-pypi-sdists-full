from enum import Enum


class FirecrestJobFieldEnum(str, Enum):
    ACCESS_URL = "access_url"
    BACKEND_ID = "backend_id"
    CREATED = "created"
    CUSTOMER = "customer"
    CUSTOMER_ABBREVIATION = "customer_abbreviation"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_NATIVE_NAME = "customer_native_name"
    CUSTOMER_UUID = "customer_uuid"
    DESCRIPTION = "description"
    ERROR_MESSAGE = "error_message"
    ERROR_TRACEBACK = "error_traceback"
    FILE = "file"
    MODIFIED = "modified"
    NAME = "name"
    PROJECT = "project"
    PROJECT_NAME = "project_name"
    PROJECT_UUID = "project_uuid"
    REPORT = "report"
    RESOURCE_TYPE = "resource_type"
    RUNTIME_STATE = "runtime_state"
    SERVICE_NAME = "service_name"
    SERVICE_SETTINGS = "service_settings"
    SERVICE_SETTINGS_ERROR_MESSAGE = "service_settings_error_message"
    SERVICE_SETTINGS_STATE = "service_settings_state"
    SERVICE_SETTINGS_UUID = "service_settings_uuid"
    STATE = "state"
    URL = "url"
    USER = "user"
    USER_USERNAME = "user_username"
    USER_UUID = "user_uuid"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

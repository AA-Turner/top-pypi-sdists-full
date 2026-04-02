from enum import Enum


class ServiceSettingsFieldEnum(str, Enum):
    CUSTOMER = "customer"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_NATIVE_NAME = "customer_native_name"
    ERROR_MESSAGE = "error_message"
    NAME = "name"
    OPTIONS = "options"
    SCOPE = "scope"
    SCOPE_UUID = "scope_uuid"
    SHARED = "shared"
    STATE = "state"
    TERMS_OF_SERVICES = "terms_of_services"
    TYPE = "type"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

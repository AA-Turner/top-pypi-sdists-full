from enum import Enum


class ServiceProviderAccountFieldEnum(str, Enum):
    CREATED = "created"
    HOME_DIRECTORY = "home_directory"
    IS_RESTRICTED = "is_restricted"
    LOGIN_SHELL = "login_shell"
    MODIFIED = "modified"
    OFFERING_COUNT = "offering_count"
    PRIMARYGROUP = "primarygroup"
    RUNTIME_STATE = "runtime_state"
    SERVICE_PROVIDER = "service_provider"
    SERVICE_PROVIDER_COMMENT = "service_provider_comment"
    SERVICE_PROVIDER_COMMENT_URL = "service_provider_comment_url"
    SERVICE_PROVIDER_NAME = "service_provider_name"
    SERVICE_PROVIDER_UUID = "service_provider_uuid"
    STATE = "state"
    UIDNUMBER = "uidnumber"
    URL = "url"
    USER = "user"
    USERNAME = "username"
    USER_EMAIL = "user_email"
    USER_FULL_NAME = "user_full_name"
    USER_USERNAME = "user_username"
    USER_UUID = "user_uuid"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

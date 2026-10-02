from enum import Enum


class ProjectPermissionLogFieldEnum(str, Enum):
    CREATED = "created"
    CREATED_BY = "created_by"
    CREATED_BY_FULL_NAME = "created_by_full_name"
    CREATED_BY_USERNAME = "created_by_username"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_UUID = "customer_uuid"
    EXPIRATION_TIME = "expiration_time"
    PROJECT = "project"
    PROJECT_CREATED = "project_created"
    PROJECT_END_DATE = "project_end_date"
    PROJECT_NAME = "project_name"
    PROJECT_UUID = "project_uuid"
    ROLE = "role"
    ROLE_NAME = "role_name"
    USER = "user"
    USER_EMAIL = "user_email"
    USER_FULL_NAME = "user_full_name"
    USER_NATIVE_NAME = "user_native_name"
    USER_USERNAME = "user_username"
    USER_UUID = "user_uuid"

    def __str__(self) -> str:
        return str(self.value)

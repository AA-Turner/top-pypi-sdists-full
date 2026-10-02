from enum import Enum


class UserRoleDetailsFieldEnum(str, Enum):
    CREATED = "created"
    CREATED_BY_FULL_NAME = "created_by_full_name"
    CREATED_BY_UUID = "created_by_uuid"
    EXPIRATION_TIME = "expiration_time"
    ROLE_NAME = "role_name"
    ROLE_UUID = "role_uuid"
    USER_EMAIL = "user_email"
    USER_FULL_NAME = "user_full_name"
    USER_IMAGE = "user_image"
    USER_USERNAME = "user_username"
    USER_UUID = "user_uuid"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class CustomerUserFieldEnum(str, Enum):
    EMAIL = "email"
    EXPIRATION_TIME = "expiration_time"
    FULL_NAME = "full_name"
    IMAGE = "image"
    PROJECTS = "projects"
    ROLE_NAME = "role_name"
    URL = "url"
    USERNAME = "username"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

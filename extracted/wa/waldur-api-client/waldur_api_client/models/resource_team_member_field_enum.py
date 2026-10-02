from enum import Enum


class ResourceTeamMemberFieldEnum(str, Enum):
    EMAIL = "email"
    EXPIRATION_TIME = "expiration_time"
    FULL_NAME = "full_name"
    IMAGE = "image"
    RESOURCE_PROJECTS = "resource_projects"
    ROLES = "roles"
    ROLE_NAME = "role_name"
    ROLE_UUID = "role_uuid"
    URL = "url"
    USERNAME = "username"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

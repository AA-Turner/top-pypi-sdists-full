from enum import Enum


class SystemRole(str, Enum):
    # These are prefixed with 'system_' to differentiate from the org-level roles in Authz
    system_admin = "system_admin"
    system_user = "system_user"


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"
    read_only = "read_only"

from spotlight.api.permission.enum import PermissionType
from spotlight.core.common.base import Base


class PermissionRequest(Base):
    resource_id: str
    permission_type: PermissionType
    permission_id: str
    view: bool
    edit: bool
    delete: bool
    edit_permission: bool

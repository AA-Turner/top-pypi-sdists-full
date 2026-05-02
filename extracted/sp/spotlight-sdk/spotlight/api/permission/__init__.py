"""
Permission API.
"""

from spotlight.api.permission.asynchronous import (
    async_get_permission,
    async_get_permission_by_resource_id,
    async_get_permissions_by_resource_id,
    async_create_permission,
    async_update_permission,
    async_delete_permission,
)
from spotlight.api.permission.synchronous import (
    get_permission,
    get_permission_by_resource_id,
    get_permissions_by_resource_id,
    create_permission,
    update_permission,
    delete_permission,
)

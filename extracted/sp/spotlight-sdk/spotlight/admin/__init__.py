"""
Admin API.
"""

from spotlight.admin.asynchronous import (
    async_get_client_id,
    async_get_users,
    async_get_user,
    async_update_user,
    async_execute_actions_email,
    async_get_groups,
    async_get_group_members,
    async_add_group_to_user,
    async_delete_group_from_user,
    async_get_roles,
    async_get_roles_for_user,
    async_add_role_mapping_to_user,
    async_get_offline_token,
    async_create_offline_token,
    async_update_offline_token,
    async_delete_offline_token,
    async_get_user_count,
)
from spotlight.admin.synchronous import (
    get_client_id,
    get_users,
    get_user,
    update_user,
    execute_actions_email,
    get_groups,
    get_group_members,
    add_group_to_user,
    delete_group_from_user,
    get_roles,
    get_roles_for_user,
    add_role_mapping_to_user,
    get_offline_token,
    create_offline_token,
    update_offline_token,
    delete_offline_token,
    get_user_count,
)

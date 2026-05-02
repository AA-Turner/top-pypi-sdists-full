"""
Asynchronous admin API requests.
"""

from typing import List, Dict, Optional

from spotlight.admin.__util import (
    _get_client_id_request_info,
    _get_users_request_info,
    _get_user_request_info,
    _update_user_request_info,
    _get_groups_request_info,
    _get_group_members_request_info,
    _add_group_to_user_request_info,
    _delete_group_from_user_request_info,
    _get_roles_request_info,
    _get_roles_for_user_request_info,
    _add_role_mapping_to_user_request_info,
    _execute_actions_email_request_info,
    _delete_offline_token_request_info,
    _update_offline_token_request_info,
    _create_offline_token_request_info,
    _get_offline_token_request_info,
    _get_user_count_request_info,
)
from spotlight.core.common.decorators import async_data_request
from spotlight.core.common.function import no_transform
from spotlight.core.common.requests import (
    __async_get_request,
    __async_put_request,
    __async_post_request,
    __async_delete_request,
)


@async_data_request(transformers=[no_transform])
async def async_get_client_id():
    """
    Asynchronously get keycloak client ID.

    Returns:
        Keycloak client ID.
    """
    request_info = _get_client_id_request_info()
    return await __async_get_request(**request_info)


@async_data_request
async def async_get_users(limit: int = 500, page_offset: int = 0):
    """
    Asynchronously get all users.

    Returns:
        List of user response.
    """
    request_info = _get_users_request_info(limit, page_offset)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_user_count():
    """
    Get the total number of users.

    Returns:
        The total number of users.
    """
    request_info = _get_user_count_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_user(user_id: str):
    """
    Asynchronously get user by ID.

    Args:
        user_id (str): User ID

    Returns:
        User response
    """
    request_info = _get_user_request_info(user_id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform], processor=lambda r: r)
def async_execute_actions_email(
    user_id: str, actions: List[str], client_id: str, redirect_uri: str
):
    """
    Asynchronously update user.

    Args:
        user_id (str): User ID
        actions: (List[str]): Required user actions
        client_id: (str): Client ID
        redirect_uri: (str): Redirect URI after executing actions

    Returns:
        User response
    """
    request_info = _execute_actions_email_request_info(
        user_id, actions, client_id, redirect_uri
    )
    return __async_put_request(**request_info)


@async_data_request(transformers=[no_transform], processor=lambda r: r)
async def async_update_user(user_id: str, data: dict):
    """
    Asynchronously update user.

    Args:
        user_id (str): User ID
        data (dict): User request

    Returns:
        User response
    """
    request_info = _update_user_request_info(user_id, data)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_groups():
    """
    Asynchronously get groups.

    Returns:
        List of groups.
    """
    request_info = _get_groups_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_group_members(id: str):
    """
    Asynchronously get group members given group ID.

    Args:
        id (str): Group ID

    Returns:
        List of user response
    """
    request_info = _get_group_members_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform], processor=lambda r: r)
async def async_add_group_to_user(user_id: str, group_id: str):
    """
    Asynchronously add user to group.

    Args:
        user_id (str): User ID
        group_id (str): Group ID

    Returns:
        None
    """
    request_info = _add_group_to_user_request_info(user_id, group_id)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform], processor=lambda r: r)
async def async_delete_group_from_user(user_id: str, group_id: str):
    """
    Asynchronously delete user from group.

    Args:
        user_id (str): User ID
        group_id (str): Group ID

    Returns:
        None
    """
    request_info = _delete_group_from_user_request_info(user_id, group_id)
    return await __async_delete_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_roles():
    """
    Asynchronously get roles.

    Returns:
        List of role response.
    """
    request_info = _get_roles_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_roles_for_user(user_id: str):
    """
    Asynchronously get roles for user.

    Args:
        user_id (str): User ID

    Returns:
        List of role response
    """
    request_info = _get_roles_for_user_request_info(user_id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform], processor=lambda r: r)
async def async_add_role_mapping_to_user(user_id: str, role_ids: List[Dict[str, str]]):
    """
    Asynchronously add role mapping to user.

    Args:
        user_id (str): User ID
        role_ids (List[Dict[str, str]]): List of role ID mapping

    Returns:
        None
    """
    request_info = _add_role_mapping_to_user_request_info(user_id, role_ids)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_offline_token(user_id: str) -> dict:
    """
    Asynchronously get offline token for user.

    Args:
        user_id (str): User ID

    Returns:
        dict: Offline token response
    """
    request_info = _get_offline_token_request_info(user_id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_create_offline_token(
    user_id: str, refresh_token: str, exp: Optional[int] = None
) -> dict:
    """
    Asynchronously create offline token for user.

    Args:
        user_id (str): User ID
        refresh_token (str): Refresh token
        exp: (Optional[Int]): Expiration timestamp

    Returns:
        dict: Offline token response
    """
    request_info = _create_offline_token_request_info(user_id, refresh_token, exp)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_update_offline_token(
    user_id: str, refresh_token: str, exp: Optional[int] = None
) -> dict:
    """
    Asynchronously update offline token for user.

    Args:
        user_id (str): User ID
        refresh_token (str): Refresh token
        exp: (Optional[Int]): Expiration timestamp

    Returns:
        dict: Offline token response
    """
    request_info = _update_offline_token_request_info(user_id, refresh_token, exp)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_delete_offline_token(user_id: str) -> None:
    """
    Asynchronously delete offline token for user.

    Args:
        user_id (str): User ID

    Returns:
        None
    """
    request_info = _delete_offline_token_request_info(user_id)
    return await __async_delete_request(**request_info)

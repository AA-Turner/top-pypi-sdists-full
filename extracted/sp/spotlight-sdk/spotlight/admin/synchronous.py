"""
Admin API requests.
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
    _create_offline_token_request_info,
    _update_offline_token_request_info,
    _get_offline_token_request_info,
    _delete_offline_token_request_info,
    _get_user_count_request_info,
)
from spotlight.core.common.decorators import data_request
from spotlight.core.common.function import no_transform
from spotlight.core.common.requests import (
    __get_request,
    __put_request,
    __post_request,
    __delete_request,
)


@data_request(transformers=[no_transform])
def get_client_id():
    """
    Get keycloak client ID.

    Returns:
        Keycloak client ID.
    """
    request_info = _get_client_id_request_info()
    return __get_request(**request_info)


@data_request
def get_users(limit: int = 500, page_offset: int = 0):
    """
    Get all users.

    Returns:
        List of user response.
    """
    request_info = _get_users_request_info(limit, page_offset)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_user_count():
    """
    Get the total number of users.

    Returns:
        The total number of users.
    """
    request_info = _get_user_count_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_user(user_id: str):
    """
    Get user by ID.

    Args:
        user_id (str): User ID

    Returns:
        User response
    """
    request_info = _get_user_request_info(user_id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform], processor=lambda r: r)
def execute_actions_email(
    user_id: str, actions: List[str], client_id: str, redirect_uri: str
):
    """
    Update user.

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
    return __put_request(**request_info)


@data_request(transformers=[no_transform], processor=lambda r: r)
def update_user(user_id: str, data: dict):
    """
    Update user.

    Args:
        user_id (str): User ID
        data (dict): User request

    Returns:
        User response
    """
    request_info = _update_user_request_info(user_id, data)
    return __put_request(**request_info)


@data_request(transformers=[no_transform])
def get_groups():
    """
    Get groups.

    Returns:
        List of groups.
    """
    request_info = _get_groups_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_group_members(id: str):
    """
    Get group members given group ID.

    Args:
        id (str): Group ID

    Returns:
        List of user response
    """
    request_info = _get_group_members_request_info(id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform], processor=lambda r: r)
def add_group_to_user(user_id: str, group_id: str):
    """
    Add user to group.

    Args:
        user_id (str): User ID
        group_id (str): Group ID

    Returns:
        None
    """
    request_info = _add_group_to_user_request_info(user_id, group_id)
    return __put_request(**request_info)


@data_request(transformers=[no_transform], processor=lambda r: r)
def delete_group_from_user(user_id: str, group_id: str):
    """
    Delete user from group.

    Args:
        user_id (str): User ID
        group_id (str): Group ID

    Returns:
        None
    """
    request_info = _delete_group_from_user_request_info(user_id, group_id)
    return __delete_request(**request_info)


@data_request(transformers=[no_transform])
def get_roles():
    """
    Get roles.

    Returns:
        List of role response.
    """
    request_info = _get_roles_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_roles_for_user(user_id: str):
    """
    Get roles for user.

    Args:
        user_id (str): User ID

    Returns:
        List of role response
    """
    request_info = _get_roles_for_user_request_info(user_id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform], processor=lambda r: r)
def add_role_mapping_to_user(user_id: str, role_ids: List[Dict[str, str]]):
    """
    Add role mapping to user.

    Args:
        user_id (str): User ID
        role_ids (List[Dict[str, str]]): List of role ID mapping

    Returns:
        None
    """
    request_info = _add_role_mapping_to_user_request_info(user_id, role_ids)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def get_offline_token(user_id: str) -> dict:
    """
    Get offline token for user.

    Args:
        user_id (str): User ID

    Returns:
        dict: Offline token response
    """
    request_info = _get_offline_token_request_info(user_id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def create_offline_token(
    user_id: str, refresh_token: str, exp: Optional[int] = None
) -> dict:
    """
    Create offline token for user.

    Args:
        user_id (str): User ID
        refresh_token (str): Refresh token
        exp: (Optional[Int]): Expiration timestamp

    Returns:
        dict: Offline token response
    """
    request_info = _create_offline_token_request_info(user_id, refresh_token, exp)
    return __put_request(**request_info)


@data_request(transformers=[no_transform])
def update_offline_token(
    user_id: str, refresh_token: str, exp: Optional[int] = None
) -> dict:
    """
    Update offline token for user.

    Args:
        user_id (str): User ID
        refresh_token (str): Refresh token
        exp: (Optional[Int]): Expiration timestamp

    Returns:
        dict: Offline token response
    """
    request_info = _update_offline_token_request_info(user_id, refresh_token, exp)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def delete_offline_token(user_id: str) -> None:
    """
    Delete offline token for user.

    Args:
        user_id (str): User ID

    Returns:
        None
    """
    request_info = _delete_offline_token_request_info(user_id)
    return __delete_request(**request_info)

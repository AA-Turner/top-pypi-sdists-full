from typing import List, Dict, Optional


def _get_client_id_request_info() -> dict:
    return {
        "endpoint": "clients?clientId=realm-management",
        "url_key": "keycloak_admin",
    }


def _get_users_request_info(limit: int, page_offset: int) -> dict:
    return {
        "endpoint": "users",
        "params": {"max": limit, "first": page_offset},
        "url_key": "keycloak_admin",
    }


def _get_user_count_request_info() -> dict:
    return {"endpoint": f"users/count", "url_key": "keycloak_admin"}


def _get_user_request_info(user_id: str) -> dict:
    return {"endpoint": f"users/{user_id}", "url_key": "keycloak_admin"}


def _execute_actions_email_request_info(
    user_id: str, actions: List[str], client_id: str, redirect_uri: str
) -> dict:
    return {
        "endpoint": f"users/{user_id}/execute-actions-email",
        "params": {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "lifespan": 604800,
        },
        "url_key": "keycloak_admin",
        "json": actions,
    }


def _update_user_request_info(user_id: str, data: dict) -> dict:
    return {"endpoint": f"users/{user_id}", "url_key": "keycloak_admin", "json": data}


def _get_groups_request_info() -> dict:
    return {"endpoint": "groups", "url_key": "keycloak_admin"}


def _get_group_members_request_info(id: str) -> dict:
    return {"endpoint": f"groups/{id}/members", "url_key": "keycloak_admin"}


def _add_group_to_user_request_info(user_id: str, group_id: str) -> dict:
    return {
        "endpoint": f"users/{user_id}/groups/{group_id}",
        "url_key": "keycloak_admin",
    }


def _delete_group_from_user_request_info(user_id: str, group_id: str) -> dict:
    return {
        "endpoint": f"users/{user_id}/groups/{group_id}",
        "url_key": "keycloak_admin",
    }


def _get_roles_request_info() -> dict:
    return {"endpoint": "roles", "url_key": "keycloak_admin"}


def _get_roles_for_user_request_info(user_id: str) -> dict:
    return {"endpoint": f"users/{user_id}/role-mappings", "url_key": "keycloak_admin"}


def _add_role_mapping_to_user_request_info(
    user_id: str, role_ids: List[Dict[str, str]]
) -> dict:
    return {
        "endpoint": f"users/{user_id}/role-mappings/realm",
        "url_key": "keycloak_admin",
        "json": role_ids,
    }


def _get_offline_token_request_info(user_id: str) -> dict:
    return {"endpoint": f"config/offline_token/{user_id}"}


def _create_offline_token_request_info(
    user_id: str, refresh_token: str, exp: Optional[int] = None
) -> dict:
    return {
        "endpoint": f"config/offline_token",
        "json": {"user_id": user_id, "refresh_token": refresh_token, "exp": exp},
    }


def _update_offline_token_request_info(
    user_id: str, refresh_token: str, exp: Optional[int] = None
) -> dict:
    return {
        "endpoint": f"config/offline_token/{user_id}",
        "json": {"user_id": user_id, "refresh_token": refresh_token, "exp": exp},
    }


def _delete_offline_token_request_info(user_id: str) -> dict:
    return {"endpoint": f"config/offline_token/{user_id}"}

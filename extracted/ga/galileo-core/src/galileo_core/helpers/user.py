from functools import partial
from typing import List, Optional
from urllib.parse import parse_qs, urlparse

from pydantic import UUID4

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.helpers.pagination import paginated_request
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.auth_method import AuthMethod
from galileo_core.schemas.core.user import (
    CreateUserRequest,
    CreateUserResponse,
    InviteUsersRequest,
    UpdateUserRoleRequest,
    User,
)
from galileo_core.schemas.core.user_role import UserRole


def get_sign_up_token(
    email: str,
    config: Optional[GalileoConfig] = None,
) -> str:
    """
    Get an access token from a signup link for a new user.

    Parameters
    ----------
    email: str
        The user's email address.

    Returns
    -------
    str
        A JWT access token as a string.

    Raises
    ------
    ValueError
        If authentication fails or the token cannot be retrieved.
    """
    config = config or GalileoConfig.get()

    response = config.api_client.request(
        RequestMethod.POST,
        Routes.signup_link,
        params={"user_email": email},
    )

    parsed_url = urlparse(response["signup_url"])
    query_params = parse_qs(parsed_url.query)
    token = query_params.get("token", [None])[0]

    if not token:
        raise ValueError("Token not found in URL.")
    return token


def create_user(
    email: str,
    password: str,
    auth_method: AuthMethod = AuthMethod.email,
    role: UserRole = UserRole.read_only,
    config: Optional[GalileoConfig] = None,
) -> CreateUserResponse:
    """
    Create user.

    Parameters
    ----------
    email: str
        The user's email address.

    password: str
        The user's password.

    auth_method: AuthMethod = AuthMethod.email
        The method of authentication for the user.

    role: UserRole = UserRole.read_only
        The user's assigned role.


    Returns
    -------
    CreateUserResponse
        Created user.
    """
    config = config or GalileoConfig.get()
    logger.debug("Creating a new user...")

    new_user = CreateUserRequest(
        email=email,
        auth_method=auth_method,
        password=password,
        role=role,
    )
    sign_up_token = get_sign_up_token(email=email, config=config)

    response_dict = config.api_client.request(
        RequestMethod.POST, Routes.users, json=new_user.model_dump(mode="json"), params={"signup_token": sign_up_token}
    )
    user = CreateUserResponse.model_validate(response_dict)
    logger.debug(f"Created user {str(user.id)} with role {user.role.value}.")
    return user


def get_current_user(config: Optional[GalileoConfig] = None) -> User:
    """
    Get the current user.

    Returns
    -------
    User
        Current user.
    """
    config = config or GalileoConfig.get()
    logger.debug("Getting current user...")
    response_dict = config.api_client.request(RequestMethod.GET, Routes.current_user)
    user = User.model_validate(response_dict)
    logger.debug(f"Got current user {user.email}.")
    return user


def invite_users(
    emails: List[str],
    role: UserRole = UserRole.user,
    group_ids: Optional[List[UUID4]] = None,
    auth_method: AuthMethod = AuthMethod.email,
    config: Optional[GalileoConfig] = None,
) -> None:
    """
    Invite users.

    Parameters
    ----------
    emails : List[str]
        List of emails to invite.
    role : UserRole, optional
        Roles to grant invited users, by default UserRole.user
    group_ids : Optional[List[UUID4]], optional
        Group IDs to add the users to, by default None, which means they are not added to any group.
    auth_method : AuthMethod, optional
        Authentication method to use, by default AuthMethod.email
    """
    config = config or GalileoConfig.get()
    group_ids = group_ids or list()
    request = InviteUsersRequest(emails=emails, role=role, group_ids=group_ids, auth_method=auth_method)
    logger.debug(f"Inviting users {request.emails} with role {request.role}...")
    config.api_client.request(RequestMethod.POST, Routes.invite_users, json=request.model_dump(mode="json"))
    logger.debug(f"Invited users {request.emails} with role {request.role}.")


def list_users(config: Optional[GalileoConfig] = None) -> List[User]:
    """
    List all users.

    Returns
    -------
    List[User]
        List of all users.
    """
    config = config or GalileoConfig.get()
    logger.debug("Listing users...")
    all_users = paginated_request(partial(config.api_client.request, RequestMethod.GET, Routes.users), "users")
    users = [User.model_validate(user) for user in all_users]
    logger.debug(f"Listed all users, found {len(users)} users.")
    return users


def update_user(user_id: UUID4, role: UserRole, config: Optional[GalileoConfig] = None) -> User:
    """
    Update user.

    Parameters
    ----------
    user_id : User.id
        User ID to update.
    role : UserRole
        New role to assign to the user.

    Returns
    -------
    User
        Updated user.
    """
    config = config or GalileoConfig.get()
    logger.debug(f"Updating user {str(user_id)} to {role}...")

    request = UpdateUserRoleRequest(role=role)
    response_dict = config.api_client.request(
        RequestMethod.PUT, Routes.update_user.format(user_id=user_id), json=request.model_dump(mode="json")
    )
    user = User.model_validate(response_dict)
    logger.debug(f"Updated user {str(user_id)} role to {user.role.value}.")
    return user

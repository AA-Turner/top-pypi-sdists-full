from functools import partial
from typing import List, Optional

from pydantic import UUID4

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.helpers.pagination import paginated_request
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.group import (
    AddGroupMemberRequest,
    AddGroupMemberResponse,
    CreateGroupRequest,
    CreateGroupResponse,
)
from galileo_core.schemas.core.group_role import GroupRole
from galileo_core.schemas.core.group_visibility import GroupVisibility


def create_group(
    name: str,
    description: Optional[str] = None,
    visibility: GroupVisibility = GroupVisibility.public,
    config: Optional[GalileoConfig] = None,
) -> CreateGroupResponse:
    """
    Create a group.

    Parameters
    ----------
    name : str
        Name of the group.
    description : Optional[str], optional
        Description for the group, by default None
    visibility : GroupVisibility, optional
        Visiblity of the group, by default GroupVisibility.public

    Returns
    -------
    CreateGroupResponse
        Response object for the created group.
    """
    config = config or GalileoConfig.get()
    request = CreateGroupRequest(name=name, description=description, visibility=visibility)
    logger.debug(f"Creating group {request.name} with visibility {visibility}...")
    response_dict = config.api_client.request(RequestMethod.POST, Routes.groups, json=request.model_dump(mode="json"))
    group_response = CreateGroupResponse.model_validate(response_dict)
    logger.debug(f"Created group with name {group_response.name}, ID {group_response.id}.")
    return group_response


def list_groups(config: Optional[GalileoConfig] = None) -> List[CreateGroupResponse]:
    """
    List all groups for the user.

    Returns
    -------
    List[CreateGroupResponse]
        List of all groups.
    """
    config = config or GalileoConfig.get()
    logger.debug("Listing groups...")
    all_groups = paginated_request(partial(config.api_client.request, RequestMethod.GET, Routes.groups), "groups")
    groups = [CreateGroupResponse.model_validate(group) for group in all_groups]
    logger.debug(f"Listed all groups, found {len(groups)} groups.")
    return groups


def add_users_to_group(
    group_id: UUID4, user_ids: List[UUID4], role: GroupRole = GroupRole.member, config: Optional[GalileoConfig] = None
) -> List[AddGroupMemberResponse]:
    """
    Add users to a an existing group with the specified role.

    Parameters
    ----------
    group_id : UUID4
        Group ID.
    user_ids : List[UUID4]
        List of user IDs to add to the group.
    role : GroupRole
        Role of the user in the group, by default GroupRole.member.

    Returns
    -------
    List[AddGroupMemberResponse]
        List of responses for each user added to the group.
    """
    config = config or GalileoConfig.get()
    request = [AddGroupMemberRequest(user_id=user_id, role=role) for user_id in user_ids]
    logger.debug(f"Adding {len(request)} users to group {group_id} with role {role}...")
    response = config.api_client.request(
        RequestMethod.POST,
        Routes.group_members.format(group_id=group_id),
        json=[r.model_dump(mode="json") for r in request],
    )
    parsed_response = [AddGroupMemberResponse.model_validate(r) for r in response]
    logger.debug(f"Added {len(response)} users to group {group_id} with role {role}.")
    return parsed_response

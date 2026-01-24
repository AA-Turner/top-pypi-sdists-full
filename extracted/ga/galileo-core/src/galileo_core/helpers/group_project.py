from functools import partial
from typing import List, Optional

from pydantic import UUID4

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.helpers.pagination import paginated_request
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.collaboration_role import CollaboratorRole
from galileo_core.schemas.core.group_project import GroupProjectCollaboratorRequest, GroupProjectCollaboratorResponse


def share_project_with_group(
    project_id: UUID4,
    group_id: UUID4,
    role: CollaboratorRole = CollaboratorRole.viewer,
    config: Optional[GalileoConfig] = None,
) -> GroupProjectCollaboratorResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Sharing project {project_id} with group {group_id} with role {role}...")
    response_dict = config.api_client.request(
        RequestMethod.POST,
        Routes.project_groups.format(project_id=project_id),
        json=[GroupProjectCollaboratorRequest(group_id=group_id, role=role).model_dump(mode="json")],
    )
    group_collaborators = [GroupProjectCollaboratorResponse.model_validate(group) for group in response_dict]
    logger.debug(f"Shared project {project_id} with group {group_id} with role {role}.")
    return group_collaborators[0]


def unshare_project_with_group(
    project_id: UUID4,
    group_id: UUID4,
    config: Optional[GalileoConfig] = None,
) -> None:
    config = config or GalileoConfig.get()
    logger.debug(f"Removing access for group {group_id} from project {project_id}")
    config.api_client.request(
        RequestMethod.DELETE, Routes.project_group.format(project_id=project_id, group_id=group_id)
    )
    logger.debug(f"Access for group {group_id} removed from project {project_id}.")


def list_group_project_collaborators(
    project_id: UUID4, config: Optional[GalileoConfig] = None
) -> List[GroupProjectCollaboratorResponse]:
    config = config or GalileoConfig.get()
    logger.debug("Listing groups the project has been shared with…")
    group_project_collaborators = paginated_request(
        partial(config.api_client.request, RequestMethod.GET, Routes.project_groups.format(project_id=project_id)),
        "collaborators",
    )
    groups = [GroupProjectCollaboratorResponse.model_validate(group) for group in group_project_collaborators]
    logger.debug(f"Listed all groups, found {len(groups)} groups.")
    return groups


def update_group_project_collaborator(
    project_id: UUID4,
    group_id: UUID4,
    role: CollaboratorRole = CollaboratorRole.viewer,
    config: Optional[GalileoConfig] = None,
) -> GroupProjectCollaboratorResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Updating project {project_id}: assigning role {role} to group {group_id}…")
    response_dict = config.api_client.request(
        RequestMethod.PATCH,
        Routes.project_group.format(project_id=project_id, group_id=group_id),
        json=GroupProjectCollaboratorRequest(group_id=group_id, role=role).model_dump(mode="json"),
    )
    group_project = GroupProjectCollaboratorResponse.model_validate(response_dict)
    logger.debug(f"Updated project {project_id}: assigned role {role} to group {group_id}…")
    return group_project

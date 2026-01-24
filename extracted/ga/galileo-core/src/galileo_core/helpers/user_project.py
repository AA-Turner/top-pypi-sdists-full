from functools import partial
from typing import List, Optional

from pydantic import UUID4

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.helpers.pagination import paginated_request
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.collaboration_role import CollaboratorRole
from galileo_core.schemas.core.user_project import UserProjectCollaboratorRequest, UserProjectCollaboratorResponse


def share_project_with_user(
    project_id: UUID4,
    user_id: UUID4,
    role: CollaboratorRole = CollaboratorRole.viewer,
    config: Optional[GalileoConfig] = None,
) -> UserProjectCollaboratorResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Sharing project {project_id} with user {user_id} with role {role}...")
    response_dict = config.api_client.request(
        RequestMethod.POST,
        Routes.project_users.format(project_id=project_id),
        json=[UserProjectCollaboratorRequest(user_id=user_id, role=role).model_dump(mode="json")],
    )
    user_shared = [UserProjectCollaboratorResponse.model_validate(user) for user in response_dict]
    logger.debug(f"Shared project {project_id} with user {user_id} with role {role}.")
    return user_shared[0]


def unshare_project_with_user(
    project_id: UUID4,
    user_id: UUID4,
    config: Optional[GalileoConfig] = None,
) -> None:
    config = config or GalileoConfig.get()
    logger.debug(f"Removing access for user {user_id} from project {project_id}")
    config.api_client.request(RequestMethod.DELETE, Routes.project_user.format(project_id=project_id, user_id=user_id))
    logger.debug(f"Access for user {user_id} removed from project {project_id}.")


def list_user_project_collaborators(
    project_id: UUID4, config: Optional[GalileoConfig] = None
) -> List[UserProjectCollaboratorResponse]:
    config = config or GalileoConfig.get()
    logger.debug("Listing users the project has been shared with…")
    user_project_collaborators = paginated_request(
        partial(config.api_client.request, RequestMethod.GET, Routes.project_users.format(project_id=project_id)),
        "collaborators",
    )
    users = [UserProjectCollaboratorResponse.model_validate(user) for user in user_project_collaborators]
    logger.debug(f"Listed all users, found {len(users)} users.")
    return users


def update_user_project_collaborator(
    project_id: UUID4,
    user_id: UUID4,
    role: CollaboratorRole = CollaboratorRole.viewer,
    config: Optional[GalileoConfig] = None,
) -> UserProjectCollaboratorResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Updating project {project_id}: assigning role {role} to user {user_id}…")
    response_dict = config.api_client.request(
        RequestMethod.PATCH,
        Routes.project_user.format(project_id=project_id, user_id=user_id),
        json=UserProjectCollaboratorRequest(user_id=user_id, role=role).model_dump(mode="json"),
    )
    user_project = UserProjectCollaboratorResponse.model_validate(response_dict)
    logger.debug(f"Updated project {project_id}: assigned role {role} to user {user_id}…")
    return user_project

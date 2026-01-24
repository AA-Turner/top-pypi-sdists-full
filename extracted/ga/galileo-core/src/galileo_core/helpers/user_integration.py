from functools import partial
from typing import List, Optional

from pydantic import UUID4

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.exceptions.http import GalileoHTTPException
from galileo_core.helpers.logger import logger
from galileo_core.helpers.pagination import paginated_request
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.collaboration_role import CollaboratorRole
from galileo_core.schemas.core.collaborator import UserCollaboratorCreate
from galileo_core.schemas.core.integration.user_integration import (
    UserIntegrationCollaboratorResponse,
)


def list_user_integration_collaborators(
    integration_id: UUID4,
    config: Optional[GalileoConfig] = None,
) -> List[UserIntegrationCollaboratorResponse]:
    config = config or GalileoConfig.get()
    logger.debug("Listing users the integration has been shared with…")
    user_integration_collaborators = paginated_request(
        partial(
            config.api_client.request, RequestMethod.GET, Routes.integration_users.format(integration_id=integration_id)
        ),
        "collaborators",
    )
    users = [UserIntegrationCollaboratorResponse.model_validate(user) for user in user_integration_collaborators]
    logger.debug(f"Listed all users, found {len(users)} users.")
    return users


def share_integration_with_user(
    integration_id: UUID4,
    user_id: UUID4,
    config: Optional[GalileoConfig] = None,
) -> UserIntegrationCollaboratorResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Sharing integration {integration_id} with user {user_id} with role {CollaboratorRole.viewer}...")
    response_dict = config.api_client.request(
        RequestMethod.POST,
        Routes.integration_users.format(integration_id=integration_id),
        json=[UserCollaboratorCreate(user_id=user_id).model_dump(mode="json")],
    )
    user_shared = [UserIntegrationCollaboratorResponse.model_validate(user) for user in response_dict]
    logger.debug(f"Shared integration {integration_id} with user {user_id} with role {CollaboratorRole.viewer}.")

    try:
        return user_shared[0]
    except IndexError:
        raise GalileoHTTPException(
            message="Galileo API returned empty response.",
            status_code=422,
            response_text=f"Response body {user_shared}",
        )


def update_user_integration_collaborator(
    integration_id: UUID4,
    user_id: UUID4,
    role: CollaboratorRole = CollaboratorRole.viewer,
    config: Optional[GalileoConfig] = None,
) -> UserIntegrationCollaboratorResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Updating integration {integration_id}: assigning role {role} to user {user_id}…")
    response_dict = config.api_client.request(
        RequestMethod.PATCH,
        Routes.integration_user.format(integration_id=integration_id, user_id=user_id),
        json=UserCollaboratorCreate(user_id=user_id, role=role).model_dump(mode="json"),
    )
    user_integration = UserIntegrationCollaboratorResponse.model_validate(response_dict)
    logger.debug(f"Updated integration {integration_id}: assigned role {role} to user {user_id}…")
    return user_integration


def delete_user_integration_collaborator(
    integration_id: UUID4,
    user_id: UUID4,
    config: Optional[GalileoConfig] = None,
) -> None:
    config = config or GalileoConfig.get()
    logger.debug(f"Removing access for user {user_id} from integration {integration_id}")
    config.api_client.request(
        RequestMethod.DELETE, Routes.integration_user.format(integration_id=integration_id, user_id=user_id)
    )
    logger.debug(f"Access for user {user_id} removed from integration {integration_id}.")

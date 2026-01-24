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
from galileo_core.schemas.core.collaborator import GroupCollaboratorCreate
from galileo_core.schemas.core.integration.group_integration import (
    GroupIntegrationCollaboratorResponse,
)


def list_group_integration_collaborators(
    integration_id: UUID4,
    config: Optional[GalileoConfig] = None,
) -> List[GroupIntegrationCollaboratorResponse]:
    config = config or GalileoConfig.get()
    logger.debug("Listing groups the integration has been shared with…")
    group_integration_collaborators = paginated_request(
        partial(
            config.api_client.request,
            RequestMethod.GET,
            Routes.integration_groups.format(integration_id=integration_id),
        ),
        "collaborators",
    )
    groups = [GroupIntegrationCollaboratorResponse.model_validate(group) for group in group_integration_collaborators]
    logger.debug(f"Listed all groups, found {len(groups)} groups.")
    return groups


def share_integration_with_group(
    integration_id: UUID4,
    group_id: UUID4,
    config: Optional[GalileoConfig] = None,
) -> GroupIntegrationCollaboratorResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Sharing integration {integration_id} with group {group_id} with role {CollaboratorRole.viewer}...")
    response_dict = config.api_client.request(
        RequestMethod.POST,
        Routes.integration_groups.format(integration_id=integration_id),
        json=[GroupCollaboratorCreate(group_id=group_id).model_dump(mode="json")],
    )
    group_shared = [GroupIntegrationCollaboratorResponse.model_validate(group) for group in response_dict]
    logger.debug(f"Shared integration {integration_id} with group {group_id} with role {CollaboratorRole.viewer}.")

    try:
        return group_shared[0]
    except IndexError:
        raise GalileoHTTPException(
            message="Galileo API returned empty response.",
            status_code=422,
            response_text=f"Response body {group_shared}",
        )


def update_group_integration_collaborator(
    integration_id: UUID4,
    group_id: UUID4,
    role: CollaboratorRole = CollaboratorRole.viewer,
    config: Optional[GalileoConfig] = None,
) -> GroupIntegrationCollaboratorResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Updating integration {integration_id}: assigning role {role} to group {group_id}…")
    response_dict = config.api_client.request(
        RequestMethod.PATCH,
        Routes.integration_group.format(integration_id=integration_id, group_id=group_id),
        json=GroupCollaboratorCreate(group_id=group_id, role=role).model_dump(mode="json"),
    )
    group_integration = GroupIntegrationCollaboratorResponse.model_validate(response_dict)
    logger.debug(f"Updated integration {integration_id}: assigned role {role} to group {group_id}…")
    return group_integration


def delete_group_integration_collaborator(
    integration_id: UUID4,
    group_id: UUID4,
    config: Optional[GalileoConfig] = None,
) -> None:
    config = config or GalileoConfig.get()
    logger.debug(f"Removing access for group {group_id} from integration {integration_id}")
    config.api_client.request(
        RequestMethod.DELETE, Routes.integration_group.format(integration_id=integration_id, group_id=group_id)
    )
    logger.debug(f"Access for group {group_id} removed from integration {integration_id}.")

from datetime import datetime
from functools import partial
from typing import List, Optional

from pydantic import UUID4

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.helpers.pagination import paginated_request
from galileo_core.helpers.user import get_current_user
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.api_key import ApiKeyResponse, CreateApiKeyRequest, CreateApiKeyResponse
from galileo_core.schemas.core.collaboration_role import CollaboratorRole


def create_api_key(
    description: str,
    expires_at: Optional[datetime] = None,
    project_id: Optional[UUID4] = None,
    project_role: Optional[CollaboratorRole] = None,
    config: Optional[GalileoConfig] = None,
) -> CreateApiKeyResponse:
    config = config or GalileoConfig.get()
    logger.debug(f"Creating API key with description {description}...")
    response_dict = config.api_client.request(
        RequestMethod.POST,
        Routes.create_api_key,
        json=CreateApiKeyRequest(
            description=description, expires_at=expires_at, project_id=project_id, project_role=project_role
        ).model_dump(mode="json"),
    )
    response = CreateApiKeyResponse.model_validate(response_dict)
    logger.debug(f"Created API key {response.id} with description {description}.")
    return response


def list_api_keys(config: Optional[GalileoConfig] = None) -> List[ApiKeyResponse]:
    config = config or GalileoConfig.get()
    user = get_current_user()
    logger.debug(f"Listing API keys for user {user.email}...")
    response_dict = paginated_request(
        partial(config.api_client.request, RequestMethod.GET, Routes.get_api_keys.format(user_id=user.id)), "api_keys"
    )
    api_keys = [ApiKeyResponse.model_validate(api_key) for api_key in response_dict]
    logger.debug(f"Listed {len(api_keys)} API keys.")
    return api_keys


def delete_api_key(api_key_id: UUID4, config: Optional[GalileoConfig] = None) -> None:
    config = config or GalileoConfig.get()
    logger.debug(f"Deleting API key {api_key_id}...")
    config.api_client.request(RequestMethod.DELETE, Routes.delete_api_key.format(api_key_id=api_key_id))
    logger.debug(f"Deleted API key {api_key_id}.")

from typing import Dict, List, Optional

from pydantic import TypeAdapter

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.integration.anthropic_auth_type import AnthropicAuthenticationType
from galileo_core.schemas.core.integration.azure import DEFAULT_AZURE_API_VERSION, AzureModelDeployment
from galileo_core.schemas.core.integration.azure_auth_type import AzureAuthenticationType
from galileo_core.schemas.core.integration.base import (
    IntegrationResponse,
)
from galileo_core.schemas.core.integration.create_integration import CreateIntegrationModel
from galileo_core.schemas.core.integration.integration_type import LLMIntegration


def list_integrations(config: Optional[GalileoConfig] = None) -> List[IntegrationResponse]:
    """
    Returns all integrations that the user has access to.

    Returns
    -------
    List[IntegrationResponse]
        A list of integrations.
    """
    config = config or GalileoConfig.get()

    logger.debug("Getting integrations...")
    integrations = [
        IntegrationResponse.model_validate(integration)
        for integration in config.api_client.request(RequestMethod.GET, Routes.integrations)
    ]
    logger.debug(f"Got {len(integrations)} integrations.")
    return integrations


def create_or_update_integration(name: str, data: dict, config: Optional[GalileoConfig] = None) -> IntegrationResponse:
    """
    Create or update an integration.

    Parameters
    ----------
    name : str
        A name of the new integration.

    data: dict
        All additional data for the new integration.

    Returns
    -------
    IntegrationResponse
        Response object for the created or updated integration.
    """
    config = config or GalileoConfig.get()

    logger.debug(f"Creating integration with name {name}...")
    adapter: TypeAdapter[CreateIntegrationModel] = TypeAdapter(CreateIntegrationModel)
    validated_data = adapter.validate_python({"name": name, **data})

    response_dict = config.api_client.request(
        RequestMethod.PUT,
        Routes.create_update_integration.format(integration_name=name),
        json=validated_data.model_dump(),
    )
    integration_response = IntegrationResponse.model_validate(response_dict)
    logger.debug(f"Created integration with name {integration_response.name}, ID {integration_response.id}.")
    return integration_response


def create_or_update_openai_integration(
    api_key: str,
    organization_id: Optional[str] = None,
    config: Optional[GalileoConfig] = None,
) -> IntegrationResponse:
    """
    Create or update an OpenAI integration.

    Parameters
    ----------
    api_key : str
        OpenAI API key.
    organization_id : Optional[str], optional
        OpenAI organization ID, by default None.

    Returns
    -------
    IntegrationResponse
        Response object for the created or updated integration.
    """
    config = config or GalileoConfig.get()
    logger.debug("Creating OpenAI integration...")
    data = {"token": api_key, "organization_id": organization_id}
    return create_or_update_integration(LLMIntegration.openai, data, config)


def create_or_update_azure_integration(
    api_key: str,
    endpoint: str,
    proxy: bool = False,
    authentication_type: AzureAuthenticationType = AzureAuthenticationType.api_key,
    authentication_scope: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    api_version: str = DEFAULT_AZURE_API_VERSION,
    azure_deployment: Optional[str] = None,
    available_deployments: Optional[List[AzureModelDeployment]] = None,
    oauth2_token_url: Optional[str] = None,
    custom_header_mapping: Optional[Dict[str, str]] = None,
    config: Optional[GalileoConfig] = None,
) -> IntegrationResponse:
    """
    Create or update an Azure integration.

    Parameters
    ----------
    api_key : str
        Azure API key.
    endpoint : str
        The Azure OpenAI endpoint.
    proxy : bool, optional
        Whether to use a proxy when making requests, by default False.
    authentication_type : AzureAuthenticationType, optional
        Type of authentication to use.
    authentication_scope : Optional[str], optional
        Scope for authentication, if applicable.
    headers : Optional[dict[str, str]], optional
        Additional headers to include in requests.
    api_version : str, optional
        Azure API version to use, by default DEFAULT_AZURE_API_VERSION.
    azure_deployment : Optional[str], optional
        The default deployment name to use.
    available_deployments : Optional[List[AzureModelDeployment]], optional
        Predefined deployments to avoid querying Azure for them.
    oauth2_token_url : Optional[str], optional
        OAuth2 token URL for custom OAuth2 authentication, if applicable.
    custom_header_mapping : Optional[Dict[str, str]], optional
        Custom header mapping for the integration, by default None.

    Returns
    -------
    IntegrationResponse
        Response object for the created or updated integration.
    """
    config = config or GalileoConfig.get()
    logger.debug("Creating Azure integration...")
    data = {
        "token": api_key,
        "endpoint": endpoint,
        "proxy": proxy,
        "authentication_type": authentication_type,
        "authentication_scope": authentication_scope,
        "headers": headers,
        "api_version": api_version,
        "azure_deployment": azure_deployment,
        "available_deployments": available_deployments,
        "oauth2_token_url": oauth2_token_url,
        "custom_header_mapping": custom_header_mapping,
    }
    return create_or_update_integration(LLMIntegration.azure, data, config)


def create_or_update_vertex_ai_integration(token: str, config: Optional[GalileoConfig] = None) -> IntegrationResponse:
    """
    Create or update a Vertex AI integration.
    Parameters
    ----------
    token : str
        Vertex AI token.
    Returns
    -------
    IntegrationResponse
        Response object for the created or updated integration.
    """
    config = config or GalileoConfig.get()
    logger.debug("Creating Vertex AI integration...")
    data = {"token": token}
    return create_or_update_integration(LLMIntegration.vertex_ai, data, config)


def create_or_update_anthropic_integration(
    api_key: str,
    endpoint: Optional[str] = None,
    authentication_type: AnthropicAuthenticationType = AnthropicAuthenticationType.api_key,
    authentication_scope: Optional[str] = None,
    oauth2_token_url: Optional[str] = None,
    custom_header_mapping: Optional[Dict[str, str]] = None,
    config: Optional[GalileoConfig] = None,
) -> IntegrationResponse:
    """
    Create or update an Anthropic integration.

    Parameters
    ----------
    api_key : str
        Anthropic API key.
    authentication_type : AnthropicAuthenticationType
        Type of authentication to use. This should be `AnthropicAuthenticationType.api_key` for API key authentication or `AnthropicAuthenticationType.custom_oauth2` for custom OAuth2 authentication.
    authentication_scope : Optional[str], optional
        Scope for authentication, if applicable.
    oauth2_token_url : Optional[str], optional
        OAuth2 token URL for custom OAuth2 authentication, if applicable.
    custom_header_mapping : Optional[Dict[str, str]], optional
        Custom header mapping for the integration, by default None.

    Returns
    -------
    IntegrationResponse
        Response object for the created or updated integration.
    """
    config = config or GalileoConfig.get()
    logger.debug("Creating Anthropic integration...")
    data = {
        "token": api_key,
        "authentication_type": authentication_type,
        "endpoint": endpoint,
        "authentication_scope": authentication_scope,
        "oauth2_token_url": oauth2_token_url,
        "custom_header_mapping": custom_header_mapping,
    }
    return create_or_update_integration(LLMIntegration.anthropic, data, config)


def create_or_update_mistral_integration(api_key: str, config: Optional[GalileoConfig] = None) -> IntegrationResponse:
    """
    Create or update a Mistral integration.

    Parameters
    ----------
    api_key : str
        Mistral API key.

    Returns
    -------
    IntegrationResponse
        Response object for the created or updated integration.
    """
    config = config or GalileoConfig.get()
    logger.debug("Creating Mistral integration...")
    data = {"token": api_key}
    return create_or_update_integration(LLMIntegration.mistral, data, config)

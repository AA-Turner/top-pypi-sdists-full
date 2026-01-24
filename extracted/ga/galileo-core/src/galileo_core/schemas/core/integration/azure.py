from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from galileo_core.schemas.core.integration.azure_auth_type import AzureAuthenticationType
from galileo_core.schemas.core.integration.integration_type import LLMIntegration

DEFAULT_AZURE_API_VERSION = "2024-10-21"


class AzureModelDeployment(BaseModel):
    model: str = Field(description="The name of the model.")
    id: str = Field(description="The ID of the deployment.")

    model_config = ConfigDict(protected_namespaces=())


class AzureExtras(BaseModel):
    proxy: bool = False
    endpoint: str
    authentication_type: AzureAuthenticationType = AzureAuthenticationType.api_key
    authentication_scope: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    api_version: str = DEFAULT_AZURE_API_VERSION
    azure_deployment: Optional[str] = None
    available_deployments: Optional[List[AzureModelDeployment]] = Field(
        default=None,
        description="The available deployments for this integration."
        " If provided, we will not try to get this list from Azure.",
    )


class AzureIntegrationCreate(AzureExtras):
    name: Literal[LLMIntegration.azure] = LLMIntegration.azure
    token: str

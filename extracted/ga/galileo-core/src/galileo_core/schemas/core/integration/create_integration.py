from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from galileo_core.schemas.core.integration.anthropic import AnthropicIntegrationCreate
from galileo_core.schemas.core.integration.aws_bedrock import AwsBedrockIntegrationCreate
from galileo_core.schemas.core.integration.azure import AzureIntegrationCreate
from galileo_core.schemas.core.integration.mistral import MistralIntegrationCreate
from galileo_core.schemas.core.integration.open_ai import OpenAIIntegrationCreate
from galileo_core.schemas.core.integration.vertex_ai import VertexAIIntegrationCreate
from galileo_core.schemas.core.integration.writer import WriterIntegrationCreate

IntegrationUnion = Union[
    AnthropicIntegrationCreate,
    MistralIntegrationCreate,
    OpenAIIntegrationCreate,
    VertexAIIntegrationCreate,
    WriterIntegrationCreate,
    AzureIntegrationCreate,
    AwsBedrockIntegrationCreate,
]

CreateIntegrationModel = Annotated[IntegrationUnion, Field(discriminator="name")]

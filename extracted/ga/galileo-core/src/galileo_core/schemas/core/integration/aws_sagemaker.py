from typing import Literal

from galileo_core.schemas.core.integration.aws import BaseAwsIntegrationCreate
from galileo_core.schemas.core.integration.integration_type import LLMIntegration


class AwsSageMakerIntegrationCreate(BaseAwsIntegrationCreate):
    name: Literal[LLMIntegration.aws_sagemaker] = LLMIntegration.aws_sagemaker

from enum import Enum


class LLMIntegration(str, Enum):
    anthropic = "anthropic"
    azure = "azure"
    aws_bedrock = "aws_bedrock"
    aws_sagemaker = "aws_sagemaker"
    databricks = "databricks"
    vertex_ai = "vertex_ai"
    openai = "openai"
    writer = "writer"
    mistral = "mistral"
    nvidia = "nvidia"

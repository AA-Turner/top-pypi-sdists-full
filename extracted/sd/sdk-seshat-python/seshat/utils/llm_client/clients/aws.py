import os
from enum import StrEnum

from langchain_aws import ChatBedrock
from langchain_core.language_models import BaseChatModel


class BedrockModels(StrEnum):
    MISTRAL_SMALL = "mistral.mistral-small-2402-v1:0"
    MISTRAL_LARGE = "mistral.mistral-large-2402-v1:0"

    LLAMA_4_Maverick_17B_Instruct = "us.meta.llama4-maverick-17b-instruct-v1:0"
    LLAMA_4_Scout_17B_Instruct = "us.meta.llama4-scout-17b-instruct-v1:0"
    LLAMA3_3_70B_Instruct = "us.meta.llama3-3-70b-instruct-v1:0"
    LLAMA_3_2_1B_Instruct = "us.meta.llama3-2-1b-instruct-v1:0"
    LLAMA_3_2_3B_Instruct = "us.meta.llama3-2-3b-instruct-v1:0"
    LLAMA_3_1_8B_Instruct = "meta.llama3-1-8b-instruct-v1:0"

    AMAZON_Nova_Premier = "us.amazon.nova-premier-v1:0"
    AMAZON_Nova_Pro = "us.amazon.nova-pro-v1:0"
    AMAZON_Nova_Lite = "us.amazon.nova-lite-v1:0"
    AMAZON_Nova_Micro = "us.amazon.nova-micro-v1:0"

    CLAUDE_3_5_Haiku = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
    CLAUDE_3_Haiku = "us.anthropic.claude-3-haiku-20240307-v1:0"


def create_bedrock_client(model: BedrockModels, **kwargs) -> BaseChatModel:
    return ChatBedrock(
        model_id=model,
        region_name="us-east-1",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        **kwargs,
    )

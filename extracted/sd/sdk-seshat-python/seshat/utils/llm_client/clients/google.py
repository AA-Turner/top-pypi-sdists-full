import os
from enum import StrEnum

from langchain_core.language_models import BaseChatModel
from langchain_google_vertexai import ChatVertexAI


class GeminiModels(StrEnum):
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite-001"


def create_google_client(model: GeminiModels, **kwargs) -> BaseChatModel:
    # Extract Google-specific configs
    location = kwargs.pop("location", "us-east1")

    # Different authentication methods
    if creds_path := os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        # Using service account file
        return ChatVertexAI(
            model_name=model,
            credentials=creds_path,
            location=location,
            **kwargs,
        )
    elif project_id := os.environ.get("GOOGLE_CLOUD_PROJECT"):
        # Using default credentials (gcloud auth)
        return ChatVertexAI(
            model_name=model,
            project=project_id,
            location=location,
            api_transport="rest",
            **kwargs,
        )
    else:
        raise ValueError(
            "Either GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT must be set"
        )

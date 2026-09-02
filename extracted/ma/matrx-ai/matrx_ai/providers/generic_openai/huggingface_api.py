from __future__ import annotations

import os

from .generic_openai_api import GenericOpenAIChat

# HuggingFace Inference Endpoint — llama.cpp / TGI
HUGGINGFACE_BASE_URL = os.environ.get(
    "HUGGING_FACE_ENDPOINT_URL",
    "https://a2w7lbho0x93g7kf.us-east-1.aws.endpoints.huggingface.cloud",
)

HUGGINGFACE_BASE_URL_2 = os.environ.get(
    "HUGGING_FACE_ENDPOINT_URL",
    "https://erk5hn0yy0gcbvjw.us-east-1.aws.endpoints.huggingface.cloud",
)


class HuggingFaceChat(GenericOpenAIChat):
    """
    HuggingFace Inference Endpoint using the OpenAI-compatible API.

    Reads HUGGING_FACE_TOKEN_ID from the environment for auth and
    HUGGING_FACE_ENDPOINT_URL for the base URL (falls back to the
    current dedicated endpoint).
    """

    def __init__(self, debug: bool = False):
        super().__init__(
            base_url=HUGGINGFACE_BASE_URL,
            api_key_env="HUGGING_FACE_TOKEN_ID",
            provider_name="huggingface",
            debug=debug,
        )

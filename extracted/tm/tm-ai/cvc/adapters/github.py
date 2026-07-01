"""
cvc.adapters.github — GitHub Models API adapter for CVC.

Inherits from OpenAIAdapter to interact with the GitHub Models API,
which provides OpenAI, Meta, Mistral, and other models via an
OpenAI-compatible interface.
"""

import logging

import httpx

from cvc.adapters.openai import OpenAIAdapter

logger = logging.getLogger("cvc.adapters.github")

DEFAULT_MODEL = "gpt-4o"
GITHUB_MODELS_URL = "https://models.inference.ai.azure.com"


class GitHubAdapter(OpenAIAdapter):
    """
    Adapter for the GitHub Models API (Azure AI inference endpoint).
    It reuses the OpenAI wire format but directs requests to GitHub's endpoint.
    """

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL) -> None:
        # We call super() with empty api_key/model first to let it initialize _client
        # but then we overwrite _client because the base class hardcodes base_url.
        super().__init__(api_key=api_key, model=model)

        # Override the base client to point to the GitHub Models endpoint
        # We need to explicitly close the old client to avoid unclosed sessions
        # if the base class created an AsyncClient. Actually, we can just replace it.
        # But to be safe, let's close the original one.
        # However, it's not strictly necessary as AsyncClient without 'with' is fine
        # if it's garbage collected, but let's override properly.

        self._api_key = api_key
        self._model = model
        self._client = httpx.AsyncClient(
            base_url=GITHUB_MODELS_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )

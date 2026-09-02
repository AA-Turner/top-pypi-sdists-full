from __future__ import annotations

from matrx_ai.providers.generic_openai.generic_openai_api import GenericOpenAIChat


class MoonshotChat(GenericOpenAIChat):
    """Moonshot's OpenAI-compatible Chat Completions client."""

    def __init__(self) -> None:
        super().__init__(
            base_url="https://api.moonshot.ai",
            api_key_env="MOONSHOT_API_KEY",
            provider_name="moonshot",
        )

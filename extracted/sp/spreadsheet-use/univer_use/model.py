import os

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

def load_chat_model(model_name: str, **kwargs) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        model_name (str): retrieve from openrouter https://openrouter.ai/models.
    """

    extra_body = {
        "usage": {"include": True},
    }

    api_key = kwargs.get("api_key", os.getenv("OPENROUTER_API_KEY"))
    base_url = kwargs.get("base_url", os.getenv("OPENROUTER_ENDPOINT"))
    provider: str = "openai"  # openai compatible provider by default

    return init_chat_model(
        model_name,
        model_provider=provider,
        base_url=base_url,
        api_key=api_key,
        extra_body=extra_body,
    )

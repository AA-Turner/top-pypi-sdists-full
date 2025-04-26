try:
    import anthropic
except ImportError:
    raise ModuleNotFoundError("Please install the Anthropic SDK to use this feature: 'pip install anthropic'")

from posthoganalytics.ai.anthropic.anthropic import WrappedMessages
from posthoganalytics.ai.anthropic.anthropic_async import AsyncWrappedMessages
from posthoganalytics.client import Client as PostHogClient


class AnthropicBedrock(anthropic.AnthropicBedrock):
    """
    A wrapper around the Anthropic Bedrock SDK that automatically sends LLM usage events to PostHog.
    """

    _ph_client: PostHogClient

    def __init__(self, posthog_client: PostHogClient, **kwargs):
        super().__init__(**kwargs)
        self._ph_client = posthog_client
        self.messages = WrappedMessages(self)


class AsyncAnthropicBedrock(anthropic.AsyncAnthropicBedrock):
    """
    A wrapper around the Anthropic Bedrock SDK that automatically sends LLM usage events to PostHog.
    """

    _ph_client: PostHogClient

    def __init__(self, posthog_client: PostHogClient, **kwargs):
        super().__init__(**kwargs)
        self._ph_client = posthog_client
        self.messages = AsyncWrappedMessages(self)


class AnthropicVertex(anthropic.AnthropicVertex):
    """
    A wrapper around the Anthropic Vertex SDK that automatically sends LLM usage events to PostHog.
    """

    _ph_client: PostHogClient

    def __init__(self, posthog_client: PostHogClient, **kwargs):
        super().__init__(**kwargs)
        self._ph_client = posthog_client
        self.messages = WrappedMessages(self)


class AsyncAnthropicVertex(anthropic.AsyncAnthropicVertex):
    """
    A wrapper around the Anthropic Vertex SDK that automatically sends LLM usage events to PostHog.
    """

    _ph_client: PostHogClient

    def __init__(self, posthog_client: PostHogClient, **kwargs):
        super().__init__(**kwargs)
        self._ph_client = posthog_client
        self.messages = AsyncWrappedMessages(self)

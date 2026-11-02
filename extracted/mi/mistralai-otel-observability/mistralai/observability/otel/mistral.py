"""Mistral SDK adapters for provider-specific telemetry extraction."""

from collections.abc import Mapping, Sequence
from typing import cast

from mistralai.client.models.chatcompletionresponse import ChatCompletionResponse

from .mistralconv import mistral_choices_to_otel_output_messages, mistral_messages_to_otel_input_messages
from .models import ChatCompletionAdapter, EventAttributeValue, GenAiMessage


class MistralChatCompletionAdapter(ChatCompletionAdapter):
    """Extract GenAI telemetry fields from a Mistral chat completion response.

    The Mistral response contains response metadata, choices, and token usage,
    but it does not echo request messages. Callers pass input messages
    separately when they want content copied onto spans.
    """

    def __init__(
        self,
        response: object,
        *,
        input_messages: Sequence[object] | None = None,
    ) -> None:
        """Validate and keep the Mistral response plus optional request messages."""
        if not isinstance(response, ChatCompletionResponse):
            message = "response must be a mistralai ChatCompletionResponse"
            raise TypeError(message)

        self._response = response
        self._input_messages = input_messages

    @property
    def response_model(self) -> str:
        """Return the model reported by the Mistral response."""
        return self._response.model

    @property
    def response_id(self) -> str:
        """Return the provider response identifier."""
        return self._response.id

    @property
    def input_messages(self) -> Sequence[GenAiMessage] | None:
        """Convert caller-supplied Mistral request messages to GenAI messages."""
        if self._input_messages is None:
            return None
        if not all(isinstance(message, dict) for message in self._input_messages):
            message = "input_messages must contain Mistral chat completion request message dictionaries"
            raise TypeError(message)
        return mistral_messages_to_otel_input_messages(
            cast("Sequence[Mapping[str, EventAttributeValue]]", self._input_messages)
        )

    @property
    def output_messages(self) -> Sequence[GenAiMessage]:
        """Convert Mistral response choices to GenAI output messages."""
        choices = [
            cast("Mapping[str, EventAttributeValue]", choice.model_dump(mode="json", exclude_none=True))
            for choice in self._response.choices
        ]
        return mistral_choices_to_otel_output_messages(choices)

    @property
    def finish_reasons(self) -> Sequence[str]:
        """Return finish reasons from all completed choices."""
        return [str(choice.finish_reason) for choice in self._response.choices if choice.finish_reason]

    @property
    def input_tokens(self) -> int | None:
        """Return prompt token usage when Mistral reports it."""
        return self._response.usage.prompt_tokens

    @property
    def output_tokens(self) -> int | None:
        """Return completion token usage when Mistral reports it."""
        return self._response.usage.completion_tokens

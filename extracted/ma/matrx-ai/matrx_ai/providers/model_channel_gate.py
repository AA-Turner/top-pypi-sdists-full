"""A model that cannot answer a typed turn is REFUSED by name, never filed as a crash.

The catalog gives every model an execution channel. Realtime (live voice), embedding and
transcription models have their own runtimes; ``UnifiedAIClient.execute()`` runs only the turn
channel. A saved agent can still be bound to a realtime model (a voice agent), and a person can
open that agent in a typed chat — live 2026-11-12, matrx-ios chat on an agent bound to
``gemini-3.8-live`` filed a ``system_error`` (ValueError) for what is the agent's own setting.

That is a CALLER REFUSAL (``is_caller_refusal``): decided before anything is sent, never retried,
rerouted to another model or filed as a provider failure. The stream ends with one sentence that
names the model and what to do; the code is in ``caller_refusal``'s registry.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.providers.errors import RetryableError

MODEL_NOT_FOR_CHAT = "model_not_for_chat"

#: Interaction modes whose models have their own runtime and never answer a typed turn.
NOT_FOR_CHAT_INTERACTIONS: frozenset[str] = frozenset({"realtime", "embedding", "rerank"})

_CHANNEL_WORDS = {
    "realtime": ("a live voice model", "the realtime session/token-broker path"),
    "embedding": ("an embedding model", "the embedding provider path"),
    "stt": ("a transcription model", "the transcription provider path"),
    "rerank": ("a search reranking model", "the knowledge-search rerank path"),
}


class ModelNotForChatError(ValueError):
    """The chosen model runs on another execution channel and cannot answer a typed turn.

    Subclasses ``ValueError`` so every caller that already caught the old plain ``ValueError``
    still does.
    """

    is_caller_refusal = True
    http_status = 400

    def __init__(self, *, model_name: str, channel: str, wire_format: str) -> None:
        what, destination = _CHANNEL_WORDS.get(channel, (f"a {channel} model", f"the {channel} path"))
        self.model_name = model_name
        self.channel = channel
        self.wire_format = wire_format
        self.code = MODEL_NOT_FOR_CHAT
        super().__init__(
            f"Model {model_name!r} uses the {channel!r} execution channel "
            f"(wire_format={wire_format!r}) and cannot run through "
            f"UnifiedAIClient.execute(); route it through {destination}."
        )
        self.user_message = (
            f"This model is {what} and can't answer a chat message. "
            "Pick a chat model for this agent and try again."
        )
        self.error_info = RetryableError(
            error_type=self.code,
            message=str(self),
            status_code=self.http_status,
            is_retryable=False,
            user_message=self.user_message,
            details=self.envelope(),
        )

    def envelope(self) -> dict[str, Any]:
        return {
            "error": self.code,
            "message": self.user_message,
            "model_name": self.model_name,
            "channel": self.channel,
            "wire_format": self.wire_format,
        }


__all__ = ["MODEL_NOT_FOR_CHAT", "ModelNotForChatError"]

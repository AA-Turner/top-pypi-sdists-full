"""Pre-flight request validation for provider adapters.

Each provider calls its validator **before** dispatching to the SDK so
malformed requests are caught locally with actionable messages instead
of propagating opaque SDK exceptions.

Design decisions:
- **Fail fast over auto-correct.** Silently prepending a synthetic user
  turn masks bugs in conversation-history management (resume, compact,
  sub-agent spawn).  We raise with a clear message and let the caller
  surface it.
- **One boundary per provider.**  Every send path (stream, non-stream,
  generate_title, validate_connection) should call the same validator so
  adding a new rule is a one-line change.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ── Bedrock model-route prefixes (case-insensitive) ──────────────────

_BEDROCK_ROUTE_PREFIXES = ("bedrock/", "bedrock.", "amazon/bedrock/")

# ── Anthropic model-route prefixes for LiteLLM ──────────────────────

_ANTHROPIC_ROUTE_PREFIXES = ("anthropic/", "anthropic.")


class ProviderRequestError(Exception):
    """A pre-flight validation rule was violated.

    Attributes:
        rule_name:  Machine-readable rule identifier.
        provider:   Provider name (``"anthropic"``, ``"litellm"``).
        model:      Model string from the config.
        message:    Human-readable explanation with remediation hints.
    """

    def __init__(
        self,
        *,
        rule_name: str,
        provider: str,
        model: str,
        message: str,
    ) -> None:
        super().__init__(message)
        self.rule_name = rule_name
        self.provider = provider
        self.model = model
        self.message = message

    def to_error_event(self) -> dict[str, Any]:
        """Return the canonical error-event dict matching the #1343 shape."""
        return {
            "event": "error",
            "data": {
                "message": self.message,
                "code": "request_invalid",
                "retryable": False,
                "provider": self.provider,
                "model": self.model,
            },
        }


# ── Rule functions (pure, raise on violation) ────────────────────────


def validate_first_message_user(
    messages: list[dict[str, Any]],
    *,
    allow_leading_system: bool = True,
    provider: str,
    model: str,
) -> None:
    """Raise if the first non-system message has a role other than ``user``.

    Applies to providers that require conversations to start with a user
    turn after an optional system message (Anthropic, Bedrock).

    Args:
        messages: The message list **as it will be sent to the SDK** (i.e.
            after ``_convert_messages`` for Anthropic, or the raw
            OpenAI-format list for LiteLLM).
        allow_leading_system: When ``True``, skip leading ``system`` roles
            before checking.  Set to ``False`` for Anthropic's converted
            message list (which never contains system messages — they are
            extracted separately).
        provider: Provider name for the error payload.
        model: Model string for the error payload.
    """
    for i, msg in enumerate(messages):
        role = msg.get("role", "")
        if role == "system" and allow_leading_system:
            continue
        if role != "user":
            raise ProviderRequestError(
                rule_name="first_message_must_be_user",
                provider=provider,
                model=model,
                message=(
                    f"First non-system message has role={role!r} at index {i}; "
                    f"provider '{provider}' (model '{model}') requires the first "
                    f"non-system message to be 'user'. This usually means a "
                    f"corrupted conversation history — try starting a new chat "
                    f"or running /compact."
                ),
            )
        return  # first non-system message is user — valid

    # Empty or system-only message list.
    raise ProviderRequestError(
        rule_name="first_message_must_be_user",
        provider=provider,
        model=model,
        message="Message list is empty or system-only; no user message to send.",
    )


def validate_not_bedrock_tools_without_confirmation(
    model: str,
    tools: list[dict[str, Any]] | None,
    *,
    confirmed: bool,
    provider: str,
) -> None:
    """Raise if the model route targets Bedrock and tools are non-empty.

    LiteLLM translates OpenAI-shape tools into Bedrock's ``toolConfig``
    internally, but the translation fails on some Bedrock model routes and
    versions.  Anteroom cannot inspect the final request (it is wrapped
    inside ``litellm.acompletion``).  Instead we detect the risky condition
    upstream and let the operator opt in via config once they have verified
    the route works end-to-end.

    Args:
        model: Model string (may contain provider routing prefix).
        tools: Tool definitions in OpenAI format, or ``None``.
        confirmed: Value of ``ai.litellm_bedrock_tools_confirmed`` config.
        provider: Provider name for the error payload.
    """
    if not tools:
        return
    lower = model.lower()
    if not any(lower.startswith(p) for p in _BEDROCK_ROUTE_PREFIXES):
        return
    if confirmed:
        return
    raise ProviderRequestError(
        rule_name="bedrock_tool_route",
        provider=provider,
        model=model,
        message=(
            f"Tool calling via LiteLLM → Bedrock ({model}) is a known-hazard "
            f"route: LiteLLM's internal toolConfig translation is known to "
            f"fail on some Bedrock model versions. Once you verify the route "
            f"works end-to-end, set `ai.litellm_bedrock_tools_confirmed: true` "
            f"in your config to opt in."
        ),
    )


def _is_anthropic_or_bedrock_route(model: str) -> bool:
    """Return ``True`` if *model* looks like an Anthropic or Bedrock LiteLLM route."""
    lower = model.lower()
    return any(lower.startswith(p) for p in _ANTHROPIC_ROUTE_PREFIXES + _BEDROCK_ROUTE_PREFIXES)

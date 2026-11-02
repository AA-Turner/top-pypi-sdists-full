from typing import Literal

_PROVIDER_ERROR_CATEGORIES = frozenset(
    {
        "validation_error",
        "transport_error",
        "logic_error",
        "provider_error",
    }
)


class ProviderError(Exception):
    """
    Raised for provider-side contract failures that must abort the call,
    including discovery errors, shared input validation failures, and
    impossible state transitions.
    Normal create/retrieve outcomes should be returned as a FailureEnvelope
    value in TaskHandle.failure or TaskState.failure.
    """

    def __init__(
        self,
        message: str,
        category: Literal["validation_error", "transport_error", "logic_error", "provider_error"] = "provider_error",
    ) -> None:
        if not isinstance(message, str) or not message:
            raise ValueError("message must be a non-empty string")
        if not isinstance(category, str) or category not in _PROVIDER_ERROR_CATEGORIES:
            allowed = ", ".join(sorted(_PROVIDER_ERROR_CATEGORIES))
            raise ValueError(f"category must be one of: {allowed}")

        self.message = message
        self.category = category
        super().__init__(message)

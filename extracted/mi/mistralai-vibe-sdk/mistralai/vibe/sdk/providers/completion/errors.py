"""Completion-layer error classification."""

from http import HTTPStatus

_CONTEXT_TOO_LARGE_SUBSTRINGS = (
    # Provider APIs do not expose a stable error code for context-limit errors.
    "context too long",
    "maximum context length",
    "input too large",
    "couldn't fit with truncation",
    "prompt is too long",
)


class CompletionContextTooLargeError(RuntimeError):
    """Raised when a provider rejects a request for exceeding context limits."""

    def __init__(self, *, provider: str, model: str) -> None:
        self.provider = provider
        self.model = model
        super().__init__(
            f"{provider} completion request exceeded the context limit for model {model}"
        )


def is_context_too_large_error(exc: BaseException) -> bool:
    """Classify provider context-limit failures across SDK wrappers."""
    seen: set[int] = set()
    pending: list[BaseException] = [exc]
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue

        if isinstance(current, CompletionContextTooLargeError):
            return True
        if getattr(current, "is_context_too_long", False):
            return True

        if _status_code(current) == HTTPStatus.BAD_REQUEST:
            text = _error_text(current).lower()
            if any(fragment in text for fragment in _CONTEXT_TOO_LARGE_SUBSTRINGS):
                return True

        seen.add(id(current))
        if current.__cause__ is not None:
            pending.append(current.__cause__)
        if current.__context__ is not None:
            pending.append(current.__context__)
    return False


def _status_code(exc: BaseException) -> int | None:
    status = getattr(exc, "status_code", None)
    if isinstance(status, int):
        return status

    response = getattr(exc, "response", None) or getattr(exc, "raw_response", None)
    response_status = getattr(response, "status_code", None)
    return response_status if isinstance(response_status, int) else None


def _error_text(exc: BaseException) -> str:
    response = getattr(exc, "response", None) or getattr(exc, "raw_response", None)
    text = getattr(response, "text", None)
    if isinstance(text, str):
        return f"{text}\n{exc}"
    return str(exc)

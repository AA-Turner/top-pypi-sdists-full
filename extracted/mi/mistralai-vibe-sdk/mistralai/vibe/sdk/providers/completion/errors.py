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
    """Classify provider context-limit failures across SDK wrappers.

    Errors may be wrapped multiple times: the provider raises a 400, an SDK wraps it
    (e.g. ``SDKError``/``litellm.BadRequestError``), and an orchestrator such as Temporal
    re-wraps it as ``ActivityError``/``ApplicationError`` when it crosses an activity
    boundary. The 400 status code is then on the inner exception, not the outer one, so
    matching is driven by the context-limit substrings rather than by the HTTP status of
    the *current* frame. We walk the full ``__cause__``/``__context__`` chain so the inner
    provider error is inspected even when the outermost frame has no status code at all.
    """
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

        # A 400 confirms the provider rejected the request; a missing status code means
        # the error was re-wrapped (e.g. across a Temporal activity boundary), in which
        # case the substring match on the unwrapped provider text is the only signal.
        if _status_code(current) in (None, HTTPStatus.BAD_REQUEST) and any(
            fragment in _error_text(current).lower() for fragment in _CONTEXT_TOO_LARGE_SUBSTRINGS
        ):
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

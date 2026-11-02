"""Coarse structural classification of a tool call's outcome.

This is intentionally heuristic. Failures in cube-cloud surface two ways:

  1. Raised exceptions (e.g. `ApolloError`), and
  2. **Error strings returned as normal results** — handlers return
     ``f"Error: {e}"`` / ``f"Error creating product '{id}': {e}"``,
     ``f"Failed to list apps: {e}"``, ``"Unknown tool: ..."``, and authorization
     denials like ``"Cube '...' is not in your authorized set ..."``.

If classification only inspected exceptions it would badly undercount errors, so
we inspect the returned string too — and the "is this an error?" gate and the
error-class assignment share one phrase set so they can't disagree. The leading
tokens handlers actually use are ``Error`` / ``Failed`` / ``Unknown ... tool``
(verified across tools/); no successful result leads with those. Richer
*semantic* error modes are derived downstream from the full stored payload —
this only assigns the coarse bucket.
"""

from __future__ import annotations

STATUS_OK = "ok"
STATUS_ERROR = "error"

# error_class enum
APOLLO_ERROR = "apollo_error"
AUTH_DENIED = "auth_denied"
NOT_FOUND = "not_found"
BAD_REQUEST = "bad_request"
TIMEOUT = "timeout"
UNKNOWN = "unknown"


def _classify_exception(exc: BaseException) -> str:
    name = type(exc).__name__
    if name == "ApolloError":
        return APOLLO_ERROR
    # Builtin/asyncio TimeoutError, plus any httpx timeout (TimeoutException,
    # ConnectTimeout, ReadTimeout, WriteTimeout, PoolTimeout — all contain "Timeout").
    if isinstance(exc, TimeoutError) or "Timeout" in name:
        return TIMEOUT
    if isinstance(exc, KeyError):
        # Missing required argument in a handler (args["..."]).
        return BAD_REQUEST
    return UNKNOWN


def _is_error_result(low: str) -> bool:
    """True if a returned result string denotes a failure. `low` is lowercased."""
    return (
        low.startswith("error")  # "Error:", "Error creating ...", "Error publishing ..."
        or low.startswith("failed")  # "Failed to ..."
        or low.startswith("unauthorized")
        or low.startswith("access denied")
        or low.startswith("not authorized")
        or low.startswith("unknown tool")
        or "unknown teleport tool" in low
        or "unknown groundcover tool" in low
        or "not in your authorized set" in low
    )


def _classify_error_string(low: str) -> str:
    """Assign an error_class to a result string already known to be an error."""
    if (
        "not in your authorized set" in low
        or "not authorized" in low
        or "unauthorized" in low
        or "access denied" in low
    ):
        return AUTH_DENIED
    if "tool" in low and "unknown" in low:
        return BAD_REQUEST
    if (
        "must be valid json" in low
        or "is required" in low
        or "must be provided" in low
        or "empty command" in low
        or "no environments specified" in low
    ):
        return BAD_REQUEST
    if "not found" in low or "no such" in low or "does not exist" in low:
        return NOT_FOUND
    if "timed out" in low or "timeout" in low:
        return TIMEOUT
    return UNKNOWN


def classify(result: str, exception: BaseException | None) -> tuple[str, str | None]:
    """Return ``(status, error_class)``. ``error_class`` is None when status is ok.

    An exception always wins (the wrapper passes a caught ApolloError here too, so
    it classifies as apollo_error rather than being reduced to its message text).
    Otherwise the result string is inspected. Informational messages (e.g.
    "isn't reporting to Groundcover") do not lead with an error token and are
    correctly treated as ok.
    """
    if exception is not None:
        return STATUS_ERROR, _classify_exception(exception)

    low = (result or "").strip().lower()
    if not _is_error_result(low):
        return STATUS_OK, None
    return STATUS_ERROR, _classify_error_string(low)

"""A response cut off in transit is a TRANSIENT transport failure, never a rejected request.

THE LIVE CASE (2026-08-26 04:41 UTC, scheduler run 78c5de02-545e-45b3-9ab9-85f05525c433):
the Google GenAI async path (aiohttp) raised

    ClientPayloadError("Response payload is not completed: <TransferEncodingError: 400,
      message='Not enough data to satisfy transfer length header.'>.
      ConnectionResetError(104, 'Connection reset by peer')")

and `classify_google_error` returned ``invalid_request`` / ``is_retryable=False`` /
"Google rejected the request: ..." — because the typed transport check knew only
httpx, and the string fallback matched the "400" inside aiohttp's own
TransferEncodingError repr as an HTTP status. The orchestrator's retry loop
(``executor.py``: ``_will_retry = error_info.is_retryable and ...``) therefore never
saw it, one blip failed a bounded batch job that had committed 839 units of work,
and the scheduler repeat guard disabled an approved schedule on that false status.

These tests feed the classifier the EXACT exception shapes from the wire. They
fail on the pre-fix classifier (verified: every case below returned
``invalid_request``/non-retryable or ``connection_error`` before the fix).
"""

from __future__ import annotations

import httpx
import pytest

from matrx_ai.providers.errors import (
    classify_anthropic_error,
    classify_common_error,
    classify_google_error,
    classify_openai_error,
)

LIVE_MESSAGE = (
    "Response payload is not completed: <TransferEncodingError: 400, "
    "message='Not enough data to satisfy transfer length header.'>. "
    "ConnectionResetError(104, 'Connection reset by peer')"
)


def _live_aiohttp_exception() -> Exception:
    import aiohttp

    return aiohttp.ClientPayloadError(LIVE_MESSAGE)


def test_google_truncated_payload_is_retryable_and_named_as_transport() -> None:
    info = classify_google_error(_live_aiohttp_exception())
    assert info.is_retryable is True, info
    assert info.error_type == "incomplete_response", info
    # The user-facing sentence must describe a transport failure, never a rejection.
    assert "rejected" not in info.user_message.lower(), info.user_message
    assert "cut off" in info.user_message.lower(), info.user_message
    # The typed path stamped which transport type it saw — the diagnostic survives.
    assert info.details.get("transport_exception") == "aiohttp.client_exceptions.ClientPayloadError"


def test_truncation_reaches_the_retry_loop_with_a_short_backoff() -> None:
    info = classify_google_error(_live_aiohttp_exception())
    assert info.get_backoff_delay(0) <= 5.0


@pytest.mark.parametrize(
    "classify",
    [classify_google_error, classify_openai_error, classify_anthropic_error],
)
def test_stringified_truncation_never_matches_as_http_400(classify) -> None:
    # An SDK wrapper that re-raises the cause as a bare Exception loses the type;
    # the string path must still see the transport, not the embedded "400".
    info = classify(Exception(LIVE_MESSAGE))
    assert info.is_retryable is True, info
    assert info.error_type == "incomplete_response", info
    assert "rejected" not in info.user_message.lower()


def test_aiohttp_server_disconnected_is_incomplete_response() -> None:
    import aiohttp

    info = classify_common_error(aiohttp.ServerDisconnectedError("Server disconnected"), "Google")
    assert info is not None and info.is_retryable and info.error_type == "incomplete_response"


def test_aiohttp_connection_error_is_connection_error() -> None:
    import aiohttp

    info = classify_common_error(aiohttp.ClientConnectionError("cannot connect"), "Google")
    assert info is not None and info.is_retryable and info.error_type == "connection_error"


def test_aiohttp_timeout_is_timeout() -> None:
    import aiohttp

    info = classify_common_error(aiohttp.ServerTimeoutError("timed out"), "Google")
    assert info is not None and info.is_retryable and info.error_type == "provider_timeout"


def test_httpx_remote_protocol_error_is_incomplete_response() -> None:
    info = classify_common_error(httpx.RemoteProtocolError("peer closed connection without sending complete message body"), "OpenAI")
    assert info is not None and info.is_retryable and info.error_type == "incomplete_response"


def test_a_real_google_400_is_still_a_rejected_request() -> None:
    # The fix must not turn genuine bad requests into retries.
    from google.genai.errors import ClientError

    exc = ClientError(400, {"error": {"message": "Invalid JSON payload received.", "status": "INVALID_ARGUMENT"}})
    info = classify_google_error(exc)
    assert info.is_retryable is False
    assert info.error_type == "invalid_request"

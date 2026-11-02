"""Unit tests for the hand-written error decoding
(rules/sdk-generation.md's "unit-test only the hand-written parts")."""

from __future__ import annotations

import httpx

from forge_dashboard.errors import APIError, decode_error


def _response(status_code: int, body: bytes = b"", headers: dict[str, str] | None = None) -> httpx.Response:
    return httpx.Response(status_code, content=body, headers=headers or {})


def test_decode_error_returns_none_below_400() -> None:
    assert decode_error(_response(200)) is None
    assert decode_error(_response(399)) is None


def test_decode_error_treats_400_as_an_error() -> None:
    # The exact boundary: 400 is an error, 399 (above) is not.
    error = decode_error(_response(400, b'{"error": "nope"}'))
    assert error is not None
    assert error.status_code == 400


def test_decode_error_parses_message() -> None:
    body = b'{"error": "repo not found"}'
    error = decode_error(_response(404, body))

    assert isinstance(error, APIError)
    assert error.status_code == 404
    assert error.message == "repo not found"


def test_decode_error_tolerates_non_json_body() -> None:
    error = decode_error(_response(502, b"<html>Bad Gateway</html>"))

    assert error is not None
    assert error.status_code == 502
    assert error.message == ""


def test_decode_error_defaults_message_when_missing() -> None:
    error = decode_error(_response(404, b"{}"))
    assert error is not None
    assert error.message == ""


def test_api_error_str() -> None:
    error = APIError(404, "nope")
    assert str(error) == "forge-dashboard: 404: nope"


def test_api_error_args_reflect_str() -> None:
    error = APIError(404, "nope")
    assert error.args == (str(error),)

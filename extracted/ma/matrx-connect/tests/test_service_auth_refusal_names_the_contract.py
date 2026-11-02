"""A 401 that does not name the contract sends the caller back to a stale doc.

On 2026-09-17 a block hunt lost an afternoon to exactly this: a document still
described an `X-API-Key` scheme that had been retired, and the service's refusal
said only "Approved-server credentials required", which confirmed nothing and
corrected nothing. The door now states how the secret must be presented — a
contract, never the secret itself.
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException
from starlette.datastructures import Headers
from starlette.requests import Request

from matrx_connect.service_auth import verify_approved_server


def _request(headers: dict[str, str]) -> Request:
    raw = [(k.lower().encode(), v.encode()) for k, v in headers.items()]
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": raw,
        "query_string": b"",
        "client": ("127.0.0.1", 1234),
    }
    request = Request(scope)
    assert isinstance(request.headers, Headers)
    return request


def _refusal(headers: dict[str, str], **kwargs) -> dict:
    with pytest.raises(HTTPException) as excinfo:
        verify_approved_server(_request(headers), secret="the-real-secret", **kwargs)
    assert excinfo.value.status_code == 401
    detail = excinfo.value.detail
    assert isinstance(detail, dict)
    return detail


def test_a_bearer_service_names_the_bearer_header() -> None:
    detail = _refusal({})
    assert detail["error"] == "service_credentials_required"
    assert detail["expected_header"] == "authorization"
    assert "Authorization: Bearer <token>" in detail["message"]


def test_a_custom_header_service_names_that_header() -> None:
    detail = _refusal({}, secret_header="x-cloud-files-bypass")
    assert detail["expected_header"] == "x-cloud-files-bypass"
    assert "x-cloud-files-bypass: <token>" in detail["message"]


def test_a_caller_following_the_retired_api_key_doc_is_told_so() -> None:
    detail = _refusal({"x-api-key": "whatever-the-old-doc-says"})
    assert "does not accept `X-API-Key`" in detail["message"]
    assert "out of date" in detail["message"]


def test_the_refusal_never_echoes_the_secret() -> None:
    for headers in ({}, {"authorization": "Bearer wrong"}, {"x-api-key": "wrong"}):
        detail = _refusal(headers)
        assert "the-real-secret" not in detail["message"]
        assert "wrong" not in detail["message"]

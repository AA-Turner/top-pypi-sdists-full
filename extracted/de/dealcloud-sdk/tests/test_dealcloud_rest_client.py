"""Tests for DealCloudRestClient (plain-text error normalization)."""

import json
import logging
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock

import httpx
import pytest
import respx
from intapp_rest_client.client import RestClient
from intapp_rest_client.exceptions import HttpError

from dealcloud_sdk.http.dealcloud_rest_client import (
    DealCloudRestClient,
    normalize_plain_text_error_body,
)


def test_normalize_plain_text_error_body():
    r = httpx.Response(400, text="  FromDate must be less then current date. \n")
    assert normalize_plain_text_error_body(r) == {
        "statusCode": 400,
        "message": "FromDate must be less then current date.",
        "error": "FromDate must be less then current date.",
    }


def test_normalize_empty_body():
    r = httpx.Response(500, text="")
    assert normalize_plain_text_error_body(r) == {
        "statusCode": 500,
        "message": None,
    }


@respx.mock
def test_dealcloud_rest_client_plain_text_error_becomes_dict():
    respx.get("https://api.example.com/api/x").mock(
        return_value=httpx.Response(
            400,
            text="Unable to make a backup request. Please select at least one list or binary",
        )
    )
    client = DealCloudRestClient(base_url="https://api.example.com")
    try:
        with pytest.raises(HttpError) as exc_info:
            client.get("/api/x")
        e = exc_info.value
        assert e.status_code == 400
        assert e.response_body == {
            "statusCode": 400,
            "message": "Unable to make a backup request. Please select at least one list or binary",
            "error": "Unable to make a backup request. Please select at least one list or binary",
        }
    finally:
        client.close()


def test_dealcloud_rest_client_streaming_error_body_is_read_before_json():
    """download_file uses httpx.stream; error bodies need read() before .json()."""
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            500,
            stream=httpx.ByteStream(b'{"detail": "server blew up"}'),
            headers={"content-type": "application/json"},
        )
    )
    client = DealCloudRestClient(base_url="https://api.example.com")
    try:
        with httpx.Client(transport=transport) as http_client:
            with http_client.stream("GET", "https://x/") as response:
                with pytest.raises(HttpError) as exc_info:
                    client._handle_error_response(response)
                assert exc_info.value.response_body == {"detail": "server blew up"}
    finally:
        client.close()


def test_handle_error_response_response_not_read_then_plain_text():
    """ResponseNotRead then non-JSON body uses normalize_plain_text_error_body."""
    client = DealCloudRestClient(base_url="https://api.example.com")
    response = MagicMock(spec=httpx.Response)
    response.status_code = 502
    response.headers = httpx.Headers({})
    response.text = "upstream timeout"

    _json_calls = [0]

    def json_side_effect():
        _json_calls[0] += 1
        if _json_calls[0] == 1:
            raise httpx.ResponseNotRead()
        raise json.JSONDecodeError("Expecting value", "upstream timeout", 0)

    response.json.side_effect = json_side_effect
    response.read.return_value = None

    try:
        with pytest.raises(HttpError) as exc_info:
            client._handle_error_response(response, request_id="req-abc")
        e = exc_info.value
        assert e.status_code == 502
        assert e.request_id == "req-abc"
        assert e.response_body["message"] == "upstream timeout"
        assert e.response_body["error"] == "upstream timeout"
    finally:
        client.close()


@respx.mock
def test_dealcloud_rest_client_download_file_fallback_when_base_has_no_method(tmp_path: Path):
    """
    Older intapp-rest-client wheels may omit RestClient.download_file; the SDK
    subclass still streams GETs via httpx (backups SAS URLs, attachments).
    """
    saved = getattr(RestClient, "download_file", None)
    try:
        if saved is not None:
            delattr(RestClient, "download_file")
        respx.get("https://api.example.com/api/files/x.bin").mock(
            return_value=httpx.Response(200, content=b"abc")
        )
        client = DealCloudRestClient(base_url="https://api.example.com")
        try:
            out = tmp_path / "x.bin"
            n = client.download_file("/api/files/x.bin", str(out))
            assert n == 3
            assert out.read_bytes() == b"abc"
        finally:
            client.close()
    finally:
        if saved is not None:
            RestClient.download_file = saved  # type: ignore[method-assign]


@respx.mock
def test_download_file_fallback_skip_auth_no_auth_headers(tmp_path: Path):
    """Fallback path with skip_auth=True does not call auth header/param helpers."""
    saved = getattr(RestClient, "download_file", None)
    try:
        if saved is not None:
            delattr(RestClient, "download_file")
        respx.get("https://api.example.com/api/public.bin").mock(
            return_value=httpx.Response(200, content=b"xyz")
        )
        client = DealCloudRestClient(base_url="https://api.example.com")
        client._get_auth_headers_sync = MagicMock()  # type: ignore[method-assign]
        client._get_auth_params_sync = MagicMock()  # type: ignore[method-assign]
        try:
            out = tmp_path / "p.bin"
            n = client.download_file("/api/public.bin", str(out), skip_auth=True)
            assert n == 3
            client._get_auth_headers_sync.assert_not_called()
            client._get_auth_params_sync.assert_not_called()
        finally:
            client.close()
    finally:
        if saved is not None:
            RestClient.download_file = saved  # type: ignore[method-assign]


@respx.mock
def test_download_file_fallback_writes_to_binary_io():
    """Destination can be a writable binary buffer (no file close in finally)."""
    saved = getattr(RestClient, "download_file", None)
    try:
        if saved is not None:
            delattr(RestClient, "download_file")
        respx.get("https://api.example.com/api/buf.bin").mock(
            return_value=httpx.Response(200, content=b"bufdata")
        )
        client = DealCloudRestClient(base_url="https://api.example.com")
        try:
            bio = BytesIO()
            n = client.download_file("/api/buf.bin", bio)
            assert n == 7
            assert bio.getvalue() == b"bufdata"
        finally:
            client.close()
    finally:
        if saved is not None:
            RestClient.download_file = saved  # type: ignore[method-assign]


@respx.mock
def test_download_file_fallback_http_error_reads_body(tmp_path: Path):
    """Non-success stream response triggers read + _handle_error_response."""
    saved = getattr(RestClient, "download_file", None)
    try:
        if saved is not None:
            delattr(RestClient, "download_file")
        respx.get("https://api.example.com/api/missing.bin").mock(
            return_value=httpx.Response(404, text="not found resource")
        )
        client = DealCloudRestClient(base_url="https://api.example.com")
        try:
            with pytest.raises(HttpError) as exc_info:
                client.download_file("/api/missing.bin", str(tmp_path / "nope.bin"))
            assert exc_info.value.status_code == 404
            assert exc_info.value.response_body["message"] == "not found resource"
        finally:
            client.close()
    finally:
        if saved is not None:
            RestClient.download_file = saved  # type: ignore[method-assign]


@respx.mock
def test_download_file_fallback_invalid_content_length_ignored(tmp_path: Path):
    """Malformed content-length falls back to unknown total (progress total None)."""
    saved = getattr(RestClient, "download_file", None)
    try:
        if saved is not None:
            delattr(RestClient, "download_file")
        respx.get("https://api.example.com/api/weird-cl.bin").mock(
            return_value=httpx.Response(
                200,
                content=b"ab",
                headers={"content-length": "not-an-int"},
            )
        )
        client = DealCloudRestClient(base_url="https://api.example.com")
        try:
            progress_calls = []

            def cb(downloaded: int, total: int | None) -> None:
                progress_calls.append((downloaded, total))

            n = client.download_file(
                "/api/weird-cl.bin",
                str(tmp_path / "w.bin"),
                progress_callback=cb,
            )
            assert n == 2
            assert progress_calls[-1] == (2, None)
        finally:
            client.close()
    finally:
        if saved is not None:
            RestClient.download_file = saved  # type: ignore[method-assign]


@respx.mock
def test_download_file_fallback_no_content_length_header(tmp_path: Path):
    """When the server omits Content-Length, total_size stays None (branch skips int())."""
    saved = getattr(RestClient, "download_file", None)
    try:
        if saved is not None:
            delattr(RestClient, "download_file")
        respx.get("https://api.example.com/api/nocl.bin").mock(
            return_value=httpx.Response(
                200,
                headers={"transfer-encoding": "chunked"},
                stream=httpx.ByteStream(b"chunked-body"),
            )
        )
        client = DealCloudRestClient(base_url="https://api.example.com")
        try:
            n = client.download_file("/api/nocl.bin", str(tmp_path / "nc.bin"))
            assert n == len(b"chunked-body")
        finally:
            client.close()
    finally:
        if saved is not None:
            RestClient.download_file = saved  # type: ignore[method-assign]


@respx.mock
def test_download_file_fallback_progress_callback_ok(tmp_path: Path):
    saved = getattr(RestClient, "download_file", None)
    try:
        if saved is not None:
            delattr(RestClient, "download_file")
        respx.get("https://api.example.com/api/prog.bin").mock(
            return_value=httpx.Response(200, content=b"1234", headers={"content-length": "4"})
        )
        client = DealCloudRestClient(base_url="https://api.example.com")
        try:
            seen = []

            def cb(d: int, t: int | None) -> None:
                seen.append((d, t))

            client.download_file("/api/prog.bin", str(tmp_path / "p.bin"), progress_callback=cb)
            assert seen == [(4, 4)]
        finally:
            client.close()
    finally:
        if saved is not None:
            RestClient.download_file = saved  # type: ignore[method-assign]


@respx.mock
def test_download_file_fallback_progress_callback_failure_logged(caplog, tmp_path: Path):
    """Progress callback exceptions are logged as warnings, download still completes."""
    saved = getattr(RestClient, "download_file", None)
    try:
        if saved is not None:
            delattr(RestClient, "download_file")
        respx.get("https://api.example.com/api/badcb.bin").mock(
            return_value=httpx.Response(200, content=b"x")
        )
        client = DealCloudRestClient(base_url="https://api.example.com")
        try:
            caplog.set_level(logging.WARNING)

            def cb(_d: int, _t: int | None) -> None:
                raise RuntimeError("progress exploded")

            n = client.download_file(
                "/api/badcb.bin",
                str(tmp_path / "c.bin"),
                progress_callback=cb,
            )
            assert n == 1
            assert any("Progress callback failed" in r.getMessage() for r in caplog.records)
        finally:
            client.close()
    finally:
        if saved is not None:
            RestClient.download_file = saved  # type: ignore[method-assign]


@respx.mock
def test_dealcloud_rest_client_json_error_unchanged():
    payload = {"message": "known json", "statusCode": 400}
    respx.get("https://api.example.com/api/y").mock(
        return_value=httpx.Response(400, json=payload)
    )
    client = DealCloudRestClient(base_url="https://api.example.com")
    try:
        with pytest.raises(HttpError) as exc_info:
            client.get("/api/y")
        assert exc_info.value.response_body == payload
    finally:
        client.close()


@respx.mock
def test_dealcloud_rest_client_unknown_status_message():
    """Status codes not in the default map use generic HTTP error text."""
    respx.get("https://api.example.com/api/teapot").mock(
        return_value=httpx.Response(418, text="I'm a teapot")
    )
    client = DealCloudRestClient(base_url="https://api.example.com")
    try:
        with pytest.raises(HttpError) as exc_info:
            client.get("/api/teapot")
        assert exc_info.value.status_code == 418
        msg = getattr(exc_info.value, "message", None) or str(exc_info.value)
        assert "HTTP error 418" in str(msg)
    finally:
        client.close()

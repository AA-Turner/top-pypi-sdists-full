import logging
import os
import sys
import threading
import time
from dataclasses import dataclass
from unittest.mock import patch
from urllib.error import URLError
from urllib.request import urlopen

import httpx
import pytest
from connector.httpx_rewrite import AsyncClient, HTTPXAsyncTransport, log_response, proxy_settings
from connector.response_logging import (
    HTTP_ERROR_CONTENT_PREVIEW_MAX_LENGTH,
    HTTP_SUCCESS_CONTENT_PREVIEW_MAX_LENGTH,
    TRUNCATION_SEPARATOR,
    ResponseLogFormatter,
    ResponseLogRecord,
    summarize_response_content,
)
from flask import Flask, request
from flask.typing import ResponseReturnValue
from gql import Client as GqlClient
from gql.dsl import DSLQuery, DSLSchema, dsl_gql
from gql.transport.exceptions import TransportProtocolError
from graphql import GraphQLSchema, build_schema


@dataclass
class RecordedRequest:
    method: str
    path: str
    headers: dict[str, str]
    body: str | None = None


class Recorder:
    request: RecordedRequest | None = None

    def get_request(self) -> RecordedRequest:
        assert self.request is not None
        return self.request

    def proxy_request(self) -> ResponseReturnValue:
        self.request = RecordedRequest(
            headers={key: val for key, val in request.headers.items()},
            path=request.path,
            method=request.method,
        )
        return {"ok": "👍"}

    def reset_request(self) -> None:
        """
        This is necessary because
        1. the server calling this recorder is only created once
            (to avoid port conflicts from rapid server shutdown/recreation)
        2. so this recorder is only created once, and is thus a global test object :(
        """
        self.request = None


@pytest.fixture(scope="session")
def port() -> int:
    return 4444


@pytest.fixture(scope="session")
def proxy_path() -> str:
    return "/cool-test-path-for-proxy"


@pytest.fixture(scope="session")
def proxy_url(port: int, proxy_path: str) -> str:
    return f"http://localhost:{port}{proxy_path}"


@pytest.fixture(scope="session")
def recorder(port: int, proxy_path: str):
    # Turn off Flask's default logging
    sys.modules["flask.cli"].show_server_banner = lambda *x: None  # type: ignore

    recorder = Recorder()
    app = Flask(__name__)
    app.route(proxy_path, methods=["GET", "POST", "PUT"])(recorder.proxy_request)
    thread = threading.Thread(target=app.run, daemon=True, kwargs=dict(host="localhost", port=port))
    thread.start()

    # Wait for the server to start (to prevent tests from failing when the server is slow to start)
    # If it's not up in under 30 seconds, raise an error
    start_time = time.time()
    timeout = 30
    while time.time() - start_time < timeout:
        try:
            urlopen(f"http://localhost:{port}{proxy_path}")
            break
        except URLError:
            time.sleep(0.1)
    else:
        raise RuntimeError("Failed to start Flask server")

    yield recorder


@pytest.fixture
def client(recorder: Recorder, port: int) -> AsyncClient:
    recorder.reset_request()
    return AsyncClient()


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_forwarding_happens(
        self, recorder: Recorder, client: AsyncClient, proxy_url: str, proxy_path: str
    ) -> None:
        """We should call our running server instead of the original host"""
        with proxy_settings(proxy_url=proxy_url):
            await client.get("https://hope-nobody-ever-registers-this-domain.com/hi")
        assert recorder.request is not None
        assert recorder.request.method == "GET"
        assert recorder.request.path == proxy_path

    @pytest.mark.asyncio
    async def test_forward_to_header_is_added(
        self, recorder: Recorder, client: AsyncClient, proxy_url: str
    ) -> None:
        """The receiving proxy should get called with an X-Forward-To header with the original request line"""
        with proxy_settings(proxy_url=proxy_url):
            await client.get("https://hope-nobody-ever-registers-this-domain.com/hi")

        proxy_received_request = recorder.get_request()
        assert (
            proxy_received_request.headers["X-Forward-To"]
            == "https://hope-nobody-ever-registers-this-domain.com/hi"
        )

    @pytest.mark.asyncio
    async def test_proxy_headers_are_sent(
        self, recorder: Recorder, client: AsyncClient, proxy_url: str
    ) -> None:
        """The receiving proxy should get called with other headers included in the request"""
        with proxy_settings(
            proxy_url=proxy_url, proxy_headers={"Absolutely-Fake": "yep this is here"}
        ):
            await client.get("https://hope-nobody-ever-registers-this-domain.com/hi/there")
        proxy_received_request = recorder.get_request()
        assert proxy_received_request.headers["Absolutely-Fake"] == "yep this is here"

    @pytest.mark.asyncio
    async def test_other_headers_are_sent(
        self, recorder: Recorder, client: AsyncClient, proxy_url: str
    ) -> None:
        """The receiving proxy should get called with other headers included in the request"""
        with proxy_settings(proxy_url=proxy_url):
            await client.get(
                "https://hope-nobody-ever-registers-this-domain.com/hi/there",
                headers={
                    "Foo": "Bar",
                    "Authorization": "Bearer SUPER_SECRET",
                },
            )
        proxy_received_request = recorder.get_request()
        assert proxy_received_request.headers["Foo"] == "Bar"
        assert proxy_received_request.headers["Authorization"] == "Bearer SUPER_SECRET"

    @pytest.mark.asyncio
    async def test_no_proxy_url_means_no_proxy_calls(
        self, recorder: Recorder, client: AsyncClient
    ) -> None:
        """If there's no proxy url set, call the actual domain"""
        with proxy_settings(proxy_url=None):
            response = await client.get(
                "https://www.google.com"  # I assume this will be around for most tests
            )
        assert response.request.url == "https://www.google.com"
        assert response.status_code == 200
        assert recorder.request is None


def load_mock_schema() -> GraphQLSchema:
    schema_file_path = os.path.join(os.path.dirname(__file__), "mock_schema.sdl")
    with open(schema_file_path, encoding="utf-8") as schema_file:
        return build_schema(schema_file.read())


class TestGraphqlAsyncTransport:
    @pytest.mark.asyncio
    async def test_graphql_async_transport_gets_proxied(
        self, recorder: Recorder, proxy_url: str
    ) -> None:
        transport = HTTPXAsyncTransport(
            url="https://definitely-doesnt-exist.com/super-graphql",
        )
        schema = DSLSchema(load_mock_schema())
        query = DSLQuery(
            schema.Query.todo().select(
                schema.Todo.id,
                schema.Todo.name,
            )
        )
        with proxy_settings(proxy_url=proxy_url):
            async with GqlClient(transport=transport) as gql_client:
                # this is going to raise because I couldn't be bothered trying to
                # respond to real graphql, and I do. not. care. - Alex
                with pytest.raises(TransportProtocolError):
                    await gql_client.execute(dsl_gql(query))

        assert recorder.request is not None
        assert recorder.get_request().method == "POST"
        assert (
            recorder.get_request().headers["X-Forward-To"]
            == "https://definitely-doesnt-exist.com/super-graphql"
        )


class TestResponseLogging:
    def test_summarize_response_content_uses_success_limit(self) -> None:
        content = "a" * (HTTP_SUCCESS_CONTENT_PREVIEW_MAX_LENGTH + 500)
        preview, original_length, truncated = summarize_response_content(content, 200)

        assert original_length == len(content)
        assert truncated is True
        assert len(preview) == HTTP_SUCCESS_CONTENT_PREVIEW_MAX_LENGTH
        assert TRUNCATION_SEPARATOR in preview

    def test_summarize_response_content_uses_error_limit(self) -> None:
        content = "b" * (HTTP_ERROR_CONTENT_PREVIEW_MAX_LENGTH + 1000)
        preview, original_length, truncated = summarize_response_content(content, 504)

        assert original_length == len(content)
        assert truncated is True
        assert len(preview) == HTTP_ERROR_CONTENT_PREVIEW_MAX_LENGTH
        assert TRUNCATION_SEPARATOR in preview

    def test_summarize_response_content_no_truncation_when_short(self) -> None:
        content = "short response body"
        preview, original_length, truncated = summarize_response_content(content, 200)

        assert preview == content
        assert original_length == len(content)
        assert truncated is False

    def test_log_response_emits_preview_and_metadata(self) -> None:
        long_content = "x" * (HTTP_SUCCESS_CONTENT_PREVIEW_MAX_LENGTH + 200)
        request_obj = httpx.Request("GET", "https://example.com/api/users")
        response = httpx.Response(
            status_code=200,
            request=request_obj,
            text=long_content,
            headers={"content-type": "application/json"},
        )

        with patch("connector.httpx_rewrite.response_logger.handle") as mock_handle:
            log_response(response)

        mock_handle.assert_called_once()
        record = mock_handle.call_args.args[0]

        assert record.status_code == 200
        assert record.content_length_original == len(long_content)
        assert record.content_truncated is True
        assert len(record.content) == HTTP_SUCCESS_CONTENT_PREVIEW_MAX_LENGTH
        assert TRUNCATION_SEPARATOR in record.content
        assert record.content_hash

    def test_response_log_formatter_tolerates_partial_record(self) -> None:
        """Non-httpx call sites may omit metadata fields; formatting must not raise."""
        record = ResponseLogRecord(
            name="integration-connectors.sdk.api_response",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="partial",
            args=(),
            exc_info=None,
        )
        record.content = '{"x": 1}'

        formatter = ResponseLogFormatter("%(message)s")
        formatted = formatter.format(record)

        assert "partial" in formatted
        assert "content_length_original" in formatted
        assert "'content_length_original': None" in formatted

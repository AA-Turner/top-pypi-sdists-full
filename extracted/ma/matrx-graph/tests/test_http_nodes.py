"""Tests for the http.* node pack.

Uses ``httpx.MockTransport`` to intercept requests — real network stays out
of CI. We exercise the node executors directly (bypassing the scheduler)
because they don't depend on channels or context; calling ``execute()``
with a stub ctx is simpler and catches every edge case faster.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import httpx
import pytest
from matrx_graph.nodes.http.get import HttpGetConfig, HttpGetExecutor, HttpGetInput
from matrx_graph.nodes.http.graphql import (
    GraphQLConfig,
    GraphQLInput,
    HttpGraphQLExecutor,
)
from matrx_graph.nodes.http.post import HttpPostConfig, HttpPostExecutor, HttpPostInput


def _install_mock(handler: Any):
    """Patch httpx.AsyncClient so every node call routes through `handler`."""
    transport = httpx.MockTransport(handler)
    original_init = httpx.AsyncClient.__init__

    def patched_init(self, *args, **kwargs):
        kwargs.pop("transport", None)
        original_init(self, *args, transport=transport, **kwargs)

    return patch.object(httpx.AsyncClient, "__init__", patched_init)


# ---------------------------------------------------------------------------
# GET
# ---------------------------------------------------------------------------


async def test_get_returns_json_body():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.query == b"q=hello"
        return httpx.Response(
            200,
            json={"items": [1, 2, 3]},
            headers={"content-type": "application/json"},
        )

    with _install_mock(handler):
        exec_ = HttpGetExecutor()
        out = await exec_.execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=HttpGetInput(url="https://example.com/api", query={"q": "hello"}),
            config=HttpGetConfig(),
        )

    assert out.status == "success"
    payload = out.result
    assert payload.status == 200
    assert payload.body == {"items": [1, 2, 3]}
    assert "json" in payload.content_type


async def test_get_non_2xx_is_still_node_success():
    def handler(_request):
        return httpx.Response(404, text="not found")

    with _install_mock(handler):
        out = await HttpGetExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=HttpGetInput(url="https://example.com/missing"),
            config=HttpGetConfig(),
        )

    # Node Result System: an HTTP response received — even 404 — is node
    # SUCCESS; downstream branches on payload.status.
    assert out.status == "success"
    assert out.result.status == 404
    assert out.result.text == "not found"


async def test_get_captures_transport_error():
    def handler(_request):
        raise httpx.ConnectError("simulated")

    with _install_mock(handler):
        out = await HttpGetExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=HttpGetInput(url="https://example.com"),
            config=HttpGetConfig(),
        )

    # Transport failure → node Failure with the structured NodeError.
    assert out.status == "error"
    assert out.error.code == "http_transport_error"
    assert "connect" in out.error.message.lower()
    assert set(out.error.details) == {"elapsed_ms"}


async def test_get_truncates_oversize_body():
    def handler(_request):
        # 4 KB payload, cap at 1024 B (min config value)
        return httpx.Response(200, text="x" * 4096)

    with _install_mock(handler):
        out = await HttpGetExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=HttpGetInput(url="https://example.com"),
            config=HttpGetConfig(max_bytes=1024),
        )

    assert out.status == "success"
    assert len(out.result.text) == 1024


# ---------------------------------------------------------------------------
# POST
# ---------------------------------------------------------------------------


async def test_post_json_body_serializes_correctly():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["body"] = request.content
        seen["content-type"] = request.headers.get("content-type")
        return httpx.Response(201, json={"created": True})

    with _install_mock(handler):
        out = await HttpPostExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=HttpPostInput(
                url="https://example.com/api",
                json_body={"name": "ada"},
            ),
            config=HttpPostConfig(),
        )

    assert out.status == "success"
    assert out.result.status == 201
    assert b'"name":"ada"' in seen["body"].replace(b" ", b"")
    assert "application/json" in seen["content-type"]


async def test_post_form_body_sends_urlencoded():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["body"] = request.content.decode()
        seen["content-type"] = request.headers.get("content-type")
        return httpx.Response(200, text="ok")

    with _install_mock(handler):
        await HttpPostExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=HttpPostInput(
                url="https://example.com",
                form={"a": "1", "b": "two"},
            ),
            config=HttpPostConfig(),
        )

    assert "application/x-www-form-urlencoded" in seen["content-type"]
    assert "a=1" in seen["body"] and "b=two" in seen["body"]


async def test_post_text_body_preserves_caller_content_type():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["body"] = request.content.decode()
        seen["content-type"] = request.headers.get("content-type")
        return httpx.Response(200, text="ok")

    with _install_mock(handler):
        await HttpPostExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=HttpPostInput(
                url="https://example.com",
                text="<xml>hi</xml>",
                headers={"content-type": "application/xml"},
            ),
            config=HttpPostConfig(),
        )

    assert seen["body"] == "<xml>hi</xml>"
    assert seen["content-type"] == "application/xml"


# ---------------------------------------------------------------------------
# GraphQL
# ---------------------------------------------------------------------------


async def test_graphql_success_unwraps_data_field():
    def handler(_request):
        return httpx.Response(
            200,
            json={"data": {"user": {"id": "1", "name": "Ada"}}},
            headers={"content-type": "application/json"},
        )

    with _install_mock(handler):
        out = await HttpGraphQLExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=GraphQLInput(
                endpoint="https://example.com/graphql",
                query="query { user { id name } }",
            ),
            config=GraphQLConfig(),
        )

    assert out.status == "success"
    assert out.result.status == 200
    assert out.result.data == {"user": {"id": "1", "name": "Ada"}}
    assert out.result.errors == []


async def test_graphql_document_errors_are_domain_data_on_200():
    def handler(_request):
        return httpx.Response(
            200,
            json={
                "data": None,
                "errors": [{"message": "Field 'user' not found"}],
            },
        )

    with _install_mock(handler):
        out = await HttpGraphQLExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=GraphQLInput(endpoint="https://x.com", query="{ user { id } }"),
            config=GraphQLConfig(),
        )

    # GraphQL document errors are DOMAIN DATA (the call itself succeeded);
    # branch on len(errors), not a payload boolean.
    assert out.status == "success"
    assert out.result.status == 200
    assert len(out.result.errors) == 1
    assert "Field 'user'" in out.result.errors[0]["message"]


async def test_graphql_transport_error_captured():
    def handler(_request):
        raise httpx.TimeoutException("slow")

    with _install_mock(handler):
        out = await HttpGraphQLExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=GraphQLInput(endpoint="https://x.com", query="{ x }"),
            config=GraphQLConfig(),
        )

    assert out.status == "error"
    assert out.error.code == "http_transport_error"
    assert "timed out" in out.error.message.lower()


async def test_graphql_variables_and_operation_name_are_sent():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        import json as _json

        seen.update(_json.loads(request.content))
        return httpx.Response(200, json={"data": {"x": 1}})

    with _install_mock(handler):
        await HttpGraphQLExecutor().execute(
            ctx=None,  # type: ignore[arg-type]
            inputs=GraphQLInput(
                endpoint="https://x.com",
                query="query Q($id: ID!) { x }",
                variables={"id": "abc"},
                operation_name="Q",
            ),
            config=GraphQLConfig(),
        )

    assert seen["query"] == "query Q($id: ID!) { x }"
    assert seen["variables"] == {"id": "abc"}
    assert seen["operationName"] == "Q"


# Silence the patch target not being available outside test context
_ = pytest


@pytest.mark.parametrize("node", ["get", "post", "custom", "graphql"])
@pytest.mark.parametrize("error_type", [httpx.ConnectError, httpx.ReadTimeout, RuntimeError])
async def test_failure_does_not_expose_request_or_transport_exception(node, error_type):
    from matrx_graph.nodes.http.custom_api import CustomApiConfig, CustomApiExecutor, CustomApiInput

    def handler(_request):
        raise error_type("private-exception-marker")

    url = "https://example.com/?private-url-marker"
    with _install_mock(handler):
        if node == "get":
            out = await HttpGetExecutor().execute(None, HttpGetInput(url=url), HttpGetConfig())
        elif node == "post":
            out = await HttpPostExecutor().execute(None, HttpPostInput(url=url), HttpPostConfig())
        elif node == "custom":
            out = await CustomApiExecutor().execute(None, CustomApiInput(url=url), CustomApiConfig(max_retries=0))
        else:
            out = await HttpGraphQLExecutor().execute(None, GraphQLInput(endpoint=url, query="{ x }"), GraphQLConfig())
    assert out.status == "error"
    assert out.error.code == "http_transport_error"
    assert "marker" not in str(out)
    assert set(out.error.details) == {"elapsed_ms"}
    expected = {httpx.ConnectError: "connect", httpx.ReadTimeout: "timed out", RuntimeError: "failed"}
    assert expected[error_type] in out.error.message.lower()


async def test_graphql_invalid_json_failure_does_not_expose_endpoint_or_response():
    with _install_mock(lambda _request: httpx.Response(503, text="private-response-marker")):
        out = await HttpGraphQLExecutor().execute(
            None, GraphQLInput(endpoint="https://example.com/?private-url-marker", query="{ x }"), GraphQLConfig()
        )
    assert out.status == "error"
    assert out.error.code == "invalid_json_response"
    assert "marker" not in str(out)
    assert out.error.details["status"] == 503
    assert set(out.error.details) == {"elapsed_ms", "status"}


@pytest.mark.parametrize("node", ["get", "post", "custom", "graphql"])
async def test_untrusted_refusal_exception_does_not_expose_its_text(node):
    from matrx_graph.nodes.http.custom_api import CustomApiConfig, CustomApiExecutor, CustomApiInput
    from matrx_utils.outbound_guard import OutboundUrlRefused

    def handler(_request):
        raise OutboundUrlRefused("private-exception-marker")

    url = "https://example.com/?private-url-marker"
    with _install_mock(handler):
        if node == "get":
            out = await HttpGetExecutor().execute(None, HttpGetInput(url=url), HttpGetConfig())
        elif node == "post":
            out = await HttpPostExecutor().execute(None, HttpPostInput(url=url), HttpPostConfig())
        elif node == "custom":
            out = await CustomApiExecutor().execute(None, CustomApiInput(url=url), CustomApiConfig(max_retries=0))
        else:
            out = await HttpGraphQLExecutor().execute(None, GraphQLInput(endpoint=url, query="{ x }"), GraphQLConfig())
    assert out.status == "error"
    assert out.error.code == "outbound_address_refused"
    assert "marker" not in str(out)
    assert set(out.error.details) == {"elapsed_ms"}


@pytest.mark.parametrize("body", [[], None])
async def test_graphql_non_object_json_is_typed_failure(body):
    with _install_mock(lambda _request: httpx.Response(200, json=body)):
        out = await HttpGraphQLExecutor().execute(
            None, GraphQLInput(endpoint="https://example.com/?private-url-marker", query="{ x }"), GraphQLConfig()
        )
    assert out.status == "error"
    assert out.error.code == "invalid_json_response"
    assert out.error.details["status"] == 200
    assert "marker" not in str(out)


@pytest.mark.parametrize("body", [
    {"errors": ["private-response-marker"]},
    {"errors": "private-response-marker"},
    {"extensions": "private-response-marker"},
])
async def test_graphql_malformed_fields_return_sanitized_failure(body):
    with _install_mock(lambda _request: httpx.Response(200, json=body)):
        out = await HttpGraphQLExecutor().execute(
            None, GraphQLInput(endpoint="https://example.com/?private-url-marker", query="{ x }"), GraphQLConfig()
        )
    assert out.status == "error"
    assert out.error.code == "invalid_json_response"
    assert out.error.details["status"] == 200
    assert set(out.error.details) == {"status", "elapsed_ms"}
    assert "marker" not in str(out)


async def test_graphql_falsey_optional_fields_remain_valid():
    with _install_mock(lambda _request: httpx.Response(200, json={"data": {"ready": True}, "errors": None, "extensions": None})):
        out = await HttpGraphQLExecutor().execute(
            None, GraphQLInput(endpoint="https://example.com/graphql", query="{ ready }"), GraphQLConfig()
        )
    assert out.status == "success"
    assert out.result.data == {"ready": True}
    assert out.result.errors == []
    assert out.result.extensions == {}

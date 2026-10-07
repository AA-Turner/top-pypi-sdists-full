"""Wire-level checks for the generated client: routes, auth, bodies, errors.

Requests go through an httpx MockTransport, so these run offline and pin the
SDK surface that scripts/generate must keep producing.
"""

import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from supermemory import AsyncSupermemory, Supermemory
from supermemory.core.api_error import ApiError
from supermemory.errors import NotFoundError

Captured = list[httpx.Request]


def _responder(captured: Captured, status: int = 200, body: Any = None) -> Callable[[httpx.Request], httpx.Response]:
    def handle(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(status, json={} if body is None else body)

    return handle


def _client(captured: Captured, **kwargs: Any) -> Supermemory:
    return Supermemory(
        api_key="sm_test",
        httpx_client=httpx.Client(transport=httpx.MockTransport(_responder(captured, **kwargs))),
    )


def _body(request: httpx.Request) -> dict[str, Any]:
    return json.loads(request.content) if request.content else {}


CASES = [
    ("add", lambda c: c.add("user_alex", content="hi", id="pref-1"), "POST", "/ns/user_alex/document"),
    ("search", lambda c: c.search("user_alex", query="hi"), "POST", "/ns/user_alex/search"),
    ("profile", lambda c: c.profile("user_alex"), "POST", "/ns/user_alex/profile"),
    ("list", lambda c: c.list("user_alex", "memories"), "POST", "/ns/user_alex/list/memories"),
    ("documents.get", lambda c: c.documents.get("user_alex", "doc1"), "GET", "/ns/user_alex/document/doc1"),
    ("documents.delete", lambda c: c.documents.delete("user_alex", ids=["d"]), "DELETE", "/ns/user_alex/document"),
    (
        "documents.batch_add",
        lambda c: c.documents.batch_add("user_alex", documents=[{"content": "x"}]),
        "POST",
        "/ns/user_alex/document/batch",
    ),
    ("memories.forget", lambda c: c.memories.forget("user_alex", ids=["m"]), "DELETE", "/ns/user_alex/memories"),
    ("profiles.get_buckets", lambda c: c.profiles.get_buckets("user_alex"), "GET", "/ns/user_alex/profile/buckets"),
    ("connectors.list", lambda c: c.connectors.list("user_alex"), "GET", "/ns/user_alex/connectors"),
    ("namespaces.list", lambda c: c.namespaces.list(), "GET", "/ns"),
    ("organization.get", lambda c: c.organization.get(), "GET", "/organization"),
]


@pytest.mark.parametrize("name,call,method,path", CASES, ids=[c[0] for c in CASES])
def test_routes(name: str, call: Callable[[Supermemory], Any], method: str, path: str) -> None:
    captured: Captured = []
    call(_client(captured))
    (request,) = captured
    assert request.method == method, name
    assert request.url.host == "api.supermemory.ai"
    assert request.url.path == path
    assert request.headers["authorization"] == "Bearer sm_test"


def test_body_uses_api_field_names() -> None:
    captured: Captured = []
    _client(captured).search("user_alex", query="meetings", limit=5, rewrite_query=True)
    (request,) = captured
    assert "limit" not in request.url.params
    assert _body(request) == {"query": "meetings", "limit": 5, "rewriteQuery": True}


def test_nested_dict_params_use_api_field_names() -> None:
    captured: Captured = []
    client = _client(captured)
    client.search(
        "user_alex",
        query="q",
        filter={
            "operator": "and",
            "operands": [
                {"field": "source", "operator": "eq", "value": "slack", "case_sensitive": False},
                {"field": "priority", "operator": "gte", "value": 3},
            ],
        },
    )
    client.connectors.create(
        "user_alex",
        request={
            "provider": "s3",
            "config": {"bucket": "b", "region": "us-east-1", "access_key_id": "AK", "secret_access_key": "SK"},
            "document_limit": 10,
        },
    )
    search, create = captured
    assert _body(search)["filter"] == {
        "operator": "and",
        "operands": [
            {"field": "source", "operator": "eq", "value": "slack", "caseSensitive": False},
            {"field": "priority", "operator": "gte", "value": 3},
        ],
    }
    assert create.url.path == "/ns/user_alex/connectors"
    assert _body(create) == {
        "provider": "s3",
        "config": {"bucket": "b", "region": "us-east-1", "accessKeyId": "AK", "secretAccessKey": "SK"},
        "documentLimit": 10,
    }


def test_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPERMEMORY_API_KEY", "sm_env")
    import importlib

    import supermemory.client

    importlib.reload(supermemory.client)  # the default is read at import time
    captured: Captured = []
    client = supermemory.client.Supermemory(
        httpx_client=httpx.Client(transport=httpx.MockTransport(_responder(captured)))
    )
    client.namespaces.list()
    assert captured[0].headers["authorization"] == "Bearer sm_env"


def test_typed_error() -> None:
    captured: Captured = []
    client = _client(captured, status=404, body={"error": "not found"})
    with pytest.raises(NotFoundError) as exc:
        client.documents.get("user_alex", "missing")
    assert isinstance(exc.value, ApiError)
    assert exc.value.status_code == 404


async def test_async_client() -> None:
    captured: Captured = []
    client = AsyncSupermemory(
        api_key="sm_test",
        httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(_responder(captured))),
    )
    await client.add("user_alex", content="hi")
    assert captured[0].url.path == "/ns/user_alex/document"
    assert _body(captured[0]) == {"content": "hi"}

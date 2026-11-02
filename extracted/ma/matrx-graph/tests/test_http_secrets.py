"""Stored secrets in http.* steps: a workflow names a secret; its value reaches only the outgoing
request — never the step's output, the run's events, the checkpoints, the log, or an error.

The fake server ECHOES everything it received (headers, query, body) — the worst case: a
partner API that reflects the caller's credentials back."""

from __future__ import annotations

import dataclasses
import json
import logging
from typing import Any
from unittest.mock import patch

import httpx
import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.secrets import SecretUnavailable, configure_secret_resolver

from tests._fixtures import FakeEmitter, make_app_context

TOKEN = "ghp_SuperSecretValue_1234567890"
KEY = "k3y-Pl4tform-Valu3"
ORG = "11111111-2222-3333-4444-555555555555"


async def _resolver(name: str, *, user_id: str | None, organization_id: str | None) -> str:
    if organization_id != ORG:
        raise SecretUnavailable(f"The secret {name!r} is not available to this organization.")
    store = {"GITHUB_TOKEN": TOKEN, "PARTNER_KEY": KEY}
    if name not in store:
        raise SecretUnavailable(f"No secret named {name!r} in this organization.")
    return store[name]


@pytest.fixture(autouse=True)
def _secret_store():
    configure_secret_resolver(_resolver)
    yield
    configure_secret_resolver(None)


seen: list[httpx.Request] = []


def _echo(request: httpx.Request) -> httpx.Response:
    seen.append(request)
    body = request.content.decode() if request.content else ""
    return httpx.Response(
        200,
        json={"headers": dict(request.headers), "query": str(request.url.query, "utf-8"), "body": body},
        headers={"content-type": "application/json", "x-echo-auth": request.headers.get("authorization", "")},
    )


def _mock():
    transport = httpx.MockTransport(_echo)
    original_init = httpx.AsyncClient.__init__

    def patched_init(self, *args, **kwargs):
        kwargs.pop("transport", None)
        original_init(self, *args, transport=transport, **kwargs)

    return patch.object(httpx.AsyncClient, "__init__", patched_init)


async def _run(node_type: str, inputs: dict, config: dict | None = None, *, org: str = ORG):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": node_type,
                    "position": {"x": 0, "y": 0},
                    "data": {"inputs": inputs, "config": config or {}},
                }
            ],
            "edges": [],
        }
    )
    emitter = FakeEmitter()
    app = dataclasses.replace(make_app_context(emitter), organization_id=org)
    checkpointer = MemoryCheckpointer()
    graph = compile_graph(defn, registry=registry)
    with _mock():
        result = await Scheduler(graph, checkpointer, app, registry=registry).run(
            run_id=f"t-{node_type}", inputs=inputs
        )
    return result, emitter, checkpointer


def _everything(result: Any, emitter: FakeEmitter, checkpointer: MemoryCheckpointer) -> str:
    """Every byte the run left behind that a person or another step could read."""
    return "\n".join(
        [
            json.dumps(result.model_dump(mode="json") if hasattr(result, "model_dump") else repr(result), default=str),
            repr(result),
            json.dumps(emitter.events, default=str),
            repr(vars(checkpointer)),
        ]
    )


async def test_header_secret_is_sent_but_never_echoed(caplog):
    seen.clear()
    caplog.set_level(logging.DEBUG)
    result, emitter, checkpointer = await _run(
        "http.get",
        {
            "url": "https://api.example.com/user",
            "headers": {"authorization": {"$secret": "GITHUB_TOKEN"}},
            "query": {"key": {"$secret": "PARTNER_KEY"}},
        },
    )
    assert result.status is RunStatus.COMPLETED, result
    # The outgoing request carried the real values.
    assert seen[-1].headers["authorization"] == TOKEN
    assert seen[-1].url.params["key"] == KEY
    out = result.last_outputs["n"]
    assert out["status"] == 200
    assert "[secret]" in out["body"]["headers"]["authorization"]
    assert out["headers"]["x-echo-auth"] == "[secret]"
    left_behind = _everything(result, emitter, checkpointer) + caplog.text
    assert TOKEN not in left_behind
    assert KEY not in left_behind
    # The reference (the NAME) is what the run stores.
    assert "GITHUB_TOKEN" in repr(vars(checkpointer))


async def test_post_body_and_custom_api_basic_auth_are_redacted(caplog):
    seen.clear()
    caplog.set_level(logging.DEBUG)
    result, emitter, checkpointer = await _run(
        "http.post",
        {"url": "https://api.example.com/x", "json_body": {"token": {"$secret": "PARTNER_KEY"}}},
    )
    assert result.status is RunStatus.COMPLETED, result
    assert json.loads(seen[-1].content) == {"token": KEY}
    assert KEY not in _everything(result, emitter, checkpointer) + caplog.text

    result, emitter, checkpointer = await _run(
        "http.custom_api",
        {
            "url": "https://api.example.com/y",
            "auth_type": "basic",
            "auth_value": {"$secret": "GITHUB_TOKEN"},
        },
        {"max_retries": 0},
    )
    assert result.status is RunStatus.COMPLETED, result
    assert seen[-1].headers["authorization"].startswith("Basic ")
    encoded = seen[-1].headers["authorization"].removeprefix("Basic ")
    left = _everything(result, emitter, checkpointer) + caplog.text
    assert TOKEN not in left
    assert encoded not in left


async def test_missing_secret_fails_naming_it_and_sends_nothing():
    seen.clear()
    result, emitter, checkpointer = await _run(
        "http.get",
        {"url": "https://api.example.com/z", "headers": {"x-api-key": {"$secret": "NOPE"}}},
    )
    assert result.status is not RunStatus.COMPLETED
    assert seen == []
    assert "NOPE" in _everything(result, emitter, checkpointer)
    assert "secret_unavailable" in _everything(result, emitter, checkpointer)


async def test_another_organizations_run_cannot_use_the_secret():
    seen.clear()
    result, emitter, checkpointer = await _run(
        "http.get",
        {"url": "https://api.example.com/z", "headers": {"authorization": {"$secret": "GITHUB_TOKEN"}}},
        org="99999999-2222-3333-4444-555555555555",
    )
    assert result.status is not RunStatus.COMPLETED
    assert seen == []
    assert TOKEN not in _everything(result, emitter, checkpointer)


async def test_no_store_connected_is_a_plain_failure():
    configure_secret_resolver(None)
    seen.clear()
    result, emitter, checkpointer = await _run(
        "http.get",
        {"url": "https://api.example.com/z", "headers": {"authorization": {"$secret": "GITHUB_TOKEN"}}},
    )
    assert result.status is not RunStatus.COMPLETED
    assert seen == []


async def test_a_formatted_secret_is_sent_wrapped_and_redacted_whole(caplog):
    seen.clear()
    caplog.set_level(logging.DEBUG)
    result, emitter, checkpointer = await _run(
        "http.get",
        {
            "url": "https://api.example.com/user",
            "headers": {"authorization": {"$secret": "GITHUB_TOKEN", "format": "Bearer {}"}},
        },
    )
    assert result.status is RunStatus.COMPLETED, result
    assert seen[-1].headers["authorization"] == f"Bearer {TOKEN}"
    out = result.last_outputs["n"]
    assert out["headers"]["x-echo-auth"] == "Bearer [secret]"
    assert TOKEN not in _everything(result, emitter, checkpointer) + caplog.text


def test_a_format_must_hold_exactly_one_slot():
    from matrx_graph.secrets import is_secret_ref

    assert is_secret_ref({"$secret": "X", "format": "Bearer {}"})
    assert is_secret_ref({"$secret": "X", "format": None})
    for bad in ("Bearer", "{} {}", "{0.__class__} {}", "token={}&x={y}"):
        assert not is_secret_ref({"$secret": "X", "format": bad}), bad
    assert not is_secret_ref({"$secret": "X", "other": "y"})


async def test_the_resolver_hears_the_workflow_it_runs_in():
    from matrx_graph.secrets import SecretValues, configure_secret_resolver, resolve_secret_refs

    heard: list[str | None] = []

    async def resolver(name, *, user_id, organization_id, workflow_id=None):  # noqa: ANN001
        heard.append(workflow_id)
        return TOKEN

    configure_secret_resolver(resolver)
    out = await resolve_secret_refs({"a": {"$secret": "X"}}, user_id="u", organization_id=ORG,
                                    found=SecretValues(), workflow_id="wf-1")
    assert out == {"a": TOKEN} and heard == ["wf-1"]

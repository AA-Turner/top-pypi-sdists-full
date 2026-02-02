import json
from collections.abc import Callable
from typing import assert_never

import pytest
from pyreqwest.http import Url
from pyreqwest.middleware import Next, SyncNext
from pyreqwest.request import OneOffRequestBuilder, Request, SyncOneOffRequestBuilder
from pyreqwest.response import Response, SyncResponse
from pyreqwest.simple import request
from pyreqwest.simple import sync_request as sync

from tests.servers.server_subprocess import SubprocessServer


@pytest.mark.parametrize(
    "method",
    [
        request.pyreqwest_get,
        request.pyreqwest_post,
        request.pyreqwest_put,
        request.pyreqwest_patch,
        request.pyreqwest_delete,
        request.pyreqwest_head,
    ],
)
async def test_oneoff_method(echo_server: SubprocessServer, method: Callable[[Url], OneOffRequestBuilder]):
    req_builder = method(echo_server.url)
    assert isinstance(req_builder, OneOffRequestBuilder)
    resp = await req_builder.send()
    assert resp.status == 200 and resp.headers["x-request-method"] == method.__name__.split("_")[1].upper()


@pytest.mark.parametrize("method", ["GET", "get", "QUERY"])
async def test_oneoff_custom_method(echo_server: SubprocessServer, method: str):
    resp = await request.pyreqwest_request(method, echo_server.url).send()
    assert resp.status == 200 and resp.headers["x-request-method"] == method


@pytest.mark.parametrize("body", ["test text payload", b"test bytes payload", {"test": "json"}])
async def test_oneoff_body(echo_server: SubprocessServer, body: str | bytes | dict[str, str]):
    req = request.pyreqwest_post(echo_server.url)
    if isinstance(body, str):
        req, expected = req.body_text(body), body
    elif isinstance(body, bytes):
        req, expected = req.body_bytes(body), body.decode()
    elif isinstance(body, dict):
        req, expected = req.body_json(body), json.dumps(body, separators=(",", ":"))
    else:
        assert_never(body)
    resp = await req.send()
    assert (await resp.json())["body_parts"] == [expected] and resp.status == 200


async def test_oneoff_headers(echo_server: SubprocessServer):
    resp = await request.pyreqwest_get(echo_server.url).header("X-Test", "Value").send()
    assert resp.status == 200
    assert dict((await resp.json())["headers"])["x-test"] == "Value"


async def test_oneoff_query(echo_server: SubprocessServer):
    resp = await request.pyreqwest_get(echo_server.url).query({"q": "val"}).send()
    assert resp.status == 200
    assert dict((await resp.json())["query"]) == {"q": "val"}


async def test_oneoff_middleware(echo_server: SubprocessServer):
    async def middleware(request: Request, next_handler: Next) -> Response:
        request.headers["X-Middleware"] = "Applied"
        return await next_handler.run(request)

    resp = await request.pyreqwest_get(echo_server.url).with_middleware(middleware).send()
    assert resp.status == 200
    assert dict((await resp.json())["headers"])["x-middleware"] == "Applied"


async def test_oneoff_reuse_not_allowed(echo_server: SubprocessServer):
    req = request.pyreqwest_get(echo_server.url)
    assert (await req.send()).status == 200
    with pytest.raises(RuntimeError, match="Request was already sent"):
        await req.send()


@pytest.mark.parametrize(
    "method",
    [
        sync.pyreqwest_get,
        sync.pyreqwest_post,
        sync.pyreqwest_put,
        sync.pyreqwest_patch,
        sync.pyreqwest_delete,
        sync.pyreqwest_head,
    ],
)
def test_sync_oneoff_method(echo_server: SubprocessServer, method: Callable[[Url], SyncOneOffRequestBuilder]):
    req_builder = method(echo_server.url)
    assert isinstance(req_builder, SyncOneOffRequestBuilder)
    resp = req_builder.send()
    assert resp.status == 200 and resp.headers["x-request-method"] == method.__name__.split("_")[1].upper()


@pytest.mark.parametrize("method", ["GET", "get", "QUERY"])
def test_sync_oneoff_custom_method(echo_server: SubprocessServer, method: str):
    resp = sync.pyreqwest_request(method, echo_server.url).send()
    assert resp.status == 200 and resp.headers["x-request-method"] == method


@pytest.mark.parametrize("body", ["test text payload", b"test bytes payload", {"test": "json"}])
async def test_sync_oneoff_body(echo_server: SubprocessServer, body: str | bytes | dict[str, str]):
    req = sync.pyreqwest_post(echo_server.url)
    if isinstance(body, str):
        req, expected = req.body_text(body), body
    elif isinstance(body, bytes):
        req, expected = req.body_bytes(body), body.decode()
    elif isinstance(body, dict):
        req, expected = req.body_json(body), json.dumps(body, separators=(",", ":"))
    else:
        assert_never(body)
    resp = req.send()
    assert resp.json()["body_parts"] == [expected] and resp.status == 200


def test_sync_oneoff_headers(echo_server: SubprocessServer):
    resp = sync.pyreqwest_get(echo_server.url).header("X-Test", "Value").send()
    assert resp.status == 200
    assert dict(resp.json()["headers"])["x-test"] == "Value"


def test_sync_oneoff_query(echo_server: SubprocessServer):
    resp = sync.pyreqwest_get(echo_server.url).query({"q": "val"}).send()
    assert resp.status == 200
    assert dict(resp.json()["query"]) == {"q": "val"}


def test_sync_oneoff_middleware(echo_server: SubprocessServer):
    def middleware(request: Request, next_handler: SyncNext) -> SyncResponse:
        request.headers["X-Middleware"] = "Applied"
        return next_handler.run(request)

    resp = sync.pyreqwest_get(echo_server.url).with_middleware(middleware).send()
    assert resp.status == 200
    assert dict(resp.json()["headers"])["x-middleware"] == "Applied"


def test_sync_oneoff_reuse_not_allowed(echo_server: SubprocessServer):
    req = sync.pyreqwest_get(echo_server.url)
    assert req.send().status == 200
    with pytest.raises(RuntimeError, match="Request was already sent"):
        req.send()

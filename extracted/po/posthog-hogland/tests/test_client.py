"""Sync client behaviour, mocked at the httpx transport layer via respx."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx

from conftest import TEST_BASE_URL
from hogland import (
    AuthenticationError,
    BoxView,
    ConfigurationError,
    Hogbox,
    Hogland,
    NotFoundError,
    ServerError,
    ValidationError,
)


def make_client() -> Hogland:
    return Hogland(token="t", base_url=TEST_BASE_URL)


def _stub_box(client: Hogland, view_json: dict[str, Any], box_id: str | None = None) -> Hogbox:
    payload = {**view_json, "id": box_id} if box_id is not None else view_json
    return Hogbox(BoxView.model_validate(payload), client)


def test_trust_env_flows_to_the_http_client() -> None:
    # The hogland control-plane client is built with trust_env=False for in-cluster /
    # PrivateLink callers so it never routes through an HTTP(S)_PROXY. If this stops
    # reaching the httpx client, those calls hit the egress proxy and 407 in prod.
    assert Hogland(token="t", base_url=TEST_BASE_URL)._http._trust_env is True
    assert Hogland(token="t", base_url=TEST_BASE_URL, trust_env=False)._http._trust_env is False


@respx.mock
def test_create_returns_handle(box_view_json: dict[str, Any]) -> None:
    respx.post(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        return_value=httpx.Response(
            200,
            json={
                **box_view_json,
                "id": "hb-1234",
                "spec": {**box_view_json["spec"], "cpus": 2, "memory_mib": 4096},
            },
        ),
    )
    client = make_client()
    box = client.create(cpus=2, memory_mib=4096)
    assert isinstance(box, Hogbox)
    assert box.id == "hb-1234"
    assert box.status == "running"


# The server's access_type default is ssh-public, which REQUIRES an
# ssh_public_key on cold boot — the README's minimal create() 400'd. A
# keyless cold-boot create must therefore send access_type="none";
# everything else defers to explicit values or the server default.
@pytest.mark.parametrize(
    ("desc", "kwargs", "want_access_type"),
    [
        (
            "keyless cold boot defaults to none",
            {"cpus": 2, "memory_mib": 4096},
            "none",
        ),
        (
            "explicit access_type wins",
            {
                "cpus": 2,
                "memory_mib": 4096,
                "access_type": "ssh-public",
                "ssh_public_key": "ssh-ed25519 AAAA k",
            },
            "ssh-public",
        ),
        (
            "restores stay untouched to inherit the snapshot's mode",
            {"snapshot_id": "snap-1"},
            None,
        ),
        (
            "key without access_type keeps the server's ssh-public default",
            {"cpus": 2, "memory_mib": 4096, "ssh_public_key": "ssh-ed25519 AAAA k"},
            None,
        ),
    ],
)
@respx.mock
def test_create_access_type_defaulting(
    box_view_json: dict[str, Any],
    desc: str,
    kwargs: dict[str, Any],
    want_access_type: str | None,
) -> None:
    route = respx.post(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        return_value=httpx.Response(200, json={**box_view_json, "id": "hb-1234"}),
    )
    make_client().create(**kwargs)
    sent = json.loads(route.calls.last.request.content)
    if want_access_type is None:
        assert "access_type" not in sent, desc
    else:
        assert sent.get("access_type") == want_access_type, desc


@respx.mock
def test_exec_round_trip(box_view_json: dict[str, Any]) -> None:
    respx.post(f"{TEST_BASE_URL}/v1/hogboxes/hb-1/exec").mock(
        return_value=httpx.Response(
            200,
            json={
                "stdout": "hi\n",
                "stderr": "",
                "exit_code": 0,
                "timed_out": False,
                "duration_ms": 12,
            },
        ),
    )
    client = make_client()
    box = _stub_box(client, box_view_json, "hb-1")
    result = box.exec(["echo", "hi"])
    assert result.stdout == "hi\n"
    assert result.exit_code == 0
    assert result.duration_ms == 12


@respx.mock
def test_read_file_returns_raw_bytes(box_view_json: dict[str, Any]) -> None:
    # Server emits application/octet-stream — not JSON. See _box.py read_file
    # for the spec-vs-reality note.
    respx.get(f"{TEST_BASE_URL}/v1/hogboxes/hb-1/files").mock(
        return_value=httpx.Response(
            200,
            content=b"hello world",
            headers={"content-type": "application/octet-stream"},
        ),
    )
    client = make_client()
    box = _stub_box(client, box_view_json, "hb-1")
    assert box.read_file("/work/x") == b"hello world"


@respx.mock
def test_write_file_sends_octet_stream(box_view_json: dict[str, Any]) -> None:
    route = respx.put(f"{TEST_BASE_URL}/v1/hogboxes/hb-1/files").mock(
        return_value=httpx.Response(200, json={"bytes_written": 5}),
    )
    client = make_client()
    box = _stub_box(client, box_view_json, "hb-1")
    result = box.write_file("/work/y", b"hello", mode="755", mkdir=True)
    assert result.bytes_written == 5

    sent = route.calls.last.request
    assert sent.headers["content-type"] == "application/octet-stream"
    assert b"hello" in sent.content
    assert sent.url.params["path"] == "/work/y"
    assert sent.url.params["mode"] == "755"
    assert sent.url.params["mkdir"] == "true"


@respx.mock
def test_delete_swallows_404(box_view_json: dict[str, Any]) -> None:
    respx.delete(f"{TEST_BASE_URL}/v1/hogboxes/hb-gone").mock(
        return_value=httpx.Response(404, json={"detail": "gone"}),
    )
    client = make_client()
    box = _stub_box(client, box_view_json, "hb-gone")
    box.delete()  # must not raise


@respx.mock
def test_delete_raises_on_other_failures(box_view_json: dict[str, Any]) -> None:
    respx.delete(f"{TEST_BASE_URL}/v1/hogboxes/hb-1").mock(
        return_value=httpx.Response(500, json={"detail": "boom"}),
    )
    client = make_client()
    box = _stub_box(client, box_view_json, "hb-1")
    with pytest.raises(ServerError):
        box.delete()


@respx.mock
def test_unauthorized_raises_typed_error() -> None:
    respx.get(f"{TEST_BASE_URL}/v1/me").mock(
        return_value=httpx.Response(
            401,
            json={"detail": "bad bearer", "title": "Unauthorized"},
            headers={"content-type": "application/problem+json"},
        ),
    )
    client = make_client()
    with pytest.raises(AuthenticationError) as excinfo:
        client.me()
    assert excinfo.value.status_code == 401
    assert "bad bearer" in str(excinfo.value)


@respx.mock
def test_not_found_and_validation_paths() -> None:
    respx.get(f"{TEST_BASE_URL}/v1/hogboxes/hb-x").mock(
        return_value=httpx.Response(404, json={"detail": "no such box"}),
    )
    respx.post(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        return_value=httpx.Response(422, json={"detail": "server-side validation tripped"}),
    )
    client = make_client()
    with pytest.raises(NotFoundError):
        client.get("hb-x")
    # cpus=0.5 is valid client-side; the mocked 422 simulates the server
    # rejecting some other field combination we don't model in pydantic.
    with pytest.raises(ValidationError):
        client.create(cpus=0.5)


@respx.mock
def test_create_with_snapshot_omits_cpus_and_memory(box_view_json: dict[str, Any]) -> None:
    # Per the spec, cpus + memory_mib must be omitted on restore to inherit
    # from the snapshot. The SDK's default kwargs are None so they fall out
    # of the request body unless the caller passes them explicitly.
    route = respx.post(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        return_value=httpx.Response(200, json={**box_view_json, "id": "hb-restored"}),
    )
    client = make_client()
    client.create(snapshot_id="alias:foo")
    sent = json.loads(route.calls.last.request.content)
    assert "cpus" not in sent
    assert "memory_mib" not in sent
    assert sent["snapshot_id"] == "alias:foo"


@respx.mock
def test_create_with_web_port_sends_web_port(box_view_json: dict[str, Any]) -> None:
    # web_port opts the box into HTTP exposure; it must reach the wire as a
    # flat ``web_port`` int.
    route = respx.post(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        return_value=httpx.Response(200, json={**box_view_json, "id": "hb-exposed"}),
    )
    make_client().create(snapshot_id="alias:foo", web_port=8000)
    sent = json.loads(route.calls.last.request.content)
    assert sent["web_port"] == 8000


@respx.mock
def test_create_without_web_port_omits_web_port(box_view_json: dict[str, Any]) -> None:
    route = respx.post(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        return_value=httpx.Response(200, json=box_view_json),
    )
    make_client().create(snapshot_id="alias:foo")
    assert "web_port" not in json.loads(route.calls.last.request.content)


def test_create_web_port_out_of_range_raises() -> None:
    # Range-checked client-side (mirrors the CLI) — a bad port fails fast
    # before any HTTP, not as a server 4xx mid-create.
    with pytest.raises(ValueError, match="web_port"):
        make_client().create(snapshot_id="alias:foo", web_port=70000)


@respx.mock
def test_web_url_reads_server_value(box_view_json: dict[str, Any]) -> None:
    # web_url() reads the server-computed box-front URL from a fresh fetch —
    # the typed BoxView drops the field, so a cached-view read won't see it.
    client = make_client()
    box = _stub_box(client, box_view_json, "hb-w")
    respx.get(f"{TEST_BASE_URL}/v1/hogboxes/hb-w").mock(
        return_value=httpx.Response(
            200, json={**box_view_json, "id": "hb-w", "web_url": "https://hb-w.boxes.example.dev/"}
        ),
    )
    assert box.web_url() == "https://hb-w.boxes.example.dev/"


@respx.mock
def test_web_url_none_when_unexposed(box_view_json: dict[str, Any]) -> None:
    client = make_client()
    box = _stub_box(client, box_view_json, "hb-u")
    respx.get(f"{TEST_BASE_URL}/v1/hogboxes/hb-u").mock(
        return_value=httpx.Response(200, json={**box_view_json, "id": "hb-u"}),
    )
    assert box.web_url() is None


def test_missing_token_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    # conftest sets HOG_TOKEN; clear it for this one test.
    monkeypatch.delenv("HOG_TOKEN", raising=False)
    with pytest.raises(ConfigurationError):
        Hogland(base_url=TEST_BASE_URL)


def test_proxy_url_builder(box_view_json: dict[str, Any]) -> None:
    client = make_client()
    box = _stub_box(client, box_view_json, "hb-9")
    assert box.proxy_url(8080) == f"{TEST_BASE_URL}/v1/hogboxes/hb-9/proxy/8080/"
    assert box.proxy_url(8080, "/health") == f"{TEST_BASE_URL}/v1/hogboxes/hb-9/proxy/8080/health"


def test_status_property_reflects_cached_view(box_view_json: dict[str, Any]) -> None:
    # box.status reads the cached view — callers needing fresh state call
    # box.refresh() first. Property naming (not a verb method) makes the
    # cached-read shape obvious; consumers compare against "running" /
    # "paused" / "failed" / "destroyed" directly.
    client = make_client()
    running = _stub_box(client, box_view_json, "hb-r")
    assert running.status == "running"

    paused_view = BoxView.model_validate(
        {**running.view.model_dump(by_alias=True), "status": "paused"}
    )
    paused = Hogbox(paused_view, client)
    assert paused.status == "paused"


@respx.mock
def test_iter_boxes_follows_cursor(box_view_json: dict[str, Any]) -> None:
    page_a = {**box_view_json, "id": "hb-a"}
    page_b = {**box_view_json, "id": "hb-b"}
    respx.get(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        side_effect=[
            httpx.Response(200, json={"items": [page_a], "next_cursor": "c2"}),
            httpx.Response(200, json={"items": [page_b]}),
        ],
    )
    client = make_client()
    ids = [box.id for box in client.iter_boxes()]
    assert ids == ["hb-a", "hb-b"]


def test_module_exposes_version() -> None:
    import hogland

    assert isinstance(hogland.__version__, str)
    assert json.dumps(hogland.__version__)  # serialisable


@pytest.mark.parametrize(
    ("timeout_seconds", "want_read"),
    [
        (None, 30.0),
        # 0 means "run up to the server's 6h max"; the read leg must cover it
        # or httpx abandons the response at 30s while the command keeps going.
        (0, 21630.0),
        (-5, 30.0),
        (1, 31.0),
        (600, 630.0),
    ],
)
def test_exec_http_timeout_extends_read_only_when_set(
    timeout_seconds: int | None, want_read: float
) -> None:
    from hogland._box import _exec_http_timeout

    base = httpx.Timeout(connect=10.0, read=30.0, write=30.0, pool=30.0)
    got = _exec_http_timeout(base, timeout_seconds)
    assert got.read == want_read
    assert got.connect == 10.0
    assert got.write == 30.0
    assert got.pool == 30.0

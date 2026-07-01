"""Unit tests for the backdated web tools (Backsearch / Backfetch / BackSearchToolset).

These exercise the SDK-side responsibilities: URL validation, the
``REDIRECT DETECTED`` template, the preapproved-host fast path, the search
``Links: <JSON>`` / REMINDER output shape, ``as_of`` backdating, bearer-auth
forwarding, and the ``ToolOutput`` rendering inside the toolset.

The backend is mocked via a fake :class:`WebTransport` — these tests never hit
the network.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import pytest

from openreward import web_service
from openreward.tools import Backfetch, Backsearch, clear_web_fetch_cache
from openreward.toolsets import BackSearchToolset
from openreward.web_service import RawResponse, WebServiceConfig, WebServiceClient


# --------------------------------------------------------------------------- #
# Fake transport                                                              #
# --------------------------------------------------------------------------- #


class _Call:
    def __init__(self, method, url, params, json_body, headers):
        self.method = method
        self.url = url
        self.params = params
        self.json = json_body
        self.headers = headers


class FakeTransport:
    """Returns canned :class:`RawResponse` objects in order, recording calls."""

    def __init__(self, responses: list[RawResponse]):
        self._responses = list(responses)
        self.calls: list[_Call] = []

    async def request(self, method, url, *, params=None, json=None, headers=None) -> RawResponse:
        self.calls.append(_Call(method, url, params, json, headers))
        if not self._responses:
            raise AssertionError(f"No more mock responses queued (got {method} {url})")
        return self._responses.pop(0)

    async def aclose(self) -> None:
        pass


def _resp(status: int = 200, *, json_body: Any = None, headers: Optional[dict] = None) -> RawResponse:
    text = "" if json_body is None else json.dumps(json_body)
    return RawResponse(status=status, headers=headers or {}, text=text)


def _patch_default_transport(monkeypatch, responses: list[RawResponse]) -> FakeTransport:
    """Make every internally-created ``WebServiceClient`` use a fake transport."""
    transport = FakeTransport(responses)
    monkeypatch.setattr(web_service, "AiohttpTransport", lambda *a, **k: transport)
    return transport


@pytest.fixture
def web_env(monkeypatch):
    monkeypatch.setenv("OPENREWARD_API_KEY", "test-token")
    monkeypatch.setenv("OPENREWARD_WEB_FETCH_URL", "http://backend.test/fetch")
    monkeypatch.setenv("OPENREWARD_WEB_SEARCH_URL", "http://backend.test/search")
    monkeypatch.setenv("OPENREWARD_WEB_DOMAIN_INFO_URL", "http://backend.test/policy/domain_info")
    monkeypatch.setenv("OPENREWARD_WEB_SKIP_PREFLIGHT", "1")
    monkeypatch.delenv("OPENREWARD_WEB_PREAPPROVED_HOSTS", raising=False)
    monkeypatch.delenv("OPENREWARD_WEB_AS_OF", raising=False)
    clear_web_fetch_cache()
    yield
    clear_web_fetch_cache()


# --------------------------------------------------------------------------- #
# Backfetch — input validation                                                #
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_fetch_rejects_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENREWARD_API_KEY", raising=False)
    r = await Backfetch().run("https://example.com", "x")
    assert r.ok is False
    assert r.error_code == "not-configured"
    assert "OPENREWARD_API_KEY" in r.error_message


@pytest.mark.asyncio
async def test_fetch_rejects_unparseable_url(web_env):
    r = await Backfetch().run("not a url", "x")
    assert r.ok is False
    assert r.error_code == "invalid-url"


@pytest.mark.asyncio
async def test_fetch_rejects_bare_hostname(web_env):
    r = await Backfetch().run("https://intranet/", "x")
    assert r.ok is False
    assert r.error_code == "hostname-too-shallow"


@pytest.mark.asyncio
async def test_fetch_rejects_userinfo(web_env):
    r = await Backfetch().run("https://user:pw@example.com/", "x")
    assert r.ok is False
    assert r.error_code == "userinfo-not-allowed"


@pytest.mark.asyncio
async def test_fetch_rejects_oversized_url(web_env):
    huge = "https://example.com/" + ("a" * 2_100)
    r = await Backfetch().run(huge, "x")
    assert r.ok is False
    assert r.error_code == "url-too-long"


@pytest.mark.asyncio
async def test_fetch_rejects_bad_as_of(web_env):
    r = await Backfetch(as_of="not-a-date").run("https://example.com/", "x")
    assert r.ok is False
    assert r.error_code == "invalid-as-of"


# --------------------------------------------------------------------------- #
# Backfetch — backend integration                                             #
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_fetch_returns_content(web_env, monkeypatch):
    _patch_default_transport(
        monkeypatch,
        [_resp(json_body={"url": "https://example.com/", "text": "Welcome to example."})],
    )
    r = await Backfetch().run("https://example.com/", "what is this")
    assert r.ok is True
    assert "Welcome to example." in r.output
    assert r.data["url"] == "https://example.com/"
    assert r.data["prompt"] == "what is this"
    assert r.data["content"] == "Welcome to example."


@pytest.mark.asyncio
async def test_fetch_threads_as_of_into_request(web_env, monkeypatch):
    transport = _patch_default_transport(
        monkeypatch,
        [_resp(json_body={"url": "https://example.com/", "text": "hi"})],
    )
    await Backfetch(as_of="2025-12-01").run("https://example.com/", "p")
    body = transport.calls[-1].json
    assert body["as_of"] == "2025-12-01"
    assert transport.calls[-1].headers["X-API-Key"] == "test-token"


@pytest.mark.asyncio
async def test_fetch_preapproved_host_fast_path(web_env, monkeypatch):
    monkeypatch.setenv("OPENREWARD_WEB_PREAPPROVED_HOSTS", "docs.python.org, example.com")
    _patch_default_transport(
        monkeypatch,
        [_resp(json_body={"url": "https://docs.python.org/3/", "text": "Welcome to Python."})],
    )
    r = await Backfetch().run("https://docs.python.org/3/", "what is this")
    assert r.ok is True
    # Preapproved fast path: raw content, no labelled envelope.
    assert r.output == "Welcome to Python."


@pytest.mark.asyncio
async def test_fetch_cross_host_redirect_returns_template(web_env, monkeypatch):
    _patch_default_transport(
        monkeypatch,
        [
            _resp(
                json_body={
                    "url": "https://example.com/",
                    "text": "",
                    "redirect": {"to": "https://other.example.org/landing", "status": 301},
                }
            )
        ],
    )
    r = await Backfetch().run("https://example.com/", "what is here")
    assert r.ok is True
    out = r.output
    assert "REDIRECT DETECTED:" in out
    assert "https://other.example.org/landing" in out
    assert 'url: "https://other.example.org/landing"' in out
    assert 'prompt: "what is here"' in out


@pytest.mark.asyncio
async def test_fetch_same_host_modulo_www_does_not_bounce(web_env, monkeypatch):
    _patch_default_transport(
        monkeypatch,
        [
            _resp(
                json_body={
                    "url": "https://example.com/",
                    "text": "Same-host content.",
                    "redirect": {"to": "https://www.example.com/landing", "status": 301},
                }
            )
        ],
    )
    r = await Backfetch().run("https://example.com/", "summarise")
    assert r.ok is True
    assert "REDIRECT DETECTED:" not in r.output
    assert "Same-host content." in r.output


@pytest.mark.asyncio
async def test_fetch_preflight_blocks_domain(web_env, monkeypatch):
    monkeypatch.setenv("OPENREWARD_WEB_SKIP_PREFLIGHT", "0")
    _patch_default_transport(
        monkeypatch,
        [_resp(json_body={"can_fetch": False, "reason": "denylisted"})],
    )
    r = await Backfetch().run("https://blocked.example.com/", "p")
    assert r.ok is False
    assert r.error_code == "domain-blocked"
    assert "denylisted" in r.error_message


# --------------------------------------------------------------------------- #
# Backsearch                                                                  #
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_search_rejects_short_query(web_env):
    r = await Backsearch().run("a")
    assert r.ok is False
    assert r.error_code == "missing-query"


@pytest.mark.asyncio
async def test_search_rejects_both_domain_lists(web_env):
    r = await Backsearch().run(
        "current events", allowed_domains=["bbc.co.uk"], blocked_domains=["cnn.com"]
    )
    assert r.ok is False
    assert r.error_code == "domain-lists-conflict"


@pytest.mark.asyncio
async def test_search_rejects_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENREWARD_API_KEY", raising=False)
    r = await Backsearch().run("hello world")
    assert r.ok is False
    assert r.error_code == "not-configured"


@pytest.mark.asyncio
async def test_search_formats_links_envelope(web_env, monkeypatch):
    _patch_default_transport(
        monkeypatch,
        [
            _resp(
                json_body={
                    "mode": "hybrid",
                    "hits": [
                        {"url": "https://bbc.co.uk/a", "title": "BBC story A"},
                        {"url": "https://reuters.com/b", "title": "Reuters story B"},
                    ],
                }
            )
        ],
    )
    r = await Backsearch().run("Trump Venezuela")
    assert r.ok is True
    out = r.output
    assert out.startswith('Web search results for query: "Trump Venezuela"')
    # Literal Links: <JSON> line, not markdown bullets.
    assert (
        'Links: [{"title": "BBC story A", "url": "https://bbc.co.uk/a"},'
        ' {"title": "Reuters story B", "url": "https://reuters.com/b"}]'
    ) in out
    assert out.rstrip().endswith(
        "REMINDER: You MUST include the sources above in your response to the user "
        "using markdown hyperlinks."
    )


@pytest.mark.asyncio
async def test_search_renders_no_links_for_empty_backend(web_env, monkeypatch):
    _patch_default_transport(monkeypatch, [_resp(json_body={"mode": "hybrid", "hits": []})])
    r = await Backsearch().run("obscure unfindable query")
    assert r.ok is True
    assert "No links found." in r.output
    assert "REMINDER:" in r.output


@pytest.mark.asyncio
async def test_search_surfaces_structured_error_message(web_env, monkeypatch):
    # Backend rejects an unparseable query with the {result, message, errorCode}
    # envelope. The agent should see the clean message, not the raw JSON body.
    _patch_default_transport(
        monkeypatch,
        [
            _resp(
                400,
                json_body={
                    "result": False,
                    "message": "Error: Invalid query",
                    "errorCode": 1,
                },
            )
        ],
    )
    r = await Backsearch().run("f(x)")
    assert r.ok is False
    assert r.error_code == "web-service-error"
    assert "Error: Invalid query" in r.error_message
    # The raw JSON envelope must not leak into the model-facing message.
    assert "{" not in r.error_message and "result" not in r.error_message


@pytest.mark.asyncio
async def test_error_carries_envelope_detail_and_code(web_env):
    # Lower-level: the raised WebServiceError exposes the parsed message + code,
    # and falls back to the raw snippet when the body isn't the envelope shape.
    transport = FakeTransport(
        [
            _resp(
                400,
                json_body={
                    "result": False,
                    "message": "Error: Invalid query",
                    "errorCode": 1,
                },
            ),
            _resp(503, json_body=None),
        ]
    )
    client = WebServiceClient(WebServiceConfig.from_env(), transport=transport)

    with pytest.raises(web_service.WebServiceError) as exc:
        await client.search(query="f(x)", as_of="2026-05-31")
    assert exc.value.status == 400
    assert exc.value.detail == "Error: Invalid query"
    assert exc.value.error_code == 1

    with pytest.raises(web_service.WebServiceError) as exc2:
        await client.search(query="anything", as_of="2026-05-31")
    assert exc2.value.status == 503
    assert exc2.value.detail is None
    assert exc2.value.error_code is None


@pytest.mark.asyncio
async def test_search_forwards_bearer_token_k_and_as_of(web_env, monkeypatch):
    transport = _patch_default_transport(
        monkeypatch, [_resp(json_body={"mode": "hybrid", "hits": []})]
    )
    await Backsearch(as_of="2025-12-31").run("hello world")
    assert len(transport.calls) == 1
    sent = transport.calls[0]
    assert sent.method == "POST"
    # Authenticate with X-API-Key, matching the rest of the SDK.
    assert sent.headers["X-API-Key"] == "test-token"
    assert "Authorization" not in sent.headers
    body = sent.json
    assert body["query"] == "hello world"
    assert body["k"] == 8  # hardcoded max results cap
    assert body["mode"] == "hybrid"
    assert body["as_of"] == "2025-12-31"


# --------------------------------------------------------------------------- #
# BackSearchToolset                                                           #
# --------------------------------------------------------------------------- #


class _EnvWithCutoff:
    """Stand-in environment that configures the cutoff via an attribute."""

    web_as_of = "2024-06-30"


def test_toolset_registered_as_builtin():
    from openreward.toolsets import BUILTIN_TOOLSETS

    assert BUILTIN_TOOLSETS["backsearch"] is BackSearchToolset
    assert BackSearchToolset.name() == "backsearch"


def test_toolset_resolves_cutoff_priority(monkeypatch):
    monkeypatch.setenv("OPENREWARD_WEB_AS_OF", "2020-01-01")
    # explicit arg wins
    assert BackSearchToolset(None, as_of="2025-12-01").as_of == "2025-12-01"
    # env attribute beats env var
    assert BackSearchToolset(_EnvWithCutoff()).as_of == "2024-06-30"
    # env var is the fallback
    assert BackSearchToolset(None).as_of == "2020-01-01"


class _ProgressingEnv:
    """Env whose simulated 'now' advances — exposes web_as_of as a property."""

    def __init__(self, start: str):
        self._now = start

    @property
    def web_as_of(self):
        return self._now

    def step(self, to: str):
        self._now = to


@pytest.mark.asyncio
async def test_toolset_cutoff_advances_with_env_date(web_env, monkeypatch):
    from openreward.toolsets.backsearch import WebSearchParams

    transport = _patch_default_transport(
        monkeypatch,
        [
            _resp(json_body={"mode": "hybrid", "hits": []}),
            _resp(json_body={"mode": "hybrid", "hits": []}),
        ],
    )
    env = _ProgressingEnv("2025-01-01")
    ts = BackSearchToolset(env)  # no pin — should track the env's clock

    await ts.web_search(WebSearchParams(query="day one"))
    assert transport.calls[-1].json["as_of"] == "2025-01-01"

    env.step("2025-06-15")  # simulation advances
    await ts.web_search(WebSearchParams(query="day two"))
    assert transport.calls[-1].json["as_of"] == "2025-06-15"


@pytest.mark.asyncio
async def test_toolset_callable_web_as_of(web_env, monkeypatch):
    from openreward.toolsets.backsearch import WebFetchParams

    transport = _patch_default_transport(
        monkeypatch, [_resp(json_body={"url": "https://example.com/", "text": "hi"})]
    )

    class _ClockEnv:
        web_as_of = staticmethod(lambda: "2023-03-03")

    ts = BackSearchToolset(_ClockEnv())
    await ts.web_fetch(WebFetchParams(url="https://example.com/", prompt="p"))
    assert transport.calls[-1].json["as_of"] == "2023-03-03"


@pytest.mark.asyncio
async def test_toolset_explicit_pin_overrides_env_clock(web_env):
    env = _ProgressingEnv("2025-01-01")
    ts = BackSearchToolset(env, as_of="2030-12-31")
    # Explicit pin is static and wins even as the env advances.
    assert ts.as_of == "2030-12-31"
    env.step("2026-01-01")
    assert ts.as_of == "2030-12-31"


@pytest.mark.asyncio
async def test_toolset_web_search_returns_tooloutput(web_env, monkeypatch):
    from openreward.toolsets.backsearch import WebSearchParams

    transport = _patch_default_transport(
        monkeypatch,
        [_resp(json_body={"mode": "hybrid", "hits": [{"url": "https://x.com/a", "title": "A"}]})],
    )
    ts = BackSearchToolset(None, as_of="2025-12-01")
    # `@tool` leaves the function callable as a normal bound method.
    out = await ts.web_search(WebSearchParams(query="hello world"))
    assert out.blocks[0].text.startswith('Web search results for query: "hello world"')
    assert out.finished is False
    assert out.metadata["hits"] == [{"url": "https://x.com/a", "title": "A"}]
    assert transport.calls[0].json["as_of"] == "2025-12-01"


@pytest.mark.asyncio
async def test_toolset_web_fetch_soft_error_is_tooloutput(web_env):
    from openreward.toolsets.backsearch import WebFetchParams

    ts = BackSearchToolset(None)
    out = await ts.web_fetch(WebFetchParams(url="not a url", prompt="p"))
    # Soft errors surface as text + metadata.error, not as a raised exception.
    assert "invalid-url" in out.blocks[0].text or "Error" in out.blocks[0].text
    assert out.metadata["error"] == "invalid-url"


def test_backsearch_composes_with_another_toolset():
    """An env can declare multiple toolsets; BackSearchToolset (no sandbox)
    composes with the sandbox-backed CLIToolset without a name collision.

    Tool discovery is class-level, so no sandbox is needed to list them."""
    from openreward.environments import Environment
    from openreward.environments.types import Blocks, TextBlock
    from openreward.toolsets import CLIToolset

    class ComposedEnv(Environment):
        toolsets = [BackSearchToolset, CLIToolset]

        @classmethod
        def list_splits(cls) -> list[str]:
            return ["train"]

        @classmethod
        def list_tasks(cls, split: str):
            return [{"id": "1"}]

        def get_prompt(self) -> Blocks:
            return [TextBlock(text="hi")]

    env = ComposedEnv(task_spec={"id": "1"})
    names = [t.name for t in env.list_tools().tools]

    # Both toolset surfaces are present...
    assert {"web_search", "web_fetch"}.issubset(names)   # BackSearchToolset
    assert {"bash", "grep", "read"}.issubset(names)       # CLIToolset
    # ...and there is no duplicate/shadowed tool name across the two toolsets.
    assert len(names) == len(set(names))


# --------------------------------------------------------------------------- #
# Engine via explicit injected client (transport-level)                       #
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_egress_block_detected_via_proxy_header(web_env):
    from openreward.tools.web import run_fetch

    config = WebServiceConfig.from_env()
    transport = FakeTransport(
        [_resp(403, json_body={"domain": "evil.test"}, headers={"x-proxy-error": "blocked-by-allowlist"})]
    )
    client = WebServiceClient(config, transport=transport)
    r = await run_fetch(url="https://evil.test/", prompt="p", client=client, config=config)
    assert r.ok is False
    assert r.error_code == "egress-blocked"

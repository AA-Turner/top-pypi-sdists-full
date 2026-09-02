"""matrx-ai resolves Mandates over the API when it runs as a CLIENT.

THE DISTINCTION (Arman, 2026-08-16): not "with a database" vs "without one" —
matrx-ai always has a database and everything persists. It is SERVER vs CLIENT.
A client has full access to its own client-side data; it cannot reach
server-only tables (`agent.mandate`), so it asks over the API instead.

Before this, a client had no way to ask, so it ran an agent id frozen in its own
source. matrx-local WILL have mandates, so this path is load-bearing.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.client_host.mandate_source import ServerMandateSource, MandateSourceFetchError


class _FakeResponse:
    def __init__(self, status_code: int, payload: object, text: str = "") -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = text or json.dumps(payload)

    def json(self) -> object:
        if isinstance(self._payload, str):
            raise ValueError("not json")
        return self._payload


class _FakeClient:
    def __init__(self, response: _FakeResponse, captured: dict) -> None:
        self._response = response
        self._captured = captured

    async def __aenter__(self) -> "_FakeClient":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        return None

    async def get(self, url: str, headers: dict) -> _FakeResponse:
        self._captured["url"] = url
        self._captured["headers"] = headers
        return self._response


@pytest.fixture
def patch_httpx(monkeypatch):
    def install(response: _FakeResponse) -> dict:
        captured: dict = {}
        import httpx

        monkeypatch.setattr(httpx, "AsyncClient", lambda **kw: _FakeClient(response, captured))
        return captured

    return install


def _ok_payload(**overrides) -> dict:
    payload = {
        "mandate_key": "podcast.deep_research",
        "agent_id": "version-abc",
        "is_version": True,
        "definition_agent_id": "master-abc",
        "config_overrides": {"temperature": 0.2},
        "contract": {"spill_variables": ["topic"], "required_variables": ["topic"]},
        "provenance": "user",
    }
    payload.update(overrides)
    return payload


@pytest.mark.asyncio
async def test_resolves_a_mandate_and_carries_the_dbs_version_decision(patch_httpx) -> None:
    captured = patch_httpx(_FakeResponse(200, _ok_payload()))
    source = ServerMandateSource("https://server.example.com", lambda: "jwt-token")

    resolution = await source("podcast.deep_research")

    assert captured["url"] == (
        "https://server.example.com/api/mandates/podcast.deep_research/resolution"
    )
    assert captured["headers"]["Authorization"] == "Bearer jwt-token"
    # is_version comes from the DB — the client transports it, never decides it.
    assert resolution.source.agent_id == "version-abc"
    assert resolution.source.is_version is True
    assert resolution.config_overrides == {"temperature": 0.2}
    assert resolution.spill_variables == frozenset({"topic"})


@pytest.mark.asyncio
async def test_a_floating_mandate_resolves_to_a_master_not_a_version(patch_httpx) -> None:
    patch_httpx(_FakeResponse(200, _ok_payload(agent_id="master-abc", is_version=False)))
    source = ServerMandateSource("https://server.example.com", lambda: "jwt-token")

    resolution = await source("podcast.deep_research")

    assert resolution.source.is_version is False


@pytest.mark.asyncio
async def test_it_REFUSES_to_resolve_anonymously(patch_httpx) -> None:
    """The answer depends on the CALLER — user and org bindings decide the
    agent. An anonymous fetch would return the system default and silently
    ignore the user's own rebind, which looks like success."""
    patch_httpx(_FakeResponse(200, _ok_payload()))
    source = ServerMandateSource("https://server.example.com", get_jwt=None)

    with pytest.raises(MandateSourceFetchError, match="anonymous"):
        await source("podcast.deep_research")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response",
    [
        _FakeResponse(404, {"detail": "no such mandate"}),
        _FakeResponse(500, {"detail": "boom"}),
        _FakeResponse(200, "not-json"),
        _FakeResponse(200, [1, 2, 3]),
        _FakeResponse(200, _ok_payload(agent_id="")),
        _FakeResponse(200, {k: v for k, v in _ok_payload().items() if k != "is_version"}),
    ],
)
async def test_every_bad_answer_raises_rather_than_guessing(patch_httpx, response) -> None:
    """No soft answers. Anything the client cannot read as a definite agent
    must raise, so run_mandated refuses the run — the client half of "no seed
    fallback"."""
    patch_httpx(response)
    source = ServerMandateSource("https://server.example.com", lambda: "jwt-token")

    with pytest.raises(MandateSourceFetchError):
        await source("podcast.deep_research")


@pytest.mark.asyncio
async def test_a_client_resolver_makes_run_mandated_refuse_loudly_on_failure(
    patch_httpx, monkeypatch
) -> None:
    """End to end: a failing client resolution surfaces as the SAME loud
    refusal a server-side failure produces, never a fallback agent."""
    from matrx_ai import mandates
    from matrx_ai import _ext
    from matrx_ai.agents.executor import AgentRunResult
    from pydantic import BaseModel

    captured: list[dict[str, object]] = []

    async def record_error(exc: BaseException, **kwargs: object) -> None:
        captured.append({"exc": exc, **kwargs})

    monkeypatch.setattr(
        _ext,
        "get_ext",
        lambda name: record_error if name == "record_error" else None,
    )

    class _Inputs(BaseModel):
        topic: str

    class _ClientAgent:
        name = "client-agent"
        mandate_key = "podcast.deep_research"
        Inputs = _Inputs

        @classmethod
        def prepare_variables(cls, inputs: BaseModel) -> dict:
            return inputs.model_dump()

        @classmethod
        async def run(cls, **kwargs) -> AgentRunResult:  # pragma: no cover
            raise AssertionError("must never run without a resolved agent")

    patch_httpx(_FakeResponse(503, {"detail": "server down"}))
    monkeypatch.setattr(
        mandates,
        "_MANDATE_RESOLVER",
        ServerMandateSource("https://server.example.com", lambda: "jwt-token"),
    )

    with pytest.raises(mandates.MandateResolutionUnavailable):
        await mandates.run_mandated(_ClientAgent, inputs={"topic": "sourdough"})

    assert len(captured) == 1
    assert captured[0]["kind"] == "mandate_resolution_failed"
    assert captured[0]["payload"] == {
        "mandate_key": "podcast.deep_research",
        "consumer": "_ClientAgent",
        "effect": "run REFUSED; no agent ran and nothing was charged",
    }

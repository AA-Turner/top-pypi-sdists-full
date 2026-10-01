"""send_once never lets the wire clone outlive the call.

The wire clone carries materialized picklist / fence VALUES; the canonical
config carries their placeholders. Whatever ends the provider call — success,
provider error, a stop, or task cancellation — the request must hold the
canonical config again, or a cancel handler that persists the partial turn
persists the secret values.

The provider client here is a stand-in for the network only; the swap/restore
under test is send_once's own code, driven by the real ``SendPrep`` type.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.config import send_boundary
from matrx_ai.config.send_boundary import SendPrep
from matrx_ai.orchestrator.send_once import send_once


class _Stopped(Exception):
    pass


def _request():
    return SimpleNamespace(
        config="CANONICAL", conversation_id="c", request_id="r", organization_id=None
    )


class _Client:
    def __init__(self, outcome):
        self.outcome = outcome
        self.saw_config = None

    async def execute(self, request):
        self.saw_config = request.config
        if isinstance(self.outcome, BaseException):
            raise self.outcome
        return self.outcome


@pytest.fixture(autouse=True)
def _wire_clone(monkeypatch):
    async def _prep(config, **_kw):
        return SendPrep(stage="loop", wire_config="WIRE")

    monkeypatch.setattr(send_boundary, "prepare_for_send", _prep)


@pytest.mark.parametrize(
    "outcome",
    ["ok", RuntimeError("provider 500"), _Stopped("stopped"), asyncio.CancelledError()],
    ids=["success", "provider_error", "stop", "cancelled"],
)
def test_canonical_config_is_restored_on_every_exit(outcome):
    request = _request()
    client = _Client(outcome)
    state = SimpleNamespace(snapshot_payload=None)

    async def _run():
        return await send_once(
            client, request, state=state, iteration=1, stop_exceptions=(_Stopped,)
        )

    if isinstance(outcome, BaseException):
        with pytest.raises(type(outcome)):
            asyncio.run(_run())
    else:
        assert asyncio.run(_run()).response == "ok"
    assert client.saw_config == "WIRE", "the provider must receive the wire clone"
    assert request.config == "CANONICAL", f"wire clone outlived the call on {outcome!r}"

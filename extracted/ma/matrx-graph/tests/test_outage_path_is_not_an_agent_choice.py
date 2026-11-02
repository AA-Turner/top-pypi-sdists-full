"""THE STRICTNESS LAW clause 6 — the outage path requires a proven outage.

``catalog_unreachable`` is the one degraded reason that survives enforcement:
an infra outage must never masquerade as validation success OR take down a
user's run. That is exactly what made it dangerous. Every catalog read sat
behind a bare ``except Exception``, so a typo in a manager call landed in the
same branch as a downed database — "validation skipped, run continues" — and
the logs could not tell the two apart.

These tests pin BOTH directions, because a guard proven in only one is not
evidence: bad code must be unable to reach the hatch, AND a real outage must
still reach it.
"""

from __future__ import annotations

import pytest

from matrx_graph import kinds
from matrx_graph.kinds import KindDegradedReason, resolve_kind


class _Manager:
    def __init__(self, exc: BaseException) -> None:
        self._exc = exc

    async def load_items(self, **_kwargs: object) -> list[object]:
        raise self._exc


@pytest.fixture(autouse=True)
def _clean_catalog(monkeypatch: pytest.MonkeyPatch):
    kinds._cache.clear()
    kinds._warned_slugs.clear()
    yield
    kinds._cache.clear()
    kinds._warned_slugs.clear()


@pytest.mark.parametrize(
    "exc",
    [
        ConnectionError("could not connect to server: Connection refused"),
        TimeoutError("pool acquire timed out"),
        OSError("network is unreachable"),
        RuntimeError("the kind_definition_manager is not registered"),
    ],
    ids=["refused", "timeout", "network", "unwired"],
)
async def test_a_real_outage_still_degrades(monkeypatch: pytest.MonkeyPatch, exc: BaseException):
    """The false positive that must NOT fire: a genuine outage is still an outage."""
    monkeypatch.setattr(kinds, "_manager", lambda: _Manager(exc))
    entry, reason = await resolve_kind("kd6_probe_outage")
    assert entry is None
    assert reason is KindDegradedReason.CATALOG_UNREACHABLE


@pytest.mark.parametrize(
    "exc",
    [
        TypeError("load_items() got an unexpected keyword argument 'kimd'"),
        AttributeError("'NoneType' object has no attribute 'load_items'"),
        NameError("name 'kind_definiton_manager' is not defined"),
        KeyError("emitted_json_shema"),
        ImportError("cannot import name 'get_instance'"),
    ],
    ids=["typo-kwarg", "none-manager", "typo-name", "typo-column", "bad-import"],
)
async def test_bad_code_cannot_reach_the_outage_path(
    monkeypatch: pytest.MonkeyPatch, exc: BaseException
):
    """The true positive: every named way of writing bad code RAISES instead."""
    monkeypatch.setattr(kinds, "_manager", lambda: _Manager(exc))
    with pytest.raises(RuntimeError, match="DEFECT IN THIS CODE"):
        await resolve_kind("kd6_probe_badcode")


async def test_the_raise_names_the_error_and_the_law(monkeypatch: pytest.MonkeyPatch):
    """A guard that fails without naming the fix trains people to silence it."""
    monkeypatch.setattr(kinds, "_manager", lambda: _Manager(TypeError("bad kwarg")))
    with pytest.raises(RuntimeError) as caught:
        await resolve_kind("kd6_probe_message")
    message = str(caught.value)
    assert "TypeError" in message
    assert KindDegradedReason.CATALOG_UNREACHABLE.value in message
    assert "clause 6" in message
    assert isinstance(caught.value.__cause__, TypeError)

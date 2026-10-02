"""A finished run records its own observation count once; the runs list reads it instead of
counting 17.8M search_performance rows per page — and a run without one still gets the exact count."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_seo import orm_repository as repo_mod
from matrx_seo.orm_repository import OBSERVATION_COUNT_KEY, OrmSeoRepository, stored_observation_count


class _Grouped:
    def __init__(self, table, log):
        self._table, self._log, self._ids = table, log, []

    def filter(self, **kw):
        self._ids = kw["run_id__in"]
        return self

    def annotate(self, **_):
        return self

    def group_by(self, *_):
        return self

    def order_by(self, *_):
        return self

    async def values(self, *_):
        self._log.append((self._table.__name__, tuple(self._ids)))
        return [{"run_id": i, "n": 7, "id": f"payload-{i}"} for i in self._ids]


def _model(name, log):
    cls = type(name, (), {})
    cls.filter = lambda self=None, **kw: _Grouped(cls, log).filter(**kw)
    return cls


@pytest.fixture
def world(monkeypatch):
    log: list = []
    obs = (_model("Obs", log),)
    monkeypatch.setattr(repo_mod, "_OBSERVATION_MODELS", obs)
    monkeypatch.setattr(repo_mod.m, "RawPayload", _model("RawPayload", log))
    return log


def test_the_stored_count_is_read_from_the_runs_own_metadata():
    assert stored_observation_count(SimpleNamespace(metadata={OBSERVATION_COUNT_KEY: 12})) == 12
    assert stored_observation_count(SimpleNamespace(metadata={})) is None
    assert stored_observation_count(SimpleNamespace(metadata=None)) is None


@pytest.mark.asyncio
async def test_a_stored_run_is_not_counted_and_an_unstored_run_still_is(world):
    runs = [SimpleNamespace(id="a"), SimpleNamespace(id="b")]
    out = await OrmSeoRepository().receipts_for_runs(runs, stored_counts={"a": 41})
    assert out["a"].existing_observations == 41, "the stored count is the answer"
    assert out["b"].existing_observations == 7, "no stored count: the exact count, as before"
    counted = [ids for name, ids in world if name == "Obs"]
    assert counted == [("b",)], "the observation tables were never asked about the stored run"

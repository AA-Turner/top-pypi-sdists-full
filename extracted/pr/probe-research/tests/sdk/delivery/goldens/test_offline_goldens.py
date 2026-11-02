"""Goldens for `open_offline_run`: the offline folder it writes and the run it returns, per
`probe.init()` keyword shape (plain, external id, conflict policies, an online init falling back)."""

from __future__ import annotations

import pytest

from probe.sdk.delivery.offline.offline import open_offline_run
from probe.sdk.settings.settings import Settings
from tests.sdk.delivery.goldens.recorder import Normaliser, check, describe_error, dump_tree


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)


SCENARIOS = {
    "plain": dict(kw={"project": "p", "experiment": "e", "name": "r1"}),
    "config_and_tags": dict(kw={"project": "p", "name": "r2", "config": {"lr": 0.1}, "tags": ["a", "b"]}),
    "external_id": dict(kw={"project": "p", "external_id": "job-7"}),
    "on_conflict_supersede": dict(kw={"project": "p", "external_id": "job-7", "on_conflict": "supersede"}),
    "on_conflict_resume_refused": dict(kw={"project": "p", "external_id": "job-7", "on_conflict": "resume"}),
    "fallback_with_sent_create": dict(kw={"project": "p", "name": "r3"}, fallback=True, sent={
        "path": "/v1/projects/p/runs", "body": {"name": "r3", "external_id": "job-9"}}),
    "with_settings": dict(kw={"project": "p", "name": "r4"},
                          settings=Settings(base_url="http://test", token="ros_pat_deadbeef", workspace="ws")),
}


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_offline_golden(name, tmp_path):
    norm = Normaliser(tmp_path)
    case = dict(SCENARIOS[name])
    base = tmp_path / "offline"
    try:
        run = open_offline_run(case.pop("kw"), base=base, **case)
        returned = {k: getattr(run, k, None) for k in ("id", "name", "offline", "external_id", "project", "experiment")}
        try:
            run.finish()
        except Exception as exc:  # noqa: BLE001 -- recorded
            returned["finish_error"] = describe_error(exc, norm)
        outcome = {"run": norm.value(returned)}
    except Exception as exc:  # noqa: BLE001 -- the refusal IS the golden
        outcome = {"error": describe_error(exc, norm)}
    check(f"offline/{name}", {**outcome, "folder": dump_tree(base, norm)})

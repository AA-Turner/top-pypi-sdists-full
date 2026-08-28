"""TASK TEMPLATES (2026-08-26) — blueprint records over groups + workers.

Operator concept: "Templates => worker groups && => module groups" — map what
groups a task needs, reserve the pool for uninterrupted execution. These tests
cover the record layer and derivations; activation orchestration is
route-layer (worker store) and exercised on dev.

    ./venv/bin/pytest tests/test_task_templates.py -q
"""
import importlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

PG = importlib.import_module("abstract_hugpy_dev.comms.priority_groups")
TT = importlib.import_module("abstract_hugpy_dev.comms.task_templates")
SETTINGS = importlib.import_module("abstract_hugpy_dev.comms.settings")


@pytest.fixture()
def isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("HUGPY_SETTINGS_PATH", str(tmp_path / "settings.json"))
    SETTINGS.settings_store._cache = None
    SETTINGS.settings_store._cache_at = 0.0
    yield tmp_path
    SETTINGS.settings_store._cache = None
    SETTINGS.settings_store._cache_at = 0.0


def test_template_roundtrip(isolated):
    PG.put_group("cast", name="cast", members=["m1"])
    rec, errors = TT.put_template("night-shoot", name="night-shoot",
                                  groups=["cast"], workers=["ae"])
    assert errors == []
    assert TT.get_template("night-shoot")["groups"] == ["cast"]
    assert TT.get_template("night-shoot")["workers"] == ["ae"]
    assert TT.get_template("night-shoot")["active"] is False


def test_template_refuses_dangling_group(isolated):
    rec, errors = TT.put_template("t", name="t", groups=["ghost"])
    assert rec is None
    assert any("no such priority group" in e for e in errors)


def test_template_requires_a_group(isolated):
    rec, errors = TT.put_template("t", name="t", groups=[])
    assert rec is None
    assert any("at least one priority group" in e for e in errors)


def test_derive_workers_prefers_own_list(isolated):
    PG.put_group("g", name="g", members=["m1"], workers=["computron"])
    TT.put_template("t", name="t", groups=["g"], workers=["ae"])
    assert TT.derive_workers(TT.get_template("t")) == ["ae"]


def test_derive_workers_unions_group_fences_in_order(isolated):
    PG.put_group("g1", name="g1", members=["m1"], workers=["ae", "computron"])
    PG.put_group("g2", name="g2", members=["m2"], workers=["op", "ae"])
    TT.put_template("t", name="t", groups=["g1", "g2"])
    assert TT.derive_workers(TT.get_template("t")) == ["ae", "computron", "op"]


def test_derive_workers_follows_inheritance(isolated):
    PG.put_group("child", name="child", members=["m1"])
    PG.put_group("parent", name="parent", members=["group:child"],
                 workers=["ae"])
    TT.put_template("t", name="t", groups=["child"])
    # child has no workers of its own; its effective (inherited) fence governs.
    assert TT.derive_workers(TT.get_template("t")) == ["ae"]


def test_mark_active_flips_flag_only(isolated):
    PG.put_group("g", name="g", members=["m1"])
    TT.put_template("t", name="t", groups=["g"])
    rec = TT.mark_active("t", True)
    assert rec["active"] is True and rec["activated_at"] is not None
    rec = TT.mark_active("t", False)
    assert rec["active"] is False


def test_put_preserves_active_state(isolated):
    PG.put_group("g", name="g", members=["m1"])
    TT.put_template("t", name="t", groups=["g"])
    TT.mark_active("t", True)
    rec, errors = TT.put_template("t", name="t", groups=["g"], workers=["ae"])
    assert errors == [] and rec["active"] is True

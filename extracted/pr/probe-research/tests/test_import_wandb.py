"""`probe import wandb`: the deterministic mirror the 2026-08-13 incident lacked.

Every test pins one of the properties whose absence caused that incident:
backdated wall clocks (not ingest time), incremental convergence (not
duplication), honest terminal status (never 'running', never overruling a
live owner), and fail-loudly writes (never a silent spool)."""

from __future__ import annotations

import sys
from types import SimpleNamespace


from probe import cli
from probe.cli import import_wandb as import_wandb_mod
from tests.conftest import make_client


class _FakeWandbRun:
    def __init__(self, rows, state="finished"):
        self._rows = rows
        self.state = state

    def scan_history(self):
        yield from self._rows


class _FakeWandb(SimpleNamespace):
    def __init__(self, run):
        super().__init__()
        self._run = run

    def Api(self):  # noqa: N802 -- mirrors the wandb surface
        return SimpleNamespace(run=lambda path: self._run)


def _install(monkeypatch, app, tmp_path, wandb_run):
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    monkeypatch.setitem(sys.modules, "wandb", _FakeWandb(wandb_run))


def _seed_target(app, *, status="crashed"):
    exp = app.seed_experiment("e")
    rid = "run-target-1"
    app._new_run(rid, exp["id"], {"name": "target"})
    app.runs[rid]["status"] = status
    return rid


def _rows(app, rid):
    return app.metric_points_posted.get(rid, [])


def test_full_import_backdates_wall_clocks_and_completes(app, tmp_path, monkeypatch):
    wandb_run = _FakeWandbRun(
        rows=[
            {"_step": 10, "_timestamp": 1_753_500_000.0, "loss": 2.5, "note": "text"},
            {"_step": 20, "_timestamp": 1_753_500_060.0, "loss": 1.5, "lr": 0.001},
        ],
        state="finished",
    )
    _install(monkeypatch, app, tmp_path, wandb_run)
    rid = _seed_target(app)

    rc = cli.main(["import", "wandb", "acme/proj/w123", "--run", rid])
    assert rc == 0

    rows = _rows(app, rid)
    # 3 numeric points (loss x2, lr x1); the text value is dropped.
    assert {(p["key"], p["step_index"]) for p in rows} == {
        ("loss", 10),
        ("loss", 20),
        ("lr", 20),
    }
    # Wall clocks are W&B's OWN timestamps, not ingest time -- the fictional
    # time axis was half the original incident. 1_753_500_000 s = 2025-07-26.
    by_step = {(p["key"], p["step_index"]): p["wall_clock"] for p in rows}
    assert by_step[("loss", 10)].startswith("2025-07-26T")
    assert by_step[("loss", 20)].startswith("2025-07-26T")
    assert by_step[("loss", 10)] != by_step[("loss", 20)]
    # Finished W&B run -> completed; linkage + resume watermark landed.
    assert app.runs[rid]["status"] == "completed"
    fk = app.runs[rid]["foreign_keys"]
    assert fk["wandb_run_id"] == "w123"
    assert fk["wandb_entity"] == "acme"
    assert fk["wandb_last_step"] == 20


def test_incremental_import_resumes_from_the_watermark(app, tmp_path, monkeypatch):
    wandb_run = _FakeWandbRun(
        rows=[
            {"_step": 10, "_timestamp": 1.0, "loss": 2.0},
            {"_step": 30, "_timestamp": 2.0, "loss": 1.0},
        ]
    )
    _install(monkeypatch, app, tmp_path, wandb_run)
    rid = _seed_target(app)
    # OUR previous import's watermark -- deliberately not a series-catalog max,
    # which an unrelated high-step series would poison.
    app.runs[rid]["foreign_keys"] = {"wandb_last_step": 10}

    assert cli.main(["import", "wandb", "acme/proj/w123", "--run", rid]) == 0
    assert {(p["key"], p["step_index"]) for p in _rows(app, rid)} == {("loss", 30)}
    assert app.runs[rid]["foreign_keys"]["wandb_last_step"] == 30


def test_chunks_flush_at_row_boundaries(app, tmp_path, monkeypatch):
    """A chunk that split one W&B row across POSTs would, on a crash between
    them, strand the row's tail behind the watermark forever."""
    rows = [{"_step": s, "_timestamp": float(s), "a": 1.0, "b": 2.0, "c": 3.0} for s in range(1, 6)]
    _install(monkeypatch, app, tmp_path, _FakeWandbRun(rows=rows))
    monkeypatch.setattr(import_wandb_mod, "_CHUNK", 4)
    rid = _seed_target(app)

    assert cli.main(["import", "wandb", "acme/proj/w123", "--run", rid]) == 0
    batches = [b["points"] for b in app.metric_batches_posted]
    # 5 rows x 3 keys, chunk budget 4 -> one 3-point row per POST (a 4th point
    # would split the next row), never a partial row.
    for batch in batches:
        steps = {p["step_index"] for p in batch}
        for step in steps:
            assert sum(1 for p in batch if p["step_index"] == step) == 3
    flat = [(p["key"], p["step_index"]) for b in batches for p in b]
    assert len(flat) == len(set(flat)) == 15


def test_failed_metrics_post_fails_the_command_loudly(app, tmp_path, monkeypatch):
    _install(
        monkeypatch,
        app,
        tmp_path,
        _FakeWandbRun(rows=[{"_step": 1, "_timestamp": 1.0, "loss": 3.0}]),
    )
    rid = _seed_target(app)
    app.fail_next_metrics = True

    assert cli.main(["import", "wandb", "acme/proj/w123", "--run", rid]) != 0
    # Nothing spooled: fail loudly means fail NOW, not replay later.
    assert not list((tmp_path / "spool").rglob("*.json"))


def test_running_wandb_run_lands_untracked_never_running(app, tmp_path, monkeypatch):
    """'running' is a promise a live process owns the run; a mirror is not
    that process. The original incident PATCHed mirrored runs to 'running'
    and armed the reaper -- this pins the honest landing."""
    wandb_run = _FakeWandbRun(rows=[{"_step": 1, "_timestamp": 1.0, "loss": 3.0}], state="running")
    _install(monkeypatch, app, tmp_path, wandb_run)
    rid = _seed_target(app)

    assert cli.main(["import", "wandb", "acme/proj/w123", "--run", rid]) == 0
    assert app.runs[rid]["status"] == "untracked"


def test_a_live_owner_keeps_its_status(app, tmp_path, monkeypatch):
    wandb_run = _FakeWandbRun(rows=[{"_step": 1, "_timestamp": 1.0, "loss": 3.0}], state="finished")
    _install(monkeypatch, app, tmp_path, wandb_run)
    rid = _seed_target(app, status="running")
    app.runs[rid]["last_heartbeat_at"] = "2026-08-13T00:00:00Z"

    assert cli.main(["import", "wandb", "acme/proj/w123", "--run", rid]) == 0
    # Points imported, status untouched: the beating owner decides its ending.
    assert _rows(app, rid)
    assert app.runs[rid]["status"] == "running"


def test_hygiene_bools_nans_and_unstamped_rows_are_dropped(app, tmp_path, monkeypatch):
    wandb_run = _FakeWandbRun(
        rows=[
            {"_step": 1, "_timestamp": 1.0, "loss": float("nan"), "flag": True, "ok": 1.5},
            {"_step": 2, "loss": 1.0},  # no _timestamp: never stamped with now()
        ],
        state="finished",
    )
    _install(monkeypatch, app, tmp_path, wandb_run)
    rid = _seed_target(app)

    assert cli.main(["import", "wandb", "acme/proj/w123", "--run", rid]) == 0
    assert {(p["key"], p["step_index"]) for p in _rows(app, rid)} == {("ok", 1)}


def test_empty_history_still_lands_the_honest_status(app, tmp_path, monkeypatch):
    _install(monkeypatch, app, tmp_path, _FakeWandbRun(rows=[], state="finished"))
    rid = _seed_target(app)

    assert cli.main(["import", "wandb", "acme/proj/w123", "--run", rid]) == 0
    assert _rows(app, rid) == []
    assert app.runs[rid]["status"] == "completed"


def test_malformed_path_is_a_clean_parameter_error(app, tmp_path, monkeypatch, capsys):
    _install(monkeypatch, app, tmp_path, _FakeWandbRun(rows=[]))
    rc = cli.main(["import", "wandb", "not-a-path", "--run", "r1"])
    assert rc == 2
    assert "entity/project/run_id" in capsys.readouterr().err


def test_missing_wandb_package_gives_the_install_hint(app, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    monkeypatch.setitem(sys.modules, "wandb", None)  # import -> ImportError
    rid = _seed_target(app)
    rc = cli.main(["import", "wandb", "acme/proj/w123", "--run", rid])
    assert rc == 2
    assert "pip install wandb" in capsys.readouterr().err

"""Every run has a project (retire unfiled runs, PR1).

A run opened with neither a project nor an experiment takes this computer's
project (`PROBE_PROJECT`, else `probe project use`); with none set it is refused
with `ProjectRequired` before any request. What these tests hold:

- no home -> refused, and the fake saw no request at all;
- `PROBE_PROJECT` (slug or id) and the `probe project use` context file give the home;
- an explicit `experiment=` is never scoped to the ambient project (Codex O3);
- a fork or child of an unfiled parent (an older CLI made it) names `probe run move`;
- `probe run start` / `probe exec` refuse before the command starts.
The offline half (refused at enqueue; an older CLI's queued create) is in
`test_offline_mode.py`; listing the unfiled runs that still exist, in
`test_unfiled_run_reads.py`.
"""

from __future__ import annotations

import json
import sys

import pytest

from probe import cli
from probe.sdk import errors
from probe.sdk.settings.settings import resolve
from tests.conftest import make_client


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    return app


def _ambient(client):
    """`client` with the project a real `Client()` resolves: PROBE_PROJECT, else the context file."""
    client.settings.project = resolve().project
    return client


def _run_posts(app):
    return [r for r in app.requests if r.method == "POST" and r.url.path.endswith("/runs")]


# -- the SDK -------------------------------------------------------------------------


def test_no_home_is_refused_before_any_request(client, app):
    before = len(app.requests)
    with pytest.raises(errors.ProjectRequired) as caught:
        client.run(description="probe the lr", config={"lr": 3e-4})
    assert isinstance(caught.value, errors.ValidationError)
    assert len(app.requests) == before, "nothing may be sent for a run with no home"
    message = str(caught.value)
    for fix in ("project=", "PROBE_PROJECT", "probe project use", "probe project create"):
        assert fix in message, fix


def test_probe_init_with_no_home_is_refused(app, tmp_path):
    import probe

    client = make_client(app, tmp_spool=tmp_path / "spool")
    with pytest.raises(errors.ProjectRequired):
        probe.init(client=client, description="fluent")
    assert app.runs == {}


def test_the_more_specific_refusals_still_win(client, app):
    with pytest.raises(errors.ValidationError, match="question= creates an experiment"):
        client.run(question="does it work?")
    with pytest.raises(errors.ValidationError, match="experiment_name"):
        client.run(experiment_name="x")
    with pytest.raises(errors.ValidationError, match="on_conflict"):
        client.run(on_conflict="nope")
    with pytest.raises(errors.ValidationError, match="intent"):
        client.run(intent="   ")
    assert not _run_posts(app)


@pytest.mark.parametrize("by", ["slug", "id"])
def test_probe_project_names_the_home(client, app, monkeypatch, by):
    project = client.create_project("cluster-jobs", kind="general")
    monkeypatch.setenv("PROBE_PROJECT", project["slug"] if by == "slug" else project["id"])
    run = _ambient(client).run(description="from a job", intent="baseline")
    assert app.runs[run.id]["project_id"] == project["id"]
    assert app.runs[run.id]["metadata"]["intent"] == "baseline"


def test_the_active_project_names_the_home(wired, capsys):
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert cli.main(["project", "use", "p"]) == 0
    capsys.readouterr()
    client = _ambient(make_client(wired))
    run = client.run(description="from the context file")
    assert wired.runs[run.id]["project_id"] == next(iter(wired.projects))


def test_a_named_project_wins_over_the_ambient_one(client, app, monkeypatch):
    client.create_project("ambient", kind="general")
    named = client.create_project("named", kind="general")
    monkeypatch.setenv("PROBE_PROJECT", "ambient")
    run = _ambient(client).run(project="named")
    assert app.runs[run.id]["project_id"] == named["id"]


def test_an_experiment_is_never_looked_up_in_the_ambient_project(client, app, monkeypatch):
    """Codex O3: filling project= beside experiment= would scope the tenant-wide
    experiment lookup to the ambient project and "not find" a real one."""
    client.create_project("ambient", kind="general")
    elsewhere = app.seed_experiment("in-b")
    monkeypatch.setenv("PROBE_PROJECT", "ambient")
    run = _ambient(client).run(experiment="in-b")
    assert app.runs[run.id]["experiment_id"] == elsewhere["id"]
    assert app.runs[run.id]["project_id"] != next(
        p for p, row in app.projects.items() if row["slug"] == "ambient"
    )


def test_a_fork_of_an_unfiled_parent_says_move_it_first(client, app):
    parent = app.seed_unfiled_run(name="old-cli-run")
    with pytest.raises(errors.ProjectRequired, match=f"probe run move {parent['id']} --to"):
        client.fork_run(parent["id"], step=10)
    assert not _run_posts(app)


def test_a_child_of_an_unfiled_parent_says_move_it_first(client, app):
    from probe.sdk.run.run import Run

    parent = Run(client, app.seed_unfiled_run(name="old-cli-run"))
    with pytest.raises(errors.ProjectRequired, match="probe run move"):
        parent.child(relation="retry")
    assert not _run_posts(app)


def test_a_pre_0054_parent_still_raises(client, app):
    from probe.sdk.run.run import Run

    old = Run(client, {"id": "r-old", "name": "old", "experiment_id": None})
    with pytest.raises(errors.ValidationError, match="predates project-direct"):
        old.child(relation="fork")


# -- the CLI -------------------------------------------------------------------------


def test_run_start_with_no_home_exits_non_zero(wired, capsys):
    assert cli.main(["run", "start", "--description", "d"]) != 0
    assert "probe project create" in capsys.readouterr().err
    assert wired.runs == {}


def test_run_start_uses_the_active_project(wired, capsys):
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["project", "use", "p"])
    capsys.readouterr()
    assert cli.main(["run", "start", "--description", "d"]) == 0
    run_id = capsys.readouterr().out.strip().splitlines()[0]
    assert wired.runs[run_id]["project_id"] == next(iter(wired.projects))


def test_exec_with_no_home_never_launches_the_command(wired, tmp_path, capsys):
    ran = tmp_path / "ran.txt"
    command = [sys.executable, "-c", f"import pathlib;pathlib.Path({str(ran)!r}).write_text('ok')"]
    assert cli.main(["exec", "--", *command]) != 0
    assert not ran.exists(), "the command ran with no run to record it"
    assert wired.runs == {}
    assert "probe project create" in capsys.readouterr().err


def test_exec_with_a_project_wraps_the_command(wired, tmp_path):
    cli.main(["project", "create", "--kind", "general", "p"])
    ran = tmp_path / "ran.txt"
    command = [sys.executable, "-c", f"import pathlib;pathlib.Path({str(ran)!r}).write_text('ok')"]
    assert cli.main(["exec", "--project", "p", "--intent", "see the curve", "--", *command]) == 0
    assert ran.read_text() == "ok"
    [row] = wired.runs.values()
    assert row["project_id"] == next(iter(wired.projects))
    assert row["status"] == "completed"
    assert row["metadata"]["intent"] == "see the curve"


def test_run_child_of_an_unfiled_parent_exits_non_zero(wired, capsys):
    parent = wired.seed_unfiled_run(name="old-cli-run")
    assert cli.main(["run", "child", parent["id"], "--relation", "branch"]) != 0
    assert f"probe run move {parent['id']}" in capsys.readouterr().err
    assert len(wired.runs) == 1


def test_run_move_files_an_unfiled_run(wired, capsys):
    cli.main(["project", "create", "--kind", "general", "p"])
    run_id = wired.seed_unfiled_run(name="old-cli-run")["id"]
    capsys.readouterr()
    assert cli.main(["run", "move", run_id, "--to", "p"]) == 0
    project_id = next(iter(wired.projects))
    assert json.loads(capsys.readouterr().out)["project_id"] == project_id
    assert wired.runs[run_id]["project_id"] == project_id

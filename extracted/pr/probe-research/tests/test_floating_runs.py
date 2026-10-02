"""Floating runs, client half (daemon v2: D1, D2, D3, S3, E2, E11).

A run opened with NEITHER an experiment NOR a project starts floating: `POST
/v1/runs`, `project_id: null`, filed later by the daemon (`probe run move`).
What these tests hold:

- the floating door is taken ONLY when both are missing; every other validation
  still fires, and experiment/project callers send exactly what they sent before
  (regression contract R7);
- `intent` rides in the run's metadata (the run schema has no field for it);
- a floating parent begets a floating child or fork instead of raising (E11);
- `probe run start` / `probe exec` open floating runs, an active project still
  wins, and `probe exec -- cmd` means the command, not a run named `cmd`;
- an old backend is told apart from an empty answer: a 405 on create, and a
  listing that ignored `unfiled=true`, are refused or reported "unknown";
- doctor, `probe session status` and MCP `browse` show what is still unfiled.

The server half (`POST /v1/runs`, `GET /v1/runs?unfiled=true`) is a parallel
PR; the fake below follows the agreed contract.
"""

from __future__ import annotations

import json
import sys

import pytest

from probe import cli
from probe.sdk import errors
from tests.conftest import make_client

SID = "11111111-2222-4333-8444-555555555555"


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    return app


def _posts(app, path):
    return [
        json.loads(r.content) for r in app.requests if r.method == "POST" and r.url.path == path
    ]


# -- the SDK -------------------------------------------------------------------------


def test_run_with_no_experiment_and_no_project_opens_floating(client, app):
    run = client.run(description="probe the lr", tags=["lr"], config={"lr": 3e-4})
    assert run.project_id is None and run.experiment_id is None
    [body] = _posts(app, "/v1/runs")
    assert body["description"] == "probe the lr"
    assert body["tags"] == ["lr"]
    assert body["config"] == {"lr": 3e-4}
    assert "name" not in body, "a floating run is not named: the server mints one"
    assert app.runs[run.id]["project_id"] is None


def test_intent_rides_in_the_run_metadata(client, app):
    run = client.run(intent="  does warmup remove the spike  ", metadata={"owner": "x"})
    [body] = _posts(app, "/v1/runs")
    assert body["metadata"] == {"owner": "x", "intent": "does warmup remove the spike"}
    assert app.runs[run.id]["metadata"]["intent"] == "does warmup remove the spike"


def test_intent_works_on_a_filed_run_too(client, app):
    client.create_project("p", kind="general")
    client.run(project="p", intent="baseline")
    [body] = _posts(app, "/v1/projects/" + next(iter(app.projects)) + "/runs")
    assert body["metadata"]["intent"] == "baseline"


def test_an_empty_intent_is_refused_before_anything_is_sent(client, app):
    with pytest.raises(errors.ValidationError, match="intent"):
        client.run(intent="   ")
    assert not _posts(app, "/v1/runs")


def test_the_other_validations_still_fire_without_an_experiment(client, app):
    with pytest.raises(errors.ValidationError, match="question= creates an experiment"):
        client.run(question="does it work?")
    with pytest.raises(errors.ValidationError, match="experiment_name"):
        client.run(experiment_name="x")
    with pytest.raises(errors.ValidationError, match="group needs an experiment"):
        client.run(group_id="g1")
    with pytest.raises(errors.ValidationError, match="on_conflict"):
        client.run(on_conflict="nope")
    assert not _posts(app, "/v1/runs")


def test_experiment_and_project_callers_are_unchanged(client, app):
    """R7: the floating door is never taken while either is named."""
    client.create_project("p", kind="general")
    client.create_experiment("e", question="q?", project_id=next(iter(app.projects)))
    client.run(project="p")
    client.run(experiment="e")
    assert not _posts(app, "/v1/runs")
    assert len([r for r in app.requests if r.method == "POST" and r.url.path.endswith("/runs")]) == 2


def test_an_old_backend_says_how_to_open_the_run_instead(client, app):
    app.supports_floating = False
    with pytest.raises(errors.CapabilityUnavailable) as caught:
        client.run(description="x")
    assert "--project" in str(caught.value) and "predates floating runs" in str(caught.value)


def test_probe_init_opens_a_floating_run(app, tmp_path):
    import probe

    client = make_client(app, tmp_spool=tmp_path / "spool")
    run = probe.init(client=client, description="fluent", intent="see it")
    try:
        assert app.runs[run.id]["project_id"] is None
        assert app.runs[run.id]["metadata"]["intent"] == "see it"
    finally:
        probe.finish()
    assert app.runs[run.id]["status"] == "completed"


def test_a_floating_parent_begets_a_floating_child(client, app):
    parent = client.run(description="parent")
    child = parent.child(relation="retry", description="again")
    assert child.project_id is None
    posts = _posts(app, "/v1/runs")
    assert posts[-1]["parent_run_id"] == parent.id
    assert posts[-1]["parent_relation"] == "retry"


def test_a_pre_0054_parent_still_raises(client, app):
    from probe.sdk.run import Run

    old = Run(client, {"id": "r-old", "name": "old", "experiment_id": None})
    with pytest.raises(errors.ValidationError, match="predates project-direct"):
        old.child(relation="fork")


def test_a_floating_source_forks_floating(client, app):
    source = client.run(description="src")
    fork = client.fork_run(source.id, step=10)
    assert fork.project_id is None
    assert _posts(app, "/v1/runs")[-1]["parent_relation"] == "fork"


def test_the_floating_body_is_the_run_create_contract(client, app):
    """The server takes the project-direct body on POST /v1/runs. What the SDK
    sends validates against the generated RunCreate model, and the fake's row
    carries every RunDetailOut key -- `project_id` present and null. (The
    checked-in schema still types it as a string: the server PR regenerates it.)"""
    from probe._generated.models import RunCreate

    client.run(description="d", tags=["t"], config={"a": 1}, intent="i", external_id="x-1")
    [body] = _posts(app, "/v1/runs")
    RunCreate.model_validate(body)
    schema = json.loads(
        (__import__("pathlib").Path(__file__).resolve().parents[1] / "schema" / "openapi.json").read_text()
    )
    required = set(schema["components"]["schemas"]["RunDetailOut"]["required"]) - {"updated_at", "summary"}
    row = next(iter(app.runs.values()))
    assert required <= row.keys()
    assert "project_id" in row and row["project_id"] is None


# -- unfiled listings ----------------------------------------------------------------------


def test_unfiled_lists_only_floating_runs(client, app):
    client.create_project("p", kind="general")
    client.run(project="p")
    floating = client.run(description="f")
    page = client.list_runs(unfiled=True)
    assert [r["id"] for r in page.items] == [floating.id]
    assert app.requests[-1].url.params["unfiled"] == "true"


def test_a_backend_that_ignores_unfiled_is_refused_not_miscounted(client, app):
    client.create_project("p", kind="general")
    client.run(project="p")
    app.supports_floating = False
    with pytest.raises(errors.CapabilityUnavailable):
        client.list_runs(unfiled=True)


def test_unfiled_runs_counts_and_ages_the_oldest(client, app):
    client.run(description="a")
    client.run(description="b")
    for row, stamp in zip(app.runs.values(), ("2026-09-20T00:00:00Z", "2026-09-25T00:00:00Z")):
        row["created_at"] = stamp
    summary = client.unfiled_runs(limit=10)
    assert summary["count"] == 2
    assert summary["more"] is False
    assert summary["oldest_created_at"] == "2026-09-20T00:00:00Z"
    assert summary["oldest_age_s"] > 5 * 86400


def test_doctor_describes_unfiled_runs():
    from probe.cli import doctor

    assert doctor.describe_unfiled({"state": "ok", "count": 0}) == "none"
    assert doctor.describe_unfiled(
        {"state": "ok", "count": 3, "more": False, "oldest_age_s": 7200.0}
    ) == "3, oldest 2h ago"
    assert doctor.describe_unfiled(
        {"state": "ok", "count": 200, "more": True, "oldest_age_s": 3 * 86400.0}
    ) == "200+, oldest 3d ago or earlier"
    assert doctor.describe_unfiled({"state": "unknown", "reason": "old backend"}) == (
        "unknown (old backend)"
    )


def test_doctor_summary_says_unknown_on_an_old_backend(client, app):
    from probe.cli import doctor

    client.create_project("p", kind="general")
    client.run(project="p")
    app.supports_floating = False
    assert doctor.unfiled_summary(client)["state"] == "unknown"
    app.supports_floating = True
    client.run(description="f")
    assert doctor.unfiled_summary(client)["count"] == 1


def test_doctor_daemon_rows_show_unfiled_ai_libraries_and_recent_errors(tmp_path, monkeypatch):
    from probe.cli import doctor
    from probe.cli.capabilities import Capabilities

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    log = tmp_path / "state" / "probe" / "daemon-errors.log"
    log.parent.mkdir(parents=True)
    log.write_text("".join(f"2026-09-26T0{i}:00:00 bite {i} failed 3 times\n" for i in range(8)))
    caps = Capabilities(
        unfiled_runs={"state": "ok", "count": 2, "more": False, "oldest_age_s": 600.0},
        daemon_ai_libraries="missing",
    )
    report = doctor.render(caps)
    assert "Unfiled runs" in report and "2, oldest 10m ago" in report
    assert "AI libraries" in report and "Who records in the wizard (switch it to the daemon, or Enter on it) installs them" in report
    assert "Recent errors" in report
    assert "bite 7 failed" in report and "bite 2 failed" not in report, "only the last lines"


def test_doctor_renders_without_the_new_fields():
    from probe.cli import doctor
    from probe.cli.capabilities import Capabilities

    report = doctor.render(Capabilities())
    assert "Unfiled runs" not in report
    assert "AI libraries" not in report


def test_session_status_reports_unfiled_runs(wired, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")
    client = make_client(wired, tmp_spool=tmp_path / "spool2")
    client.run(description="waiting to be filed")
    capsys.readouterr()
    assert cli.main(["session", "status"]) in (0, None)
    out = json.loads(capsys.readouterr().out)
    assert out["unfiled_runs"]["state"] == "ok"
    assert out["unfiled_runs"]["count"] == 1


def test_session_status_makes_no_probe_call_when_off(wired, tmp_path, monkeypatch, capsys):
    from probe.sdk import session_marker

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")
    assert session_marker.set_session_state(SID, session_marker.STATE_OFF)
    before = len(wired.requests)
    assert cli.main(["session", "status"]) in (0, None)
    out = json.loads(capsys.readouterr().out)
    assert out["unfiled_runs"] is None
    assert len(wired.requests) == before


# -- the CLI -------------------------------------------------------------------------


def test_run_start_with_no_project_opens_floating(wired, capsys):
    rc = cli.main(["run", "start", "--description", "d", "--intent", "why"])
    assert rc == 0
    run_id = capsys.readouterr().out.strip().splitlines()[0]
    assert wired.runs[run_id]["project_id"] is None
    assert wired.runs[run_id]["metadata"]["intent"] == "why"


def test_run_start_still_uses_the_active_project(wired, capsys):
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["project", "use", "p"])
    capsys.readouterr()
    rc = cli.main(["run", "start", "--description", "d"])
    assert rc == 0
    run_id = capsys.readouterr().out.strip().splitlines()[0]
    assert wired.runs[run_id]["project_id"] == next(iter(wired.projects))
    assert not _posts(wired, "/v1/runs")


def test_exec_dash_dash_cmd_opens_a_floating_run_for_that_command(wired, tmp_path):
    """`probe exec -- python train.py`: click binds `python` to the RUN
    positional; the raw args say it came after `--`, so it is the command."""
    out = tmp_path / "ran.txt"
    rc = cli.main(
        ["exec", "--", sys.executable, "-c", f"import pathlib;pathlib.Path({str(out)!r}).write_text('ok')"]
    )
    assert rc == 0
    assert out.read_text() == "ok"
    [row] = wired.runs.values()
    assert row["project_id"] is None
    assert row["status"] == "completed"
    assert row["liveness_mode"] == "wrapped"


def test_exec_with_a_run_ref_before_dash_dash_still_wraps_that_run(wired, capsys):
    cli.main(["run", "start", "--description", "opened elsewhere"])
    run_id = capsys.readouterr().out.strip().splitlines()[0]
    rc = cli.main(["exec", run_id, "--", sys.executable, "-c", "pass"])
    assert rc == 0
    assert len(wired.runs) == 1, "wrapping an existing run opens nothing new"


def test_exec_intent_rides_the_floating_run(wired):
    rc = cli.main(["exec", "--intent", "see the curve", "--", sys.executable, "-c", "pass"])
    assert rc == 0
    [row] = wired.runs.values()
    assert row["metadata"]["intent"] == "see the curve"


def test_exec_with_a_project_is_unchanged(wired):
    cli.main(["project", "create", "--kind", "general", "p"])
    rc = cli.main(["exec", "--project", "p", "--", sys.executable, "-c", "pass"])
    assert rc == 0
    assert not _posts(wired, "/v1/runs")
    [row] = wired.runs.values()
    assert row["project_id"] == next(iter(wired.projects))


def test_run_child_of_a_floating_parent_floats(wired, capsys):
    cli.main(["run", "start", "--description", "parent"])
    parent = capsys.readouterr().out.strip().splitlines()[0]
    rc = cli.main(["run", "child", parent, "--relation", "branch"])
    assert rc == 0
    child = next(r for r in wired.runs.values() if r.get("parent_run_id") == parent)
    assert child["project_id"] is None
    assert child["parent_relation"] == "branch"


def test_run_list_unfiled_goes_through_the_guard(wired, capsys):
    cli.main(["run", "start", "--description", "f"])
    capsys.readouterr()
    assert cli.main(["run", "list", "--unfiled"]) == 0
    items = json.loads(capsys.readouterr().out)["items"]
    assert len(items) == 1 and items[0]["project_id"] is None
    wired.supports_floating = False
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["run", "start", "--project", "p"])
    capsys.readouterr()
    assert cli.main(["run", "list", "--unfiled"]) == 1
    assert "predates floating runs" in capsys.readouterr().err


def test_run_move_files_the_run_and_says_so(wired, capsys):
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["run", "start", "--description", "f"])
    run_id = capsys.readouterr().out.strip().splitlines()[-1]
    project_id = next(iter(wired.projects))
    assert cli.main(["run", "move", run_id, "--to", "p"]) == 0
    assert json.loads(capsys.readouterr().out)["project_id"] == project_id
    assert wired.runs[run_id]["project_id"] == project_id


def test_a_move_the_server_ignored_is_refused_not_reported_done(client, app, monkeypatch):
    """A server that predates filing answers a run PATCH with the run where it was."""
    client.create_project("p", kind="general")
    run = client.run(description="f")
    project_id = next(iter(app.projects))
    unchanged = dict(app.runs[run.id])
    monkeypatch.setattr(client.transport, "patch", lambda path, body, **kw: dict(unchanged))
    with pytest.raises(errors.CapabilityUnavailable, match="cannot file runs"):
        client.move_run(run.id, project_id=project_id)
    moved_elsewhere = {**unchanged, "project_id": project_id, "group_id": None}
    monkeypatch.setattr(client.transport, "patch", lambda path, body, **kw: dict(moved_elsewhere))
    with pytest.raises(errors.CapabilityUnavailable):
        client.move_run(run.id, project_id=project_id, group_id="11111111-2222-4333-8444-555555555555")


def test_a_move_into_an_experiment_is_accepted(client, app, monkeypatch):
    """The server answers a move into an experiment with the experiment in
    `experiment_id` and its parent, the run's home project, in `project_id`."""
    client.create_project("p", kind="general")
    run = client.run(description="f")
    parent = next(iter(app.projects))
    experiment = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
    group = "11111111-2222-4333-8444-555555555555"
    answered = {**app.runs[run.id], "project_id": parent, "experiment_id": experiment, "group_id": group}
    monkeypatch.setattr(client.transport, "patch", lambda path, body, **kw: dict(answered))
    assert client.move_run(run.id, project_id=experiment)["experiment_id"] == experiment
    assert client.move_run(run.id, project_id=experiment, group_id=group)["group_id"] == group
    # The run still where it was (neither field names the experiment): refused.
    unchanged = {**answered, "project_id": parent, "experiment_id": None}
    monkeypatch.setattr(client.transport, "patch", lambda path, body, **kw: dict(unchanged))
    with pytest.raises(errors.CapabilityUnavailable):
        client.move_run(run.id, project_id=experiment)


# -- MCP browse ------------------------------------------------------------------------


def test_browse_at_the_lab_root_lists_unfiled_runs(app, client):
    from probe.mcp.service import ResearchReadService
    from probe.mcp.source import ResearchOSSource
    from tests.test_mcp import _browse_payload

    run = client.run(description="f", tags=["sweep"])
    app.browse_response = _browse_payload()
    envelope = ResearchReadService(ResearchOSSource(client)).browse_research()
    [node] = envelope["data"]["unfiled"]
    assert node["uuid"] == f"run:{run.id}"
    assert node["tags"] == ["sweep"]
    assert node["created_at"]
    assert "id" not in node
    assert "run" in envelope["data"]["available_views"]
    assert "completeness" not in envelope


def test_browse_omits_unfiled_when_there_are_none_and_scoped_reads_never_ask(app, client):
    from probe.mcp.service import ResearchReadService
    from probe.mcp.source import ResearchOSSource
    from tests.test_mcp import _browse_payload

    app.browse_response = _browse_payload()
    envelope = ResearchReadService(ResearchOSSource(client)).browse_research()
    assert "unfiled" not in envelope["data"]
    before = len([r for r in app.requests if r.url.params.get("unfiled")])
    ResearchReadService(ResearchOSSource(client)).browse_research(scope="experiment:x")
    assert len([r for r in app.requests if r.url.params.get("unfiled")]) == before


def test_browse_on_a_backend_without_floating_runs_marks_it_missing(app, client):
    from probe.mcp.service import ResearchReadService
    from probe.mcp.source import ResearchOSSource
    from tests.test_mcp import _browse_payload

    client.create_project("p", kind="general")
    client.run(project="p")
    app.supports_floating = False
    app.browse_response = _browse_payload()
    envelope = ResearchReadService(ResearchOSSource(client)).browse_research()
    assert "unfiled" not in envelope["data"]
    assert "unfiled_runs" in envelope["completeness"]["missing"]
    assert envelope["completeness"]["state"] == "partial"


def test_browse_delivery_carries_unfiled_on_the_first_page_only():
    from probe.mcp.browse_delivery import invoke
    from tests.test_mcp_browse_delivery import Tree, node

    tree = Tree([node("project", f"p{i}") for i in range(40)])
    unfiled = [node("run", "floaty", created_at="2026-09-26T00:00:00Z", tags=["t"])]

    def call(args):
        payload = tree(args)
        # The service adds `unfiled` only at the lab root without a cursor.
        if args.get("ref") is None and args.get("cursor") is None:
            payload["data"]["unfiled"] = unfiled
        return payload

    first = invoke({"token_budget": 1000}, call, "scope")
    assert first["data"]["unfiled"][0]["name"] == "floaty"
    assert first["data"]["unfiled"][0]["tags"] == ["t"]
    assert first["data"]["unfiled"][0]["created_at"] == "2026-09-26T00:00:00Z"
    assert first["next_cursor"], "40 projects do not fit one small page"
    second = invoke({"token_budget": 1000, "cursor": first["next_cursor"]}, call, "scope")
    assert "unfiled" not in second["data"]

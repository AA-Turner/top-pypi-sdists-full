"""Moving a run: `probe run move` and `Client.move_run` (`PATCH /v1/runs/{id}`).

Every run has a project (server 0418), so a move takes a run from one home to another. An
experiment is named as an experiment (`experiment_id`, X21b), and a server that answers with the
run where it was is refused, never reported as done.
"""

from __future__ import annotations

import json

import pytest

from probe import cli
from probe.sdk import errors
from tests.conftest import make_client


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    return app


def test_run_move_places_an_experiment_slug_with_scopes(wired, capsys):
    """`--to <experiment slug>` is placed by ONE `GET /v1/scopes?slug=` (slugs
    are one namespace with projects), never by the projects list answering an
    experiment row -- the leaf door, removed at R6 (light experiments X21) --
    and the move names it as an experiment (`experiment_id`, X21b), never as a
    project id."""
    exp = wired.seed_experiment("target-exp")
    run_id = wired.seed_run(name="f")["id"]
    assert cli.main(["run", "move", run_id, "--to", "target-exp"]) == 0
    reads = [(r.method, r.url.path, dict(r.url.params)) for r in wired.requests]
    assert ("GET", "/v1/scopes", {"slug": "target-exp"}) in reads
    assert not [r for r in reads if r[1] == "/v1/projects" and "slug" in r[2]]
    moves = [r for r in wired.requests if r.method == "PATCH" and r.url.path == f"/v1/runs/{run_id}"]
    assert json.loads(moves[-1].content) == {"experiment_id": exp["id"]}
    assert wired.runs[run_id]["experiment_id"] == exp["id"]


def test_a_move_the_server_ignored_is_refused_not_reported_done(client, app, monkeypatch):
    """A server that predates filing answers a run PATCH with the run where it was."""
    client.create_project("p", kind="general")
    run_id = app.seed_run(name="f")["id"]
    project_id = next(iter(app.projects))
    unchanged = dict(app.runs[run_id])
    monkeypatch.setattr(client.transport, "patch", lambda path, body, **kw: dict(unchanged))
    with pytest.raises(errors.CapabilityUnavailable, match="cannot file runs"):
        client.move_run(run_id, project_id=project_id)
    moved_elsewhere = {**unchanged, "project_id": project_id, "group_id": None}
    monkeypatch.setattr(client.transport, "patch", lambda path, body, **kw: dict(moved_elsewhere))
    with pytest.raises(errors.CapabilityUnavailable):
        client.move_run(run_id, project_id=project_id, group_id="11111111-2222-4333-8444-555555555555")


def test_a_move_into_an_experiment_is_accepted(client, app, monkeypatch):
    """A move into an experiment goes as `experiment_id` (X21b), and the server
    answers it with the experiment in `experiment_id` and its project, the
    run's home, in `project_id`."""
    client.create_project("p", kind="general")
    run_id = app.seed_run(name="f")["id"]
    parent = next(iter(app.projects))
    experiment = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
    group = "11111111-2222-4333-8444-555555555555"
    answered = {**app.runs[run_id], "project_id": parent, "experiment_id": experiment, "group_id": group}
    sent: list[dict] = []

    def patch(path, body, **kw):
        sent.append(dict(body))
        return dict(answered)

    monkeypatch.setattr(client.transport, "patch", patch)
    assert client.move_run(run_id, experiment_id=experiment)["experiment_id"] == experiment
    assert client.move_run(run_id, experiment_id=experiment, group_id=group)["group_id"] == group
    assert sent == [
        {"experiment_id": experiment},
        {"experiment_id": experiment, "group_id": group},
    ], "never the experiment as a project id"
    # The run still where it was (a server older than X21b ignored the field): refused.
    unchanged = {**answered, "project_id": parent, "experiment_id": None}
    monkeypatch.setattr(client.transport, "patch", lambda path, body, **kw: dict(unchanged))
    with pytest.raises(errors.CapabilityUnavailable):
        client.move_run(run_id, experiment_id=experiment)
    # Exactly one target, and an experiment by its uuid.
    for kwargs in ({}, {"project_id": parent, "experiment_id": experiment}, {"experiment_id": "exp-slug"}):
        with pytest.raises(ValueError):
            client.move_run(run_id, **kwargs)

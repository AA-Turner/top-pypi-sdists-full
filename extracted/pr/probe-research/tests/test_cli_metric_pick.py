"""The declared headline metric and the best pick, from the CLI (swarm
visibility PR4a): `probe project set P --metric/--best`, `probe experiment set
E --metric`, `probe workspace set W --best`, driven end to end through
`cli.main` against the fake API.

The server (app/metrics/router.py) owns every rule; these tests hold what the
CLI sends, what it refuses before sending anything, and how it says a 409 over
a PERSON's metric or pick: the server's message, then whose and what, exit 1.
There is no override flag.
"""

from __future__ import annotations

import importlib
import json
import re

import httpx
import pytest

from probe import cli
from tests.conftest import make_client

cli_main = importlib.import_module("probe.cli.main")

_METRIC = re.compile(r"^/v1/projects/([^/]+)(?:/experiments/([^/]+))?/metric$")
_BEST = re.compile(r"^/v1/(projects|workspaces)/([^/]+)/best$")
WORKSPACE = "mine"


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"]) == 0
    return app


class Declarations:
    """The metric and pick routes: every request they got, and a 200 echo --
    or the 409 a test sets."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict, dict]] = []
        self.conflict: dict | None = None

    def __call__(self, request: httpx.Request) -> httpx.Response | None:
        path = request.url.path
        if not (_METRIC.match(path) or _BEST.match(path)):
            return None
        body = json.loads(request.content) if request.content else {}
        self.calls.append((request.method, path, body, dict(request.url.params)))
        if self.conflict is not None:
            return httpx.Response(409, json={"detail": self.conflict})
        if _METRIC.match(path):
            return httpx.Response(200, json={"anchor": {"type": "project", "id": "x"},
                                             "metric": body or None, "cleared_here": False})
        return httpx.Response(200, json={"scope": {"type": "project", "id": "x"}, "pick": body or None,
                                         "history": []})


@pytest.fixture
def routes(wired, monkeypatch) -> Declarations:
    declarations = Declarations()
    real = wired.handler

    def handler(request: httpx.Request) -> httpx.Response:
        answer = declarations(request)
        if answer is not None:
            wired.requests.append(request)
            return answer
        return real(request)

    monkeypatch.setattr(wired, "handler", handler)
    return declarations


def _project(app) -> dict:
    return next(row for row in app.projects.values() if row.get("slug") == "p")


def _experiment(app) -> dict:
    return next(row for row in app.experiments.values() if row.get("slug") == "e")


def _workspace(app) -> dict:
    return next(row for row in app.workspaces.values() if row.get("slug") == WORKSPACE)


# ------------------------------------------------------------------- metric


def test_project_metric_is_declared_by_uuid_with_its_goal_and_reduce(wired, routes, capsys):
    assert cli.main(["project", "set", "p", "--metric", "test/acc", "--goal", "max", "--reduce", "best"]) == 0
    (call,) = routes.calls
    assert call[:3] == ("PUT", f"/v1/projects/{_project(wired)['id']}/metric",
                        {"key": "test/acc", "goal": "max", "reduce": "best"})
    assert json.loads(capsys.readouterr().out)["metric"]["key"] == "test/acc"


def test_reduce_is_left_to_the_server_when_not_given(wired, routes, capsys):
    assert cli.main(["project", "set", "p", "--metric", "loss", "--goal", "min"]) == 0
    assert routes.calls[0][2] == {"key": "loss", "goal": "min"}


def test_an_empty_metric_clears_it(wired, routes, capsys):
    assert cli.main(["project", "set", "p", "--metric", ""]) == 0
    assert routes.calls[0][:2] == ("DELETE", f"/v1/projects/{_project(wired)['id']}/metric")


def test_experiment_metric_overrides_under_its_project(wired, routes, capsys):
    project, experiment = _project(wired)["id"], _experiment(wired)["id"]
    assert cli.main(["experiment", "set", "e", "--metric", "val/f1", "--goal", "max"]) == 0
    assert cli.main(["experiment", "set", "e", "--metric", ""]) == 0
    assert [c[:3] for c in routes.calls] == [
        ("PUT", f"/v1/projects/{project}/experiments/{experiment}/metric", {"key": "val/f1", "goal": "max"}),
        ("DELETE", f"/v1/projects/{project}/experiments/{experiment}/metric", {}),
    ]


@pytest.mark.parametrize(
    "argv,says",
    [
        (["project", "set", "p", "--metric", "acc"], "--goal"),
        (["project", "set", "p", "--goal", "max"], "need --metric"),
        (["project", "set", "p", "--metric", "", "--goal", "max"], "takes no"),
        (["project", "set", "p", "--metric", "acc", "--goal", "max", "--name", "N"], "separate commands"),
        (["project", "set", "p", "--metric", "acc", "--goal", "max", "--best", "e", "--reason", "r"],
         "separate commands"),
        (["project", "set", "p", "--metric", "acc", "--goal", "max", "--authored-by", "agent"], "does not apply"),
        (["experiment", "set", "e", "--metric", "acc", "--goal", "max", "--name", "N"], "goes alone"),
        (["experiment", "set", "e", "--reduce", "best"], "need --metric"),
        (["project", "set", "p", "--metric", "acc", "--goal", "biggest"], "biggest"),
    ],
)
def test_a_metric_write_that_cannot_be_right_sends_nothing(wired, routes, capsys, argv, says):
    assert cli.main(argv) == 2
    assert says in capsys.readouterr().err
    assert routes.calls == []


# --------------------------------------------------------------------- pick


def test_project_pick_names_the_experiment_and_its_reason(wired, routes, capsys):
    assert cli.main(["project", "set", "p", "--best", "e", "--reason", "Highest test/acc at a third of the cost."]) == 0
    (call,) = routes.calls
    assert call[:3] == ("POST", f"/v1/projects/{_project(wired)['id']}/best",
                        {"experiment_id": _experiment(wired)["id"],
                         "reason": "Highest test/acc at a third of the cost."})


def test_workspace_pick_and_clear(wired, routes, capsys):
    workspace = _workspace(wired)["id"]
    assert cli.main(["workspace", "set", WORKSPACE, "--best", "e", "--reason", "It generalises."]) == 0
    assert cli.main(["workspace", "set", WORKSPACE, "--best", "", "--reason", "superseded"]) == 0
    assert cli.main(["workspace", "set", WORKSPACE, "--best", ""]) == 0
    assert [(c[0], c[1], c[2], c[3]) for c in routes.calls] == [
        ("POST", f"/v1/workspaces/{workspace}/best",
         {"experiment_id": _experiment(wired)["id"], "reason": "It generalises."}, {}),
        ("DELETE", f"/v1/workspaces/{workspace}/best", {}, {"reason": "superseded"}),
        ("DELETE", f"/v1/workspaces/{workspace}/best", {}, {}),
    ]


def test_a_project_pick_clears(wired, routes, capsys):
    assert cli.main(["project", "set", "p", "--best", ""]) == 0
    assert routes.calls[0][:2] == ("DELETE", f"/v1/projects/{_project(wired)['id']}/best")


@pytest.mark.parametrize(
    "argv,says",
    [
        (["project", "set", "p", "--best", "e"], "--reason"),
        (["project", "set", "p", "--best", "e", "--reason", "  "], "--reason"),
        (["project", "set", "p", "--reason", "why"], "needs --best"),
        (["workspace", "set", WORKSPACE, "--best", "e"], "--reason"),
        (["workspace", "set", WORKSPACE], "--best"),
    ],
)
def test_a_pick_without_its_reason_sends_nothing(wired, routes, capsys, argv, says):
    assert cli.main(argv) == 2
    assert says in capsys.readouterr().err
    assert routes.calls == []


# ------------------------------------------------------------- a person's


def test_an_agent_over_a_persons_pick_hears_whose_and_what(wired, routes, capsys):
    routes.conflict = {
        "message": "A person picked this scope's best. Tell the researcher why yours should replace it; "
                   "they change the pick from the dashboard.",
        "code": "PICK_IS_A_PERSONS",
        "pick": {"by": "user:5f0c", "at": "2026-10-25T09:00:00+00:00", "gone": False,
                 "experiment": {"id": "e-id", "slug": "wd-0-1", "name": "Wider decoder", "project_id": "p-id"}},
    }
    assert cli.main(["project", "set", "p", "--best", "e", "--reason", "mine is better"]) == 1
    err = capsys.readouterr().err
    assert "error: A person picked this scope's best." in err
    assert "their pick: Wider decoder (wd-0-1, id:e-id), by user:5f0c at 2026-10-25T09:00:00+00:00" in err


def test_a_persons_pick_the_agent_cannot_read_is_not_named(wired, routes, capsys):
    routes.conflict = {"message": "A person picked this scope's best.", "code": "PICK_IS_A_PERSONS",
                       "pick": {"by": "user:5f0c", "at": "2026-10-25T09:00:00+00:00", "gone": None,
                                "experiment": None}}
    assert cli.main(["workspace", "set", WORKSPACE, "--best", "e", "--reason", "r"]) == 1
    assert "their pick: an experiment you cannot read, by user:5f0c" in capsys.readouterr().err


def test_an_agent_over_a_persons_metric_hears_it(wired, routes, capsys):
    routes.conflict = {
        "message": "A person declared this headline metric.", "code": "METRIC_IS_A_PERSONS",
        "metric": {"key": "test/acc", "goal": "max", "reduce": "final", "cleared": False,
                   "set_by": "user:5f0c", "set_at": "2026-10-25T09:00:00+00:00"},
    }
    assert cli.main(["experiment", "set", "e", "--metric", "loss", "--goal", "min"]) == 1
    err = capsys.readouterr().err
    assert "error: A person declared this headline metric." in err
    assert "their metric: test/acc (max, final), by user:5f0c at 2026-10-25T09:00:00+00:00" in err


def test_a_persons_clear_reads_as_cleared(wired, routes, capsys):
    routes.conflict = {"message": "A person declared this headline metric.", "code": "METRIC_IS_A_PERSONS",
                       "metric": {"key": None, "goal": None, "reduce": None, "cleared": True,
                                  "set_by": "user:5f0c", "set_at": "2026-10-25T09:00:00+00:00"}}
    assert cli.main(["project", "set", "p", "--metric", "acc", "--goal", "max"]) == 1
    assert "their metric: cleared here, by user:5f0c" in capsys.readouterr().err


def test_there_is_no_override_flag():
    """D2 / A26: a CLI key cannot prove the person asked, so nothing lets an
    agent write over a person's metric or pick."""
    import typer.main

    root = typer.main.get_command(cli_main.app)
    for path in (("project", "set"), ("experiment", "set"), ("workspace", "set")):
        command = root
        for word in path:
            command = command.commands[word]
        flags = {opt for param in command.params for opt in getattr(param, "opts", [])}
        assert not {f for f in flags if "force" in f or "override" in f}, path

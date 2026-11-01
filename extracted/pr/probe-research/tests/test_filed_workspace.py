"""A new project says which workspace it was filed in, on stderr (plan anthrogen-search-fixes W5).

A project landed in a teammate's workspace twice and nobody could tell from the create's
output. `probe project create` and the folder import now print `Filed in workspace <name>
(<slug>)` on stderr; stdout stays the JSON scripts parse, and a failed name read prints the
id rather than failing the create.
"""

from __future__ import annotations

import contextlib
import sys
import uuid

import pytest

from probe import cli
from probe.cli import backfill_projects, filed_workspace
from probe.shared.reads import reads
from probe.sdk.client.client import Client
from tests.conftest import make_client


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    return app


@pytest.fixture
def answers(monkeypatch) -> list[dict]:
    """What each `create_project` answered, as the command got it."""
    seen: list[dict] = []
    real = Client.create_project

    def record(self, *args, **kwargs):
        seen.append(real(self, *args, **kwargs))
        return seen[-1]

    monkeypatch.setattr(Client, "create_project", record)
    return seen


def _workspace_reads(app, workspace_id: str) -> int:
    return sum(
        1 for r in app.requests if r.method == "GET" and r.url.path == f"/v1/workspaces/{workspace_id}"
    )


def test_project_create_names_its_workspace_on_stderr(wired, answers, capsys):
    assert cli.main(["project", "create", "--kind", "general", "filed"]) == 0
    out, err = capsys.readouterr()
    (row,) = answers
    workspace = wired.workspaces[row["workspace_id"]]
    assert f"Filed in workspace {workspace['name']} ({workspace['slug']})\n" in err
    # stdout is the create's JSON and nothing else, byte for byte as before.
    assert out == reads.render_json(row, False) + "\n"
    assert _workspace_reads(wired, row["workspace_id"]) == 1


def test_a_failed_name_read_prints_the_id_and_the_create_stands(wired, answers, capsys, monkeypatch):
    def refuse(self, workspace_id):
        raise RuntimeError("workspaces read refused")

    monkeypatch.setattr(Client, "get_workspace", refuse)
    assert cli.main(["project", "create", "--kind", "general", "unnamed"]) == 0
    out, err = capsys.readouterr()
    (row,) = answers
    assert f"Filed in workspace {row['workspace_id']}\n" in err
    assert out == reads.render_json(row, False) + "\n"


def test_the_name_read_cannot_hold_the_create_back(wired, answers, capsys, monkeypatch):
    """The read runs under its own short deadline: past it, nothing is sent and the id is printed."""
    monkeypatch.setattr(filed_workspace, "LOOKUP_SECONDS", -1.0)
    assert cli.main(["project", "create", "--kind", "general", "bounded"]) == 0
    out, err = capsys.readouterr()
    (row,) = answers
    assert f"Filed in workspace {row['workspace_id']}\n" in err
    assert _workspace_reads(wired, row["workspace_id"]) == 0
    assert out == reads.render_json(row, False) + "\n"

def test_the_create_s_json_is_out_before_the_name_is_read(wired, answers, capsys, monkeypatch):
    """A script waiting on the new id gets it even when the name read is interrupted (Ctrl-C)."""

    def interrupted(self, workspace_id):
        raise KeyboardInterrupt

    monkeypatch.setattr(Client, "get_workspace", interrupted)
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        cli.main(["project", "create", "--kind", "general", "interrupted"])
    (row,) = answers
    assert capsys.readouterr().out == reads.render_json(row, False) + "\n"


def test_a_name_that_could_drive_a_terminal_is_printed_inert():
    class _Client:
        def get_workspace(self, workspace_id):
            return {"id": workspace_id, "name": "Shyam\x1b[2J‮work", "slug": "shyam"}

    line = filed_workspace.filed_line(_Client(), {"workspace_id": "w1"})
    assert line == "Filed in workspace Shyam?[2J?work (shyam)"


def test_no_workspace_on_the_answer_prints_nothing():
    class _Client:
        def get_workspace(self, workspace_id):
            pytest.fail("read a workspace the answer did not name")

    assert filed_workspace.filed_line(_Client(), {"id": "p"}) is None
    assert filed_workspace.filed_line(_Client(), None) is None


# -- the folder import's creates ----------------------------------------------------------

WS = str(uuid.uuid4())


class _ImportClient:
    """What `backfill_projects.destination` calls, and how often it read the workspace."""

    def __init__(self):
        self.projects: dict[str, dict] = {}
        self.workspace_reads = 0

    def resolve_project(self, slug, strict=False):
        return self.projects.get(slug)

    def create_project(self, slug, name, **kw):
        row = {"id": str(uuid.uuid4()), "slug": slug, "name": name, "workspace_id": kw["workspace_id"],
               "metadata": kw.get("metadata") or {}}
        self.projects[slug] = row
        return row

    def get_workspace(self, workspace_id):
        self.workspace_reads += 1
        return {"id": workspace_id, "name": "Michael's work", "slug": "michael"}


def _destination(client, slug, origin):
    return backfill_projects.destination(
        client, slug, {"origin": origin, "name": slug}, workspace_id=WS, created={},
        remember=lambda: None, authored_by="agent",
    )


@pytest.mark.parametrize("origin", ["new", ""])  # a reviewed new project; an older CLI's plan
def test_the_folder_import_names_the_workspace_of_each_project_it_creates(capsys, origin):
    client = _ImportClient()
    _destination(client, "alpha", origin)
    _destination(client, "beta", origin)
    err = capsys.readouterr().err
    assert err.count("Filed in workspace Michael's work (michael)\n") == 2
    assert client.workspace_reads == 1  # one read per workspace, however many projects


def test_the_folder_import_says_nothing_for_a_project_it_did_not_create(capsys):
    client = _ImportClient()
    client.projects["held"] = {"id": "p", "slug": "held", "workspace_id": WS}
    assert _destination(client, "held", "")["id"] == "p"
    assert "Filed in workspace" not in capsys.readouterr().err
    assert client.workspace_reads == 0



def test_the_folder_import_says_nothing_for_a_project_a_race_made(capsys):
    """A create refused because someone made the slug first adopts their project, silently."""
    from probe.sdk import errors

    client = _ImportClient()
    raced = {"id": "p", "slug": "raced", "workspace_id": WS}
    lookups = iter([None, raced])
    client.resolve_project = lambda slug, strict=False: next(lookups)

    def conflict(*args, **kwargs):
        raise errors.ConflictError("taken")

    client.create_project = conflict
    assert _destination(client, "raced", "")["id"] == "p"
    assert "Filed in workspace" not in capsys.readouterr().err
    assert client.workspace_reads == 0


class _BrokenStream:
    def write(self, text):
        raise BrokenPipeError

    def flush(self):
        raise BrokenPipeError


@pytest.mark.parametrize("stream", [_BrokenStream(), None], ids=["broken-pipe", "no-stderr"])
def test_a_lost_stderr_never_fails_the_folder_import(capsys, monkeypatch, stream):
    """A detached job or a closed pipe loses the line, never the project it names."""
    monkeypatch.setattr(sys, "stderr", stream)
    client = _ImportClient()
    assert _destination(client, "alpha", "new")["id"]
    assert capsys.readouterr().out == ""

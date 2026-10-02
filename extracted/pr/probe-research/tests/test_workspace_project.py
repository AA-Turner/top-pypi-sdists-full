"""The workspace/project/anchored-artifact surface.

These cover the behaviours that are easy to get subtly wrong and expensive to notice:
the patch/move split, the reindex fan-out firing only on a real change, the scoped
upload contract rejecting run-only fields, and a workspace file MOVE (not copy) into
the Shared folder.
"""

from __future__ import annotations

import json

import pytest

from probe import cli
from probe.sdk.client import Anchor
from probe.sdk.config import load_context, save_context

from tests.conftest import _WS_MINE, _WS_OTHER, make_client


def _out(capsys) -> dict | list:
    return json.loads(capsys.readouterr().out)


# -- workspaces --------------------------------------------------------------
def test_workspace_list_preserves_alphabetical_server_order(client, app):
    app.workspaces[_WS_OTHER]["name"] = "alpha"
    rows = client.list_workspaces()

    assert [r["id"] for r in rows] == [_WS_OTHER, _WS_MINE]


def test_workspace_list_tolerates_a_legacy_null_owner_row(client, app, monkeypatch, capsys):
    """A retired shared workspace still exists on un-migrated installs. A client that
    assumes every workspace has an owner crashes on exactly these rows."""
    monkeypatch.setattr(cli, "Client", lambda **kw: client)
    app.workspaces["33333333-3333-3333-3333-333333333333"] = {
        "id": "33333333-3333-3333-3333-333333333333",
        "customer_id": "lab-42",
        "name": "Team (legacy)",
        "slug": "team",
        "kind": "shared",
        "owner_user_id": None,
        "project_count": 0,
        "created_at": "2026-01-01T00:00:00Z",
        "archived_at": None,
    }

    assert cli.main(["workspace", "list"]) == 0

    legacy = next(r for r in _out(capsys) if r["slug"] == "team")
    assert legacy == {
        "id": "33333333-3333-3333-3333-333333333333",
        "name": "Team (legacy)",
        "slug": "team",
        "projects": 0,
    }


def test_workspace_rename_changes_only_the_name(client):
    before = client.get_workspace(_WS_MINE)

    after = client.rename_workspace(_WS_MINE, "Renamed")

    assert after["name"] == "Renamed"
    assert after["slug"] == before["slug"]
    assert after["owner_user_id"] == before["owner_user_id"]


def test_workspace_rename_rejects_a_blank_name(client):
    from probe.sdk import errors

    with pytest.raises(errors.RosError):
        client.rename_workspace(_WS_MINE, "   ")


def test_workspace_use_clears_the_active_project(client, monkeypatch, capsys):
    monkeypatch.setattr(cli, "Client", lambda **kw: client)
    save_context({"workspace": {"id": _WS_OTHER, "project": "stale-project"}})

    assert cli.main(["workspace", "use", f"id:{_WS_MINE}"]) == 0

    anchor = load_context()["workspace"]
    assert anchor["id"] == _WS_MINE
    assert anchor.get("project") is None


def test_workspace_delete_clears_the_selected_pin_before_the_next_create(
    client, app, monkeypatch, capsys, tmp_path
):
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(app, tmp_spool=tmp_path / "spool"))
    client.delete_workspace(_WS_MINE)
    assert cli.main(["workspace", "use", "teammate"]) == 0
    capsys.readouterr()

    assert cli.main(["workspace", "delete", "teammate", "--yes"]) == 0

    assert load_context().get("workspace") is None
    assert client.list_workspaces() == []
    capsys.readouterr()
    assert cli.main(["project", "create", "after-delete", "--kind", "general"]) == 0
    project = _out(capsys)
    workspace = client.get_workspace(project["workspace_id"])
    assert workspace["name"] == "Default workspace"
    assert workspace["id"] != _WS_OTHER
    create = next(r for r in reversed(app.requests) if r.method == "POST")
    assert "workspace_id" not in json.loads(create.content)


def test_workspace_delete_preserves_an_unrelated_pin_and_environment_override(
    app, monkeypatch, tmp_path
):
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(app, tmp_spool=tmp_path / "spool"))
    anchor = {"id": _WS_MINE, "project": "active-project"}
    save_context({"workspace": anchor})
    monkeypatch.setenv("PROBE_WORKSPACE", _WS_OTHER)

    assert cli.main(["workspace", "delete", "teammate", "--yes"]) == 0

    assert load_context()["workspace"] == anchor
    from probe.sdk.config import resolve

    assert resolve().workspace == _WS_OTHER


def test_workspace_delete_failure_preserves_the_selected_pin(client, app, monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(app, tmp_spool=tmp_path / "spool"))
    project = client.create_project("keep", kind="general", workspace_id=_WS_OTHER)
    anchor = {"id": _WS_OTHER, "project": f"id:{project['id']}"}
    save_context({"workspace": anchor})

    assert cli.main(["workspace", "delete", "teammate", "--yes"]) != 0

    assert load_context()["workspace"] == anchor
    assert client.get_workspace(_WS_OTHER)["id"] == _WS_OTHER


# -- projects ----------------------------------------------------------------
def test_project_create_files_into_the_given_workspace(client):
    proj = client.create_project("alpha", workspace_id=_WS_MINE, kind="general")

    assert proj["workspace_id"] == _WS_MINE


def test_project_list_filters_by_workspace(client):
    client.create_project("in-mine", workspace_id=_WS_MINE, kind="general")
    client.create_project("in-other", workspace_id=_WS_OTHER, kind="general")

    slugs = [p["slug"] for p in client.list_projects(workspace_id=_WS_MINE).items]

    assert slugs == ["in-mine"]


def test_project_list_all_omits_the_filter(client):
    client.create_project("in-mine", workspace_id=_WS_MINE, kind="general")
    client.create_project("in-other", workspace_id=_WS_OTHER, kind="general")

    # No workspace_id at all IS "all workspaces" — there is no all-sentinel.
    slugs = sorted(p["slug"] for p in client.list_projects().items)

    assert slugs == ["in-mine", "in-other"]


def test_deleted_projects_leave_the_listing_for_good(client):
    proj = client.create_project("temp", workspace_id=_WS_MINE, kind="general")
    assert [p["slug"] for p in client.list_projects().items] == ["temp"]

    client.delete_project(proj["id"])
    assert [p["slug"] for p in client.list_projects().items] == []


def test_default_named_project_has_no_delete_exception(client):
    proj = client.create_project("default", workspace_id=_WS_MINE, kind="general")

    assert client.delete_project(proj["id"]) is None
    assert client.resolve_project("default") is None


def test_project_workspace_id_may_be_null_on_a_legacy_row(client, app):
    """Required-present but nullable-value. Typing it non-optional crashes the client
    on rows that predate workspaces."""
    created = client.create_project("legacy", kind="general")
    app.projects[created["id"]]["workspace_id"] = None
    proj = client.get_project(created["id"])

    assert "workspace_id" in proj
    assert proj["workspace_id"] is None


def test_project_create_lets_the_server_choose_a_remaining_workspace(client, app):
    client.delete_workspace(_WS_MINE)
    app.requests.clear()

    project = client.create_project("remaining", kind="general")

    assert project["workspace_id"] == _WS_OTHER
    assert [(r.method, r.url.path) for r in app.requests] == [("POST", "/v1/projects")]
    assert "workspace_id" not in json.loads(app.requests[0].content)


def test_project_create_accepts_a_server_fallback_after_every_workspace_is_deleted(client, app):
    client.delete_workspace(_WS_MINE)
    client.delete_workspace(_WS_OTHER)
    assert client.list_workspaces() == []
    app.requests.clear()

    project = client.create_project("fallback", kind="general")

    assert [(r.method, r.url.path) for r in app.requests] == [("POST", "/v1/projects")]
    workspace = client.get_workspace(project["workspace_id"])
    assert workspace["name"] == "Default workspace"
    assert workspace["slug"] == "default"
    assert workspace["owner_user_id"] is None
    assert workspace["id"] not in (_WS_MINE, _WS_OTHER)


def test_subproject_without_workspace_keeps_the_parent_workspace(client):
    parent = client.create_project("parent", kind="general", workspace_id=_WS_OTHER)

    child = client.create_project("child", kind="general", parent_project_id=parent["id"])

    assert child["workspace_id"] == _WS_OTHER


# -- the patch / move split --------------------------------------------------
def test_move_reindexes_descendants(client, app):
    proj = client.create_project("movable", workspace_id=_WS_MINE, kind="general")
    exp = client.create_experiment("e1", "E1", question="h", project_id=proj["id"])
    app.experiments[exp["id"]]["project_id"] = proj["id"]

    client.move_project(proj["id"], _WS_OTHER)

    assert exp["id"] in app.reindexed


def test_a_no_op_move_skips_the_fan_out(client, app):
    """The fan-out fires only when the workspace actually changes."""
    proj = client.create_project("stay", workspace_id=_WS_MINE, kind="general")
    exp = client.create_experiment("e1", "E1", question="h", project_id=proj["id"])
    app.experiments[exp["id"]]["project_id"] = proj["id"]

    client.move_project(proj["id"], _WS_MINE)

    assert app.reindexed == []


def test_move_to_an_unknown_workspace_is_422(client):
    from probe.sdk import errors

    proj = client.create_project("movable", workspace_id=_WS_MINE, kind="general")

    with pytest.raises(errors.RosError) as exc:
        client.move_project(proj["id"], "99999999-9999-9999-9999-999999999999")
    assert "422" in str(exc.value) or "unknown workspace" in str(exc.value)


def test_patch_refuses_workspace_and_points_at_move(client, monkeypatch, capsys):
    """An accidental reindex storm should be unrepresentable, not merely discouraged."""
    monkeypatch.setattr(cli, "Client", lambda **kw: client)
    proj = client.create_project("p", workspace_id=_WS_MINE, kind="general")

    code = cli.main(["project", "patch", f"id:{proj['id']}", "--workspace", f"id:{_WS_OTHER}"])

    assert code != 0
    assert "probe project move" in capsys.readouterr().err
    assert client.get_project(proj["id"])["workspace_id"] == _WS_MINE


def test_project_use_pins_the_owning_workspace(client, monkeypatch, capsys):
    """Selecting a project from another workspace moves the anchor with it, rather
    than storing a mismatched workspace+project pair."""
    monkeypatch.setattr(cli, "Client", lambda **kw: client)
    save_context({"workspace": {"id": _WS_MINE, "project": None}})
    proj = client.create_project("elsewhere", workspace_id=_WS_OTHER, kind="general")

    assert cli.main(["project", "use", f"id:{proj['id']}"]) == 0

    anchor = load_context()["workspace"]
    assert anchor["id"] == _WS_OTHER
    # `project use` records the EXPLICIT id form: an id survives a rename where a
    # slug does not, but a bare id would read as a slug when it flows back in.
    assert anchor["project"] == f"id:{proj['id']}"


# -- anchored artifacts ------------------------------------------------------
@pytest.mark.parametrize("anchor", [Anchor.PROJECT, Anchor.EXPERIMENT, Anchor.WORKSPACE])
def test_upload_to_each_anchor_puts_bytes_and_confirms(client, app, tmp_path, anchor):
    blob = tmp_path / "weights.bin"
    blob.write_bytes(b"BYTES")

    out = client.upload_file(anchor, "anchor-1", "weights.bin", str(blob))

    assert out["status"] == "complete"
    assert len(app.puts) == 1
    assert app.blobs[app.puts[0].rsplit("/", 1)[-1]] == b"BYTES"


def test_have_skips_the_put_but_still_returns_the_artifact(client, app, tmp_path):
    blob = tmp_path / "dedup.bin"
    blob.write_bytes(b"SAME")
    client.upload_file(Anchor.PROJECT, "p1", "dedup.bin", str(blob))
    app.puts.clear()

    out = client.upload_file(Anchor.PROJECT, "p2", "dedup.bin", str(blob))

    assert app.puts == []  # server already had the bytes
    assert out["status"] == "complete"  # still a uniform return shape


@pytest.mark.parametrize(
    "kwargs", [{"kind": "harbor_trial"}, {"meta": {"a": 1}}, {"span_id": "s"}, {"step_index": 3}]
)
def test_run_only_fields_are_refused_before_the_wire(client, app, tmp_path, kwargs):
    """ScopedUploadRequest forbids extras, so the server 422s with a message that does
    not say which field. Refusing here names it."""
    blob = tmp_path / "f.bin"
    blob.write_bytes(b"x")

    with pytest.raises(ValueError) as exc:
        client.upload_file(Anchor.PROJECT, "p1", "f.bin", str(blob), **kwargs)

    assert next(iter(kwargs)) in str(exc.value)
    assert app.puts == []


def test_a_file_anchor_has_no_metadata_only_form(client):
    with pytest.raises(ValueError, match="file anchor"):
        client.create_anchored_reference(Anchor.WORKSPACE, _WS_MINE, {"name": "x"})


def test_cli_artifact_add_shifts_the_positional_under_an_anchor(
    client, app, monkeypatch, tmp_path, capsys
):
    """`add ./f.bin --project P` — the single positional is the PATH, not a run."""
    monkeypatch.setattr(cli, "Client", lambda **kw: client)
    # An anchor must now NAME something: a ref that does not resolve is an error
    # rather than a raw string handed to a UUID-typed route.
    client.create_project("p1", workspace_id=_WS_MINE, kind="general")
    blob = tmp_path / "f.bin"
    blob.write_bytes(b"x")

    assert cli.main(["artifact", "add", str(blob), "--project", "p1"]) == 0

    assert _out(capsys)["name"] == "f.bin"


def test_cli_artifact_add_rejects_two_anchors(client, monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "Client", lambda **kw: client)
    blob = tmp_path / "f.bin"
    blob.write_bytes(b"x")

    code = cli.main(
        ["artifact", "add", str(blob), "--project", "p1", "--workspace", f"id:{_WS_MINE}"]
    )

    assert code != 0


# -- shared folder -----------------------------------------------------------
def test_sharing_a_workspace_file_is_a_move_not_a_copy(client, app, tmp_path):
    blob = tmp_path / "note.md"
    blob.write_bytes(b"hello")
    art = client.upload_file(Anchor.WORKSPACE, _WS_MINE, "note.md", str(blob))

    client.share_workspace_file(art["id"])

    assert client.list_anchored(Anchor.WORKSPACE, _WS_MINE) == []
    assert [f["id"] for f in client.list_anchored(Anchor.SHARED)] == [art["id"]]


def test_unshare_uses_the_remaining_workspace_after_its_source_is_deleted(client, app, tmp_path):
    blob = tmp_path / "note.md"
    blob.write_bytes(b"hello")
    art = client.upload_file(Anchor.WORKSPACE, _WS_MINE, "note.md", str(blob))
    client.share_workspace_file(art["id"])
    client.delete_workspace(_WS_MINE)

    client.unshare_file(art["id"])

    assert client.list_anchored(Anchor.SHARED) == []
    assert [f["id"] for f in client.list_anchored(Anchor.WORKSPACE, _WS_OTHER)] == [art["id"]]
    assert _WS_MINE not in app.workspaces


def test_list_projects_by_parent_returns_only_that_projects_children(client):
    """`--parent` answers "what is under this project?" -- the read side of the
    tree, which the CLI could not ask for at all: it had `--workspace`,
    `--all` and `--tag`, so an agent could BUILD a tree and never list it.
    """
    parent = client.create_project("root", workspace_id=_WS_MINE, kind="training")
    child = client.create_project(
        "phase", workspace_id=_WS_MINE, kind="data", parent_project_id=parent["id"]
    )
    client.create_project("unrelated", workspace_id=_WS_MINE, kind="general")

    page = client.list_projects(parent_id=parent["id"])

    assert [p["slug"] for p in page.items] == [child["slug"]]


def test_a_backend_that_ignores_parent_id_is_refused_not_mislabelled(client, monkeypatch):
    """THE DEPLOY-SKEW TRAP. A pre-0148 backend ignores `parent_id=` and returns
    EVERY project in the tenant -- which this caller would otherwise present as
    one project's children. The dashboard carries the same guard client-side.
    Refuse rather than answer confidently and wrongly.
    """
    from probe.sdk import errors
    from probe.sdk.client import Client

    with pytest.raises(errors.NotFoundError) as exc:
        Client._verify_parent_filter(
            "11111111-1111-1111-1111-111111111111",
            [{"slug": "someone-elses", "parent_project_id": None}],
            "GET /v1/projects",
        )
    assert "predates" in str(exc.value)

    # A correctly-filtered page passes, and an empty page proves nothing.
    Client._verify_parent_filter(
        "11111111-1111-1111-1111-111111111111",
        [{"parent_project_id": "11111111-1111-1111-1111-111111111111"}],
        "GET /v1/projects",
    )
    Client._verify_parent_filter("11111111-1111-1111-1111-111111111111", [], "GET /v1/projects")

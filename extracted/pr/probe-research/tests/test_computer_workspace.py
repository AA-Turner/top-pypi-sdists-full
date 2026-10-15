"""The setup wizard's "Where should this computer's work go?" step (2026-10-14).

Each computer files its new projects into one workspace, saved as the context's
pin (what `probe workspace use` writes). The step asks on a guided install,
picks silently for `--yes`/no TTY, and never blocks a finished install.
"""

from __future__ import annotations

import pytest

from probe.cli import computer_workspace as cw
from probe.cli import tui
from probe.sdk.config import load_context, save_context
from tests.conftest import _WS_MINE, _WS_OTHER, FakeApp, make_client

pytestmark = pytest.mark.usefixtures("real_computer_workspace")


@pytest.fixture
def app(monkeypatch) -> FakeApp:
    app = FakeApp()
    monkeypatch.setenv("PROBE_TOKEN", "ros_pat_deadbeef")
    monkeypatch.delenv("PROBE_WORKSPACE", raising=False)

    def factory(**kw):
        return make_client(app, workspace=kw["settings"].workspace)

    monkeypatch.setattr("probe.sdk.client.Client", factory)
    return app


def _pinned() -> str | None:
    return (load_context().get("workspace") or {}).get("id")


def _row(ident, **fields):
    return {"id": ident, "name": ident, "created_at": "2026-09-01T00:00:00Z", **fields}


# -- preselection --------------------------------------------------------------
def test_preselect_keeps_this_computers_current_workspace():
    rows = [_row("a", is_default=True), _row("b")]
    assert cw.preselect(rows, pinned="b", user_id="me") == "b"


def test_preselect_offers_a_members_legacy_saved_workspace():
    rows = [_row("a", created_by="user:me"), _row("b", is_default=True)]
    assert cw.preselect(rows, pinned=None, user_id="me") == "b"


def test_preselect_offers_the_newest_workspace_the_member_made():
    rows = [
        _row("old-mine", created_by="user:me", created_at="2026-08-01T00:00:00Z"),
        _row("new-mine", created_by="user:me", created_at="2026-10-01T00:00:00Z"),
        _row("theirs", created_by="user:them", created_at="2026-10-02T00:00:00Z"),
    ]
    assert cw.preselect(rows, pinned=None, user_id="me") == "new-mine"


def test_preselect_falls_back_to_the_teams_oldest():
    rows = [_row("b", created_at="2026-09-02T00:00:00Z"), _row("a", created_at="2026-09-01T00:00:00Z")]
    assert cw.preselect(rows, pinned="gone", user_id=None) == "a"


def test_preselect_skips_a_legacy_workspace_the_member_can_no_longer_write():
    rows = [_row("a", is_default=True, writable=False), _row("b", created_by="user:me")]
    assert cw.preselect(rows, pinned=None, user_id="me") == "b"


# -- the step --------------------------------------------------------------------
def test_unattended_takes_the_members_legacy_saved_workspace(app, monkeypatch):
    app.workspaces[_WS_OTHER]["is_default"] = True
    monkeypatch.setattr(cw, "run_picker", lambda *a, **k: pytest.fail("asked unattended"))

    lines = cw.choose(asking=False)

    assert _pinned() == _WS_OTHER
    assert lines == [
        "✔ this computer's work goes into Teammate (`probe workspace use <slug>` changes it)"
    ]


def test_unattended_never_guesses_between_several(app, monkeypatch):
    """`--yes` or an agent-run install (no TTY) with nothing to go on: no pin,
    and the line that says how to pick -- never the oldest or the newest."""
    monkeypatch.setattr(cw, "run_picker", lambda *a, **k: pytest.fail("asked unattended"))

    lines = cw.choose(asking=False)

    assert _pinned() is None
    assert lines == [
        "! this team has several workspaces and this computer has none set yet; "
        "`probe workspace use <slug>` sets it later (see `probe workspace list`)"
    ]


def test_unattended_skips_a_legacy_workspace_the_member_can_no_longer_write(app, monkeypatch):
    app.workspaces[_WS_OTHER].update(is_default=True, writable=False)

    cw.choose(asking=False)

    assert _pinned() is None


def test_an_unattended_rerun_never_undoes_an_explicit_clear(app, monkeypatch):
    app.workspaces[_WS_OTHER]["is_default"] = True
    save_context({"workspace_handover": True})  # `probe workspace use --clear` wrote it

    cw.choose(asking=False)

    assert _pinned() is None


def test_a_stale_pin_is_dropped_even_before_the_team_has_a_workspace(app, monkeypatch):
    save_context({"workspace": {"id": "00000000-0000-4000-8000-00000000dead", "project": None}})
    app.workspaces.clear()

    assert cw.choose(asking=False) == []
    assert "workspace" not in load_context()


def test_a_stale_pin_is_dropped_rather_than_kept(app, monkeypatch):
    """A pin to a deleted workspace (or another team's) would refuse every create."""
    save_context({"workspace": {"id": "00000000-0000-4000-8000-00000000dead", "project": None}})

    lines = cw.choose(asking=False)

    assert _pinned() is None
    assert lines[0].startswith("! this team has several workspaces")


def test_the_choice_is_saved_even_when_probe_workspace_names_it(app, monkeypatch):
    """PROBE_WORKSPACE only overrides one shell: the computer's choice is the file."""
    monkeypatch.setenv("PROBE_WORKSPACE", _WS_OTHER)
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: _WS_OTHER)

    lines = cw.choose(asking=True)

    assert _pinned() == _WS_OTHER
    assert len(lines) == 1


def test_an_env_override_of_the_choice_is_said(app, monkeypatch):
    monkeypatch.setenv("PROBE_WORKSPACE", _WS_MINE)
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: _WS_OTHER)

    lines = cw.choose(asking=True)

    assert _pinned() == _WS_OTHER
    assert lines[1] == f"! PROBE_WORKSPACE={_WS_MINE} overrides it in this shell"


def test_unattended_keeps_a_computer_that_already_has_a_workspace(app, monkeypatch):
    save_context({"workspace": {"id": _WS_MINE, "project": "id:keep-me"}})
    monkeypatch.setattr(cw, "run_picker", lambda *a, **k: pytest.fail("asked unattended"))

    cw.choose(asking=False)

    assert load_context()["workspace"] == {"id": _WS_MINE, "project": "id:keep-me"}


def test_a_team_with_one_workspace_is_not_asked(app, monkeypatch):
    del app.workspaces[_WS_OTHER]
    monkeypatch.setattr(cw, "run_picker", lambda *a, **k: pytest.fail("one workspace, nothing to ask"))

    cw.choose(asking=True)

    assert _pinned() == _WS_MINE


def test_the_picked_workspace_is_saved_for_this_computer(app, monkeypatch):
    seen = {}

    def pick(rows, selected):
        seen["rows"] = sorted(str(r["id"]) for r in rows)
        seen["selected"] = selected
        return _WS_OTHER

    monkeypatch.setattr(cw, "run_picker", pick)

    lines = cw.choose(asking=True)

    assert seen["rows"] == sorted([_WS_MINE, _WS_OTHER])
    assert _pinned() == _WS_OTHER
    assert "Teammate" in lines[0]


def test_create_a_new_workspace_from_the_picker(app, monkeypatch):
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: cw.NEW_WORKSPACE)
    monkeypatch.setattr(tui, "text", lambda *a, **k: "Protein Lab")

    lines = cw.choose(asking=True)

    created = next(w for w in app.workspaces.values() if w["slug"] == "protein-lab")
    assert created["name"] == "Protein Lab"
    assert _pinned() == created["id"]
    assert "Protein Lab" in lines[0]


def test_a_taken_slug_takes_the_servers_suggestion(app, monkeypatch):
    make_client(app).create_workspace("protein-lab", "Protein Lab")
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: cw.NEW_WORKSPACE)
    monkeypatch.setattr(tui, "text", lambda *a, **k: "Protein Lab")

    cw.choose(asking=True)

    created = next(w for w in app.workspaces.values() if w["slug"] == "protein-lab-2")
    assert _pinned() == created["id"]


def test_a_blank_name_creates_my_workspace(app, monkeypatch):
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: cw.NEW_WORKSPACE)
    monkeypatch.setattr(tui, "text", lambda *a, **k: "  ")

    cw.choose(asking=True)

    created = next(w for w in app.workspaces.values() if w["slug"] == "my-workspace")
    assert created["name"] == "My workspace"
    assert _pinned() == created["id"]


def test_backing_out_leaves_this_computer_unset_and_says_how_to_fix_it(app, monkeypatch):
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: tui.BACK)

    lines = cw.choose(asking=True)

    assert _pinned() is None
    assert lines == [
        "! this computer has no workspace set yet; `probe workspace use <slug>` sets it later"
    ]


def test_an_unreachable_server_never_blocks_the_install(app, monkeypatch):
    def down(*_a, **_k):
        raise ConnectionError("no route to host")

    monkeypatch.setattr("probe.sdk.client.Client", down)

    lines = cw.choose(asking=True)

    assert _pinned() is None
    assert lines[0].startswith("! could not set this computer's workspace (ConnectionError)")


def test_signed_out_does_nothing(monkeypatch):
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.setattr("probe.sdk.client.Client", lambda **_k: pytest.fail("no credential"))

    assert cw.choose(asking=True) == []

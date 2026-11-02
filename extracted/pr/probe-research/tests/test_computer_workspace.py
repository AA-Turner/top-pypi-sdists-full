"""The setup wizard's "Where should this computer's work go?" step (2026-10-14).

Each computer files its new projects into one workspace, saved as the context's
pin (what `probe workspace use` writes). The step asks on a guided install,
picks silently for `--yes`/no TTY, and never blocks a finished install.
"""

from __future__ import annotations

import pytest

from probe.cli.wizard.account import computer_workspace as cw
from probe.cli.wizard import terminal as tui
from probe.sdk.settings.settings import load_context, save_context
from tests.conftest import _WS_MINE, _WS_OTHER, FakeApp, make_client

pytestmark = pytest.mark.usefixtures("real_computer_workspace")


@pytest.fixture
def app(monkeypatch) -> FakeApp:
    app = FakeApp()
    monkeypatch.setenv("PROBE_TOKEN", "ros_pat_deadbeef")
    monkeypatch.delenv("PROBE_WORKSPACE", raising=False)

    def factory(**kw):
        return make_client(app, workspace=kw["settings"].workspace)

    monkeypatch.setattr("probe.sdk.client.client.Client", factory)
    monkeypatch.setattr("probe.sdk.client.resources.runs.attach.Client", factory)
    return app


def _pinned() -> str | None:
    return (load_context().get("workspace") or {}).get("id")


def _row(ident, **fields):
    return {"id": ident, "name": ident, "created_at": "2026-09-01T00:00:00Z", **fields}


# -- preselection: pin -> home -> newest the member could make their home ---------
def _eligible(ident, created_at="2026-09-01T00:00:00Z", **fields):
    return _row(ident, created_at=created_at, home_eligible=True, **fields)


def test_preselect_keeps_this_computers_current_workspace():
    rows = [_row("a", is_default=True), _row("b")]
    assert cw.preselect(rows, pinned="b") == "b"


@pytest.mark.parametrize(
    "rows, pinned, expected",
    [
        # The home beats a newer workspace, and a pin the team no longer lists.
        ([_eligible("home", is_default=True), _eligible("newer", "2026-10-01T00:00:00Z")], "gone", "home"),
        # No home: the newest the member could make their home, never a newer one
        # they may write only as an admin (`writable` without `home_eligible`).
        (
            [
                _eligible("old"),
                _eligible("new", "2026-10-01T00:00:00Z"),
                _row("admin-only", created_at="2026-10-02T00:00:00Z", writable=True, home_eligible=False),
            ],
            None,
            "new",
        ),
        # Same moment: the id breaks the tie, so every run starts on the same row.
        ([_eligible("a"), _eligible("b")], None, "b"),
        # A stale home mark on a workspace they can no longer write is not the home.
        ([_row("z-locked", is_default=True, writable=False), _eligible("open")], None, "open"),
        # Nothing they could make their home: the picker's top row.
        ([_row("a"), _row("b", writable=False)], None, None),
    ],
)
def test_preselect_starts_on_the_home_else_the_newest_eligible(rows, pinned, expected):
    assert cw.preselect(rows, pinned=pinned) == expected


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
    """`--yes` or an agent-run install (no TTY) with no home and no workspace the
    member could make their home: no pin, and the line that says how to pick."""
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


def _make_eligible(app, *, home=None, newer=None):
    """Both seeded workspaces could be the member's home; `newer` was made later."""
    for ident, row in app.workspaces.items():
        row.update(home_eligible=True, is_default=ident == home)
        if ident == newer:
            row["created_at"] = "2026-06-01T00:00:00Z"


def test_unattended_pins_the_home_over_a_newer_workspace(app, monkeypatch):
    _make_eligible(app, home=_WS_MINE, newer=_WS_OTHER)
    monkeypatch.setattr(cw, "run_picker", lambda *a, **k: pytest.fail("asked unattended"))

    lines = cw.choose(asking=False)

    assert _pinned() == _WS_MINE
    assert lines == ["✔ this computer's work goes into Mine (`probe workspace use <slug>` changes it)"]
    assert app.home_saves == []


def test_unattended_without_a_home_pins_the_newest_and_says_so_but_never_saves_it_as_home(app, monkeypatch):
    """D-c: an agent-run install still files somewhere the member may write, and says
    which; the member's home stays theirs to choose."""
    _make_eligible(app, newer=_WS_OTHER)

    lines = cw.choose(asking=False)

    assert _pinned() == _WS_OTHER
    assert lines == [
        "! you have no home workspace yet, so this computer's work goes into the team's newest, "
        "Teammate; `probe workspace use <slug>` changes it"
    ]
    assert app.home_saves == []
    assert not any(w.get("is_default") for w in app.workspaces.values())


@pytest.mark.parametrize("key", ["workspace_cleared", "workspace_handover"])
def test_unattended_never_pins_anything_after_an_explicit_clear(app, monkeypatch, key):
    """Neither the home nor the newest: `--clear` (new key, or the legacy one) was a choice."""
    _make_eligible(app, home=_WS_OTHER, newer=_WS_MINE)
    save_context({key: True})

    lines = cw.choose(asking=False)

    assert _pinned() is None
    assert lines[0].startswith("! this team has several workspaces")


def test_a_stale_pin_goes_with_any_older_clear_and_the_home_takes_its_place(app, monkeypatch):
    """The old handover wrote its flag WITH a pin: once that pin is dead, the flag
    is no clear, and the computer gets the member's home."""
    _make_eligible(app, home=_WS_OTHER)
    save_context({"workspace": {"id": "00000000-0000-4000-8000-00000000dead", "project": None},
                  "workspace_handover": True})

    cw.choose(asking=False)

    assert _pinned() == _WS_OTHER
    assert "workspace_handover" not in load_context()


@pytest.mark.parametrize("asking", [True, False])
@pytest.mark.parametrize("has_home", [False, True])
def test_a_teams_only_workspace_is_pinned_and_becomes_a_homeless_members_home(app, monkeypatch, asking, has_home):
    """Nothing to choose between, so nothing is asked, and a member with no home gets it."""
    del app.workspaces[_WS_OTHER]
    _make_eligible(app, home=_WS_MINE if has_home else None)
    monkeypatch.setattr(cw, "run_picker", lambda *a, **k: pytest.fail("one workspace, nothing to ask"))

    cw.choose(asking=asking)

    assert _pinned() == _WS_MINE
    assert app.home_saves == ([] if has_home else [_WS_MINE])


def test_a_teams_only_workspace_the_member_cannot_make_home_is_pinned_without_a_save(app, monkeypatch):
    del app.workspaces[_WS_OTHER]

    cw.choose(asking=False)

    assert _pinned() == _WS_MINE
    assert app.home_saves == []


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
    monkeypatch.setattr(tui.forms, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.choices, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.clipboard, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.layout, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.status_board, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.terminal, "text", lambda *a, **k: "Protein Lab")

    lines = cw.choose(asking=True)

    created = next(w for w in app.workspaces.values() if w["slug"] == "protein-lab")
    assert created["name"] == "Protein Lab"
    assert _pinned() == created["id"]
    assert "Protein Lab" in lines[0]


def test_a_taken_slug_takes_the_servers_suggestion(app, monkeypatch):
    make_client(app).create_workspace("protein-lab", "Protein Lab")
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: cw.NEW_WORKSPACE)
    monkeypatch.setattr(tui.forms, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.choices, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.clipboard, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.layout, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.status_board, "text", lambda *a, **k: "Protein Lab")
    monkeypatch.setattr(tui.terminal, "text", lambda *a, **k: "Protein Lab")

    cw.choose(asking=True)

    created = next(w for w in app.workspaces.values() if w["slug"] == "protein-lab-2")
    assert _pinned() == created["id"]


def test_a_blank_name_creates_my_workspace(app, monkeypatch):
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: cw.NEW_WORKSPACE)
    monkeypatch.setattr(tui.forms, "text", lambda *a, **k: "  ")
    monkeypatch.setattr(tui.choices, "text", lambda *a, **k: "  ")
    monkeypatch.setattr(tui.clipboard, "text", lambda *a, **k: "  ")
    monkeypatch.setattr(tui.layout, "text", lambda *a, **k: "  ")
    monkeypatch.setattr(tui.status_board, "text", lambda *a, **k: "  ")
    monkeypatch.setattr(tui.terminal, "text", lambda *a, **k: "  ")

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


def test_the_picker_starts_on_the_home(app, monkeypatch):
    _make_eligible(app, home=_WS_OTHER, newer=_WS_MINE)
    seen = {}

    def pick(rows, selected):
        seen["selected"] = selected
        return selected

    monkeypatch.setattr(cw, "run_picker", pick)

    cw.choose(asking=True)

    assert seen["selected"] == _WS_OTHER
    assert _pinned() == _WS_OTHER


@pytest.mark.parametrize("home", [None, _WS_MINE])
def test_an_explicit_pick_is_saved_as_home_only_when_the_member_has_none(app, monkeypatch, home):
    """R8: the person chose it, so a member with no home gets it as their home;
    a member with one keeps it (the pin is per computer, the home per person)."""
    _make_eligible(app, home=home)
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: _WS_OTHER)

    cw.choose(asking=True)

    assert _pinned() == _WS_OTHER
    assert app.home_saves == ([_WS_OTHER] if home is None else [])
    assert app.workspaces[home or _WS_OTHER]["is_default"] is True


def test_an_explicit_pick_the_member_cannot_make_home_is_only_pinned(app, monkeypatch):
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: _WS_OTHER)

    cw.choose(asking=True)

    assert _pinned() == _WS_OTHER
    assert app.home_saves == []


def test_a_refused_home_save_still_pins_and_finishes(app, monkeypatch):
    from probe.sdk import errors

    _make_eligible(app)
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: _WS_OTHER)

    def refused(workspace_id):
        raise errors.ServerError("down", status=503)

    def factory(**kw):
        client = make_client(app, workspace=kw["settings"].workspace)
        client.save_home_workspace = refused
        return client

    monkeypatch.setattr("probe.sdk.client.client.Client", factory)

    lines = cw.choose(asking=True)

    assert _pinned() == _WS_OTHER
    assert lines[0].startswith("✔ this computer's work goes into Teammate")
    assert lines[1] == ("! could not also make it your home workspace (ServerError); "
                        "pick your home in the dashboard")


@pytest.mark.parametrize("answer", [None, tui.BACK])
def test_cancelling_with_a_home_pins_the_home(app, monkeypatch, answer):
    _make_eligible(app, home=_WS_OTHER)
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: answer)

    lines = cw.choose(asking=True)

    assert _pinned() == _WS_OTHER
    assert lines == ["✔ this computer's work goes into Teammate (`probe workspace use <slug>` changes it)"]
    assert app.home_saves == []


def test_cancelling_without_a_home_never_pins_the_newest(app, monkeypatch):
    """A3: Ctrl-C is not consent to file into a teammate's newest workspace."""
    _make_eligible(app, newer=_WS_OTHER)
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: None)

    lines = cw.choose(asking=True)

    assert _pinned() is None
    assert lines == ["! this computer has no workspace set yet; `probe workspace use <slug>` sets it later"]


def test_cancelling_keeps_this_computers_pin_over_the_home(app, monkeypatch):
    _make_eligible(app, home=_WS_OTHER)
    save_context({"workspace": {"id": _WS_MINE, "project": "id:keep-me"}})
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: None)

    cw.choose(asking=True)

    assert load_context()["workspace"] == {"id": _WS_MINE, "project": "id:keep-me"}


def test_cancelling_after_an_explicit_clear_pins_nothing(app, monkeypatch):
    _make_eligible(app, home=_WS_OTHER)
    save_context({"workspace_cleared": True})
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: None)

    cw.choose(asking=True)

    assert _pinned() is None


@pytest.mark.parametrize("home", [None, _WS_OTHER])
def test_backing_out_of_create_keeps_the_home_or_leaves_it_unset(app, monkeypatch, home):
    _make_eligible(app, home=home)
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: cw.NEW_WORKSPACE)
    monkeypatch.setattr(cw, "_create", lambda client, **k: None)

    lines = cw.choose(asking=True)

    assert _pinned() == home
    if home is None:
        assert lines == ["! no workspace created; `probe workspace use <slug>` sets it later"]


def test_a_created_workspace_is_pinned_and_the_server_alone_makes_it_home(app, monkeypatch):
    """The create answers it as the home of a member who had none; no second save."""
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: cw.NEW_WORKSPACE)
    monkeypatch.setattr(cw, "_create", lambda client, **k: client.create_workspace("lab", "Lab"))

    cw.choose(asking=True)

    created = next(w for w in app.workspaces.values() if w["slug"] == "lab")
    assert _pinned() == created["id"]
    assert app.home_saves == []


def test_a_pick_replaces_an_earlier_clear(app, monkeypatch):
    save_context({"workspace_cleared": True, "workspace_handover": True})
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: _WS_OTHER)

    cw.choose(asking=True)

    context = load_context()
    assert context["workspace"]["id"] == _WS_OTHER
    assert "workspace_cleared" not in context and "workspace_handover" not in context


def test_an_unreachable_server_never_blocks_the_install(app, monkeypatch):
    def down(*_a, **_k):
        raise ConnectionError("no route to host")

    monkeypatch.setattr("probe.sdk.client.client.Client", down)
    monkeypatch.setattr("probe.sdk.client.resources.runs.attach.Client", down)

    lines = cw.choose(asking=True)

    assert _pinned() is None
    assert lines[0].startswith("! could not set this computer's workspace (ConnectionError)")


def test_signed_out_does_nothing(monkeypatch):
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.setattr("probe.sdk.client.client.Client", lambda **_k: pytest.fail("no credential"))
    monkeypatch.setattr("probe.sdk.client.resources.runs.attach.Client", lambda **_k: pytest.fail("no credential"))

    assert cw.choose(asking=True) == []


# -- a computer limited to one workspace (`probe workspace limit`) ---------------
def test_a_limited_computer_is_not_asked_and_keeps_its_workspace(app, monkeypatch):
    """The pin may not move off a limited workspace: the step checks the workspace
    still exists (one list, without the limit) and says where work goes."""
    monkeypatch.setattr(cw, "run_picker", lambda *a, **k: pytest.fail("a limited computer is not asked"))
    save_context({"workspace": {"id": _WS_OTHER, "project": None, "limit": True, "name": "Teammate"}})
    before = len(app.requests)

    lines = cw.choose(asking=True)

    assert lines == ["✔ this computer is limited to Teammate, and its work goes there (`probe workspace limit` changes it)"]
    assert _pinned() == _WS_OTHER and load_context()["workspace"]["limit"] is True
    assert [r.url.path for r in app.requests[before:]] == ["/v1/workspaces"]


def test_the_picker_lists_every_workspace_whatever_the_environment_limits(app, monkeypatch):
    """PROBE_WORKSPACE_LIMIT narrows one process's reads, never the picker's list."""
    from probe.sdk.settings import workspace_limit as wl

    monkeypatch.setenv(wl.LIMIT_ENV, _WS_MINE)

    def limited(**kw):  # the client a real process builds: its settings' limit sent
        client = make_client(app, workspace=kw["settings"].workspace)
        client.settings.workspace_limit = kw["settings"].workspace_limit
        return client

    monkeypatch.setattr("probe.sdk.client.client.Client", limited)
    monkeypatch.setattr("probe.sdk.client.resources.runs.attach.Client", limited)
    seen = {}

    def pick(rows, selected):
        seen["rows"] = [r["id"] for r in rows]
        return _WS_OTHER

    monkeypatch.setattr(cw, "run_picker", pick)
    _make_eligible(app)  # so the pick is also saved as the member's home
    cw.choose(asking=True)
    lists = [r for r in app.requests if r.url.path == "/v1/workspaces"]
    assert set(seen["rows"]) == {_WS_MINE, _WS_OTHER}
    assert lists and all(r.headers.get(wl.LIMIT_HEADER.lower()) is None for r in lists)
    # ...while the step's other requests carry it.
    others = [r for r in app.requests if r.url.path != "/v1/workspaces"]
    assert others and all(r.headers.get(wl.LIMIT_HEADER.lower()) == _WS_MINE for r in others)


def test_a_limit_naming_a_workspace_this_team_lacks_is_lifted(app, monkeypatch):
    """A re-login to another team (or a deleted workspace) would leave every request
    refused under the old limit: it goes with its pin, and the step goes on."""
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: _WS_OTHER)
    gone = "99999999-9999-9999-9999-999999999999"
    save_context({"workspace": {"id": gone, "project": None, "limit": True, "name": "Old team's"}})

    lines = cw.choose(asking=True)

    assert lines[0] == "! this computer's workspace limit named Old team's, which this team does not have: it was lifted"
    assert _pinned() == _WS_OTHER and "limit" not in load_context()["workspace"]

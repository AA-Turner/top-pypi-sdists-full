"""Desktop filing defaults use the terminal wizard's pin and account boundaries."""
from contextlib import nullcontext
from types import SimpleNamespace
from uuid import uuid4

import pytest

from probe.cli import desktop, computer_workspace, setup, doctor
from probe.sdk.config import load_context, save_context
from probe.sdk import session_marker, workspace_limit
from tests.conftest import _WS_MINE, _WS_OTHER, FakeApp, make_client

SCOPE = {"userId": "user", "customerId": "lab-42"}


@pytest.fixture
def desktop_client(monkeypatch):
    app = FakeApp()
    client = make_client(app)
    monkeypatch.setattr(desktop, "_client", lambda: nullcontext(client))
    monkeypatch.setattr(desktop, "_identity", lambda c: {"user_id": "user", "customer_id": "lab-42"})
    return app, client


def test_read_uses_wizard_preselection_and_never_changes_pin(desktop_client):
    app, _ = desktop_client
    app.workspaces[_WS_OTHER]["is_default"] = True
    result = desktop.dispatch({"op": "computer_workspace"})
    assert result["selected"] == _WS_OTHER
    assert result["scope"] == SCOPE
    assert not load_context().get("workspace")


def test_save_clears_old_project_but_retry_keeps_a_new_project(desktop_client):
    save_context({"workspace": {"id": _WS_MINE, "project": "old"}})
    request = {"op": "set_computer_workspace", "workspaceId": _WS_OTHER, **SCOPE}
    assert desktop.dispatch(request)["workspace"]["id"] == _WS_OTHER
    assert load_context()["workspace"] == {"id": _WS_OTHER, "project": None}
    save_context({"workspace": {"id": _WS_OTHER, "project": "new"}})
    desktop.dispatch(request)
    assert load_context()["workspace"]["project"] == "new"


@pytest.mark.parametrize("change", [{"customerId": "other"}, {"userId": "other"}, {"workspaceId": "deleted"}])
def test_stale_identity_or_workspace_never_changes_config(desktop_client, change):
    save_context({"workspace": {"id": _WS_MINE, "project": "keep"}})
    with pytest.raises(ValueError):
        desktop.dispatch({"op": "set_computer_workspace", "workspaceId": _WS_OTHER, **SCOPE, **change})
    assert load_context()["workspace"] == {"id": _WS_MINE, "project": "keep"}


def test_readonly_workspace_cannot_be_a_filing_destination(desktop_client):
    app, _ = desktop_client
    app.workspaces[_WS_OTHER]["writable"] = False
    with pytest.raises(ValueError, match="write"):
        desktop.dispatch({"op": "set_computer_workspace", "workspaceId": _WS_OTHER, **SCOPE})
    assert not load_context().get("workspace")


def test_limit_cannot_be_bypassed_and_its_keys_survive_same_pin(desktop_client):
    anchor = {"id": _WS_MINE, "project": None, workspace_limit.LIMIT_KEY: True,
              "name": "Mine", "slug": "mine", "team_items": "hide"}
    save_context({"workspace": anchor})
    with pytest.raises(ValueError, match="limit"):
        desktop.dispatch({"op": "set_computer_workspace", "workspaceId": _WS_OTHER, **SCOPE})
    computer_workspace._pin({"id": _WS_MINE}, pinned=None)
    assert workspace_limit.stored(load_context()) is not None
    with pytest.raises(ValueError, match="limit"):
        desktop.dispatch({"op": "create_computer_workspace", "name": "New", "requestId": str(uuid4()), **SCOPE})


def test_create_retries_use_one_workspace(desktop_client):
    app, _ = desktop_client
    before = len(app.workspaces)
    request = {"op": "create_computer_workspace", "name": "Desktop experiments", "requestId": str(uuid4()), **SCOPE}
    first = desktop.dispatch(request)
    assert desktop.dispatch(request) == first
    assert len(app.workspaces) == before + 1
    assert load_context()["workspace"]["id"] == first["workspace"]["id"]


@pytest.mark.parametrize("name", [" ", "a" * 121])
def test_invalid_name_is_refused_before_creating(desktop_client, name):
    app, _ = desktop_client
    before = len(app.workspaces)
    with pytest.raises(ValueError, match="1 to 120"):
        desktop.dispatch({"op": "create_computer_workspace", "name": name,
                          "requestId": str(uuid4()), **SCOPE})
    assert len(app.workspaces) == before
    assert not load_context().get("workspace")


def test_setup_options_use_the_wizard_readers_and_writers(desktop_client, monkeypatch):
    monkeypatch.setattr(doctor, "collect", lambda **kw: SimpleNamespace(agent_configured=False))
    result = desktop.dispatch({"op": "setup_options"})
    assert {row["id"] for row in result["settings"]} == {
        setup.Setting.PLAN_REVIEW, setup.Setting.PASTED_IMAGES, setup.Setting.REASONING_SUMMARIES}
    for key, read in [(setup.Setting.PLAN_REVIEW, session_marker.plan_review_on),
                      (setup.Setting.PASTED_IMAGES, session_marker.pasted_images_on)]:
        desktop.dispatch({"op": "set_setup_option", "setting": str(key), "enabled": False, **SCOPE})
        assert read() is False
    with pytest.raises(ValueError, match="account"):
        desktop.dispatch({"op": "set_setup_option", "setting": "pasted_images", "enabled": True, **SCOPE, "userId": "other"})
    assert session_marker.pasted_images_on() is False

"""Desktop filing defaults use the terminal wizard's pin and account boundaries."""
from contextlib import contextmanager, nullcontext
import json
from types import SimpleNamespace
from uuid import uuid4

import pytest

from probe.cli import desktop, computer_workspace, setup, doctor
from probe.cli import wizard_lock
from probe.cli import reasoning_summaries as reasoning
from probe.cli.capabilities import Capabilities, agent_source
from probe._shared import oscompat
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


@pytest.fixture
def setup_lock(monkeypatch):
    """A real competing flock, with its release driven by a deterministic clock."""
    @contextmanager
    def hold(*, release_after=None, on_release=lambda: None):
        path = wizard_lock.lock_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        elapsed = [0.0]
        with open(path, "a+") as handle:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)

            def sleep(seconds):
                elapsed[0] += seconds
                if release_after is not None and elapsed[0] >= release_after:
                    on_release()
                    oscompat.flock(handle.fileno(), oscompat.LOCK_UN)

            monkeypatch.setattr(wizard_lock, "time", SimpleNamespace(
                monotonic=lambda: elapsed[0], sleep=sleep))
            yield elapsed

    return hold


def workspace_request(create):
    return {"op": "create_computer_workspace", "name": "Desktop experiments",
            "requestId": str(uuid4()), **SCOPE} if create else {
        "op": "set_computer_workspace", "workspaceId": _WS_OTHER, **SCOPE}


@pytest.mark.parametrize("create", [False, True])
def test_workspace_save_waits_for_setup_then_writes_once(desktop_client, setup_lock, monkeypatch, create):
    app, _ = desktop_client
    before = len(app.workspaces)
    save_context({"workspace": {"id": _WS_MINE, "project": "keep-until-saved"}})
    writes = []
    pin = computer_workspace._pin

    def save(row, **kwargs):
        writes.append(row["id"])
        return pin(row, **kwargs)

    monkeypatch.setattr(computer_workspace, "_pin", save)

    def before_release():
        assert writes == []
        assert len(app.workspaces) == before
        assert load_context()["workspace"] == {"id": _WS_MINE, "project": "keep-until-saved"}

    # Longer than the terminal's 250 ms grace, as a post-install update is.
    with setup_lock(release_after=1.0, on_release=before_release) as elapsed:
        answer, code = desktop.respond(json.dumps(workspace_request(create)).encode())
    result = json.loads(answer)
    assert code == 0, result
    assert elapsed[0] >= 1.0
    assert writes == [result["data"]["workspace"]["id"]]
    assert len(app.workspaces) == before + int(create)
    assert load_context()["workspace"] == {"id": writes[0], "project": None}


@pytest.mark.parametrize("create", [False, True])
def test_workspace_save_rechecks_account_after_waiting(desktop_client, setup_lock, monkeypatch, create):
    app, _ = desktop_client
    before = len(app.workspaces)
    save_context({"workspace": {"id": _WS_MINE, "project": "keep"}})

    def switch_account():
        monkeypatch.setattr(desktop, "_identity", lambda c: {"user_id": "other", "customer_id": "lab-42"})

    with setup_lock(release_after=1.0, on_release=switch_account):
        answer, code = desktop.respond(json.dumps(workspace_request(create)).encode())
    assert code == 1
    assert "account or destination changed" in json.loads(answer)["error"]
    assert len(app.workspaces) == before
    assert load_context()["workspace"] == {"id": _WS_MINE, "project": "keep"}


@pytest.mark.parametrize("create", [False, True])
def test_workspace_save_stops_waiting_without_reading_or_writing(setup_lock, monkeypatch, create):
    save_context({"workspace": {"id": _WS_MINE, "project": "keep"}})
    monkeypatch.setattr(desktop, "_client", lambda: pytest.fail("A waiting save must not read the account"))
    with setup_lock() as elapsed:
        answer, code = desktop.respond(json.dumps(workspace_request(create)).encode())
    assert code == wizard_lock.BUSY_EXIT_CODE
    assert json.loads(answer) == {"v": 1, "ok": False, "error": wizard_lock.BUSY_MESSAGE}
    assert 60.0 <= elapsed[0] < 60.02
    assert load_context()["workspace"] == {"id": _WS_MINE, "project": "keep"}


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
        setup.Setting.PASTED_IMAGES, setup.Setting.REASONING_SUMMARIES}
    for key, read in [(setup.Setting.PASTED_IMAGES, session_marker.pasted_images_on)]:
        desktop.dispatch({"op": "set_setup_option", "setting": str(key), "enabled": False, **SCOPE})
        assert read() is False
    with pytest.raises(ValueError, match="account"):
        desktop.dispatch({"op": "set_setup_option", "setting": "pasted_images", "enabled": True, **SCOPE, "userId": "other"})
    assert session_marker.pasted_images_on() is False


def test_retired_plan_review_setting_is_rejected(desktop_client, monkeypatch):
    monkeypatch.setattr(doctor, "collect", lambda **kw: SimpleNamespace(agent_configured=False))
    with pytest.raises(ValueError, match="Unknown setup setting"):
        desktop.dispatch({"op": "set_setup_option", "setting": "plan_review", "enabled": False, **SCOPE})


@pytest.mark.parametrize("claude_config,codex_config", [
    ('{"showThinkingSummaries": false, "theme": "dark"}', 'model_reasoning_summary = "none"\n'),
    ('', 'model_reasoning_summary = "none"\n'),
    (' \n', 'model_reasoning_summary = "none"\n'),
    ('{}', "'model_reasoning_summary' = 'none'\n"),
])
def test_desktop_enables_real_agent_reasoning_configs(desktop_client, monkeypatch, claude_config, codex_config):
    monkeypatch.setattr(doctor, "collect", lambda **kw: Capabilities(
        agent_source=agent_source(), tracking_plugin_installed=agent_source() in reasoning.SOURCES))
    for source, text in [(reasoning.CLAUDE_CODE, claude_config), (reasoning.CODEX, codex_config)]:
        path = reasoning.settings_path(source)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    result = desktop.dispatch({"op": "set_setup_option", "setting": "reasoning_summaries", "enabled": True, **SCOPE})
    assert next(row for row in result["settings"] if row["id"] == "reasoning_summaries")["enabled"] is True
    assert all(reasoning.current(source) is reasoning.State.ON for source in reasoning.SOURCES)
    # An explicit choice survives leaving daemon mode and uninstall.
    for source in reasoning.SOURCES:
        reasoning.undo_for_agent(source)
        assert reasoning.current(source) is reasoning.State.ON


@pytest.mark.parametrize("enabled", [True, False])
def test_partial_reasoning_save_names_the_agent_and_never_claims_success(desktop_client, monkeypatch, enabled):
    monkeypatch.setattr(doctor, "collect", lambda **kw: Capabilities(
        agent_source=agent_source(), tracking_plugin_installed=agent_source() in reasoning.SOURCES))
    path = reasoning.settings_path(reasoning.CLAUDE_CODE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"broken":')
    with pytest.raises(ValueError, match="Claude Code"):
        desktop.dispatch({"op": "set_setup_option", "setting": "reasoning_summaries", "enabled": enabled, **SCOPE})
    assert path.read_text() == '{"broken":'
    expected = reasoning.State.ON if enabled else reasoning.State.OFF
    assert reasoning.current(reasoning.CODEX) is expected
    result = desktop.dispatch({"op": "setup_options"})
    assert next(row for row in result["settings"] if row["id"] == "reasoning_summaries")["enabled"] is False

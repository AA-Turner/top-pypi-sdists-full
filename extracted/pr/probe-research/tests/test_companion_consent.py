"""The Probe daemon's key: one browser approval (`probe companion authorize`).

The wizard's "Who records" row is the consent surface (`setup.apply_recorder`,
tests/test_who_records.py); the tracking-default row no longer has a `daemon`
position (Richard 2026-09-29), so it touches no credential.
"""

from __future__ import annotations

import importlib

import pytest

from probe.cli import daemon_cli
from probe.cli import setup as wizard
from probe.sdk.config import save_context

main = importlib.import_module("probe.cli.main")


@pytest.fixture
def calls(monkeypatch):
    seen = {"authorize": [], "revoke": []}

    def fake_authorize(grants, *, base_url, open_browser=True, **_):
        seen["authorize"].append(grants)
        save_context({"companion_token": "probe_pat_" + "0" * 32})
        return {}, []

    def fake_revoke(token, *, base_url, what):
        seen["revoke"].append(token)
        return [f"released {what}"]

    monkeypatch.setattr(wizard, "authorize", fake_authorize)
    monkeypatch.setattr(wizard, "_revoke", fake_revoke)
    # Choosing `daemon` also provisions the daemon's AI libraries (E11). Pin
    # "already installed" so these tests are about the key, whatever this
    # machine has installed; the install path has its own test below.
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "installed")
    return seen


def test_the_approval_link_is_printed_while_the_flow_waits(monkeypatch, capsys):
    """`probe companion authorize --no-browser` promises the link. Without a
    prompt callback the device flow prints nothing and polls until it expires."""
    from probe.sdk.device import DevicePrompt

    def fake_authorize(grants, *, base_url, open_browser=True, on_prompt=None, **_):
        on_prompt(DevicePrompt("ABCD-EFGH", "https://x/device", "https://x/device?code=ABCD-EFGH"))
        return {}, []

    monkeypatch.setattr(wizard, "authorize", fake_authorize)
    main._authorize_companion("https://x", open_browser=False)
    out = capsys.readouterr().out
    assert "https://x/device?code=ABCD-EFGH" in out
    assert "ABCD-EFGH" in out


def test_a_declined_approval_says_the_agent_keeps_recording(monkeypatch):
    monkeypatch.setattr(wizard, "authorize", lambda grants, **kw: ({}, ["approval declined"]))
    lines = main._authorize_companion("https://x")
    assert lines[0] == "approval declined"
    assert "keeps recording" in lines[1]


def test_the_command_exits_nonzero_when_no_key_was_minted(monkeypatch):
    """A script must be able to tell an expired or declined approval from a key."""
    from typer.testing import CliRunner

    from probe.cli.companion import companion_app

    monkeypatch.setattr(wizard, "authorize", lambda grants, **kw: ({}, ["approval expired"]))
    result = CliRunner().invoke(companion_app, ["authorize", "--no-browser"])
    assert result.exit_code == 1
    assert "approval expired" in result.output


def test_the_command_exits_zero_once_the_key_is_held(calls):
    from typer.testing import CliRunner

    from probe.cli.companion import companion_app

    result = CliRunner().invoke(companion_app, ["authorize", "--no-browser"])
    assert result.exit_code == 0
    assert "own key" in result.output


def test_a_declined_approval_with_an_old_key_saved_still_exits_nonzero(monkeypatch):
    """The command promises a NEW key: a declined approval leaves the old one
    saved, and that must not read as success to a script."""
    from typer.testing import CliRunner

    from probe.cli.companion import companion_app

    save_context({"companion_token": "probe_pat_" + "7" * 32})
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "installed")
    monkeypatch.setattr(wizard, "authorize", lambda grants, **kw: ({}, ["approval declined"]))
    result = CliRunner().invoke(companion_app, ["authorize", "--no-browser"])
    assert result.exit_code == 1


# -- the key from this device's sign-in (Richard 2026-10-26: no browser) -------


class _Client:
    """`probe.sdk.client.Client` standing in for the server's mint routes:
    `answers` is what each POST does, in order (an exception is raised)."""

    calls: list = []
    answers: list = []

    def __init__(self, **_kw) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_exc) -> None:
        return None

    def _answer(self, route: str):
        _Client.calls.append(route)
        answer = _Client.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer

    def mint_companion_credential(self):
        return self._answer("companion")

    def mint_capture_credential(self, source):
        return self._answer(f"capture:{source}")


@pytest.fixture
def mint_server(monkeypatch, tmp_path, real_sign_in_mint):
    from probe.sdk import client as client_mod

    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    save_context({"token": "probe_pat_" + "1" * 32, "base_url": "https://api.test"})
    _Client.calls, _Client.answers = [], []
    monkeypatch.setattr(client_mod, "Client", _Client)
    return _Client


DAEMON_KEY = {"grant": "companion", "token": "probe_pat_" + "2" * 32, "token_id": "t"}


def test_a_failed_send_is_retried_once_then_the_browser_takes_over(mint_server):
    """Each mint frees the slot of the key before it: a second send revokes a key
    whose answer was lost, and a third would revoke one more for nothing."""
    from probe.sdk import errors

    mint_server.answers = [errors.ServerError("502"), DAEMON_KEY]
    assert wizard.mint_from_sign_in(wizard.COMPANION_GRANT, base_url="https://api.test") == {"grants": [DAEMON_KEY]}
    assert mint_server.calls == ["companion", "companion"]
    mint_server.calls, mint_server.answers = [], [errors.TransportError("reset"), errors.ServerError("503")]
    assert wizard.mint_from_sign_in(wizard.COMPANION_GRANT, base_url="https://api.test") is None
    assert len(mint_server.calls) == 2


@pytest.mark.parametrize("refusal", ["not_found", "conflict", "auth", "not_json", "wrong_grant"])
def test_a_refusal_or_a_strange_answer_falls_back_to_the_browser_at_once(mint_server, refusal):
    """An older server (404), another machine's sign-in (404), no device (409),
    a narrower credential (403), a proxy's page: one send, then the browser."""
    from probe.sdk import errors

    mint_server.answers = [{
        "not_found": errors.NotFoundError("404"),
        "conflict": errors.ConflictError("device_required"),
        "auth": errors.AuthError("403"),
        "not_json": ValueError("Expecting value"),
        "wrong_grant": {"grant": "capture", "token": "ros_ing_x"},
    }[refusal]]
    assert wizard.mint_from_sign_in(wizard.COMPANION_GRANT, base_url="https://api.test") is None
    assert mint_server.calls == ["companion"]


def test_no_saved_sign_in_or_another_token_in_the_environment_mints_nothing(mint_server, monkeypatch):
    """`PROBE_TOKEN` naming another credential would save the daemon's key beside
    the wrong account."""
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "9" * 32)
    assert wizard.mint_from_sign_in(wizard.COMPANION_GRANT, base_url="https://api.test") is None
    monkeypatch.delenv("PROBE_TOKEN")
    save_context({"token": None})
    assert wizard.mint_from_sign_in(wizard.COMPANION_GRANT, base_url="https://api.test") is None
    assert mint_server.calls == []


def test_a_key_from_the_sign_in_is_saved_and_opens_no_browser(mint_server, monkeypatch):
    from probe.sdk import config as config_mod
    from probe.sdk import device

    mint_server.answers = [DAEMON_KEY]
    monkeypatch.setattr(device, "device_authorize", lambda *a, **k: pytest.fail("no browser after a sign-in mint"))
    lines = main._authorize_companion("https://api.test", open_browser=False, sign_in=True)
    assert config_mod.load_context()["companion_token"] == DAEMON_KEY["token"]
    assert lines == ["The Probe daemon has its own key."]


def test_without_the_consent_shown_the_browser_approval_runs(mint_server, monkeypatch):
    """A run nobody watched (`sign_in=False`) never mints from the sign-in: the
    browser approval is where the daemon's consent is shown."""
    from probe.sdk import device

    opened = []
    monkeypatch.setattr(device, "device_authorize", lambda *a, **k: opened.append(k.get("grants")) or {"grants": []})
    main._authorize_companion("https://api.test", open_browser=False)
    assert mint_server.calls == [] and opened == [[wizard.COMPANION_GRANT]]

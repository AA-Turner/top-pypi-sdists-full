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

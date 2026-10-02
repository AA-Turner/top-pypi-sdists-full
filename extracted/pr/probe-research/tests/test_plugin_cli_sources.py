"""plugin_cli is the claude/codex MARKETPLACE shim and must fail loud for
anything else -- the silent pi->"claude" fallthrough here is how capture's
uninstall once ran `claude plugin uninstall` for a pi device."""

import pytest

from probe.cli import capture, pi_config, plugin_cli


def test_binary_name_claude_code():
    assert plugin_cli.binary_name("claude_code") == "claude"


def test_binary_name_codex():
    assert plugin_cli.binary_name("codex") == "codex"


def test_binary_name_raises_on_pi():
    with pytest.raises(ValueError, match="pi_config"):
        plugin_cli.binary_name("pi")


def test_binary_name_raises_on_unknown():
    with pytest.raises(ValueError):
        plugin_cli.binary_name("some-future-harness")


def test_capture_uninstall_routes_pi_through_pi_config(monkeypatch):
    calls = []
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setattr(
        pi_config,
        "remove_package_entry",
        lambda: (calls.append("removed"), plugin_cli.claude_cli.Result(ok=True, detail="gone"))[1],
    )
    # plugin_cli must never be consulted on the pi path -- binary_name would
    # raise, and uninstall reaching a marketplace CLI is the audited bug.
    monkeypatch.setattr(
        plugin_cli,
        "uninstall",
        lambda *a, **k: pytest.fail("plugin_cli.uninstall reached for pi"),
    )
    ok, warnings = capture._uninstall_plugin()
    assert ok is True
    assert warnings == []
    assert calls == ["removed"]


def test_capture_uninstall_pi_failure_surfaces_detail(monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setattr(
        pi_config,
        "remove_package_entry",
        lambda: plugin_cli.claude_cli.Result(ok=False, detail="settings.json is not JSON"),
    )
    ok, warnings = capture._uninstall_plugin()
    assert ok is False
    assert any("settings.json is not JSON" in w for w in warnings)

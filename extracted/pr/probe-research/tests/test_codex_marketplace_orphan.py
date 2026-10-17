"""A Codex marketplace checkout orphaned by a deleted config entry.

Deleting `[marketplaces.research-os-agent]` from `~/.codex/config.toml` (or the
whole file) leaves `~/.codex/.tmp/marketplaces/research-os-agent` behind. From
then on `add` refuses ("already added from a different source"), `upgrade`
refuses ("not configured as a Git marketplace") and every install is "not
found in marketplace" -- and before this, re-running the installer could not
get out of it. `FakeCodex` models codex-cli 0.163.0 as measured against a real
CODEX_HOME.
"""

from __future__ import annotations

import json
import subprocess

import pytest

from probe.cli import plugin_cli, updater
from probe.cli import setup as wizard

PUBLISHED = "prbe-ai/research-os-agent"
NAME = "research-os-agent"


class FakeCodex:
    def __init__(self, *, configured: str | None, checkout: bool, list_fails: bool = False):
        self.configured = configured  # the config.toml entry's source, None = no entry
        self.checkout = checkout  # ~/.codex/.tmp/marketplaces/<name> on disk
        self.list_fails = list_fails
        self.ran: list[str] = []

    def __call__(self, cmd, **kwargs):
        args = cmd[1:]
        self.ran.append(" ".join(args))
        match args:
            case ["plugin", "marketplace", "add", location]:
                if self.checkout and self.configured != location:
                    return self._fail(
                        f"Error: marketplace '{NAME}' is already added from a different source; "
                        "remove it before adding this source"
                    )
                self.configured, self.checkout = location, True
                return self._ok(f"Added marketplace `{NAME}`.")
            case ["plugin", "marketplace", "remove", _]:
                self.configured, self.checkout = None, False
                return self._ok(f"Removed marketplace `{NAME}`.")
            case ["plugin", "marketplace", "upgrade", _]:
                if self.configured is None:
                    return self._fail(
                        f"Error: marketplace `{NAME}` is not configured as a Git marketplace"
                    )
                return self._ok("Upgraded.")
            case ["plugin", "marketplace", "list", "--json"]:
                if self.list_fails:
                    return self._fail("Error: config.toml: invalid TOML")
                entries = (
                    [{"name": NAME, "marketplaceSource": {"sourceType": "git", "source": self.configured}}]
                    if self.configured is not None
                    else []
                )
                return self._ok(json.dumps({"marketplaces": entries}))
            case ["plugin", "add", plugin_id]:
                if not self.checkout:
                    return self._fail(f"Error: plugin `{plugin_id.split('@')[0]}` was not found")
                return self._ok("Added plugin.")
            case ["plugin", "list", "--json"]:
                return self._ok(json.dumps([]))
        return self._ok("")

    @staticmethod
    def _ok(out: str) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess([], 0, stdout=out, stderr="")

    @staticmethod
    def _fail(err: str) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess([], 1, stdout="", stderr=err)


@pytest.fixture
def codex(monkeypatch):
    def install(**state) -> FakeCodex:
        fake = FakeCodex(**state)
        monkeypatch.setattr(plugin_cli.shutil, "which", lambda _n: "/usr/bin/codex")
        monkeypatch.setattr(plugin_cli.subprocess, "run", fake)
        return fake

    return install


def test_the_installer_repairs_an_orphaned_checkout(codex):
    """The reported machine: entry gone, checkout left. One installer run fixes it."""
    fake = codex(configured=None, checkout=True)

    refreshed = wizard.refresh_marketplace(source="codex")

    assert refreshed.ok, refreshed.detail
    assert f"plugin marketplace remove {NAME}" in fake.ran
    assert fake.configured is not None and fake.checkout
    assert wizard.install_plugin("probe-research", source="codex").ok


def test_a_configured_fork_is_never_removed(codex):
    """Same refusal, but Codex lists the name: somebody chose that source."""
    fork = "https://github.com/someone/research-os-agent.git"
    fake = codex(configured=fork, checkout=True)

    added = plugin_cli.add_marketplace(plugin_cli.CODEX, PUBLISHED, name=NAME)

    assert not added.ok
    assert fork in added.detail
    assert f"codex plugin marketplace remove {NAME}" in added.detail
    assert not any("remove" in r for r in fake.ran)
    assert fake.configured == fork


def test_an_unreadable_listing_removes_nothing(codex):
    fake = codex(configured=None, checkout=True, list_fails=True)

    added = plugin_cli.add_marketplace(plugin_cli.CODEX, PUBLISHED, name=NAME)

    assert not added.ok
    assert "already added from a different source" in added.detail
    assert f"codex plugin marketplace remove {NAME}" in added.detail
    assert not any("remove" in r for r in fake.ran)


def test_without_a_name_add_is_never_repaired(codex):
    fake = codex(configured=None, checkout=True)

    assert not plugin_cli.add_marketplace(plugin_cli.CODEX, PUBLISHED).ok
    assert fake.ran == [f"plugin marketplace add {PUBLISHED}"]


def test_when_add_and_refresh_both_fail_both_are_reported(monkeypatch):
    """Only `upgrade`'s "not configured" used to surface -- a symptom of the
    refused `add` it was printed instead of."""
    monkeypatch.setattr(
        plugin_cli,
        "add_marketplace",
        lambda source, location, *, name=None: wizard.claude_cli.Result(
            ok=False, detail="add refused", command=f"codex plugin marketplace add {location}"
        ),
    )
    monkeypatch.setattr(
        plugin_cli,
        "refresh_marketplace",
        lambda source, name: wizard.claude_cli.Result(
            ok=False, detail="upgrade refused", command=f"codex plugin marketplace upgrade {name}"
        ),
    )

    result = wizard.refresh_marketplace(source="codex")

    assert not result.ok
    assert f"`codex plugin marketplace add {PUBLISHED}` failed: add refused" in result.detail
    assert f"`codex plugin marketplace upgrade {NAME}` failed: upgrade refused" in result.detail


def test_auto_update_repairs_a_missing_entry(codex, monkeypatch):
    """`probe update` only upgrades, so a lost entry used to fail every update."""
    monkeypatch.setattr(updater.shutil, "which", lambda _n: "/usr/bin/codex")
    fake = codex(configured=None, checkout=True)

    updater.update_codex_plugins()

    assert f"plugin marketplace remove {NAME}" in fake.ran
    assert fake.ran.index(f"plugin marketplace upgrade {NAME}") < fake.ran.index(
        f"plugin marketplace remove {NAME}"
    )
    assert fake.configured is not None
    assert "plugin add probe-research@research-os-agent" in fake.ran

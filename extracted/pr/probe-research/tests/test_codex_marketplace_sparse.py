"""Codex clones Probe's marketplace sparse, so `upgrade` beats its 30 s git timeout.

Without `sparse_paths` every `codex plugin marketplace upgrade` is a full clone
of the mirror (1,698 commits, ~12 MB on 2026-10-31, ~22 commits a day) under
codex-cli's fixed 30 s timeout. It ran 10-15 s on a good connection and timed
out ("fatal: early EOF") five cycles in a row on a slower one, paging the team
as "automatic update keeps failing". Blobless and sparse it is 3-4 s.
"""

from __future__ import annotations

import subprocess

import pytest

from probe.shared.harness import plugins as plugin_cli
from probe.shared.harness.harnesses.codex import config as codex_config
from probe.foundation.compat.compat import tomllib

REPO = "prbe-ai/research-os-agent"
NAME = "research-os-agent"
SPARSE = ["--sparse", ".agents", "--sparse", "plugins"]

#: The entry `codex plugin marketplace add prbe-ai/research-os-agent` wrote
#: before `--sparse`, beside the tables that surround it on a real machine.
BEFORE_SPARSE = """model = "gpt-5"

[marketplaces.prbe-ai]
last_updated = "2026-07-11T05:27:33Z"
source_type = "git"
source = "https://github.com/prbe-ai/prbe-codex-tap-plugin.git"

[marketplaces.research-os-agent]
source_type = "git"
source = "https://github.com/prbe-ai/research-os-agent.git"

[plugins."probe-research-tap@research-os-agent"]
enabled = true
"""


def _read(path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _entry(path) -> dict:
    return _read(path)["marketplaces"][NAME]


def test_an_install_added_before_sparse_gains_the_paths(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(BEFORE_SPARSE, encoding="utf-8")

    result = codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config)

    assert result.changed and result.previous == BEFORE_SPARSE
    assert _entry(config)["sparse_paths"] == [".agents", "plugins"]
    # The one line is the whole change: every other table reads as before.
    added = [line for line in config.read_text().splitlines() if line not in BEFORE_SPARSE.splitlines()]
    assert added == ['sparse_paths = [".agents", "plugins"]']
    assert "sparse_paths" not in _read(config)["marketplaces"]["prbe-ai"]


def test_the_migration_runs_once(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(BEFORE_SPARSE, encoding="utf-8")
    codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config)
    once = config.read_text()

    assert not codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config).changed
    assert config.read_text() == once


@pytest.mark.parametrize(
    "entry",
    [
        # Paths somebody chose, an empty list included, are theirs.
        'source_type = "git"\nsource = "https://github.com/prbe-ai/research-os-agent.git"\nsparse_paths = []\n',
        # A fork's layout is its own.
        'source_type = "git"\nsource = "https://github.com/someone/research-os-agent.git"\n',
        # A local checkout has nothing to clone.
        'source_type = "local"\nsource = "/Users/dev/research-os-agent"\n',
    ],
)
def test_a_source_somebody_chose_is_left_alone(tmp_path, entry):
    config = tmp_path / "config.toml"
    original = f"[marketplaces.{NAME}]\n{entry}"
    config.write_text(original, encoding="utf-8")

    assert not codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config).changed
    assert config.read_text() == original


@pytest.mark.parametrize(
    "source",
    [
        "prbe-ai/research-os-agent",
        "https://github.com/prbe-ai/research-os-agent",
        "git@github.com:prbe-ai/research-os-agent.git",
        "ssh://git@github.com/prbe-ai/research-os-agent.git",
    ],
)
def test_every_spelling_of_the_published_source_is_migrated(tmp_path, source):
    config = tmp_path / "config.toml"
    config.write_text(f'[marketplaces."{NAME}"]\nsource_type = "git"\nsource = "{source}"\n', encoding="utf-8")

    assert codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config).changed
    assert _entry(config)["sparse_paths"] == [".agents", "plugins"]


@pytest.mark.parametrize(
    "source",
    [
        "https://evilgithub.com/prbe-ai/research-os-agent.git",
        "https://git.corp/mirrors/github.com/prbe-ai/research-os-agent.git",
    ],
)
def test_a_lookalike_host_is_not_the_published_source(tmp_path, source):
    config = tmp_path / "config.toml"
    original = f'[marketplaces.{NAME}]\nsource_type = "git"\nsource = "{source}"\n'
    config.write_text(original, encoding="utf-8")

    assert not codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config).changed
    assert config.read_text() == original


def test_a_marketplaces_key_that_is_not_a_table_is_no_change(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text('marketplaces = "x"\n', encoding="utf-8")

    assert not codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config).changed


def test_no_file_and_no_entry_are_no_change(tmp_path):
    missing = tmp_path / "config.toml"
    assert not codex_config.write_marketplace_sparse_paths(NAME, REPO, path=missing).changed
    assert not missing.exists()

    other = tmp_path / "other.toml"
    other.write_text('model = "gpt-5"\n', encoding="utf-8")
    assert not codex_config.write_marketplace_sparse_paths(NAME, REPO, path=other).changed


def test_a_config_that_does_not_parse_is_refused_untouched(tmp_path):
    config = tmp_path / "config.toml"
    broken = BEFORE_SPARSE + "[unterminated\n"
    config.write_text(broken, encoding="utf-8")

    with pytest.raises(codex_config.ConfigError):
        codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config)
    assert config.read_text() == broken


def test_an_inline_table_is_refused_untouched(tmp_path):
    config = tmp_path / "config.toml"
    inline = f'[marketplaces]\n{NAME} = {{ source_type = "git", source = "{REPO}" }}\n'
    config.write_text(inline, encoding="utf-8")

    with pytest.raises(codex_config.ConfigError):
        codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config)
    assert config.read_text() == inline


def test_crlf_line_endings_are_kept(tmp_path):
    config = tmp_path / "config.toml"
    config.write_bytes(BEFORE_SPARSE.replace("\n", "\r\n").encode())

    assert codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config).changed
    raw = config.read_bytes().decode()
    assert '\r\nsparse_paths = [".agents", "plugins"]\r\n' in raw
    assert "\n" not in raw.replace("\r\n", "")


def test_a_save_landing_mid_edit_is_kept(tmp_path, monkeypatch):
    """Codex saving the file between our read and our replace: its save wins,
    the migration is refused (the next run retries)."""
    config = tmp_path / "config.toml"
    config.write_text(BEFORE_SPARSE, encoding="utf-8")
    theirs = BEFORE_SPARSE + '\n[mcp_servers.probe-research]\nurl = "https://mcp.research.prbe.ai/mcp"\n'
    validated = codex_config._validated

    def codex_saves_meanwhile(text, *, what):
        if what == "the updated Codex config":
            config.write_text(theirs, encoding="utf-8")
        validated(text, what=what)

    monkeypatch.setattr(codex_config, "_validated", codex_saves_meanwhile)
    with pytest.raises(codex_config.ConfigError):
        codex_config.write_marketplace_sparse_paths(NAME, REPO, path=config)
    assert config.read_text() == theirs


def test_a_symlinked_config_keeps_its_link_and_mode(tmp_path):
    real = tmp_path / "dotfiles" / "config.toml"
    real.parent.mkdir()
    real.write_text(BEFORE_SPARSE, encoding="utf-8")
    real.chmod(0o640)
    link = tmp_path / "config.toml"
    link.symlink_to(real)

    assert codex_config.write_marketplace_sparse_paths(NAME, REPO, path=link).changed
    assert link.is_symlink() and link.resolve() == real.resolve()
    assert real.stat().st_mode & 0o777 == 0o640
    assert _entry(real)["sparse_paths"] == [".agents", "plugins"]


def test_the_sparse_paths_cover_every_plugin_codex_installs():
    """Codex reads `.agents/plugins/marketplace.json` and each plugin's folder;
    a plugin outside `MARKETPLACE_SPARSE_PATHS` would be missing from the clone."""
    import json
    from pathlib import Path

    manifest = Path(__file__).resolve().parents[1] / ".agents" / "plugins" / "marketplace.json"
    covered = codex_config.MARKETPLACE_SPARSE_PATHS
    assert manifest.relative_to(manifest.parents[2]).parts[0] in covered
    for plugin in json.loads(manifest.read_text(encoding="utf-8"))["plugins"]:
        assert Path(plugin["source"]["path"]).parts[0] in covered, plugin["name"]


# --- the commands -----------------------------------------------------------


class Ran(list):
    """The agent-CLI calls made, answering `git --version` with `git` (not recorded)."""

    git = "git version 2.39.5 (Apple Git-154)"


@pytest.fixture
def ran(monkeypatch):
    calls = Ran()

    def fake_run(cmd, **_kwargs):
        if cmd[1:] == ["--version"]:
            return subprocess.CompletedProcess(cmd, 0, stdout=calls.git, stderr="")
        calls.append(list(cmd[1:]))
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(plugin_cli.shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(plugin_cli.subprocess, "run", fake_run)
    return calls


def _seed_config(text: str = BEFORE_SPARSE):
    config = codex_config.config_path()
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(text, encoding="utf-8")
    return config


def _record_paths_at_each_call(monkeypatch, config) -> list[object]:
    """The entry's `sparse_paths` at the moment each agent-CLI call starts."""
    seen: list[object] = []
    fake_run = plugin_cli.subprocess.run

    def recording(cmd, **kwargs):
        if cmd[1:] != ["--version"]:
            seen.append(_entry(config).get("sparse_paths"))
        return fake_run(cmd, **kwargs)

    monkeypatch.setattr(plugin_cli.subprocess, "run", recording)
    return seen


def test_codex_adds_the_marketplace_sparse(ran):
    assert plugin_cli.add_marketplace(plugin_cli.CODEX, REPO, name=NAME).ok
    assert ran == [["plugin", "marketplace", "add", REPO, *SPARSE]]


def test_claude_code_adds_it_as_before(ran):
    assert plugin_cli.add_marketplace(plugin_cli.CLAUDE, REPO, name=NAME).ok
    assert ran == [["plugin", "marketplace", "add", REPO]]


def test_a_codex_refresh_migrates_the_config_before_upgrading(ran, monkeypatch):
    config = _seed_config()
    seen = _record_paths_at_each_call(monkeypatch, config)

    assert plugin_cli.refresh_marketplace(plugin_cli.CODEX, NAME).ok
    assert ran == [["plugin", "marketplace", "upgrade", NAME]]
    assert seen == [[".agents", "plugins"]]


def test_an_add_migrates_the_config_first(ran, monkeypatch):
    """The wizard runs `add` before `upgrade`, and codex-cli 0.163.0 refuses
    `add --sparse` over an entry without those paths as "already added from a
    different source" (measured against a real CODEX_HOME)."""
    config = _seed_config()
    seen = _record_paths_at_each_call(monkeypatch, config)

    assert plugin_cli.add_marketplace(plugin_cli.CODEX, REPO, name=NAME).ok
    assert ran == [["plugin", "marketplace", "add", REPO, *SPARSE]]
    assert seen == [[".agents", "plugins"]]


@pytest.mark.parametrize(
    ("entry", "flags"),
    [
        # Paths somebody chose: `add` passes them, so Codex finds the same entry.
        ('sparse_paths = []\n', []),
        ('sparse_paths = ["plugins"]\n', ["--sparse", "plugins"]),
    ],
)
def test_an_add_passes_the_paths_the_entry_already_has(ran, entry, flags):
    _seed_config(
        f'[marketplaces.{NAME}]\nsource_type = "git"\n'
        f'source = "https://github.com/{REPO}.git"\n{entry}'
    )

    assert plugin_cli.add_marketplace(plugin_cli.CODEX, REPO, name=NAME).ok
    assert ran == [["plugin", "marketplace", "add", REPO, *flags]]


def test_an_add_over_an_entry_it_cannot_edit_passes_no_paths(ran):
    """An inline table the migration refuses: no `--sparse`, so `add` still
    matches it (before, a refusal and "run `remove`" over the published source)."""
    _seed_config(f'[marketplaces]\n{NAME} = {{ source_type = "git", source = "{REPO}" }}\n')

    assert plugin_cli.add_marketplace(plugin_cli.CODEX, REPO, name=NAME).ok
    assert ran == [["plugin", "marketplace", "add", REPO]]


@pytest.mark.parametrize("git", ["git version 2.17.1", "git version 1.8.3.1", None])
def test_a_git_without_sparse_checkout_keeps_the_full_clone(ran, git, monkeypatch):
    """`git sparse-checkout` shipped in git 2.25.0: on an older git (or none
    found) every sparse clone fails, where the full one works."""
    if git is None:
        monkeypatch.setattr(plugin_cli.shutil, "which", lambda name: None if name == "git" else f"/usr/bin/{name}")
    else:
        ran.git = git
    config = _seed_config()

    assert plugin_cli.refresh_marketplace(plugin_cli.CODEX, NAME).ok
    assert plugin_cli.add_marketplace(plugin_cli.CODEX, REPO, name=NAME).ok
    assert ran == [["plugin", "marketplace", "upgrade", NAME], ["plugin", "marketplace", "add", REPO]]
    assert config.read_text() == BEFORE_SPARSE


def test_git_2_25_is_enough(ran):
    ran.git = "git version 2.25.1"
    _seed_config("")

    assert plugin_cli.add_marketplace(plugin_cli.CODEX, REPO, name=NAME).ok
    assert ran == [["plugin", "marketplace", "add", REPO, *SPARSE]]


def test_a_config_it_cannot_edit_still_upgrades(ran):
    broken = BEFORE_SPARSE + "[unterminated\n"
    config = _seed_config(broken)

    assert plugin_cli.refresh_marketplace(plugin_cli.CODEX, NAME).ok
    assert ran == [["plugin", "marketplace", "upgrade", NAME]]
    assert config.read_text() == broken


def test_manual_steps_print_the_same_codex_add():
    from probe.cli.wizard.actions.onboarding import manual_steps

    steps = manual_steps(base_url="https://api.research.prbe.ai", agent_source="codex")
    assert f"codex plugin marketplace add {REPO} --sparse .agents --sparse plugins" in steps
    claude = manual_steps(base_url="https://api.research.prbe.ai", agent_source="claude_code")
    assert f"claude plugin marketplace add {REPO}" in claude
    assert "--sparse" not in claude

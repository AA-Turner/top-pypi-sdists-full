"""Unit tests for tools/mirror_render.py — every guard, plus determinism.

The mirror has no staging environment: the first time the render logic runs
for real, it runs against the public repo every installed plugin pulls from.
So each guard is proven here on fixture trees, and the render is proven
deterministic (that determinism is what makes a failed mirror job safe to
re-run).
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_TOOL = Path(__file__).resolve().parent.parent / "tools" / "mirror_render.py"

spec = importlib.util.spec_from_file_location("mirror_render", _TOOL)
mirror_render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mirror_render)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def make_source(root: Path, *, cli="0.72.0", plugin="0.17.0", tap="0.2.1") -> Path:
    """A minimal but complete agent/ tree that passes every guard."""
    agent = root / "agent"
    _write_json(
        agent / ".claude-plugin" / "marketplace.json",
        {
            "name": "research-os-agent",
            "plugins": [
                {"name": "probe-research", "source": "./plugins/probe-research"},
                {"name": "probe-research-daemon", "source": "./plugins/probe-research-daemon"},
                {"name": "probe-research-tap", "source": "./plugins/probe-research-tap"},
            ],
        },
    )
    _write_json(
        agent / "plugins" / "probe-research" / ".claude-plugin" / "plugin.json",
        {"name": "probe-research", "version": plugin},
    )
    # The daemon profile's lean plugin: released with probe-research.
    _write_json(
        agent / "plugins" / "probe-research-daemon" / ".claude-plugin" / "plugin.json",
        {"name": "probe-research-daemon", "version": plugin},
    )
    (agent / "plugins" / "probe-research" / "skills").mkdir(parents=True)
    (agent / "plugins" / "probe-research" / "skills" / "s.md").write_text("skill\n")
    _write_json(
        agent / "plugins" / "probe-research-tap" / ".claude-plugin" / "plugin.json",
        {"name": "probe-research-tap", "version": tap},
    )
    _write_json(
        agent / ".agents" / "plugins" / "marketplace.json",
        {
            "name": "research-os-agent",
            "plugins": [
                {
                    "name": "probe-research",
                    "source": {"source": "local", "path": "./plugins/probe-research"},
                },
                {
                    "name": "probe-research-daemon",
                    "source": {"source": "local", "path": "./plugins/probe-research-daemon"},
                },
                {
                    "name": "probe-research-tap",
                    "source": {"source": "local", "path": "./plugins/probe-research-tap"},
                },
            ],
        },
    )
    _write_json(
        agent / "client-version.json",
        {
            "cli": {"latest": cli, "min": "0.6.0"},
            "plugin": {"latest": plugin, "min": "0.6.0"},
            "tap": {"latest": tap, "min": "0.1.0"},
            "advisory": None,
        },
    )
    # pi's half of the mirror: the plugin dir, plus the root package.json that
    # makes the whole repo a loadable pi package. Deliberately in NEITHER
    # marketplace manifest -- pi has no marketplace, and `_check_pi_package` is
    # what holds it to account instead.
    pi_pkg = agent / "plugins" / "probe-research-pi"
    (pi_pkg / "skills" / "track-work").mkdir(parents=True)
    (pi_pkg / "skills" / "track-work" / "SKILL.md").write_text("skill\n")
    (pi_pkg / "index.ts").write_text("export default function () {}\n")
    _write_json(pi_pkg / "mcp.json", {"mcpServers": {}})
    _write_json(
        pi_pkg / "package.json", {"name": "probe-research-pi", "dependencies": {"dep": "^1"}}
    )
    _write_json(
        agent / "mirror-package.json",
        {
            "name": "probe-research-pi",
            "pi": {
                "extensions": ["plugins/probe-research-pi/index.ts"],
                "skills": ["plugins/probe-research-pi/skills/track-work"],
                "mcp": "./plugins/probe-research-pi/mcp.json",
            },
            "dependencies": {"dep": "^1"},
        },
    )
    (agent / "CHANGELOG.md").write_text("# Changelog\n")
    (agent / "docs").mkdir(parents=True, exist_ok=True)
    (agent / "docs" / "mirror-README.md").write_text("# Distribution mirror\n")
    (agent / "LICENSE").write_text("Apache License 2.0\n")
    return agent


def make_mirror(root: Path, *, cli="0.72.0", plugin="0.17.0", tap="0.2.1") -> Path:
    """A live-mirror stand-in carrying the version-bearing files."""
    mirror = root / "mirror"
    _write_json(
        mirror / "plugins" / "probe-research" / ".claude-plugin" / "plugin.json",
        {"name": "probe-research", "version": plugin},
    )
    _write_json(
        mirror / "plugins" / "probe-research-tap" / ".claude-plugin" / "plugin.json",
        {"name": "probe-research-tap", "version": tap},
    )
    _write_json(
        mirror / "client-version.json",
        {
            "cli": {"latest": cli, "min": "0.6.0"},
            "plugin": {"latest": plugin, "min": "0.6.0"},
            "tap": {"latest": tap, "min": "0.1.0"},
        },
    )
    (mirror / "stale-src").mkdir(parents=True)
    (mirror / "stale-src" / "old.py").write_text("# pre-migration source file\n")
    return mirror


def _tree(path: Path) -> dict[str, str]:
    return {
        str(p.relative_to(path)): p.read_text()
        for p in sorted(path.rglob("*"))
        if p.is_file() and ".git" not in p.parts
    }


# --- structural guards (exit 2 class) ---------------------------------------


def test_malformed_marketplace_aborts(tmp_path):
    agent = make_source(tmp_path)
    (agent / ".claude-plugin" / "marketplace.json").write_text("{not json")
    with pytest.raises(mirror_render.GuardError, match="not valid JSON"):
        mirror_render.check_source(agent)


def test_missing_plugin_source_dir_aborts(tmp_path):
    agent = make_source(tmp_path)
    shutil.rmtree(agent / "plugins" / "probe-research-tap")
    with pytest.raises(mirror_render.GuardError, match="source dir"):
        mirror_render.check_source(agent)


def test_daemon_plugin_version_must_match_probe_research(tmp_path):
    """The lean plugin ships in the same release as probe-research (release.yml
    bumps both): a mismatch means one bump was missed."""
    agent = make_source(tmp_path)
    _write_json(
        agent / "plugins" / "probe-research-daemon" / ".claude-plugin" / "plugin.json",
        {"name": "probe-research-daemon", "version": "0.16.0"},
    )
    with pytest.raises(mirror_render.GuardError, match="probe-research-daemon plugin.json"):
        mirror_render.check_source(agent)


def test_tap_manifest_version_mismatch_aborts(tmp_path):
    agent = make_source(tmp_path)
    _write_json(
        agent / "plugins" / "probe-research-tap" / ".claude-plugin" / "plugin.json",
        {"name": "probe-research-tap", "version": "0.99.0"},
    )
    with pytest.raises(mirror_render.GuardError, match="version mismatch"):
        mirror_render.check_source(agent)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda a: _write_json(
                a / ".claude-plugin" / "marketplace.json", {"name": "x", "plugins": []}
            ),
            "no plugins",
        ),
        (
            lambda a: _write_json(
                a / "client-version.json",
                {"cli": {"latest": "0.72.0"}, "plugin": {"latest": "0.17.0"}},
            ),
            "missing 'tap'",
        ),
        (
            lambda a: (a / ".claude-plugin" / "marketplace.json").write_text("[]"),
            "must be a JSON object",
        ),
        (
            lambda a: _write_json(
                a / "client-version.json",
                {
                    "cli": {"latest": 720},
                    "plugin": {"latest": "0.17.0"},
                    "tap": {"latest": "0.2.1"},
                },
            ),
            "expected a version string",
        ),
        (
            lambda a: _write_json(
                a / "client-version.json",
                {
                    "cli": {"latest": "1.2.x"},
                    "plugin": {"latest": "0.17.0"},
                    "tap": {"latest": "0.2.1"},
                },
            ),
            "not MAJOR.MINOR.PATCH",
        ),
        (
            lambda a: _write_json(
                a / "client-version.json",
                {
                    "cli": {"latest": "0.72.0", "min": "99.0.0"},
                    "plugin": {"latest": "0.17.0"},
                    "tap": {"latest": "0.2.1"},
                },
            ),
            "unsatisfiable update loop",
        ),
        (
            lambda a: _write_json(
                a / ".claude-plugin" / "marketplace.json",
                {
                    "name": "x",
                    "plugins": [{"name": "probe-research", "source": "./plugins/probe-research"}],
                },
            ),
            "rendered plugin dirs",
        ),
        (
            lambda a: _write_json(
                a / ".agents" / "plugins" / "marketplace.json",
                {
                    "name": "x",
                    "plugins": [
                        {
                            "name": "probe-research",
                            "source": {"source": "local", "path": "./plugins/probe-research"},
                        }
                    ],
                },
            ),
            "codex marketplace plugin sources",
        ),
        (
            lambda a: (a / ".agents" / "plugins" / "marketplace.json").write_text("{oops"),
            "not valid JSON",
        ),
    ],
)
def test_structural_guard_matrix(tmp_path, mutate, message):
    agent = make_source(tmp_path)
    mutate(agent)
    with pytest.raises(mirror_render.GuardError, match=message):
        mirror_render.check_source(agent)


# --- pi package guard (_check_pi_package) -----------------------------------


def test_pi_package_is_absent_from_both_marketplaces_and_still_renders(tmp_path):
    """The whole point of the exemption: pi has no marketplace entry, and the
    two marketplace cross-checks must not demand one."""
    source, mirror = make_source(tmp_path), make_mirror(tmp_path)

    mirror_render.check_source(source)  # must not raise

    mirror_render.render(source, mirror)
    assert (mirror / "package.json").is_file()
    assert (mirror / "plugins" / "probe-research-pi" / "index.ts").is_file()


def test_root_manifest_pointing_at_a_missing_file_aborts(tmp_path):
    """A typo'd path would install cleanly and then load nothing -- the exact
    silent failure the guard exists to make loud."""
    source = make_source(tmp_path)
    _write_json(
        source / "mirror-package.json",
        {
            "name": "research-os-agent",
            "pi": {"extensions": ["plugins/probe-research-pi/typo.ts"]},
        },
    )

    with pytest.raises(mirror_render.GuardError, match="does not exist"):
        mirror_render.check_source(source)


def test_root_manifest_pointing_outside_a_rendered_plugin_dir_aborts(tmp_path):
    """Referencing content the mirror does not carry ships a manifest whose
    targets are absent on the far side."""
    source = make_source(tmp_path)
    stray = source / "plugins" / "not-rendered"
    stray.mkdir(parents=True)
    (stray / "index.ts").write_text("export default function () {}\n")
    _write_json(
        source / "mirror-package.json",
        {
            "name": "research-os-agent",
            "pi": {"extensions": ["plugins/not-rendered/index.ts"]},
        },
    )

    with pytest.raises(mirror_render.GuardError, match="RENDER_ITEMS does not carry"):
        mirror_render.check_source(source)


def test_root_manifest_with_no_pi_section_aborts(tmp_path):
    source = make_source(tmp_path)
    _write_json(source / "mirror-package.json", {"name": "research-os-agent"})

    with pytest.raises(mirror_render.GuardError, match="no 'pi' manifest"):
        mirror_render.check_source(source)


def test_a_rendered_pi_package_the_manifest_never_references_aborts(tmp_path):
    """Both directions. A pi dir that is exempt from the marketplace checks AND
    unreferenced by the root manifest would ship as dead weight."""
    source = make_source(tmp_path)
    _write_json(
        source / "mirror-package.json",
        {
            "name": "research-os-agent",
            # Valid, existing, rendered -- but belongs to the CLAUDE plugin, so
            # plugins/probe-research-pi ends up referenced by nothing.
            "pi": {"skills": ["plugins/probe-research/skills"]},
        },
    )

    with pytest.raises(mirror_render.GuardError, match="dead weight"):
        mirror_render.check_source(source)


def test_a_runtime_dependency_missing_from_the_root_manifest_aborts(tmp_path):
    """pi installs the mirror with `npm install --omit=dev` at the CLONE ROOT,
    so the root manifest is the only dependency list that reaches a user. A
    missing one does not error -- it HANGS the extension load, which is how
    `typebox` (a value import declared as a devDependency) was caught."""
    source = make_source(tmp_path)
    manifest = json.loads((source / "mirror-package.json").read_text())
    manifest["dependencies"] = {}
    _write_json(source / "mirror-package.json", manifest)

    with pytest.raises(mirror_render.GuardError, match="does not declare 'dep'"):
        mirror_render.check_source(source)


def test_a_drifted_dependency_spec_aborts(tmp_path):
    source = make_source(tmp_path)
    manifest = json.loads((source / "mirror-package.json").read_text())
    manifest["dependencies"] = {"dep": "^2"}
    _write_json(source / "mirror-package.json", manifest)

    with pytest.raises(mirror_render.GuardError, match="keep them identical"):
        mirror_render.check_source(source)


def test_node_modules_is_never_rendered_or_scanned(tmp_path):
    """A developer who has run the plugin's vitest suite has a node_modules
    full of npm's `.bin` symlinks. Without the exclusion the render either
    aborts on those or copies a dependency tree into the public repo."""
    source, mirror = make_source(tmp_path), make_mirror(tmp_path)
    nm = source / "plugins" / "probe-research-pi" / "node_modules" / ".bin"
    nm.mkdir(parents=True)
    (nm / "tsserver").symlink_to("/nonexistent/tsserver")

    mirror_render.check_source(source)  # must not raise on the symlink
    mirror_render.render(source, mirror)

    assert not (mirror / "plugins" / "probe-research-pi" / "node_modules").exists()


def test_symlink_in_render_item_aborts(tmp_path):
    agent = make_source(tmp_path)
    (agent / "plugins" / "probe-research" / "skills" / "escape.md").symlink_to(
        agent / ".." / ".." / "somewhere-else"
    )
    with pytest.raises(mirror_render.GuardError, match="symlink in render item"):
        mirror_render.check_source(agent)


def test_plugin_manifest_version_mismatch_aborts(tmp_path):
    agent = make_source(tmp_path)
    _write_json(
        agent / "plugins" / "probe-research" / ".claude-plugin" / "plugin.json",
        {"name": "probe-research", "version": "0.99.0"},
    )
    with pytest.raises(mirror_render.GuardError, match="version mismatch"):
        mirror_render.check_source(agent)


def test_missing_render_item_aborts(tmp_path):
    agent = make_source(tmp_path)
    (agent / "LICENSE").unlink()
    with pytest.raises(mirror_render.GuardError, match="render item missing"):
        mirror_render.check_source(agent)


# --- regression guard (exit 3 class) -----------------------------------------


def test_version_regression_aborts(tmp_path):
    agent = make_source(tmp_path, plugin="0.16.0", tap="0.2.1")
    mirror = make_mirror(tmp_path, plugin="0.17.0")
    with pytest.raises(mirror_render.RegressionError, match="OLDER"):
        mirror_render.check_regression(agent, mirror)


def test_equal_versions_pass(tmp_path):
    agent = make_source(tmp_path)
    mirror = make_mirror(tmp_path)
    mirror_render.check_regression(agent, mirror)  # must not raise


def test_newer_source_passes(tmp_path):
    agent = make_source(tmp_path, plugin="0.18.0")
    mirror = make_mirror(tmp_path)
    mirror_render.check_regression(agent, mirror)


def test_short_version_equals_padded_version(tmp_path):
    """ "0.17" and "0.17.0" are the same version, not a regression."""
    agent = make_source(tmp_path)
    _write_json(
        tmp_path / "agent" / "client-version.json",
        {
            "cli": {"latest": "0.72", "min": "0.6.0"},
            "plugin": {"latest": "0.17.0", "min": "0.6.0"},
            "tap": {"latest": "0.2.1", "min": "0.1.0"},
        },
    )
    mirror = make_mirror(tmp_path, cli="0.72.0")
    mirror_render.check_regression(agent, mirror)


def test_missing_mirror_plugins_dir_skips_not_wedges(tmp_path):
    agent = make_source(tmp_path)
    mirror = make_mirror(tmp_path)
    shutil.rmtree(mirror / "plugins")
    mirror_render.check_regression(agent, mirror)


def test_unreadable_mirror_side_skips_not_wedges(tmp_path):
    """First sync: the mirror may hold anything. Only the SOURCE going
    backwards is a failure; an unparsable mirror copy skips that comparison."""
    agent = make_source(tmp_path)
    mirror = make_mirror(tmp_path)
    (mirror / "client-version.json").write_text("{broken")
    mirror_render.check_regression(agent, mirror)


# --- render ------------------------------------------------------------------


def test_render_produces_exactly_the_item_list_and_stomps_strays(tmp_path):
    agent = make_source(tmp_path)
    mirror = make_mirror(tmp_path)
    mirror_render.render(agent, mirror)
    tree = _tree(mirror)
    assert "README.md" in tree  # docs/mirror-README.md lands as README.md
    assert "LICENSE" in tree
    assert ".claude-plugin/marketplace.json" in tree
    assert "plugins/probe-research/.claude-plugin/plugin.json" in tree
    assert "plugins/probe-research/skills/s.md" in tree
    assert not any(p.startswith("stale-src") for p in tree), (
        "pre-existing mirror content must be stomped — the mirror is a build artifact"
    )
    assert not any(p.startswith((".github", "src", "tests")) for p in tree)


def test_render_is_deterministic(tmp_path):
    """Same source in, byte-identical mirror out — re-running a failed job is safe."""
    agent = make_source(tmp_path)
    first = tmp_path / "m1"
    second = tmp_path / "m2"
    first.mkdir()
    second.mkdir()
    mirror_render.render(agent, first)
    mirror_render.render(agent, second)
    assert _tree(first) == _tree(second)
    # And re-rendering over an existing render changes nothing.
    mirror_render.render(agent, first)
    assert _tree(first) == _tree(second)


# --- CLI exit codes (the workflow's actual interface) ------------------------


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(_TOOL), *args], capture_output=True, text=True)


def test_check_only_renders_nothing(tmp_path):
    make_source(tmp_path)
    mirror = make_mirror(tmp_path)
    before = _tree(mirror)
    ok = _run_cli("--source", str(tmp_path), "--mirror", str(mirror), "--check-only")
    assert ok.returncode == 0, ok.stderr
    assert _tree(mirror) == before, "--check-only must not touch the mirror"


def test_nonexistent_mirror_dir_is_a_guard_error(tmp_path):
    make_source(tmp_path)
    gone = _run_cli("--source", str(tmp_path), "--mirror", str(tmp_path / "nope"))
    assert gone.returncode == mirror_render.GUARD_EXIT, gone.stderr


def test_cli_exit_codes(tmp_path):
    make_source(tmp_path)
    make_mirror(tmp_path)
    ok = _run_cli("--source", str(tmp_path), "--mirror", str(tmp_path / "mirror"))
    assert ok.returncode == 0, ok.stderr

    # regression → exit 3
    _write_json(
        tmp_path / "agent" / "client-version.json",
        {
            "cli": {"latest": "0.1.0", "min": "0.1.0"},
            "plugin": {"latest": "0.17.0", "min": "0.6.0"},
            "tap": {"latest": "0.2.1", "min": "0.1.0"},
        },
    )
    reg = _run_cli("--source", str(tmp_path), "--mirror", str(tmp_path / "mirror"), "--check-only")
    assert reg.returncode == mirror_render.REGRESSION_EXIT, reg.stderr

    # structural guard → exit 2
    (tmp_path / "agent" / ".claude-plugin" / "marketplace.json").write_text("{broken")
    bad = _run_cli("--source", str(tmp_path), "--mirror", str(tmp_path / "mirror"), "--check-only")
    assert bad.returncode == mirror_render.GUARD_EXIT, bad.stderr


def test_the_repos_own_mirror_manifest_points_at_skills_that_exist() -> None:
    """THE REAL manifest against THE REAL tree, which nothing else here does.

    Every other test in this file builds a synthetic source directory and checks
    the validator's logic against it. That proves the guard works and says
    nothing about whether `agent/mirror-package.json` is currently correct -- so
    when the switch skill split landed, `pi.skills` still named
    `instrument-training-runs`, this file stayed green, and the miss surfaced in
    the RELEASE, after PyPI and npm had already published.

    The guard itself did its job there (it refused rather than mirroring a
    package that would install and load nothing). This is the same check, run
    where it is cheap to fix.
    """
    import json

    agent_root = Path(__file__).resolve().parents[1]
    manifest = json.loads((agent_root / "mirror-package.json").read_text(encoding="utf-8"))
    entries = manifest.get("pi", {}).get("skills", [])
    assert entries, "mirror-package.json declares no pi.skills"
    missing = [entry for entry in entries if not (agent_root / entry).is_dir()]
    assert not missing, (
        f"mirror-package.json names skills that do not exist under agent/: {missing}. "
        "pi would install this package and load nothing for them."
    )

    # ...and the two manifests must agree. They are separate files with separate
    # lists, which is exactly how one of them went stale.
    package = json.loads(
        (agent_root / "plugins" / "probe-research-pi" / "package.json").read_text(
            encoding="utf-8"
        )
    )
    shipped = [
        f"plugins/probe-research-pi/{entry.removeprefix('./')}"
        for entry in package.get("pi", {}).get("skills", [])
    ]
    assert sorted(entries) == sorted(shipped), (
        "mirror-package.json and probe-research-pi/package.json disagree about "
        f"pi.skills: {sorted(entries)} vs {sorted(shipped)}"
    )

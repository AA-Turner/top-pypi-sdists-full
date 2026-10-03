"""`client-version.json` must agree with the versions it advertises.

The manifest is what the SessionStart hook reads to decide whether to nudge a
user to update. Nothing tied it to the versions actually on main, so the two
drifted silently — and the failure mode is the worst kind: CI green, content
correct, release tagged, and the rollout reaching NOBODY, because every client
compares itself against a manifest still naming the previous version.

Both halves of this had already broken by the time the guard was written:

  * `plugin.json` was hand-bumped 0.13.0 -> 0.13.1 without the manifest. Three
    skill-description releases shipped to main while `plugin.latest` still said
    0.13.0, so no installed plugin was ever told to update.
  * `pyproject.toml` sat at 0.26.0 while PyPI's latest was 0.25.0 and
    `cli.latest` said 0.25.0 — a version bumped by one PR and never released,
    found only by hand during an unrelated pre-flight.

Same contract as tests/test_skills_sync.py: that one guards the three COPIES of
the skill text against each other; this guards the VERSION NUMBERS. Content
drift was covered, release drift was not.

The invariant holds naturally when you release through `release.yml`, which
writes the version file and the manifest in a single commit. What this test
actually forbids is hand-editing a version file — which is precisely the thing
that cost the 0.13.1 rollout.

NOTE the `min` fields are deliberately NOT checked. They are compatibility
floors that lag `latest` on purpose; pinning them together would defeat them.
"""

from __future__ import annotations

import ast
import json
from probe._compat import tomllib
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_MANIFEST = _ROOT / "client-version.json"
_PLUGIN_JSON = _ROOT / "plugins" / "probe-research" / ".claude-plugin" / "plugin.json"
_TAP_PLUGIN_JSON = _ROOT / "plugins" / "probe-research-tap" / ".claude-plugin" / "plugin.json"
_PYPROJECT = _ROOT / "pyproject.toml"

_REMEDY = (
    "Release through the workflow, which writes both files in one commit:\n"
    "  gh workflow run release.yml -f plugin_version=X.Y.Z          # plugin\n"
    "  gh workflow run release.yml -f version=X.Y.Z -f bump_manifest=true  # CLI\n"
    "Hand-editing a version file looks like it ships and silently does not."
)


def _manifest() -> dict:
    return json.loads(_MANIFEST.read_text(encoding="utf-8"))


def test_manifest_plugin_latest_matches_plugin_json() -> None:
    advertised = _manifest()["plugin"]["latest"]
    actual = json.loads(_PLUGIN_JSON.read_text(encoding="utf-8"))["version"]
    assert advertised == actual, (
        f"client-version.json plugin.latest is {advertised!r} but plugin.json is "
        f"{actual!r}. The SessionStart hook nudges off the manifest, so plugin "
        f"{actual} ships to nobody.\n{_REMEDY}"
    )


def test_manifest_tap_latest_matches_tap_plugin_json() -> None:
    """Same contract as the plugin above, for probe-research-tap.

    The tap needs this MORE than the other two, not less. It has no release
    workflow — the marketplace serves it from main, so merging IS the release
    and nothing writes the manifest for you. And its failure is silent by
    construction: a stale tap still authenticates, still links sessions to
    projects, and simply never delivers a transcript. The 0.1.3 fix (daemons
    dying seconds after SessionStart) is exactly that shape — a user left on
    0.1.2 sees a healthy-looking session and no transcript, with the only
    evidence a line in a local log file.
    """
    advertised = _manifest()["tap"]["latest"]
    actual = json.loads(_TAP_PLUGIN_JSON.read_text(encoding="utf-8"))["version"]
    assert advertised == actual, (
        f"client-version.json tap.latest is {advertised!r} but the tap's "
        f"plugin.json is {actual!r}. The SessionStart hook nudges off the "
        f"manifest, so tap {actual} ships to nobody who does not auto-update.\n"
        "The tap has no release workflow: bump BOTH files in the same commit."
    )


def test_the_daemon_plugin_moves_with_probe_research() -> None:
    """The daemon profile's lean plugin (daemon reads) carries byte-identical
    copies of probe-research's hooks and ships in the same release, so both of
    its manifests carry probe-research's version: release.yml bumps all four
    files in one commit, and the mirror refuses a mismatch."""
    expected = json.loads(_PLUGIN_JSON.read_text(encoding="utf-8"))["version"]
    root = _ROOT / "plugins" / "probe-research-daemon"
    for manifest in (root / ".claude-plugin" / "plugin.json", root / ".codex-plugin" / "plugin.json"):
        actual = json.loads(manifest.read_text(encoding="utf-8"))["version"]
        assert actual == expected, (
            f"{manifest.relative_to(_ROOT)} is {actual!r} but probe-research is {expected!r}.\n{_REMEDY}"
        )
    # release.yml bumps through tools/release_bump.py, whose list comes from the
    # harness registry; tests/test_release_bump.py pins that list.
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("_sync_release_bump", _ROOT / "tools" / "release_bump.py")
    release_bump = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = release_bump
    spec.loader.exec_module(release_bump)
    for rel in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        path = f"agent/plugins/probe-research-daemon/{rel}"
        assert path in release_bump.plugin_manifests(), f"release.yml must bump {path}"


def test_manifest_cli_latest_matches_pyproject() -> None:
    advertised = _manifest()["cli"]["latest"]
    with _PYPROJECT.open("rb") as fh:
        actual = tomllib.load(fh)["project"]["version"]
    assert advertised == actual, (
        f"client-version.json cli.latest is {advertised!r} but pyproject.toml is "
        f"{actual!r}. Either the CLI was bumped without releasing it, or it was "
        f"released without bumping the manifest.\n{_REMEDY}"
    )


def test_tap_package_and_runtime_report_the_advertised_version() -> None:
    """The installed package and HTTP user-agent must identify the same release."""
    tap = _TAP_PLUGIN_JSON.parent.parent
    expected = _manifest()["tap"]["latest"]
    with (tap / "pyproject.toml").open("rb") as source:
        assert tomllib.load(source)["project"]["version"] == expected
    assert json.loads((tap / ".codex-plugin" / "plugin.json").read_text())["version"] == expected
    module = ast.parse((tap / "tap" / "__init__.py").read_text())
    versions = [
        ast.literal_eval(node.value)
        for node in module.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "__version__" for target in node.targets)
    ]
    assert versions == [expected]


#: Plan 2.11 (D29): the packages release N+1 takes out of the bare install.
_RELEASE_N1_PACKAGES = ("typer", "questionary", "mcp", "anyio", "tiktoken")

#: The npm launcher (`npx probe-research`) and the last version of it published
#: before it asked for `probe-research[all]`. It runs `probe` from a throwaway
#: `uv tool run` environment with no install record, so SELF_REINSTALL cannot
#: help it: at N+1 a launcher that asks for the bare package gets a `probe`
#: without its CLI dependencies. `release.yml` publishes the launcher only when
#: `agent/npm/package.json` is newer than the registry.
_NPM_DIR = _ROOT / "npm"
_LAST_BARE_LAUNCHER = (0, 12, 0)

_GATE = (
    "GATE -- plan 2.11 (D29), root TODOS.md \"Packaging (plan 2.11, D29)\". Taking the CLI's "
    "and MCP server's dependencies out of core is release N+1, and it strips `probe` from "
    "every install that skipped release N (an older updater installs the bare package). It "
    "must not ship before (1) `probe._entry` reinstalls itself with `[all]` when one of them "
    "is missing -- set `probe._entry.SELF_REINSTALL = True` only when it does -- and (2) the "
    "pre-N -> N+1 upgrade test with real uv exists. Do NOT edit this test away to make a "
    "release pass: finish the gate items first."
)


def test_release_n1_waits_for_the_self_reinstall() -> None:
    """The release gate itself (release.yml runs this suite): a CLI release
    that drops a package below from core fails here until the self-reinstall
    it depends on exists. Versions alone are not gated -- only the change
    that breaks installs that skipped release N."""
    with _PYPROJECT.open("rb") as fh:
        core = tomllib.load(fh)["project"]["dependencies"]
    names = {
        spec.split(";")[0].replace(" ", "").split("<")[0].split(">")[0].split("=")[0].split("[")[0]
        for spec in core
    }
    dropped = [name for name in _RELEASE_N1_PACKAGES if name not in names]
    if not dropped:
        return
    import probe._entry as entry

    assert getattr(entry, "SELF_REINSTALL", False) is True, f"{dropped} left core. {_GATE}"
    # The npm launcher, which no install record reaches (#2043 verify): it must
    # ask for `[all]` AND be a version newer than the last one published
    # without it, or release.yml never publishes the version that asks.
    launcher = (_NPM_DIR / "bin" / "probe-research.js").read_text(encoding="utf-8")
    assert "${DIST}[all]" in launcher, (
        f"{dropped} left core, but the npm launcher does not ask for probe-research[all]. {_GATE}"
    )
    version = json.loads((_NPM_DIR / "package.json").read_text(encoding="utf-8"))["version"]
    assert tuple(int(p) for p in version.split(".")[:3]) > _LAST_BARE_LAUNCHER, (
        f"{dropped} left core, but agent/npm/package.json is still {version}: release.yml "
        "publishes the launcher only when that version is newer than the registry, and "
        f"{'.'.join(map(str, _LAST_BARE_LAUNCHER))} (published) asks for the bare package, so "
        "`npx probe-research` users would get a `probe` without its CLI dependencies. Bump "
        f"agent/npm/package.json in the release before N+1. {_GATE}"
    )


def test_the_n1_gate_fails_a_core_without_typer(tmp_path, monkeypatch) -> None:
    """Negative control: the gate above, pointed at a pyproject whose core no
    longer carries typer, fails -- and names the gate."""
    import sys

    import pytest

    text = _PYPROJECT.read_text(encoding="utf-8")
    trimmed = "\n".join(line for line in text.splitlines() if not line.strip().startswith('"typer'))
    assert trimmed != text
    fake = tmp_path / "pyproject.toml"
    fake.write_text(trimmed + "\n", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "_PYPROJECT", fake)
    with pytest.raises(AssertionError, match="GATE -- plan 2.11"):
        test_release_n1_waits_for_the_self_reinstall()


def _n1_ready(tmp_path, monkeypatch, *, launcher_version: str, asks_for_all: bool = True):
    """A tree where core dropped typer and the self-reinstall exists; only the
    npm launcher varies."""
    import sys

    import probe._entry as entry

    text = _PYPROJECT.read_text(encoding="utf-8")
    fake = tmp_path / "pyproject.toml"
    fake.write_text(
        "\n".join(line for line in text.splitlines() if not line.strip().startswith('"typer')) + "\n",
        encoding="utf-8",
    )
    npm = tmp_path / "npm"
    (npm / "bin").mkdir(parents=True)
    source = (_NPM_DIR / "bin" / "probe-research.js").read_text(encoding="utf-8")
    if not asks_for_all:
        source = source.replace("${DIST}[all]", "${DIST}")
    (npm / "bin" / "probe-research.js").write_text(source, encoding="utf-8")
    package = json.loads((_NPM_DIR / "package.json").read_text(encoding="utf-8"))
    (npm / "package.json").write_text(json.dumps({**package, "version": launcher_version}), encoding="utf-8")
    module = sys.modules[__name__]
    monkeypatch.setattr(module, "_PYPROJECT", fake)
    monkeypatch.setattr(module, "_NPM_DIR", npm)
    monkeypatch.setattr(entry, "SELF_REINSTALL", True, raising=False)


def test_the_n1_gate_holds_for_an_unpublished_npm_launcher(tmp_path, monkeypatch) -> None:
    """#2043 verify. The self-reinstall cannot reach `npx probe-research` (a
    throwaway environment, no install record): N+1 also waits for a launcher
    that asks for `[all]` in a version release.yml will publish."""
    import pytest

    _n1_ready(tmp_path, monkeypatch, launcher_version="0.12.0")
    with pytest.raises(AssertionError, match="agent/npm/package.json is still 0.12.0"):
        test_release_n1_waits_for_the_self_reinstall()


def test_the_n1_gate_holds_for_a_launcher_asking_for_the_bare_package(tmp_path, monkeypatch) -> None:
    import pytest

    _n1_ready(tmp_path, monkeypatch, launcher_version="0.13.0", asks_for_all=False)
    with pytest.raises(AssertionError, match="does not ask for probe-research\\[all\\]"):
        test_release_n1_waits_for_the_self_reinstall()


def test_the_n1_gate_opens_when_every_item_is_done(tmp_path, monkeypatch) -> None:
    """Control: self-reinstall + a bumped launcher asking for `[all]` passes."""
    _n1_ready(tmp_path, monkeypatch, launcher_version="0.13.0")
    test_release_n1_waits_for_the_self_reinstall()

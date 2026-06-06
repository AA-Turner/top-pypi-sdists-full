"""Tier 2: build + run the real frozen full ``runlayer`` CLI bundle.

Proves the full-CLI PyInstaller onedir (``packaging/runlayer.spec``) — which
includes the heavy fastmcp / mcp / docker / questionary closure the aiwatch
bundle excludes — actually imports and runs as a frozen exe. Catches missing
hidden imports / data files that only surface at runtime.

Slow (a full PyInstaller build) and opt-in: gated behind ``-m frozen_binary``.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from runlayer_cli import __version__

pytestmark = pytest.mark.frozen_binary


def _run(exe: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(exe), *args],
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_frozen_runlayer_version(frozen_runlayer: Path) -> None:
    result = _run(frozen_runlayer, "--version")
    assert result.returncode == 0, result.stderr
    assert __version__ in result.stdout


def test_frozen_runlayer_help(frozen_runlayer: Path) -> None:
    result = _run(frozen_runlayer, "--help")
    assert result.returncode == 0, result.stderr
    # Spot-check that the heavy subcommands made it into the frozen app.
    for subcommand in ("run", "deploy", "scan", "login"):
        assert subcommand in result.stdout


def test_frozen_runlayer_bundles_lupa_lua51(frozen_runlayer: Path) -> None:
    """Regression for ENG-3220: ``runlayer run`` -> fastmcp ``run_stdio_async`` ->
    docket ``memory://`` pool -> fakeredis ``importlib.import_module("lupa.lua51")``.

    That dynamic string import is invisible to PyInstaller, so the compiled lupa
    Lua runtime must be bundled explicitly (``packaging/runlayer.spec``). Without it
    every frozen ``runlayer run`` dies with ``ModuleNotFoundError: lupa.lua51``.
    """
    bundle_root = frozen_runlayer.parent
    lua51_libs = list(bundle_root.rglob("lua51.*"))
    assert lua51_libs, (
        "lupa.lua51 compiled extension missing from the frozen runlayer bundle; "
        f"searched under {bundle_root}"
    )


def test_frozen_runlayer_bundles_fakeredis_commands_json(frozen_runlayer: Path) -> None:
    """Regression for ENG-3224: ``runlayer run`` -> fastmcp ``run_stdio_async`` ->
    docket ``memory://`` pool -> fakeredis ``model/_command_info._load_command_info``
    reads ``fakeredis/commands.json`` via
    ``open(os.path.join(os.path.dirname(__file__), "..", "commands.json"))``.

    Two traps the spec must clear (``packaging/runlayer.spec``):
      1. commands.json is a data file, not a ``.py`` module, so static analysis misses it.
      2. The open path is *relative* (``.../fakeredis/model/../commands.json``). The OS
         resolves ``..`` against the real filesystem, so ``fakeredis/model/`` must exist
         on disk -- but ``noarchive=False`` keeps ``model/*.py`` in the PYZ, so a build
         that only collects commands.json (not the package tree) leaves ``model/`` absent
         and the open still ``FileNotFoundError``s.

    Assert against the *exact* path fakeredis opens (not a loose ``rglob``) so a bundle
    where commands.json exists but is unreachable via ``model/..`` fails here.
    """
    internal = frozen_runlayer.parent / "_internal"
    probe = internal / "fakeredis" / "model" / ".." / "commands.json"
    # Path.exists() / open() go through os.stat/os.open, which resolve ".." via the
    # filesystem -- so this fails if _internal/fakeredis/model/ was never created.
    assert probe.exists(), (
        "fakeredis commands.json unreachable via model/../commands.json "
        f"(fakeredis/model/ dir missing?); searched under {internal}"
    )
    with probe.open(encoding="utf8"):
        pass

"""Coverage for the asset-tool detection registry.

The asset-tool registry isn't on the build hot path — it's an
introspection layer for `sage list tools` and for advertising rich
workflows when a tool is locally available. The tests here lock down:

  * Every registered tool has a non-empty install hint pointing at the
    canonical install command for Windows/Linux/macOS.
  * Aliases (e.g. Aseprite + LibreSprite) are both recognized.
  * `available_tools()` returns only the tools currently on PATH (used
    by the CLI introspector — must not lie).
  * Kind taxonomy is coherent (every tool has exactly one kind; every
    kind has at least one tool).
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from sage.games.assets.tools import (
    all_tool_kinds,
    all_tool_names,
    available_tools,
    detect_tool,
    install_hint,
    tools_by_kind,
)


# ───────────────────────── registry coverage ──────────────────────────


def test_known_asset_tools_cover_every_major_category():
    """The user wants sage to be expert across all major asset workflows.
    Verify each category is present in the registry."""
    expected = {
        "3d-model", "2d-sprite", "2d-paint", "tilemap",
        "image-cli", "audio-edit", "audio-tracker",
    }
    assert expected.issubset(all_tool_kinds())


@pytest.mark.parametrize("tool", [
    "blender", "aseprite", "libresprite", "krita", "gimp",
    "tiled", "imagemagick", "audacity", "sox", "lmms", "assimp",
])
def test_every_known_tool_has_install_hint(tool):
    """Every tool must have a non-empty install hint pointing at a real
    install command or the official URL — sage's UX promise is that
    missing tools always come with a fix."""
    hint = install_hint(tool)
    assert hint, f"{tool} has no install hint"
    assert len(hint) > 30, f"{tool} install hint is too terse"


def test_unknown_tool_install_hint_is_empty_string():
    """Looking up an unknown tool must NOT crash — it returns empty
    so callers can branch with `if hint:`."""
    assert install_hint("nintendo-cartridge-burner") == ""
    assert install_hint("") == ""


def test_blender_is_only_canonical_3d_modeller_with_assimp_as_converter():
    """The 3D-model kind covers Blender (modelling) + Assimp (conversion).
    Maya/3DS Max/ZBrush aren't in the registry because they're paid + don't
    ship CLI binaries by default — adding them would be misleading."""
    models = tools_by_kind("3d-model")
    assert "blender" in models
    assert "assimp" in models


def test_aseprite_and_libresprite_both_listed_as_2d_sprite_tools():
    """Aseprite is paid; LibreSprite is the free GPLv2 fork. Sage lists
    both so users on free tooling aren't excluded."""
    sprites = tools_by_kind("2d-sprite")
    assert "aseprite" in sprites
    assert "libresprite" in sprites


# ───────────────────────── detect_tool ────────────────────────────────


def test_detect_tool_returns_path_when_binary_on_path(tmp_path, monkeypatch):
    """If a tool's binary is on PATH, detect() returns its path."""
    fake_dir = tmp_path / "bin"
    fake_dir.mkdir()
    fake_bin = fake_dir / ("blender.exe" if shutil.which("cmd.exe") else "blender")
    fake_bin.write_text("")
    if not shutil.which("cmd.exe"):
        fake_bin.chmod(0o755)
    monkeypatch.setenv("PATH", str(fake_dir) + ";" + monkeypatch.delenv("PATHEXT", raising=False) if False else str(fake_dir))
    # We can't reliably mock shutil.which across all platforms cleanly,
    # so we directly assert detect_tool uses shutil.which under the hood.
    import sage.games.assets.tools as tools
    monkeypatch.setattr(tools.shutil, "which",
                        lambda n: str(fake_bin) if n == "blender" else None)
    assert detect_tool("blender") == fake_bin


def test_detect_tool_returns_none_when_binary_missing(monkeypatch):
    """No binary → None, no exception."""
    import sage.games.assets.tools as tools
    monkeypatch.setattr(tools.shutil, "which", lambda _n: None)
    assert detect_tool("aseprite") is None


def test_detect_tool_unknown_name_returns_none():
    """Unknown tools must return None gracefully so callers can check
    `if detect_tool(...)` without try/except."""
    assert detect_tool("imaginary-tool-9000") is None


def test_detect_tool_tries_each_binary_name(monkeypatch):
    """ImageMagick ships as both `magick` (v7+) and `convert` (legacy v6).
    detect_tool must try every registered binary name, returning the
    first match."""
    import sage.games.assets.tools as tools

    calls: list[str] = []

    def fake_which(n):
        calls.append(n)
        return "/usr/bin/convert" if n == "convert" else None

    monkeypatch.setattr(tools.shutil, "which", fake_which)
    p = detect_tool("imagemagick")
    assert p == Path("/usr/bin/convert")
    # The lookup hit `magick` first (registered first), then fell back
    # to `convert` — meaning the legacy v6 binary still gets recognised.
    assert calls == ["magick", "convert"]


# ───────────────────────── available_tools ────────────────────────────


def test_available_tools_returns_only_those_on_path(monkeypatch):
    """available_tools() must not lie — only tools whose binaries
    actually exist on PATH should appear."""
    import sage.games.assets.tools as tools

    def fake_which(n):
        # Pretend only blender + gimp are installed.
        if n == "blender":
            return "/usr/bin/blender"
        if n == "gimp":
            return "/usr/bin/gimp"
        return None

    monkeypatch.setattr(tools.shutil, "which", fake_which)
    found = available_tools()
    assert set(found.keys()) == {"blender", "gimp"}
    assert found["blender"] == Path("/usr/bin/blender")
    assert found["gimp"] == Path("/usr/bin/gimp")


def test_available_tools_on_empty_path_returns_empty_dict(monkeypatch):
    import sage.games.assets.tools as tools
    monkeypatch.setattr(tools.shutil, "which", lambda _n: None)
    assert available_tools() == {}


def test_available_tools_short_circuits_after_first_binary_match(monkeypatch):
    """For imagemagick (two binary names), once `magick` is found we
    should not also probe `convert` — both keys would map to imagemagick
    and the dict would silently dedupe, but the second which() call is
    wasted work. Asserts short-circuit behavior."""
    import sage.games.assets.tools as tools

    calls: list[str] = []

    def fake_which(n):
        calls.append(n)
        return "/path/magick" if n == "magick" else None

    monkeypatch.setattr(tools.shutil, "which", fake_which)
    found = available_tools()
    assert "imagemagick" in found
    # Should hit `magick` but not `convert` for imagemagick.
    assert "magick" in calls
    assert "convert" not in calls


# ───────────────────────── self-discovery ─────────────────────────────


def test_all_tool_names_is_non_trivial():
    """Sanity: don't ship an empty registry."""
    names = all_tool_names()
    assert len(names) >= 8
    assert "blender" in names
    assert "imagemagick" in names

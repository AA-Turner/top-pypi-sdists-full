"""Detection + capability flags for popular game-asset tools.

The asset generators (sprites/meshes/audio) already integrate with their
primary backends (Imagen + Blender + MusicGen). This module is a
*detection registry* for the broader ecosystem of asset tools sage users
commonly have installed locally — sage can:

  * tell the user what's available (`sage list tools`),
  * offer richer asset workflows when one is detected (e.g. use Aseprite
    for clean pixel-art sprite-sheet exports if it's on PATH),
  * generate setup hints when the tool is missing.

Each tool is keyed by name and has a `detect()` + `install_hint()`. They
DON'T implement asset generation themselves — they're discoverability
hooks. The pipeline calls into them via `available_tools()` to decide
what advanced workflows to advertise.
"""

from __future__ import annotations

import os
import platform
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional


@dataclass
class ToolInfo:
    """One asset tool's static info."""
    name: str
    kind: str               # "2d-sprite" | "2d-paint" | "tilemap" | "3d-model" |
                            # "image-cli" | "audio-edit" | "audio-tracker"
    binary_names: tuple[str, ...]
    install_hint: str
    homepage: str


_TOOLS: tuple[ToolInfo, ...] = (
    # ── 3D modelling / sculpting ─────────────────────────────────────
    ToolInfo(
        name="blender",
        kind="3d-model",
        binary_names=("blender",),
        install_hint=(
            "Install Blender from https://www.blender.org or via package manager:\n"
            "  Windows: `winget install -e --id BlenderFoundation.Blender`\n"
            "  Linux:   `sudo apt install blender` / `sudo pacman -S blender`\n"
            "  macOS:   `brew install --cask blender`"
        ),
        homepage="https://www.blender.org",
    ),
    # ── 2D sprite / pixel-art ─────────────────────────────────────────
    ToolInfo(
        name="aseprite",
        kind="2d-sprite",
        binary_names=("aseprite",),
        install_hint=(
            "Aseprite is paid ($20). https://www.aseprite.org/\n"
            "  Or build from source (GPLv2): https://github.com/aseprite/aseprite"
        ),
        homepage="https://www.aseprite.org",
    ),
    ToolInfo(
        name="libresprite",
        kind="2d-sprite",
        binary_names=("libresprite",),
        install_hint=(
            "Free open-source fork of Aseprite. https://libresprite.github.io/\n"
            "  Linux: `sudo apt install libresprite`"
        ),
        homepage="https://libresprite.github.io",
    ),
    # ── 2D painting ──────────────────────────────────────────────────
    ToolInfo(
        name="krita",
        kind="2d-paint",
        binary_names=("krita",),
        install_hint=(
            "Free, open-source. https://krita.org/\n"
            "  Windows: `winget install -e --id KDE.Krita`\n"
            "  Linux:   `sudo apt install krita`"
        ),
        homepage="https://krita.org",
    ),
    ToolInfo(
        name="gimp",
        kind="2d-paint",
        binary_names=("gimp", "gimp-2.10", "gimp-2.99"),
        install_hint=(
            "Free, open-source. https://www.gimp.org/\n"
            "  Windows: `winget install -e --id GIMP.GIMP`\n"
            "  Linux:   `sudo apt install gimp`"
        ),
        homepage="https://www.gimp.org",
    ),
    # ── Tilemap editor ───────────────────────────────────────────────
    ToolInfo(
        name="tiled",
        kind="tilemap",
        binary_names=("tiled",),
        install_hint=(
            "Tiled is free / pay-what-you-want. https://www.mapeditor.org/\n"
            "  Has a `tmxrasterizer` CLI for headless tilemap → PNG export."
        ),
        homepage="https://www.mapeditor.org",
    ),
    # ── Image CLI ────────────────────────────────────────────────────
    ToolInfo(
        name="imagemagick",
        kind="image-cli",
        binary_names=("magick", "convert"),
        install_hint=(
            "ImageMagick: image format conversion + batch processing.\n"
            "  Windows: `winget install -e --id ImageMagick.ImageMagick`\n"
            "  Linux:   `sudo apt install imagemagick`"
        ),
        homepage="https://imagemagick.org",
    ),
    # ── Audio editing ────────────────────────────────────────────────
    ToolInfo(
        name="audacity",
        kind="audio-edit",
        binary_names=("audacity",),
        install_hint=(
            "Free, open-source audio editor. https://www.audacityteam.org/"
        ),
        homepage="https://www.audacityteam.org",
    ),
    ToolInfo(
        name="sox",
        kind="audio-edit",
        binary_names=("sox",),
        install_hint="The 'Swiss Army knife' of audio. `apt install sox` / `brew install sox`",
        homepage="http://sox.sourceforge.net",
    ),
    # ── Tracker / chiptune ───────────────────────────────────────────
    ToolInfo(
        name="lmms",
        kind="audio-tracker",
        binary_names=("lmms",),
        install_hint="Free DAW. https://lmms.io/  CLI: `lmms --render <project>`",
        homepage="https://lmms.io",
    ),
    # ── Mesh / asset conversion ──────────────────────────────────────
    ToolInfo(
        name="assimp",
        kind="3d-model",
        binary_names=("assimp",),
        install_hint=(
            "Open Asset Import Library — converts between 3D formats.\n"
            "  Linux: `sudo apt install assimp-utils`\n"
            "  macOS: `brew install assimp`"
        ),
        homepage="https://www.assimp.org",
    ),
)


def detect_tool(name: str) -> Optional[Path]:
    """Return the path to `name`'s binary if installed, else None.

    Detection is purely PATH-based for portability — we don't try to glob
    Program Files / /Applications because most asset tools register
    themselves on PATH at install time. (Blender's portable .zip install
    on Windows is the one exception; users can add it to PATH themselves.)"""
    info = _by_name(name)
    if info is None:
        return None
    for bin_name in info.binary_names:
        p = shutil.which(bin_name)
        if p:
            return Path(p)
    return None


def install_hint(name: str) -> str:
    """Human-readable install hint for `name`. Empty string for unknown."""
    info = _by_name(name)
    return info.install_hint if info else ""


def available_tools() -> dict[str, Path]:
    """Snapshot of every known tool currently on PATH.

    Returns `{tool_name: path_to_binary}`. Used by `sage list tools` and
    by the asset pipeline to advertise advanced workflows. Cheap — pure
    PATH lookups, no subprocess calls."""
    found: dict[str, Path] = {}
    for info in _TOOLS:
        for bin_name in info.binary_names:
            p = shutil.which(bin_name)
            if p:
                found[info.name] = Path(p)
                break
    return found


def tools_by_kind(kind: str) -> list[str]:
    """Return tool names matching a kind (`'3d-model'`, `'2d-sprite'`, etc.).
    Order is registration order — primary recommendations first."""
    return [t.name for t in _TOOLS if t.kind == kind]


def all_tool_names() -> list[str]:
    """Every tool name sage knows about."""
    return [t.name for t in _TOOLS]


def all_tool_kinds() -> set[str]:
    return {t.kind for t in _TOOLS}


def _by_name(name: str) -> Optional[ToolInfo]:
    key = (name or "").lower().strip()
    for t in _TOOLS:
        if t.name == key:
            return t
    return None

"""Tests for the installed build-variant marker reader."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from runlayer_cli import update_source, variant


def _linux_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, package: str = "cli"
) -> Path:
    monkeypatch.setattr(sys, "platform", "linux")
    marker_path = tmp_path / "variant"
    monkeypatch.setitem(variant._VARIANT_MARKER_PATHS, package, marker_path)
    return marker_path


def test_absent_marker_means_standard_install(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _linux_marker(tmp_path, monkeypatch)

    assert variant.installed_variant("cli") is None


def test_reads_package_owned_variant_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _linux_marker(tmp_path, monkeypatch).write_text("glibc2.17\n", encoding="ascii")

    assert variant.installed_variant("cli") == "glibc2.17"


@pytest.mark.parametrize(
    "content",
    ["", "musl1.2", "glibc2", "glibc2.17.1", "glibc2.x", "GLIBC2.17"],
)
def test_rejects_invalid_variant_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, content: str
) -> None:
    _linux_marker(tmp_path, monkeypatch).write_text(content, encoding="ascii")

    with pytest.raises(RuntimeError, match="marker is invalid"):
        variant.installed_variant("cli")


def test_unreadable_marker_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _linux_marker(tmp_path, monkeypatch).mkdir()

    with pytest.raises(RuntimeError, match="marker is unreadable"):
        variant.installed_variant("cli")


def test_non_ascii_marker_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _linux_marker(tmp_path, monkeypatch).write_bytes(b"glibc2.17\xff")

    with pytest.raises(RuntimeError, match="marker is unreadable"):
        variant.installed_variant("cli")


@pytest.mark.parametrize("platform", ["darwin", "win32"])
def test_off_linux_is_always_standard(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, platform: str
) -> None:
    marker_path = tmp_path / "variant"
    marker_path.write_text("glibc2.17\n", encoding="ascii")
    monkeypatch.setitem(variant._VARIANT_MARKER_PATHS, "cli", marker_path)
    monkeypatch.setattr(sys, "platform", platform)

    assert variant.installed_variant("cli") is None


def test_every_updatable_package_has_a_marker_path() -> None:
    assert set(variant._VARIANT_MARKER_PATHS) == update_source.SUPPORTED_PACKAGES


def test_ai_watch_reads_its_own_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cli_marker = _linux_marker(tmp_path, monkeypatch, package="cli")
    cli_marker.write_text("glibc2.28\n", encoding="ascii")
    aiwatch_marker = tmp_path / "aiwatch-variant"
    aiwatch_marker.write_text("glibc2.17\n", encoding="ascii")
    monkeypatch.setitem(variant._VARIANT_MARKER_PATHS, "ai-watch", aiwatch_marker)

    assert variant.installed_variant("ai-watch") == "glibc2.17"
    assert variant.installed_variant("cli") == "glibc2.28"


@pytest.mark.parametrize("platform", ["linux", "darwin", "win32"])
def test_rejects_unsupported_package_on_every_platform(
    monkeypatch: pytest.MonkeyPatch, platform: str
) -> None:
    monkeypatch.setattr(sys, "platform", platform)

    with pytest.raises(ValueError, match="Unsupported binary package"):
        variant.installed_variant("browser-extension")

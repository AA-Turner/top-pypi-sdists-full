"""Unit tests for the PE VSVersionInfo file generator."""

from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

import pytest
from packaging.version import Version

PACKAGING_DIR = Path(__file__).resolve().parents[1] / "packaging"
sys.path.insert(0, str(PACKAGING_DIR))

import _version_file  # noqa: E402
from _version_file import write_version_file  # noqa: E402


def _make_pyproject(tmp_path: Path, version: str) -> None:
    (tmp_path / "pyproject.toml").write_text(
        textwrap.dedent(f"""\
            [project]
            name = "runlayer"
            version = "{version}"
        """)
    )


def _extract_filevers(content: str) -> tuple[int, ...]:
    match = re.search(r"filevers=\(([^)]+)\)", content)
    assert match, f"filevers not found in:\n{content}"
    return tuple(int(x.strip()) for x in match.group(1).split(","))


def _extract_string_struct(content: str, key: str) -> str:
    match = re.search(rf'StringStruct\("{key}",\s*["\']([^"\']+)', content)
    assert match, f"StringStruct({key}) not found in:\n{content}"
    return match.group(1)


@pytest.mark.parametrize(
    "version_str, expected_tuple",
    [
        ("0.24.9", (0, 24, 9, 0)),
        ("1.0.0", (1, 0, 0, 0)),
        ("2.3.4.5", (2, 3, 4, 5)),
        ("0.24.9rc1", (0, 24, 9, 0)),
        ("1.0.0.dev3", (1, 0, 0, 0)),
        ("2.0.0a1", (2, 0, 0, 0)),
    ],
)
def test_numeric_tuple(version_str: str, expected_tuple: tuple[int, ...]):
    parsed = Version(version_str)
    release = (*parsed.release, 0, 0, 0, 0)[:4]
    assert release == expected_tuple
    assert all(isinstance(v, int) for v in release)


@pytest.mark.parametrize(
    "version_str",
    ["0.24.9", "0.24.9rc1", "1.0.0.dev3"],
)
def test_write_version_file(version_str: str, tmp_path: Path):
    _make_pyproject(tmp_path, version_str)
    (tmp_path / "packaging").mkdir()
    build_dir = tmp_path / "build"
    build_dir.mkdir()

    orig = _version_file.__file__
    _version_file.__file__ = str(tmp_path / "packaging" / "_version_file.py")
    try:
        path = write_version_file(
            name="aiwatch",
            description="Runlayer AI Watch",
            build_dir=build_dir,
        )
    finally:
        _version_file.__file__ = orig

    content = Path(path).read_text()
    assert _extract_string_struct(content, "FileVersion") == version_str
    assert _extract_string_struct(content, "ProductVersion") == version_str
    assert _extract_string_struct(content, "InternalName") == "aiwatch"
    assert _extract_string_struct(content, "OriginalFilename") == "aiwatch.exe"
    assert _extract_string_struct(content, "CompanyName") == "Runlayer Inc."
    assert _extract_string_struct(content, "FileDescription") == "Runlayer AI Watch"

    expected_tuple = (*Version(version_str).release, 0, 0, 0, 0)[:4]
    assert _extract_filevers(content) == expected_tuple


def test_hook_name(tmp_path: Path):
    _make_pyproject(tmp_path, "1.2.3")
    (tmp_path / "packaging").mkdir()
    build_dir = tmp_path / "build"
    build_dir.mkdir()

    orig = _version_file.__file__
    _version_file.__file__ = str(tmp_path / "packaging" / "_version_file.py")
    try:
        path = write_version_file(
            name="aiwatch-hook",
            description="Runlayer AI Watch Hook",
            build_dir=build_dir,
        )
    finally:
        _version_file.__file__ = orig

    content = Path(path).read_text()
    assert _extract_string_struct(content, "InternalName") == "aiwatch-hook"
    assert _extract_string_struct(content, "OriginalFilename") == "aiwatch-hook.exe"
    assert (
        _extract_string_struct(content, "FileDescription") == "Runlayer AI Watch Hook"
    )

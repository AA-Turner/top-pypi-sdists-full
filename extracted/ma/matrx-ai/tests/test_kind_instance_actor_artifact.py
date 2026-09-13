"""Tests for the published-wheel provenance guard."""

from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path

import pytest

_GUARD_PATH = Path(__file__).parents[1] / "scripts/verify_kind_instance_actor_artifact.py"
_SPEC = importlib.util.spec_from_file_location("kind_instance_actor_artifact_guard", _GUARD_PATH)
assert _SPEC and _SPEC.loader
_GUARD = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_GUARD)
MEMBER = _GUARD.MEMBER
verify_wheel = _GUARD.verify_wheel


def _wheel(path: Path, source: str) -> Path:
    wheel = path / "matrx_ai_test-0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(MEMBER, source)
    return wheel


def test_artifact_guard_accepts_the_current_instance_create_source(tmp_path: Path) -> None:
    source = (
        Path(__file__).parents[1] / "matrx_ai/tools/implementations/kind_instance.py"
    ).read_text()
    verify_wheel(_wheel(tmp_path, source))


def test_artifact_guard_rejects_an_old_unattributed_instance_create(tmp_path: Path) -> None:
    stale_source = """
async def instance_create():
    created = await KindInstance.create_item()
"""
    with pytest.raises(AssertionError, match="outside declared_actor"):
        verify_wheel(_wheel(tmp_path, stale_source))

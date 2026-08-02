# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for the shim TTL CI rule."""

from datetime import date
from pathlib import Path

from omnibase_compat.tooling.shim_ttl_check import _check_file, main


def _write_shim(tmp_path: Path, content: str) -> Path:
    f = tmp_path / "test_shim.py"
    f.write_text(content)
    return f


def test_past_ttl_flagged(tmp_path: Path) -> None:
    path = _write_shim(
        tmp_path,
        "# sunset: omnibase_core >= 0.12.0 (2020-01-01)\nclass Foo: pass\n",
    )
    violations = _check_file(path, date.today())
    assert len(violations) == 1
    assert "2020-01-01" in violations[0]


def test_future_ttl_clean(tmp_path: Path) -> None:
    path = _write_shim(
        tmp_path,
        "# sunset: omnibase_core >= 0.12.0 (2099-12-31)\nclass Foo: pass\n",
    )
    violations = _check_file(path, date.today())
    assert violations == []


def test_no_sunset_annotation_clean(tmp_path: Path) -> None:
    path = _write_shim(tmp_path, "class Foo: pass\n")
    violations = _check_file(path, date.today())
    assert violations == []


def test_main_fails_on_past_ttl(tmp_path: Path) -> None:
    _write_shim(
        tmp_path,
        "# sunset: omnibase_core >= 0.12.0 (2020-06-01)\nclass Bar: pass\n",
    )
    rc = main([str(tmp_path)])
    assert rc == 1


def test_main_passes_on_future_ttl(tmp_path: Path) -> None:
    _write_shim(
        tmp_path,
        "# sunset: omnibase_core >= 0.12.0 (2099-01-01)\nclass Bar: pass\n",
    )
    rc = main([str(tmp_path)])
    assert rc == 0

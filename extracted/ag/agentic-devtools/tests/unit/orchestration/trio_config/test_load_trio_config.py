"""Tests for ``load_trio_config``."""

import json
from pathlib import Path

import pytest

from agentic_devtools.orchestration.trio_config import TrioConfigValidationError, load_trio_config
from tests.unit.orchestration.trio_config._samples import document


def test_load_trio_config_reports_io_json_and_root_failures(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    with pytest.raises(TrioConfigValidationError) as io_error:
        load_trio_config(missing)
    assert io_error.value.__cause__ is not None

    malformed = tmp_path / "malformed.json"
    malformed.write_text("{", encoding="utf-8")
    with pytest.raises(TrioConfigValidationError) as json_error:
        load_trio_config(malformed)
    assert isinstance(json_error.value.__cause__, json.JSONDecodeError)

    invalid_utf8 = tmp_path / "invalid-utf8.json"
    invalid_utf8.write_bytes(b"\x80")
    with pytest.raises(TrioConfigValidationError) as unicode_error:
        load_trio_config(invalid_utf8)
    assert isinstance(unicode_error.value.__cause__, UnicodeDecodeError)

    root = tmp_path / "root.json"
    root.write_text("[]", encoding="utf-8")
    with pytest.raises(TrioConfigValidationError):
        load_trio_config(root)


def test_load_trio_config_reads_valid_document(tmp_path: Path) -> None:
    valid_path = tmp_path / "valid.json"
    valid_path.write_text(json.dumps(document()), encoding="utf-8")
    assert load_trio_config(valid_path).trio_ref == "example-trio"

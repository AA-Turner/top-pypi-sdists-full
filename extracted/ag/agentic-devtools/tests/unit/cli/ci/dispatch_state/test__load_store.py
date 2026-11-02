import json
from pathlib import Path

import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module
from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord

SHA = "a" * 40


def test_returns_empty_store_for_missing_file(tmp_path: Path) -> None:
    assert dispatch_state_module._load_store(tmp_path / "missing.json") == {}


def test_loads_records_from_file(tmp_path: Path) -> None:
    path = tmp_path / "dispatch-state.json"
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    path.write_text(json.dumps({"version": 1, "records": {record.identity.key: record.to_dict()}}), encoding="utf-8")

    loaded = dispatch_state_module._load_store(path)

    assert loaded == {record.identity.key: record.to_dict()}


def test_rejects_blank_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "dispatch-state.json"
    path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="file is blank"):
        dispatch_state_module._load_store(path)

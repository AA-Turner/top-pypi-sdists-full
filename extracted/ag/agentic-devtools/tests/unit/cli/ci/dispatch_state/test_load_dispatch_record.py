import json
from pathlib import Path
from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    DispatchRecord,
    DispatchState,
    load_dispatch_record,
)

SHA = "a" * 40


def test_fails_closed_for_invalid_store_content(tmp_path: Path) -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    with pytest.raises(ValueError):
        DispatchRecord.from_dict(cast(Any, []))
    with pytest.raises(ValueError):
        DispatchRecord.from_dict({"state": "invalid"})
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError):
        load_dispatch_record(bad, identity)
    bad.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError):
        load_dispatch_record(bad, identity)
    bad.write_text('{"version": 2, "records": {}}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_dispatch_record(bad, identity)
    bad.write_text('{"version": 1}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_dispatch_record(bad, identity)


def test_returns_none_for_missing_store_and_rejects_blank_store(tmp_path: Path) -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    blank = tmp_path / "blank.json"
    blank.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="file is blank"):
        load_dispatch_record(blank, identity)
    assert load_dispatch_record(tmp_path / "missing.json", identity) is None


def test_accepts_legacy_record_map_payload(tmp_path: Path) -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    path = tmp_path / "legacy.json"
    legacy_record = DispatchRecord.new(identity).with_state("reserved", marker_comment_id=3)
    path.write_text(json.dumps({identity.key: legacy_record.to_dict()}), encoding="utf-8")

    loaded = load_dispatch_record(path, identity)

    assert loaded is not None
    assert loaded.state is DispatchState.RESERVED


def test_rejects_non_canonical_or_corrupt_records_in_store(tmp_path: Path) -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    path = tmp_path / "bad-records.json"
    good = DispatchRecord.new(identity).to_dict()
    path.write_text(json.dumps({"wrong:key": good}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_dispatch_record(path, identity)

    path.write_text(json.dumps({identity.key: []}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_dispatch_record(path, identity)


def test_rejects_retry_count_over_terminal_budget_on_reload(tmp_path: Path) -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    path = tmp_path / "bad-retry.json"
    reserved = DispatchRecord.new(identity).with_state("reserved", marker_comment_id=3).to_dict()

    path.write_text(json.dumps({identity.key: {**reserved, "retry_count": 4}}), encoding="utf-8")
    with pytest.raises(ValueError, match="invalid record"):
        load_dispatch_record(path, identity)

    path.write_text(json.dumps({identity.key: {**reserved, "retry_count": 999}}), encoding="utf-8")
    with pytest.raises(ValueError, match="invalid record"):
        load_dispatch_record(path, identity)

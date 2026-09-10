import json

import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module
from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord

SHA = "a" * 40


def test_accepts_v1_records_payload() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    content = json.dumps({"version": 1, "records": {record.identity.key: record.to_dict()}})

    loaded = dispatch_state_module._read_store(content)

    assert loaded == {record.identity.key: record.to_dict()}


def test_rejects_invalid_json_or_record_keys() -> None:
    with pytest.raises(ValueError, match="file is blank"):
        dispatch_state_module._read_store("")

    with pytest.raises(ValueError, match="not valid JSON"):
        dispatch_state_module._read_store("{")

    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    content = json.dumps({"version": 1, "records": {"wrong:key": record.to_dict()}})
    with pytest.raises(ValueError, match="record key does not match"):
        dispatch_state_module._read_store(content)


def test_rejects_non_contiguous_ordinals_per_scope() -> None:
    first = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state(
        "abandoned",
        reason="done",
        evidence={"operation": "dispatch"},
    )
    third = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 3)).with_state(
        "abandoned",
        reason="done",
        evidence={"operation": "dispatch"},
    )
    content = json.dumps(
        {"version": 1, "records": {first.identity.key: first.to_dict(), third.identity.key: third.to_dict()}}
    )

    with pytest.raises(ValueError, match="contiguous"):
        dispatch_state_module._read_store(content)


def test_rejects_multiple_unresolved_ordinals_per_scope() -> None:
    first = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state(
        "reserved",
        marker_comment_id=3,
    )
    second = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 2))
    content = json.dumps(
        {"version": 1, "records": {first.identity.key: first.to_dict(), second.identity.key: second.to_dict()}}
    )

    with pytest.raises(ValueError, match="single unresolved"):
        dispatch_state_module._read_store(content)


def test_rejects_unresolved_record_when_it_is_not_latest() -> None:
    first = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state(
        "reserved",
        marker_comment_id=3,
    )
    second = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 2)).with_state(
        "abandoned",
        reason="done",
        evidence={"operation": "dispatch"},
    )
    content = json.dumps(
        {"version": 1, "records": {first.identity.key: first.to_dict(), second.identity.key: second.to_dict()}}
    )

    with pytest.raises(ValueError, match="latest ordinal"):
        dispatch_state_module._read_store(content)

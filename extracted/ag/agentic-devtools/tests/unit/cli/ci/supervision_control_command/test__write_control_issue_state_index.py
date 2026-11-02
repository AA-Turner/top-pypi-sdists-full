"""Tests for the _write_control_issue_state_index symbol."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.cli.ci.supervision_control import (
    CONTROL_MARKER,
    IGNORE_LABEL,
    SUPERVISED_LABEL,
    Checkpoint,
    HoldReceipt,
    QuarantineReceipt,
    SupervisionControl,
)
from agentic_devtools.cli.ci.supervision_control_command import (
    CONTROL_STATE_INDEX_MARKER,
    CONTROL_STATE_INDEX_MAX_COMMENT_CHARS,
    OPERATION_RECEIPT_MARKER,
    _write_control_issue_state_index,
    find_latest_quarantine_owner_key,
    hold_receipt_to_json,
    quarantine_receipt_to_json,
)


def _decode_state_index_body(body: str) -> dict[str, object]:
    from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment

    normalized = normalize_ai_pr_loop_comment(body)
    assert normalized is not None
    return json.loads(normalized.split("\n", 1)[1])


def _record(key: str, operation: str, receipt: dict[str, object], *, completed: bool = False) -> str:
    raw: dict[str, object] = {
        "idempotency_key": key,
        "operation": operation,
        "receipt": receipt,
    }
    if completed:
        raw["completed"] = True
    return f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(raw)


def test_write_control_issue_state_index_compacts_history_and_keeps_active_receipts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    control = SupervisionControl()
    active_quarantine = _record(
        "active:q",
        "quarantine",
        quarantine_receipt_to_json(QuarantineReceipt("active", (7,), {7: "head-7"}, (7,))),
        completed=True,
    )
    completed_quarantine = _record(
        "done:q",
        "quarantine",
        quarantine_receipt_to_json(QuarantineReceipt("done", (8,), {8: "head-8"}, (8,))),
    )
    completed_restore = _record(
        "done:q:restore",
        "restore-prs",
        {"run_id": "done", "quarantine_key": "done:q", "changed": [8]},
        completed=True,
    )
    active_hold = _record(
        "active:hold",
        "hold",
        hold_receipt_to_json(HoldReceipt("active", ("loop.yml",), {"loop.yml": True})),
    )
    completed_hold = _record(
        "done:hold",
        "hold",
        hold_receipt_to_json(HoldReceipt("done", ("loop.yml",), {"loop.yml": True})),
    )
    completed_resume = _record(
        "done:resume",
        "resume",
        {"run_id": "done", "hold_key": "done:hold", "states": {"loop.yml": True}},
        completed=True,
    )
    pending_restore = _record(
        "pending:q:restore",
        "restore-prs",
        {"run_id": "pending", "quarantine_key": "pending:q", "changed": [10]},
    )
    pending_resume = _record(
        "pending:resume",
        "resume",
        {"run_id": "pending", "hold_key": "pending:hold", "states": {"loop.yml": True}},
    )
    ensure_receipt = {
        "labels_created": [IGNORE_LABEL],
        "labels_reused": [SUPERVISED_LABEL],
        "control_issue": 42,
        "control_issue_created": False,
    }
    ensure_records = [_record(f"ensure:{index}", "ensure-labels", ensure_receipt) for index in range(101)]
    recent_restore = _record(
        "new:q:restore",
        "restore-prs",
        {"run_id": "new", "quarantine_key": "new:q", "changed": [9]},
    )
    recent_resume = _record(
        "new:resume",
        "resume",
        {"run_id": "new", "hold_key": "new:hold", "states": {"loop.yml": True}},
    )
    old_checkpoint = control.encode_checkpoint(Checkpoint("old", {"status": "old"}, "owner/repo"))
    latest_checkpoint = control.encode_checkpoint(Checkpoint("new", {"status": "latest"}, "owner/repo"))
    other_repository_checkpoint = control.encode_checkpoint(Checkpoint("other", {}, "other/repo"))
    captured: dict[str, object] = {}
    gh_text_calls: list[list[str]] = []

    def write_comment(arguments: list[str]) -> str:
        gh_text_calls.append(arguments)
        body = arguments[arguments.index("--body") + 1]
        captured["entries"] = _decode_state_index_body(body)["entries"]
        return ""

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", write_comment)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
        lambda *_args: captured.get("entries", []),
    )

    result = _write_control_issue_state_index(
        "owner/repo",
        42,
        "automation",
        control,
        [
            active_quarantine,
            completed_quarantine,
            completed_restore,
            active_hold,
            completed_hold,
            completed_resume,
            pending_restore,
            pending_resume,
            *ensure_records,
            recent_restore,
            recent_resume,
            old_checkpoint,
            latest_checkpoint,
            other_repository_checkpoint,
            f"{CONTROL_MARKER}\nnot-json",
            "unrecognized comment",
        ],
    )

    entries = captured["entries"]
    assert result == entries
    assert active_quarantine in entries
    assert active_hold in entries
    assert completed_quarantine not in entries
    assert completed_restore not in entries
    assert completed_hold not in entries
    assert completed_resume not in entries
    assert pending_restore in entries
    assert pending_resume in entries
    assert ensure_records[0] not in entries
    assert ensure_records[-1] in entries
    assert recent_restore in entries
    assert recent_resume in entries
    assert old_checkpoint not in entries
    assert latest_checkpoint in entries
    assert len(gh_text_calls) == 1
    assert gh_text_calls[0][:5] == ["issue", "comment", "42", "--repo", "owner/repo"]
    assert gh_text_calls[0][gh_text_calls[0].index("--body") + 1].startswith(f"{CONTROL_STATE_INDEX_MARKER}\n")


def test_write_control_issue_state_index_drops_superseded_restored_quarantines(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    control = SupervisionControl()
    old_quarantine = _record(
        "old:q",
        "quarantine",
        quarantine_receipt_to_json(QuarantineReceipt("old", (7, 8), {7: "head-7", 8: "head-8"}, (7, 8))),
        completed=True,
    )
    new_quarantine = _record(
        "new:q",
        "quarantine",
        quarantine_receipt_to_json(QuarantineReceipt("new", (7,), {7: "head-7"}, (7,))),
        completed=True,
    )
    quarantine_without_owned_heads = _record(
        "no-owned-heads:q",
        "quarantine",
        quarantine_receipt_to_json(QuarantineReceipt("no-owned-heads", (9,), {9: "head-9"}, ())),
        completed=True,
    )
    completed_restore = _record(
        "new:q:restore",
        "restore-prs",
        {"run_id": "new", "quarantine_key": "new:q", "changed": [7]},
        completed=True,
    )
    ensure_receipt = {
        "labels_created": [IGNORE_LABEL],
        "labels_reused": [SUPERVISED_LABEL],
        "control_issue": 42,
        "control_issue_created": False,
    }
    later_records = [_record(f"ensure:{index}", "ensure-labels", ensure_receipt) for index in range(101)]
    captured: dict[str, object] = {}

    def write_comment(arguments: list[str]) -> str:
        captured["entries"] = _decode_state_index_body(arguments[arguments.index("--body") + 1])["entries"]
        return ""

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", write_comment)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
        lambda *_args: captured.get("entries", []),
    )

    entries = _write_control_issue_state_index(
        "owner/repo",
        42,
        "automation",
        control,
        [old_quarantine, new_quarantine, quarantine_without_owned_heads, completed_restore, *later_records],
    )

    assert old_quarantine in entries
    assert new_quarantine in entries
    assert quarantine_without_owned_heads not in entries
    assert completed_restore in entries
    assert find_latest_quarantine_owner_key(control, entries, 7, "head-7") == "new:q"
    assert find_latest_quarantine_owner_key(control, entries, 8, "head-8") == "old:q"


def test_write_control_issue_state_index_rejects_unexpected_quarantine_receipt_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    quarantine = _record(
        "quarantine",
        "quarantine",
        quarantine_receipt_to_json(QuarantineReceipt("run", (7,), {7: "head-7"}, (7,))),
        completed=True,
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command.find_operation_receipt",
        lambda *_args: {},
    )

    with pytest.raises(RuntimeError, match="stored quarantine receipt is malformed"):
        _write_control_issue_state_index("owner/repo", 42, "automation", SupervisionControl(), [quarantine])


def test_write_control_issue_state_index_shards_large_active_receipts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    control = SupervisionControl()
    records = [
        _record(
            f"active:{index}",
            "quarantine",
            quarantine_receipt_to_json(
                QuarantineReceipt(f"run-{index}", (index + 1,), {index + 1: f"head-{index}"}, (index + 1,))
            ),
            completed=True,
        )
        for index in range(500)
    ]
    written_bodies: list[str] = []
    captured_entries: list[str] = []

    def write_comment(arguments: list[str]) -> str:
        body = arguments[arguments.index("--body") + 1]
        written_bodies.append(body)
        entries = _decode_state_index_body(body)["entries"]
        assert isinstance(entries, list)
        assert all(isinstance(entry, str) for entry in entries)
        captured_entries.extend(entry for entry in entries if isinstance(entry, str))
        return ""

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", write_comment)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
        lambda *_args: captured_entries,
    )

    result = _write_control_issue_state_index("owner/repo", 42, "automation", control, records)

    assert result == records
    assert len(written_bodies) > 1
    assert all(len(body) <= CONTROL_STATE_INDEX_MAX_COMMENT_CHARS for body in written_bodies)
    assert all(record in result for record in records)


@pytest.mark.parametrize("preceding_small_record", [False, True])
def test_write_control_issue_state_index_rejects_an_oversized_single_entry(
    preceding_small_record: bool,
) -> None:
    records = []
    if preceding_small_record:
        records.append(
            _record(
                "small",
                "quarantine",
                quarantine_receipt_to_json(QuarantineReceipt("small", (), {}, ())),
            )
        )
    records.append(
        _record(
            "large",
            "quarantine",
            quarantine_receipt_to_json(QuarantineReceipt("r" * 60_500, (), {}, ())),
        )
    )

    with pytest.raises(RuntimeError, match="entry exceeds the comment size limit"):
        _write_control_issue_state_index("owner/repo", 42, "automation", SupervisionControl(), records)


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (f"{OPERATION_RECEIPT_MARKER}\nnot-json", "JSON is invalid"),
        (f"{OPERATION_RECEIPT_MARKER}\n{{}}", "receipt is malformed"),
    ],
)
def test_write_control_issue_state_index_rejects_malformed_receipts(
    body: str,
    message: str,
) -> None:
    with pytest.raises(RuntimeError, match=message):
        _write_control_issue_state_index("owner/repo", 42, "automation", SupervisionControl(), [body])


def test_write_control_issue_state_index_rejects_a_read_back_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", lambda _args: "")
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
        lambda *_args: ["unexpected"],
    )

    with pytest.raises(RuntimeError, match="read-back mismatch"):
        _write_control_issue_state_index("owner/repo", 42, "automation", SupervisionControl(), [])


def test_write_control_issue_state_index_merges_receipt_added_concurrently(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    control = SupervisionControl()
    stale_receipt = _record(
        "stale",
        "ensure-labels",
        {
            "labels_created": [],
            "labels_reused": [IGNORE_LABEL, SUPERVISED_LABEL],
            "control_issue": 42,
            "control_issue_created": False,
        },
    )
    concurrent_receipt = _record(
        "concurrent",
        "ensure-labels",
        {
            "labels_created": [],
            "labels_reused": [IGNORE_LABEL, SUPERVISED_LABEL],
            "control_issue": 42,
            "control_issue_created": False,
        },
    )
    observed: list[list[str]] = []
    writes: list[list[str]] = []
    read_count = 0

    def read_comments(*_args: object) -> list[str]:
        nonlocal read_count
        read_count += 1
        if read_count == 1:
            return [concurrent_receipt]
        if writes:
            return observed[-1]
        return [concurrent_receipt]

    def write_comment(arguments: list[str]) -> str:
        writes.append(arguments)
        entries = _decode_state_index_body(arguments[arguments.index("--body") + 1])["entries"]
        assert isinstance(entries, list)
        assert all(isinstance(entry, str) for entry in entries)
        observed.append([entry for entry in entries if isinstance(entry, str)])
        return ""

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", write_comment)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
        read_comments,
    )

    result = _write_control_issue_state_index(
        "owner/repo",
        42,
        "automation",
        control,
        [stale_receipt],
    )

    assert stale_receipt in result
    assert concurrent_receipt in result
    assert len(writes) == 1


def test_write_control_issue_state_index_fails_after_repeated_concurrent_updates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = {
        "labels_created": [],
        "labels_reused": [IGNORE_LABEL, SUPERVISED_LABEL],
        "control_issue": 42,
        "control_issue_created": False,
    }
    reads = 0

    def read_comments(*_args: object) -> list[str]:
        nonlocal reads
        reads += 1
        return [_record(f"concurrent-{reads}", "ensure-labels", receipt)]

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
        read_comments,
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh_text",
        lambda _arguments: pytest.fail("index must not publish after repeated concurrent changes"),
    )

    with pytest.raises(RuntimeError, match="changed repeatedly during index update"):
        _write_control_issue_state_index("owner/repo", 42, "automation", SupervisionControl(), [])

    assert reads == 4

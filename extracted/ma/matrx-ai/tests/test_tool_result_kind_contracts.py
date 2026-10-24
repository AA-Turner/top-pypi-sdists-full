"""Dry-run exact contracts for proposed desktop and data-fetch tool results."""

import pytest
from matrx_graph.content_ir.sdk import kind_catalog
from pydantic import ValidationError

from matrx_ai.tools.kinds.data_fetch import DataFetchNotStarted
from matrx_ai.tools.kinds.desktop import (
    DesktopClipboardReadResult,
    DesktopClipboardWriteResult,
    DesktopProcessKillResult,
    DesktopProcessListResult,
    DesktopProcessPortsResult,
    DesktopTranscribeResult,
)


@pytest.mark.parametrize(
    ("model", "payload", "kind"),
    [
        (
            DesktopTranscribeResult,
            {
                "text": "hello", "language": "en", "duration_s": 1.0, "model": "whisper",
                "elapsed_ms": 100, "segments": [{"start_s": 0.0, "end_s": 1.0, "text": "hello"}],
                "segments_total": 1, "path": "/tmp/a.wav",
            },
            "desktop_transcribe_result",
        ),
        (
            DesktopProcessListResult,
            {
                "action": "list",
                "processes": [{"pid": 10, "ppid": None, "name": "editor", "command": "editor", "cpu_percent": None, "memory_bytes": None, "user": None}],
                "total": 1, "truncated": False,
            },
            "desktop_process_list_result",
        ),
        (DesktopProcessPortsResult, {"action": "ports", "ports": [{"port": 443, "protocol": "tcp", "address": "127.0.0.1", "pid": None, "process": None}]}, "desktop_process_ports_result"),
        (DesktopProcessKillResult, {"action": "kill", "pid": 10, "signal": "SIGTERM", "exited": True}, "desktop_process_kill_result"),
        (DesktopClipboardReadResult, {"action": "read", "text": "copied", "truncated": False}, "desktop_clipboard_read_result"),
        (DesktopClipboardWriteResult, {"action": "write", "bytes": 6}, "desktop_clipboard_write_result"),
    ],
)
def test_desktop_contract_roundtrip_preserves_the_supplied_fields(model, payload, kind):
    wire = {"__kind": kind, **payload}
    validated = model.model_validate(wire)
    assert validated.model_dump(mode="json", by_alias=True, exclude_unset=True) == wire


@pytest.mark.parametrize(
    ("model", "payload"),
    [
        (DesktopProcessListResult, {"action": "ports", "processes": [], "total": 0, "truncated": False}),
        (DesktopProcessKillResult, {"action": "kill", "pid": 10, "signal": "SIGUSR1", "exited": True}),
    ],
)
def test_desktop_contracts_reject_mismatched_variants_and_signals(model, payload):
    with pytest.raises(ValidationError):
        model.model_validate(payload)


def test_transcription_projection_enforces_protocol_constraints_and_producer_truncation():
    valid = {
        "text": "hello", "language": "en", "duration_s": 1.0, "model": "whisper-small",
        "elapsed_ms": 1, "segments": [{"start_s": 0.0, "end_s": 1.0, "text": "hello"}],
        "segments_total": 1, "path": "/tmp/a.wav",
    }
    assert DesktopTranscribeResult.model_validate({"__kind": "desktop_transcribe_result", **valid})
    invalid = [
        {**valid, "text": "x" * 400_001},
        {**valid, "language": None},
        {**valid, "language": "x" * 9},
        {**valid, "duration_s": -0.1},
        {**valid, "model": "Bad Model"},
        {**valid, "model": "x" * 129},
        {**valid, "elapsed_ms": -1},
        {**valid, "segments": [{"start_s": 0.0, "end_s": 1.0, "text": "x" * 4_001}]},
        {**valid, "segments": [{"start_s": -0.1, "end_s": 1.0, "text": "x"}]},
        {**valid, "segments": [{"start_s": 0.0, "end_s": -0.1, "text": "x"}]},
        {**valid, "segments": [{"start_s": 0.0, "end_s": 1.0, "text": "x"}] * 201},
        {**valid, "segments_total": -1},
        {**valid, "segments_total": 20_001},
        {**valid, "path": ""},
        {**valid, "path": "relative/audio.wav"},
    ]
    for payload in invalid:
        with pytest.raises(ValidationError):
            DesktopTranscribeResult.model_validate({"__kind": "desktop_transcribe_result", **payload})


def test_process_and_port_contracts_enforce_generated_numeric_and_string_bounds():
    process = {
        "pid": 10, "ppid": None, "name": "editor", "command": "editor", "cpu_percent": None,
        "memory_bytes": None, "user": None,
    }
    valid_list = {"__kind": "desktop_process_list_result", "action": "list", "processes": [process], "total": 1, "truncated": False}
    assert DesktopProcessListResult.model_validate(valid_list)
    for field, value in (("pid", -1), ("ppid", -1), ("cpu_percent", -0.1), ("memory_bytes", -1), ("user", "u" * 129), ("name", "n" * 257), ("command", "c" * 1_025)):
        with pytest.raises(ValidationError):
            DesktopProcessListResult.model_validate({**valid_list, "processes": [{**process, field: value}]})
    with pytest.raises(ValidationError):
        DesktopProcessListResult.model_validate({**valid_list, "total": -1})

    port = {"action": "ports", "ports": [{"port": 443, "protocol": "tcp", "address": "127.0.0.1", "pid": 10, "process": "editor"}]}
    assert DesktopProcessPortsResult.model_validate({"__kind": "desktop_process_ports_result", **port})
    for field, value in (("port", 0), ("port", 65_536), ("address", "a" * 65), ("pid", -1), ("process", "p" * 257)):
        invalid_port = {**port, "ports": [{**port["ports"][0], field: value}]}
        with pytest.raises(ValidationError):
            DesktopProcessPortsResult.model_validate({"__kind": "desktop_process_ports_result", **invalid_port})


def test_kill_and_clipboard_write_contracts_enforce_protocol_bounds():
    for pid in (0, 9_007_199_254_740_992):
        with pytest.raises(ValidationError):
            DesktopProcessKillResult.model_validate(
                {"__kind": "desktop_process_kill_result", "action": "kill", "pid": pid, "signal": "SIGTERM", "exited": True}
            )
    with pytest.raises(ValidationError):
        DesktopClipboardWriteResult.model_validate(
            {"__kind": "desktop_clipboard_write_result", "action": "write", "bytes": -1}
        )
    with pytest.raises(ValidationError):
        DesktopClipboardWriteResult.model_validate(
            {"__kind": "desktop_clipboard_write_result", "action": "write", "bytes": 9_007_199_254_740_992}
        )


def test_data_fetch_not_started_receipt_has_exact_status_and_fields():
    payload = {"__kind": "data_fetch_not_started", "status": "not_started", "message": "Not started in chat."}
    validated = DataFetchNotStarted.model_validate(payload)
    assert validated.model_dump(mode="json", by_alias=True, exclude_unset=True) == payload
    with pytest.raises(ValidationError):
        DataFetchNotStarted.model_validate({**payload, "status": "started"})
    assert kind_catalog()["data_fetch_not_started"].disposition == "envelope"

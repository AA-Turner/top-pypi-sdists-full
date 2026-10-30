# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for how `ExecutionResult` reads a run's output."""

from __future__ import annotations

import json
import tracemalloc
from dataclasses import asdict
from pathlib import Path

import pytest
from airbyte_protocol.models import Type as AirbyteMessageType

from airbyte_ops_mcp.regression_tests.models import (
    MAX_ANALYTICS_TYPES,
    Command,
    ComparableOutputs,
    ConnectorUnderTest,
    ExecutionResult,
    TargetOrControl,
    split_records_per_stream,
)

pytestmark = pytest.mark.unit


def _result(stdout: Path, command: Command = Command.READ) -> ExecutionResult:
    return ExecutionResult(
        connector_under_test=ConnectorUnderTest(
            image_name="airbyte/source-test:1.0.0",
            target_or_control=TargetOrControl.TARGET,
        ),
        command=command,
        stdout_file_path=stdout,
        stderr_file_path=stdout.parent / "stderr.txt",
        success=True,
        exit_code=0,
    )


def _state(stream: str, cursor: int) -> dict:
    return {
        "type": "STATE",
        "state": {
            "type": "STREAM",
            "stream": {
                "stream_descriptor": {"name": stream},
                "stream_state": {"cursor": cursor},
            },
        },
    }


def _analytics(type_: str, value: str | None) -> dict:
    """One analytics message, shaped as the CDK writes it to stdout."""
    return {
        "type": "TRACE",
        "trace": {
            "type": "ANALYTICS",
            "emitted_at": 1,
            "analytics": {"type": type_, "value": value},
        },
    }


def test_read_stream_statuses_and_errors_are_bounded_and_public_only(
    tmp_path: Path,
) -> None:
    stdout = tmp_path / "stdout.txt"
    messages = [
        {
            "type": "TRACE",
            "trace": {
                "type": "STREAM_STATUS",
                "emitted_at": index,
                "stream_status": {
                    "stream_descriptor": {"name": "new"},
                    "status": "INCOMPLETE",
                },
            },
        }
        for index in range(17)
    ]
    messages.extend(
        {
            "type": "TRACE",
            "trace": {
                "type": "ERROR",
                "emitted_at": index,
                "error": {
                    "failure_type": "config_error",
                    "stream_descriptor": {"name": "new"},
                    "message": "x" * 600,
                    "internal_message": "SECRET_INTERNAL",
                    "stack_trace": "SECRET_STACK",
                },
            },
        }
        for index in range(6)
    )
    stdout.write_text("\n".join(json.dumps(message) for message in messages))

    result = _result(stdout)
    comparable = ComparableOutputs.from_execution_result(result)

    assert len(comparable.stream_statuses["new"]) == 16
    assert len(comparable.stream_errors["new"]) == 5
    assert len(comparable.stream_errors["new"][0].message) == 200
    serialized = json.dumps(asdict(comparable))
    assert "SECRET_INTERNAL" not in serialized
    assert "SECRET_STACK" not in serialized
    assert comparable.stream_statuses == result.get_stream_statuses()
    assert (
        ComparableOutputs.from_execution_result(
            _result(stdout, Command.CHECK)
        ).stream_errors
        is None
    )


def _write_large_read(stdout: Path, records: int) -> None:
    """A read of `records` records of a few KB each, with checkpoints between."""
    body = "x" * 2000
    with stdout.open("w") as out:
        for index in range(records):
            stream = "users" if index % 2 else "events"
            out.write(
                json.dumps(
                    {
                        "type": "RECORD",
                        "record": {
                            "stream": stream,
                            "data": {
                                "id": index,
                                "body": body,
                                "tags": list(range(40)),
                            },
                            "emitted_at": index,
                        },
                    }
                )
                + "\n"
            )
            if index % 1000 == 999:
                out.write(json.dumps(_state("users", index)) + "\n")
                out.write(json.dumps(_state("events", index - 1)) + "\n")


def test_artifacts_and_summary_do_not_hold_the_output_in_memory(tmp_path: Path) -> None:
    """Peak memory must stay flat however large the read is.

    The old path held stdout as one string, as a list of lines, as parsed
    messages and as per-type lists of their JSON -- four copies -- and a cold
    PayPal read was OOM-killed twice before a single artifact was written. The
    bound here is a quarter of the file, which the old path exceeded by itself
    on the first copy; a flat implementation lands well under it.
    """
    stdout = tmp_path / "stdout.txt"
    _write_large_read(stdout, records=20_000)
    size = stdout.stat().st_size
    assert size > 40 * 1024 * 1024
    result = _result(stdout)

    tracemalloc.start()
    try:
        result.save_artifacts(tmp_path / "artifacts")
        counts = result.get_message_count_per_type()
        per_stream = result.get_record_count_per_stream()
        outputs = ComparableOutputs.from_execution_result(result)
        _current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    assert peak < size // 4
    assert peak < 16 * 1024 * 1024
    assert counts == {AirbyteMessageType.RECORD: 20_000, AirbyteMessageType.STATE: 40}
    assert per_stream == {"users": 10_000, "events": 10_000}
    assert outputs.final_states == {
        (None, "users"): {"cursor": 19_999},
        (None, "events"): {"cursor": 19_998},
    }
    assert (
        tmp_path / "artifacts" / "airbyte_messages" / "record.jsonl"
    ).stat().st_size > 0


def test_save_artifacts_answers_every_later_question_from_its_own_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    stdout = tmp_path / "stdout.txt"
    stdout.write_text(
        "\n".join(
            json.dumps(message)
            for message in (
                {
                    "type": "RECORD",
                    "record": {"stream": "users", "data": {"id": 1}, "emitted_at": 1},
                },
                _state("users", 1),
                {"type": "LOG", "log": {"level": "INFO", "message": "bye"}},
                _analytics("http-request-count", "40"),
            )
        )
    )
    result = _result(stdout)
    opened = 0
    real_open = Path.open

    def _counting_open(self: Path, *args, **kwargs):
        nonlocal opened
        if self == stdout:
            opened += 1
        return real_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", _counting_open)

    result.save_artifacts(tmp_path / "artifacts")
    result.get_message_count_per_type()
    result.get_record_count_per_stream()
    result.get_final_state_per_stream()
    ComparableOutputs.from_execution_result(result)

    assert result.summary.analytics == {"http-request-count": "40"}
    assert opened == 1


def test_the_summary_keeps_the_last_value_of_each_analytics_counter(
    tmp_path: Path,
) -> None:
    """As the protocol carries it: a string, or `None` for a message without one.

    The CDK emits each counter once, in its entrypoint's `finally`; a run that
    somehow emitted two has only one pair that saw the whole run. Turning the
    string into a number is the reader's job, so a value that is not one is
    kept rather than dropped or zeroed here. A handful of types, well under
    the cap, so every one of them is kept.
    """
    stdout = tmp_path / "stdout.txt"
    stdout.write_text(
        "\n".join(
            json.dumps(message)
            for message in (
                _analytics("http-request-count", "5"),
                _analytics("file-cdk-csv-stream-count", "3"),
                _analytics("http-request-count", "50"),
                _analytics("http-cache-hit-count", None),
                {"type": "TRACE", "trace": {"type": "ERROR", "emitted_at": 1}},
            )
        )
    )

    assert _result(stdout).summary.analytics == {
        "http-request-count": "50",
        "file-cdk-csv-stream-count": "3",
        "http-cache-hit-count": None,
    }


def test_the_summary_keeps_a_bounded_number_of_analytics_types(
    tmp_path: Path,
) -> None:
    """A connector minting an analytics type per page must not grow the summary.

    The first `MAX_ANALYTICS_TYPES` distinct types are kept and still updated;
    a type past the cap is dropped. Bounded memory is the property the summary
    promises, and a run that floods the cap before its counters arrive reads as
    "not reported" rather than growing with the read.
    """
    stdout = tmp_path / "stdout.txt"
    stdout.write_text(
        "\n".join(
            json.dumps(message)
            for message in (
                *(
                    _analytics(f"page-{n}-rows", "1")
                    for n in range(MAX_ANALYTICS_TYPES)
                ),
                _analytics(f"page-{MAX_ANALYTICS_TYPES}-rows", "1"),
                _analytics("page-0-rows", "2"),
            )
        )
    )

    analytics = _result(stdout).summary.analytics

    assert len(analytics) == MAX_ANALYTICS_TYPES
    assert f"page-{MAX_ANALYTICS_TYPES}-rows" not in analytics
    assert analytics["page-0-rows"] == "2"


def test_messages_are_parsed_on_demand_and_never_kept(tmp_path: Path) -> None:
    stdout = tmp_path / "stdout.txt"
    stdout.write_text(
        json.dumps(
            {
                "type": "RECORD",
                "record": {"stream": "users", "data": {"id": 1}, "emitted_at": 1},
            }
        )
        + "\nnot a message\n\n"
        + json.dumps(
            {
                "type": "RECORD",
                "record": {"stream": "users", "data": {"id": 2}, "emitted_at": 2},
            }
        )
    )
    result = _result(stdout)

    first_pass = [message.record.data["id"] for message in result.get_records()]
    second_pass = [message.record.data["id"] for message in result.get_records()]

    assert first_pass == second_pass == [1, 2]
    assert result._summary is None


def test_the_first_spec_catalog_and_status_win(tmp_path: Path) -> None:
    stdout = tmp_path / "stdout.txt"
    stdout.write_text(
        "\n".join(
            json.dumps(message)
            for message in (
                {
                    "type": "CONNECTION_STATUS",
                    "connectionStatus": {"status": "SUCCEEDED"},
                },
                {"type": "CONNECTION_STATUS", "connectionStatus": {"status": "FAILED"}},
                {
                    "type": "CATALOG",
                    "catalog": {
                        "streams": [
                            {
                                "name": "first",
                                "json_schema": {},
                                "supported_sync_modes": ["full_refresh"],
                            }
                        ]
                    },
                },
                {
                    "type": "CATALOG",
                    "catalog": {
                        "streams": [
                            {
                                "name": "second",
                                "json_schema": {},
                                "supported_sync_modes": ["full_refresh"],
                            }
                        ]
                    },
                },
                {
                    "type": "SPEC",
                    "spec": {"connectionSpecification": {"title": "first"}},
                },
                {
                    "type": "SPEC",
                    "spec": {"connectionSpecification": {"title": "second"}},
                },
            )
        )
    )
    result = _result(stdout, command=Command.CHECK)

    assert result.is_check_successful() is True
    assert result.get_connection_status().status.value == "SUCCEEDED"
    assert [stream.name for stream in result.get_catalog().streams] == ["first"]
    assert result.get_spec().connectionSpecification == {"title": "first"}


def test_a_stdout_tail_cut_mid_character_is_skipped_not_fatal(tmp_path: Path) -> None:
    """A deadline kill can land inside a multi-byte character.

    Both readers decode the file in text mode; left strict, the iteration
    itself raises on the truncated sequence, outside the per-line handling,
    and the CLI dies with no report and no `incomplete` output.
    """
    stdout = tmp_path / "stdout.txt"
    whole = b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 1}, "emitted_at": 1}}\n'
    cut = b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 2, "name": "\xe2\x82'
    stdout.write_bytes(whole + cut)
    result = _result(stdout)

    result.save_artifacts(tmp_path / "artifacts")

    assert result.get_record_count_per_stream() == {"users": 1}
    assert result.get_message_count_per_type() == {AirbyteMessageType.RECORD: 1}
    assert [message.record.data["id"] for message in result.get_records()] == [1]
    record_file = tmp_path / "artifacts" / "airbyte_messages" / "record.jsonl"
    assert record_file.read_text().count("\n") == 0
    assert '"id":1' in record_file.read_text()
    per_stream = split_records_per_stream(stdout)
    assert per_stream["users"].read_bytes().count(b"\n") == 1

from datetime import datetime, timezone

import pytest
from isolate.backends.settings import IsolateSettings
from isolate.common import timestamp
from isolate.connections.grpc import definitions
from isolate.logs import Log, LogLevel, LogSource


def test_log_default_timestamp():
    log = Log(message="message", source=LogSource.USER, level=LogLevel.DEBUG)
    assert log.timestamp is not None
    assert log.timestamp <= datetime.now(timezone.utc)


def test_timestamp_conversion():
    now = datetime.now(timezone.utc)
    now_timestamp = timestamp.from_datetime(now)
    assert now_timestamp.ToMilliseconds() == int(now.timestamp() * 1000.0)


def test_level_gt_comparison():
    assert LogLevel.INFO > LogLevel.DEBUG


def test_level_lt_comparison():
    assert LogLevel.WARNING < LogLevel.ERROR


def test_level_str():
    assert str(LogLevel.INFO) == "info"


def test_log_definition_conversion():
    message = definitions.Log(message="message", source=0, level=3)
    level_definition = definitions.LogLevel.Name(message.level)
    assert LogLevel[level_definition.upper()] == LogLevel.WARNING


def test_json_logs():
    log = Log(
        message='{"line": "This is a log line", "user_id": 123, "task": "test"}',
        source=LogSource.USER,
        level=LogLevel.INFO,
        is_json=True,
    )
    assert log.message_str() == "This is a log line"
    meta = log.message_meta()
    assert meta["user_id"] == 123
    assert meta["task"] == "test"
    assert "line" not in meta

    # Ensure metatada didn't modify the original message
    assert log.message_str() == "This is a log line"

    non_json_log = Log(
        message="This is a plain log line",
        source=LogSource.USER,
        level=LogLevel.INFO,
        is_json=False,
    )
    assert non_json_log.message_str() == "This is a plain log line"
    meta = non_json_log.message_meta()
    assert meta == {}

    malformed_json_log = Log(
        # Missing closing brace
        message='{"line": "This is a line", "user_id": 123, "task": "test"',
        source=LogSource.USER,
        level=LogLevel.INFO,
        is_json=True,
    )
    assert (
        malformed_json_log.message_str()
        == '{"line": "This is a line", "user_id": 123, "task": "test"'
    )
    meta = malformed_json_log.message_meta()
    assert meta == {}


@pytest.mark.parametrize(
    ("message", "expected_level"),
    [
        ('{"event": "failed", "level": "error"}', LogLevel.ERROR),
        ('{"event": "slow", "level": "warn"}', LogLevel.WARNING),
        ('{"event": "slow", "levelname": "WARNING"}', LogLevel.WARNING),
        ('{"event": "details", "severity": "debug"}', LogLevel.DEBUG),
        ('{"event": "details", "severity": " trace "}', LogLevel.TRACE),
        ('  {"event": "ready", "level": "info"}', LogLevel.INFO),
        ('{"event": "contains [error] text", "level": "info"}', LogLevel.INFO),
    ],
)
def test_infer_structured_log_level(message, expected_level):
    settings = IsolateSettings()
    log = Log(message=message, source=LogSource.USER, level=LogLevel.STDOUT)

    assert settings._infer_log_level(log).level == expected_level


def test_infer_structured_log_level_from_json_transport():
    settings = IsolateSettings()
    log = Log(
        message=(
            '{"line": "{\\"event\\": \\"failed\\", \\"level\\": \\"error\\"}", '
            '"trace_id": "trace-1"}'
        ),
        source=LogSource.USER,
        level=LogLevel.STDOUT,
        is_json=True,
    )

    assert settings._infer_log_level(log).level == LogLevel.ERROR


@pytest.mark.parametrize(
    "message",
    [
        '{"event": "failed", "error": "boom"}',
        '{"event": "failed", "level": "verbose"}',
        '{"event": "failed", "level": 40}',
        '{"event": "failed", "level": {"name": "error"}}',
        '{"event": "failed", "level": "error"',
        '[{"level": "error"}]',
    ],
)
def test_unrecognized_structured_log_level_defaults_to_info(message):
    settings = IsolateSettings()
    log = Log(message=message, source=LogSource.USER, level=LogLevel.STDERR)

    assert settings._infer_log_level(log).level == LogLevel.INFO


@pytest.mark.parametrize("error", [ValueError, RecursionError])
def test_structured_log_level_parse_failure_defaults_to_info(monkeypatch, error):
    def raise_parse_error(_):
        raise error

    monkeypatch.setattr("isolate.backends.settings.json.loads", raise_parse_error)
    settings = IsolateSettings()
    log = Log(
        message='{"event": "failed", "level": "error"}',
        source=LogSource.USER,
        level=LogLevel.STDOUT,
    )

    assert settings._infer_log_level(log).level == LogLevel.INFO


def test_text_log_level_preserves_error_first_precedence():
    settings = IsolateSettings()
    log = Log(
        message="info started [error] failed",
        source=LogSource.USER,
        level=LogLevel.STDOUT,
    )

    assert settings._infer_log_level(log).level == LogLevel.ERROR


def test_explicit_log_level_is_not_inferred():
    settings = IsolateSettings()
    log = Log(
        message='{"event": "failed", "level": "error"}',
        source=LogSource.USER,
        level=LogLevel.WARNING,
    )

    assert settings._infer_log_level(log) is log

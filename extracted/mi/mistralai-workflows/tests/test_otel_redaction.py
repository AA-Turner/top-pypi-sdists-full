import ctypes
import json
import logging
import threading
import time
from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock

import pytest
import structlog
from mistralai.extra.observability import DEFAULT_REDACTED_VALUE, RedactingSpanExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import InMemoryLogRecordExporter, SimpleLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from mistralai.workflows import client as client_module
from mistralai.workflows.core.config.config import OtelRedactionMode
from mistralai.workflows.core.logging import LogFormat, LogLevel, build_json_log_formatter, setup_logging
from mistralai.workflows.core.tracing._otel_config import (
    _apply_span_redaction,
    _LogBodyRedactor,
    _StructlogAwareLoggingHandler,
)

_SENSITIVE_KEY = "gen_ai.input.messages"
_SAFE_KEY = "gen_ai.request.model"
_SECRET = "Bearer sk-abcdefghijklmnopqrstuvwx"


def _export_span_through(mode: OtelRedactionMode, attributes: dict[str, str] | None = None) -> dict[str, object]:
    memory = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(_apply_span_redaction(memory, mode)))

    tracer = provider.get_tracer(__name__)
    span = tracer.start_span("chat")
    span.set_attributes(attributes or {_SENSITIVE_KEY: f"question {_SECRET}", _SAFE_KEY: "mistral-large"})
    span.end()
    provider.force_flush()

    finished = memory.get_finished_spans()
    assert len(finished) == 1
    return dict(finished[0].attributes or {})


class TestApplySpanRedaction:
    def test_none_returns_exporter_unwrapped(self) -> None:
        exporter = InMemorySpanExporter()
        assert _apply_span_redaction(exporter, OtelRedactionMode.NONE) is exporter

    @pytest.mark.parametrize("mode", [OtelRedactionMode.DEFAULT, OtelRedactionMode.STRICT])
    def test_non_none_wraps_with_redacting_exporter(self, mode: OtelRedactionMode) -> None:
        wrapped = _apply_span_redaction(InMemorySpanExporter(), mode)
        assert isinstance(wrapped, RedactingSpanExporter)


class TestRedactionBehavior:
    def test_none_leaves_attributes_intact(self) -> None:
        attributes = _export_span_through(OtelRedactionMode.NONE)
        assert attributes[_SENSITIVE_KEY] == f"question {_SECRET}"
        assert attributes[_SAFE_KEY] == "mistral-large"

    def test_default_scrubs_secret_but_keeps_key_and_structure(self) -> None:
        attributes = _export_span_through(OtelRedactionMode.DEFAULT)
        # Content-oriented policy: the matched secret substring is masked in place,
        # the surrounding text survives, and safe attributes are untouched.
        assert attributes[_SENSITIVE_KEY] == f"question {DEFAULT_REDACTED_VALUE}"
        assert attributes[_SAFE_KEY] == "mistral-large"

    def test_strict_drops_whole_sensitive_value(self) -> None:
        attributes = _export_span_through(OtelRedactionMode.STRICT)
        # Key-oriented policy: sensitive-keyed values are replaced wholesale, while
        # a known-safe attribute is preserved.
        assert attributes[_SENSITIVE_KEY] == DEFAULT_REDACTED_VALUE
        assert attributes[_SAFE_KEY] == "mistral-large"

    def test_strict_drops_workflow_arguments_and_result(self) -> None:
        attributes = _export_span_through(
            OtelRedactionMode.STRICT, {"wf.arguments": '{"account": "123"}', "wf.result": '{"balance": 42}'}
        )
        assert attributes == {"wf.arguments": DEFAULT_REDACTED_VALUE, "wf.result": DEFAULT_REDACTED_VALUE}


def _export_logs_through(mode: OtelRedactionMode, emit: Callable[[], None]) -> list[tuple[Any, dict[str, Any]]]:
    """Export logs through the handler and JSON formatter wired as in config_otel; return parsed bodies."""
    setup_logging(log_level=LogLevel.INFO, log_format=LogFormat.CONSOLE)
    memory = InMemoryLogRecordExporter()
    provider = LoggerProvider()
    provider.add_log_record_processor(SimpleLogRecordProcessor(memory))
    handler = _StructlogAwareLoggingHandler(logger_provider=provider, redaction=mode)
    handler.setFormatter(
        build_json_log_formatter(_LogBodyRedactor(mode), redact_credentials=mode is not OtelRedactionMode.NONE)
    )

    root = logging.getLogger()
    root.addHandler(handler)
    try:
        emit()
    finally:
        root.removeHandler(handler)

    exported = []
    for finished in memory.get_finished_logs():
        record = finished.log_record
        attributes = {key: value for key, value in (record.attributes or {}).items() if not key.startswith("code.")}
        # json.loads also asserts that every exported body is valid JSON.
        exported.append((json.loads(str(record.body)), attributes))
    return exported


class _Holding:
    def __repr__(self) -> str:
        return "Holding(owner=jane@acme.com)"


class TestLogRedaction:
    _SQL = f"query failed: SELECT * FROM trades WHERE auth = '{_SECRET}'"
    _EXTRAS = {"workflowName": "portfolio_insights", "db_error": f"auth {_SECRET} rejected"}

    def _emit_third_party_error(self) -> None:
        logging.getLogger("sqlalchemy.engine").error(self._SQL, extra=self._EXTRAS)

    def _extras_of(self, attributes: dict[str, Any]) -> dict[str, Any]:
        # Only compare the attributes the test sets: the environment can inject its own into every
        # log record (CI's ddtrace adds dd.trace_id, dd.span_id, ...), and those are exported too.
        return {key: attributes.get(key) for key in self._EXTRAS}

    def test_none_leaves_body_and_attributes_intact(self) -> None:
        [(body, attributes)] = _export_logs_through(OtelRedactionMode.NONE, self._emit_third_party_error)
        assert body["event"] == self._SQL
        assert self._extras_of(attributes) == self._EXTRAS

    def test_default_scrubs_secrets_in_body_and_attributes(self) -> None:
        [(body, attributes)] = _export_logs_through(OtelRedactionMode.DEFAULT, self._emit_third_party_error)
        assert body["event"] == f"query failed: SELECT * FROM trades WHERE auth = '{DEFAULT_REDACTED_VALUE}'"
        assert body["logger"] == "sqlalchemy.engine"
        assert self._extras_of(attributes) == {
            "workflowName": "portfolio_insights",
            "db_error": f"auth {DEFAULT_REDACTED_VALUE} rejected",
        }

    def test_default_scrubs_string_values_and_keeps_numbers(self) -> None:
        # Numbers render unquoted in the JSON body; a 13-digit epoch-ms timestamp matches the
        # card-number pattern, so redacting the rendered text would corrupt the body.
        def emit() -> None:
            structlog.get_logger("portfolio").info(
                "Trade booked",
                started_at_ms=1793000000000,
                price=1234567890123.45,
                client={"email": "jane@acme.com", "tags": ["vip", "jane@acme.com"]},
                holding=_Holding(),
            )

        [(body, _)] = _export_logs_through(OtelRedactionMode.DEFAULT, emit)
        assert body["started_at_ms"] == 1793000000000
        assert body["price"] == 1234567890123.45
        assert body["client"] == {"email": DEFAULT_REDACTED_VALUE, "tags": ["vip", DEFAULT_REDACTED_VALUE]}
        assert body["holding"] == f"Holding(owner={DEFAULT_REDACTED_VALUE})"

    def test_default_scrubs_formatted_exception(self) -> None:
        def emit() -> None:
            try:
                raise ValueError(f"upstream rejected {_SECRET}")
            except ValueError:
                logging.getLogger("httpx").exception("Request failed")

        [(body, attributes)] = _export_logs_through(OtelRedactionMode.DEFAULT, emit)
        assert _SECRET not in body["exception"]
        assert DEFAULT_REDACTED_VALUE in body["exception"]
        assert _SECRET not in str(attributes)

    def test_strict_replaces_body_with_redacted_object_and_scrubs_attributes(self) -> None:
        [(body, attributes)] = _export_logs_through(OtelRedactionMode.STRICT, self._emit_third_party_error)
        assert body == {"event": DEFAULT_REDACTED_VALUE}
        assert self._extras_of(attributes) == {
            "workflowName": "portfolio_insights",
            "db_error": f"auth {DEFAULT_REDACTED_VALUE} rejected",
        }


class TestClientTelemetryConfiguration:
    def test_configures_global_provider_without_redaction_when_otel_enabled(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        recorded = MagicMock()
        monkeypatch.setattr(client_module, "configure_telemetry", recorded)
        monkeypatch.setattr(client_module.config.common, "otel_enabled", True)

        client = MagicMock()
        client_module._configure_client_telemetry(client)

        recorded.assert_called_once_with(client, provider="global", redaction=False)

    def test_noop_when_otel_disabled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        recorded = MagicMock()
        monkeypatch.setattr(client_module, "configure_telemetry", recorded)
        monkeypatch.setattr(client_module.config.common, "otel_enabled", False)

        client_module._configure_client_telemetry(MagicMock())

        recorded.assert_not_called()

    def test_telemetry_failure_does_not_propagate(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _boom(*_args: object, **_kwargs: object) -> None:
            raise ValueError("no hooks")

        monkeypatch.setattr(client_module, "configure_telemetry", _boom)
        monkeypatch.setattr(client_module.config.common, "otel_enabled", True)

        client_module._configure_client_telemetry(MagicMock())


class _Interrupt(Exception):
    pass


class TestOtelLoggingHandlerLock:
    def test_interrupted_log_call_does_not_block_later_logs(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Temporal's deadlock detector interrupts a workflow thread stuck for 2s with
        # PyThreadState_SetAsyncExc. If that thread was waiting on a handler lock, the exception can
        # fire right after the lock is acquired and leak it, so every later log call hangs forever.
        setup_logging(log_level=LogLevel.INFO, log_format=LogFormat.CONSOLE)
        mode = OtelRedactionMode.DEFAULT
        memory = InMemoryLogRecordExporter()
        provider = LoggerProvider()
        provider.add_log_record_processor(SimpleLogRecordProcessor(memory))
        handler = _StructlogAwareLoggingHandler(logger_provider=provider, redaction=mode)
        body_redactor = _LogBodyRedactor(mode)
        slow_started = threading.Event()
        release_slow = threading.Event()

        def slow_redactor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            if event_dict.get("event") == "slow":
                slow_started.set()
                release_slow.wait(timeout=5)
            return body_redactor(logger, method_name, event_dict)

        handler.setFormatter(build_json_log_formatter(slow_redactor))
        stdlib_logger = logging.getLogger("tests.otel_handler_lock")
        monkeypatch.setattr(stdlib_logger, "handlers", [handler])
        monkeypatch.setattr(stdlib_logger, "propagate", False)
        monkeypatch.setattr(stdlib_logger, "level", logging.INFO)

        def log_interruptible(message: str) -> None:
            try:
                stdlib_logger.info(message)
            except _Interrupt:
                pass

        slow = threading.Thread(target=log_interruptible, args=("slow",), daemon=True)
        slow.start()
        assert slow_started.wait(timeout=5)
        waiter = threading.Thread(target=log_interruptible, args=("waiting",), daemon=True)
        waiter.start()
        time.sleep(0.2)
        if waiter.is_alive() and waiter.ident is not None:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(waiter.ident), ctypes.py_object(_Interrupt))
        release_slow.set()
        slow.join(timeout=5)
        waiter.join(timeout=5)

        later = threading.Thread(target=stdlib_logger.info, args=("later",), daemon=True)
        later.start()
        later.join(timeout=2)

        assert not later.is_alive(), "log call blocked on a leaked handler lock"
        exported_events = [json.loads(str(log.log_record.body))["event"] for log in memory.get_finished_logs()]
        assert "later" in exported_events

from collections.abc import Iterator
from typing import Any

import pytest

from mistralai.workflows import activity, get_workflow_definition, workflow
from mistralai.workflows.core.logging import (
    LogFormat,
    LogLevel,
    _add_temporal_context_processor,
    build_json_log_formatter,
    setup_logging,
)

from .utils import create_test_worker


@activity()
async def log_from_activity(message: str) -> str:
    import structlog

    structlog.get_logger("test_activity").info("activity_log", payload=message)
    return f"logged:{message}"


@workflow.define(name="logging_test_workflow")
class LoggingTestWorkflow:
    @workflow.entrypoint
    async def run(self, message: str) -> str:
        return await log_from_activity(message)


@pytest.fixture
def capture_structlog() -> Iterator[list[dict[str, Any]]]:
    import structlog

    captured: list[dict[str, Any]] = []

    def capture_event(_logger: Any, _method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        captured.append(event_dict.copy())
        raise structlog.DropEvent

    old_config = structlog.get_config()
    setup_logging(log_level=LogLevel.DEBUG)

    config = structlog.get_config()
    processors = list(config["processors"])
    processors[-1] = capture_event
    structlog.configure(**{**config, "processors": processors, "cache_logger_on_first_use": False})

    yield captured
    structlog.configure(**old_config)


class TestOtlpLogFormat:
    def test_otlp_renders_json_while_console_keeps_user_format(self) -> None:
        import json
        import logging

        import structlog

        captured: list[logging.LogRecord] = []

        class _Capture(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                captured.append(record)

        setup_logging(log_level=LogLevel.INFO, log_format=LogFormat.CONSOLE)
        root = logging.getLogger()
        console_formatter = root.handlers[0].formatter
        assert console_formatter is not None

        capture = _Capture()
        root.addHandler(capture)
        try:
            structlog.get_logger("otlp_test").info("hello", foo="bar")
        finally:
            root.removeHandler(capture)

        assert captured
        record = captured[-1]

        otlp_body = build_json_log_formatter().format(record)
        parsed = json.loads(otlp_body)
        assert parsed["event"] == "hello"
        assert parsed["foo"] == "bar"

        console_body = console_formatter.format(record)
        with pytest.raises(json.JSONDecodeError):
            json.loads(console_body)
        assert "hello" in console_body


class TestTemporalContextProcessor:
    def test_noop_outside_temporal(self) -> None:
        event_dict = {"event": "hello", "key": "value"}
        result = _add_temporal_context_processor(None, "info", event_dict)

        assert "workflow.execution_id" not in result
        assert "workflow.run_id" not in result
        assert result == {"event": "hello", "key": "value"}

    def test_attribute_errors_are_not_swallowed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        class BrokenWorkflowInfo:
            workflow_id = "test-workflow-id"

            @property
            def run_id(self) -> str:
                raise RuntimeError("attribute access should surface")

        monkeypatch.setattr("mistralai.workflows.core.logging.temporalio.workflow.info", lambda: BrokenWorkflowInfo())

        with pytest.raises(RuntimeError, match="attribute access should surface"):
            _add_temporal_context_processor(None, "info", {"event": "hello"})

    @pytest.mark.asyncio
    async def test_activity_logs_contain_workflow_and_run_ids(
        self,
        temporal_env: Any,
        capture_structlog: list[dict[str, Any]],
    ) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[LoggingTestWorkflow],
            activities=[log_from_activity],
        ):
            workflow_definition = get_workflow_definition(LoggingTestWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_definition.name,
                {"message": "ping"},
                id="test-logging",
                task_queue="test-task-queue",
            )
            result = await handle.result()

        assert result["result"] == "logged:ping"

        log = next((event for event in capture_structlog if event.get("event") == "activity_log"), None)
        assert log is not None
        assert log["payload"] == "ping"
        assert log.get("workflow.execution_id") == handle.id
        assert log.get("workflow.run_id") == handle.first_execution_run_id

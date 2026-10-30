"""Importing the SDK leaves the process's logging alone; worker start and the CLIs set it up.

Each case runs in a fresh interpreter: the import under test happens once per process.
"""

import json
import os
import subprocess
import sys
import textwrap
from typing import Any

import pytest

_SNAPSHOT = """
import json, logging, structlog

def snapshot():
    root = logging.getLogger()
    return {
        "handlers": [id(handler) for handler in root.handlers],
        "root_level": root.level,
        "structlog_configured": structlog.is_configured(),
        "noisy_levels": {name: logging.getLogger(name).level for name in ("httpx", "httpcore", "asyncio", "urllib3")},
    }
"""

_HOST_HANDLERS = """
import io
host_output = io.StringIO()
host_handler = logging.StreamHandler(host_output)
host_handler.setFormatter(logging.Formatter("HOST %(name)s %(levelname)s %(message)s"))
logging.getLogger().addHandler(host_handler)
logging.getLogger().addHandler(logging.NullHandler())
logging.getLogger().setLevel(logging.DEBUG)
"""


def _env_without_worker_settings() -> dict[str, str]:
    worker_settings = {"DEPLOYMENT_NAME", "TEMPORAL_TASK_QUEUE", "LOG_FORMAT", "LOG_LEVEL"}
    return {key: value for key, value in os.environ.items() if key not in worker_settings}


def _run(script: str, **env: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", textwrap.dedent(script)],
        capture_output=True,
        text=True,
        env={**_env_without_worker_settings(), **env},
        timeout=120,
    )


def _last_json_line(output: str) -> dict[str, Any]:
    return json.loads(output.strip().splitlines()[-1])


class TestImportHasNoLoggingSideEffects:
    @pytest.mark.parametrize("host_setup", ["", _HOST_HANDLERS], ids=["no_handlers", "host_handlers"])
    def test_import_leaves_root_logger_and_structlog_untouched(self, host_setup: str) -> None:
        result = _run(
            _SNAPSHOT
            + host_setup
            + """
before = snapshot()
import mistralai.workflows
import mistralai.workflows.core.worker
print(json.dumps({"before": before, "after": snapshot()}))
"""
        )

        assert result.returncode == 0, result.stderr
        states = _last_json_line(result.stdout)
        assert states["after"] == states["before"]
        assert states["after"]["structlog_configured"] is False
        assert result.stdout.strip().count("\n") == 0, "importing the SDK must not print"
        assert result.stderr == ""

    def test_sdk_events_reach_the_host_handlers(self) -> None:
        result = _run(
            _SNAPSHOT
            + _HOST_HANDLERS
            + """
import mistralai.workflows
from mistralai.workflows.core.worker import logger
logger.info("sdk_event", answer=42)
print(json.dumps({"host_output": host_output.getvalue()}))
"""
        )

        assert result.returncode == 0, result.stderr
        host_output = _last_json_line(result.stdout)["host_output"]
        assert "HOST mistralai.workflows.core.worker INFO sdk_event answer=42" in host_output

    def test_host_records_carry_the_sdk_call_site_and_one_traceback(self) -> None:
        result = _run(
            _SNAPSHOT
            + _HOST_HANDLERS
            + """
import copy
host_handler.setFormatter(logging.Formatter("%(filename)s:%(funcName)s:%(lineno)d %(message)s"))
from mistralai.workflows.core._logger import get_logger
logger = get_logger("sdk.module")
host_output.truncate(0)
host_output.seek(0)

def caller():
    logger.info("plain")
    logger.bind(run="r1").warning("bound")
    logger.log(logging.INFO, "via_log")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("failed")

caller()
copy.copy(logger)
print(json.dumps({"host_output": host_output.getvalue()}))
"""
        )

        assert result.returncode == 0, result.stderr
        host_output = _last_json_line(result.stdout)["host_output"]
        call_sites = [line.split(" ", 1)[0].rsplit(":", 1)[0] for line in host_output.splitlines()[:4]]
        assert call_sites == ["<string>:caller"] * 4
        assert "bound run=r1" in host_output
        assert host_output.count("ZeroDivisionError: division by zero") == 1

    def test_without_logging_setup_only_warnings_reach_stderr(self) -> None:
        result = _run(
            """
import mistralai.workflows
from mistralai.workflows.core.worker import logger
logger.debug("sdk_debug_event")
logger.info("sdk_info_event")
logger.warning("sdk_warning_event", answer=42)
"""
        )

        assert result.returncode == 0, result.stderr
        assert result.stdout == ""
        assert result.stderr.strip() == "sdk_warning_event answer=42"


class TestEntryPointsSetUpLogging:
    _START_WORKER = """
import asyncio
import mistralai.workflows as workflows
try:
    asyncio.run(workflows.run_worker([], enable_config_discovery=False))
except ValueError:
    pass
print(json.dumps(snapshot()))
"""

    def test_worker_start_sets_up_sdk_logging(self) -> None:
        result = _run(_SNAPSHOT + self._START_WORKER, LOG_FORMAT="json", LOG_LEVEL="INFO")

        assert result.returncode == 0, result.stderr
        state = _last_json_line(result.stdout)
        assert len(state["handlers"]) == 1
        assert state["structlog_configured"] is True
        assert state["root_level"] == 20
        assert state["noisy_levels"] == {"httpx": 30, "httpcore": 30, "asyncio": 30, "urllib3": 30}
        events = [json.loads(line) for line in result.stderr.splitlines() if line.startswith("{")]
        by_event = {event["event"]: event for event in events}
        assert by_event["Configuration loaded"]["logger"] == "mistralai.workflows.core.config.config"
        assert by_event["Worker config"]["logger"] == "mistralai.workflows.core.worker"
        assert by_event["Worker stopped due to unhandled exception"]["level"] == "error"
        assert all({"timestamp", "level", "logger", "event"} <= event.keys() for event in events)

    def test_worker_start_keeps_a_host_structlog_configuration(self) -> None:
        result = _run(
            _SNAPSHOT
            + _HOST_HANDLERS
            + """
structlog.configure(
    processors=[structlog.stdlib.filter_by_level, structlog.processors.KeyValueRenderer(key_order=["event"])],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
)
before = snapshot()
"""
            + self._START_WORKER
            + """
print(json.dumps({"before": before, "host_output": host_output.getvalue()}))
"""
        )

        assert result.returncode == 0, result.stderr
        lines = result.stdout.strip().splitlines()
        assert json.loads(lines[-2]) == _last_json_line(result.stdout)["before"]
        assert "event='Configuration loaded'" in _last_json_line(result.stdout)["host_output"]

    def test_worker_start_keeps_host_handlers_added_after_import(self) -> None:
        # The host imports the SDK first, sets up stdlib logging only, then starts a worker.
        result = _run(
            _SNAPSHOT
            + """
import mistralai.workflows
"""
            + _HOST_HANDLERS
            + """
before = snapshot()
"""
            + self._START_WORKER
            + """
print(json.dumps({"before": before, "host_output": host_output.getvalue()}))
""",
            LOG_FORMAT="json",
            LOG_LEVEL="INFO",
        )

        assert result.returncode == 0, result.stderr
        lines = result.stdout.strip().splitlines()
        before = _last_json_line(result.stdout)["before"]
        after = json.loads(lines[-2])
        assert after["handlers"] == before["handlers"]
        assert after["root_level"] == before["root_level"] == 10
        assert after["noisy_levels"] == before["noisy_levels"]
        assert after["structlog_configured"] is True
        host_output = _last_json_line(result.stdout)["host_output"]
        assert "HOST mistralai.workflows.core.config.config INFO Configuration loaded" in host_output
        assert "HOST mistralai.workflows.core.worker ERROR Worker stopped due to unhandled exception" in host_output
        assert host_output.count("Traceback (most recent call last)") == 1
        # Only the config-discovery UserWarning reaches stderr: no SDK handler, no structlog warning.
        assert "Configuration loaded" not in result.stderr
        assert "structlog" not in result.stderr

    def test_host_logging_records_carry_call_site_one_traceback_and_otlp_fields(self) -> None:
        # Host stdlib logging, then the SDK's setup, then a handler with the OTLP export's formatter
        # (config_otel adds it inside run_worker). Loggers made before and after the setup both count.
        result = _run(
            _SNAPSHOT
            + _HOST_HANDLERS
            + """
import structlog
import mistralai.workflows.core.workflow as workflow_module
from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.config.config import setup_default_logging
from mistralai.workflows.core.logging import build_json_log_formatter
setup_default_logging()
records = []
class RecordKeeper(logging.Handler):
    def emit(self, record):
        records.append(record)
logging.getLogger().addHandler(RecordKeeper())
# The host's own OTel log handler, with no formatter.
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import InMemoryLogExporter, SimpleLogRecordProcessor
host_exporter = InMemoryLogExporter()
host_provider = LoggerProvider()
host_provider.add_log_record_processor(SimpleLogRecordProcessor(host_exporter))
logging.getLogger().addHandler(LoggingHandler(logger_provider=host_provider))
get_logger("sdk.module").info("before_otlp_export")
host_handler.setFormatter(logging.Formatter("%(filename)s:%(funcName)s:%(lineno)d %(message)s"))
otlp_output = io.StringIO()
otlp_handler = logging.StreamHandler(otlp_output)
otlp_handler.setFormatter(build_json_log_formatter())
logging.getLogger().addHandler(otlp_handler)
host_output.truncate(0)
host_output.seek(0)
loggers = [workflow_module.logger, get_logger("sdk.module"), structlog.get_logger("user.module")]

def caller():
    for logger in loggers:
        logger.info("plain", answer=42)
    try:
        1 / 0
    except ZeroDivisionError:
        loggers[1].exception("failed", run="r1")
    loggers[1].info("with_stack", stack_info=True)

caller()
print(json.dumps({
    "host_output": host_output.getvalue(),
    "otlp_output": otlp_output.getvalue(),
    # Formatters set "message" (and "asctime") on every record.
    "extra_record_attributes": sorted(
        {key for record in records for key in vars(record)} - {*vars(logging.makeLogRecord({})), "message", "asctime"}
    ),
    "host_otel_body_types": sorted({type(log.log_record.body).__name__ for log in host_exporter.get_finished_logs()}),
    "host_otel_attributes": sorted(
        {key for log in host_exporter.get_finished_logs() for key in log.log_record.attributes or {}}
    ),
}))
"""
        )

        assert result.returncode == 0, result.stderr
        output = _last_json_line(result.stdout)
        host_lines = output["host_output"].splitlines()
        call_sites = [line.split(" ", 1)[0].rsplit(":", 1)[0] for line in host_lines[:4]]
        assert call_sites == ["<string>:caller"] * 4
        assert host_lines[0].endswith(" plain answer=42")
        assert output["host_output"].count("Traceback (most recent call last)") == 1
        otlp_events = [json.loads(line) for line in output["otlp_output"].splitlines()]
        assert [event["event"] for event in otlp_events] == ["plain", "plain", "plain", "failed", "with_stack"]
        assert all(event["answer"] == 42 for event in otlp_events[:3])
        assert otlp_events[3]["run"] == "r1"
        assert otlp_events[3]["exception"].count("Traceback (most recent call last)") == 1
        # The exported stack is the caller's, not the formatter's.
        assert "in caller" in otlp_events[4]["stack"]
        assert "logging/__init__.py" not in otlp_events[4]["stack"]
        # A host's own handlers and exporters get plain text and no extra record attributes.
        assert output["extra_record_attributes"] == []
        assert output["host_otel_body_types"] == ["str"]
        assert not [key for key in output["host_otel_attributes"] if not key.startswith(("code.", "exception."))]

    def test_diagnose_leaves_logging_alone_and_later_warnings_reach_stderr(self) -> None:
        # wf-diagnose prints its report to stdout and sets up no logging: an SDK warning logged
        # after the SDK is loaded still reaches stderr through Python's last-resort handler.
        result = _run(
            _SNAPSHOT
            + """
before = snapshot()
from mistralai.workflows.scripts.diagnose import _load_sdk
_load_sdk()
from mistralai.workflows.core.worker import logger
logger.warning("sdk_warning_event")
print(json.dumps({"before": before, "after": snapshot()}))
"""
        )

        assert result.returncode == 0, result.stderr
        assert result.stdout.strip().count("\n") == 0
        state = _last_json_line(result.stdout)
        assert state["after"] == state["before"]
        assert state["after"]["structlog_configured"] is False
        assert "sdk_warning_event" in result.stderr

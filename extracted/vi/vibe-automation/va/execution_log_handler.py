import logging
import structlog

from va.clients.execution_service_client import append_execution_log
from va.utils import is_test_execution
from va.configure_structlog import _PRE_CHAIN


class ExecutionLogHandler(logging.Handler):
    """Forward all SDK log records to the Execution Service."""

    def __init__(self, execution_id: str, level: int = logging.INFO):
        super().__init__(level)
        self.execution_id = execution_id

        self.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=structlog.processors.JSONRenderer(),
                foreign_pre_chain=_PRE_CHAIN,
            )
        )

    def emit(self, record: logging.LogRecord) -> None:
        # Don't try to forward any logs during local test executions
        if is_test_execution(self.execution_id):
            return

        # Ignore logs originating from the Execution Service client itself to
        # avoid infinite recursion.
        if record.name.startswith("va.clients"):
            return

        try:
            json_log_line = self.format(record)
            append_execution_log(self.execution_id, json_log_line)

        except Exception:
            # Best-effort: don't crash execution because logging failed.
            pass

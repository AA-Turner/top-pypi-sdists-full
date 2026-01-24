import copy
import logging
import sys
from logging.handlers import HTTPHandler, QueueHandler, QueueListener
from queue import Queue
from typing import TextIO

import simplejson as json

from fluidattacks_core.logging.filters import (
    EnabledTelemetryFilter,
    ErrorOnlyFilter,
    NoProductionFilter,
    ProductionOnlyFilter,
)
from fluidattacks_core.logging.formatters import ColorfulFormatter, CustomJsonFormatter


class CustomQueueHandler(QueueHandler):
    """Class to fix QueueHandler missing exc_info field."""

    def prepare(self, record: logging.LogRecord) -> logging.LogRecord:
        original_exc_info = record.exc_info

        # Avoid duplicate exc_text in the log message
        no_exc_record = copy.copy(record)
        no_exc_record.exc_info = None
        prepared = super().prepare(no_exc_record)

        prepared.exc_info = original_exc_info

        return prepared


class DebuggingHandler(logging.StreamHandler[TextIO]):
    """Logging handler for console environments implemented with `QueueHandler`.

    Includes:
    - Filters: `NoProductionFilter`
    - Formatter: `ColorfulFormatter`
    """

    def __init__(self, stream: TextIO = sys.stderr) -> None:
        super().__init__(stream)
        self.addFilter(NoProductionFilter())
        self.setFormatter(ColorfulFormatter())


class ProductionSyncHandler(logging.StreamHandler[TextIO]):
    """Logging handler for production environments implemented with `logging.StreamHandler`.

    Includes:
    - Filters: `ProductionOnlyFilter`
    - Formatter: `CustomJsonFormatter`
    """

    def __init__(self, stream: TextIO = sys.stderr) -> None:
        super().__init__(stream)
        self.addFilter(ProductionOnlyFilter())
        self.setFormatter(CustomJsonFormatter())


class ProductionAsyncHandler(CustomQueueHandler):
    """Logging handler for production environments implemented with `QueueHandler`.

    Includes:
    - Filters: `NoBatchFilter`, `ProductionOnlyFilter`
    - Formatter: `CustomJsonFormatter`
    """

    def __init__(self, stream: TextIO = sys.stderr) -> None:
        handler = logging.StreamHandler(stream)
        handler.addFilter(ProductionOnlyFilter())
        handler.setFormatter(CustomJsonFormatter())

        self.queue = Queue()
        self.listener = QueueListener(self.queue, handler)

        self.listener.start()
        self.shutting_down = False
        super().__init__(self.queue)

    def emit(self, record: logging.LogRecord) -> None:
        if self.shutting_down:
            return
        super().emit(record)

    def close(self) -> None:
        self.shutting_down = True
        self.listener.stop()
        super().close()


class DatadogLogsHandler(HTTPHandler):
    """Logging handler for sending logs to Datadog using `HTTPHandler` from Python logging."""

    def __init__(self, service: str, source: str, client_token: str) -> None:
        self.host = "http-intake.logs.datadoghq.com"
        self.url = f"/api/v2/logs?dd-api-key={client_token}&ddsource={source}&service={service}"

        super().__init__(host=self.host, url=self.url, method="POST", secure=True)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            log_data = self.format(record)
            json_string = json.dumps([log_data])

            h = self.getConnection(self.host, self.secure)
            h.putrequest(self.method, self.url)

            h.putheader("Content-Type", "application/json")
            h.putheader("Content-Length", str(len(json_string)))
            h.endheaders()

            h.send(json_string.encode("utf-8"))
            h.getresponse()
        except Exception:  # noqa: BLE001
            self.handleError(record)


class TelemetryAsyncHandler(CustomQueueHandler):
    """Logging handler for sending logs to telemetry services asynchronously.

    To enable telemetry, set the `TELEMETRY_OPT_OUT` environment variable different from `true`.

    Includes:
    - Filters: `ErrorOnlyFilter`, `EnabledTelemetryFilter`
    - Formatter: `CustomJsonFormatter`
    """

    def __init__(self, service: str, source: str, dd_client_token: str) -> None:
        """Initialize the TelemetryAsyncHandler.

        Args:
            service: The service name.
            source: The source name.
            dd_client_token: The Datadog Client Token.

        """
        self.addFilter(ErrorOnlyFilter())
        self.addFilter(EnabledTelemetryFilter())

        handler = DatadogLogsHandler(service, source, dd_client_token)
        handler.setFormatter(CustomJsonFormatter())

        self.queue = Queue()
        self.listener = QueueListener(self.queue, handler)

        self.listener.start()
        self.shutting_down = False
        super().__init__(self.queue)

    def emit(self, record: logging.LogRecord) -> None:
        if self.shutting_down:
            return
        super().emit(record)

    def close(self) -> None:
        self.shutting_down = True
        if self.listener:
            self.listener.stop()
        super().close()

"""
    Easy logging wrapper for cosmicfrog library, supports Insights logging if available
"""
import logging
import os
import sys
from logging import Logger

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter, AzureMonitorLogExporter

app_logger = {}


def get_logger(console_only: bool = False) -> Logger:
    """
    Gets an appropriate Logger instance (configured, connected to Azure Monitor if available)
    """
    current_pid = str(os.getpid())

    if current_pid in app_logger:
        return app_logger[current_pid]

    log_level = os.getenv("FROG_LOG_LEVEL") or logging.DEBUG
    log_level = int(log_level)

    logger = logging.getLogger(current_pid)
    app_logger[current_pid] = logger

    # Add log to Azure Monitor (OL internal only)
    if not console_only:
        insights_connection = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

        if insights_connection:
            # Set up OpenTelemetry for Azure Monitor
            resource = Resource.create({"service.name": "cosmicfrog"})

            # Set up the TracerProvider for traces
            tracer_provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(tracer_provider)
            trace_exporter = AzureMonitorTraceExporter(connection_string=insights_connection)
            trace_processor = BatchSpanProcessor(trace_exporter)
            tracer_provider.add_span_processor(trace_processor)

            # Set up the LoggerProvider for logs
            logger_provider = LoggerProvider(resource=resource)
            set_logger_provider(logger_provider)
            log_exporter = AzureMonitorLogExporter(connection_string=insights_connection)
            log_processor = BatchLogRecordProcessor(log_exporter)
            logger_provider.add_log_record_processor(log_processor)

            # Integrate OpenTelemetry with the standard logging module
            otel_logging_handler = LoggingHandler(
                level=log_level, logger_provider=logger_provider
            )
            logger.addHandler(otel_logging_handler)

            logger.info("Azure Monitor logging is configured")

    # Add log to console
    stdhandler = logging.StreamHandler(sys.stdout)
    stdhandler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdhandler.setFormatter(formatter)
    logger.addHandler(stdhandler)

    logger.setLevel(log_level)

    return logger

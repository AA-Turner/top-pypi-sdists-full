"""Structured logging configuration using structlog."""

import logging
import os
import sys

import structlog


def setup_logging() -> None:
    """Configure structured logging. JSON in production, console in dev."""
    is_production = os.getenv("APP_ENV") == "production"
    log_level = getattr(logging, os.getenv("APP_LOG_LEVEL", "INFO").upper(), logging.INFO)

    renderer = structlog.processors.JSONRenderer() if is_production else structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Also configure stdlib logging to use structlog
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level)

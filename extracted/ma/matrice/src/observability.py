"""Sentry error tracking initialization."""

import os

import sentry_sdk
import structlog

logger = structlog.get_logger()


def init_sentry() -> None:
    """Initialize Sentry. No-op if SENTRY_DSN is not set."""
    dsn = os.getenv("SENTRY_DSN", "")
    if not dsn:
        logger.warning("SENTRY_DSN not set, error tracking disabled")
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=os.getenv("APP_ENV", "development"),
        traces_sample_rate=0.1,
        enable_tracing=True,
    )
    logger.info("sentry initialized", environment=os.getenv("APP_ENV"))

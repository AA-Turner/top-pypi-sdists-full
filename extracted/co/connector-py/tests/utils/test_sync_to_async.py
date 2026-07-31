"""Tests for connector.utils.sync_to_async."""

import contextvars
import logging
import threading

import pytest
from connector.utils.sync_to_async import sync_to_async

REQUEST_METADATA: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_metadata", default=None
)


class Client:
    @sync_to_async
    def echo(self, value: int, *, offset: int = 0) -> int:
        return value + offset

    @sync_to_async
    def thread_name(self) -> str:
        return threading.current_thread().name

    @sync_to_async
    def read_context(self) -> str | None:
        return REQUEST_METADATA.get()

    @sync_to_async
    def log_something(self, logger: logging.Logger) -> None:
        logger.info("emitted from the worker thread")

    @sync_to_async
    def explode(self) -> None:
        raise ValueError("boom")


class ContextAttributeFilter(logging.Filter):
    """Mirrors how the host injects request metadata onto records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_metadata = REQUEST_METADATA.get()
        return True


class TestSyncToAsync:
    async def test_passes_through_args_and_return_value(self):
        assert await Client().echo(1, offset=2) == 3

    async def test_runs_off_the_event_loop(self):
        assert await Client().thread_name() != threading.current_thread().name

    async def test_propagates_exceptions(self):
        with pytest.raises(ValueError, match="boom"):
            await Client().explode()

    async def test_contextvars_reach_the_worker_thread(self):
        """Regression guard: run_in_executor drops contextvars, to_thread copies them."""
        REQUEST_METADATA.set("tableau")
        assert await Client().read_context() == "tableau"

    async def test_logs_from_worker_thread_keep_request_metadata(self, caplog):
        """The failure this guards against: records emitted in the worker arrive unattributed."""
        REQUEST_METADATA.set("tableau")
        logger = logging.getLogger("test_sync_to_async")
        logger.addFilter(ContextAttributeFilter())
        try:
            with caplog.at_level(logging.INFO, logger=logger.name):
                await Client().log_something(logger)
        finally:
            logger.filters.clear()

        assert [r.request_metadata for r in caplog.records] == ["tableau"]

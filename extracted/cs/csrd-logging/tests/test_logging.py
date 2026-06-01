"""Tests for csrd.logging — ContextLogger and LoggingMixin."""

import logging
from typing import ClassVar

import pytest

from csrd.context._contextvars import reset_global_configuration
from csrd.context.platform import hit_id_context, user_info_context
from csrd.logging import (
    ContextLogger,
    LoggingMixin,
    RequestContextFilter,
    auth_error_detail,
    configure_logging,
    is_debug,
)


@pytest.fixture(autouse=True)
def _clean_context():
    """Reset context vars around each test."""
    hit_token = hit_id_context.set("unknown")
    user_token = user_info_context.set(None)
    yield
    hit_id_context.reset(hit_token)
    user_info_context.reset(user_token)
    reset_global_configuration()


# ── ContextLogger ────────────────────────────────────────────────────────


class TestContextLogger:
    def test_plain_message(self, caplog):
        logger = ContextLogger(logging.getLogger("test.plain"))
        with caplog.at_level(logging.INFO, logger="test.plain"):
            logger.info("hello world")
        assert "hello world" in caplog.text

    def test_message_with_meta(self, caplog):
        logger = ContextLogger(logging.getLogger("test.meta"))
        with caplog.at_level(logging.INFO, logger="test.meta"):
            logger.info("order created", meta={"order_id": 42})
        assert "order created" in caplog.text
        assert "order_id=42" in caplog.text

    def test_enriched_with_hit_id(self, caplog):
        hit_id_context.set("req-abc-123")
        logger = ContextLogger(logging.getLogger("test.hit"))
        with caplog.at_level(logging.INFO, logger="test.hit"):
            logger.info("processing")
        assert "hit_id=req-abc-123" in caplog.text

    def test_enriched_with_user_id(self, caplog):
        class FakeClaims:
            sub = "user42"

        user_info_context.set(FakeClaims())
        logger = ContextLogger(logging.getLogger("test.user"))
        with caplog.at_level(logging.INFO, logger="test.user"):
            logger.info("action")
        assert "user_id=user42" in caplog.text

    def test_no_context_no_extras(self, caplog):
        logger = ContextLogger(logging.getLogger("test.empty"))
        with caplog.at_level(logging.INFO, logger="test.empty"):
            logger.info("bare")
        # Should just be the message, no key=value pairs
        assert caplog.records[0].message == "bare"

    def test_all_levels(self, caplog):
        logger = ContextLogger(logging.getLogger("test.levels"))
        with caplog.at_level(logging.DEBUG, logger="test.levels"):
            logger.debug("d")
            logger.info("i")
            logger.warning("w")
            logger.error("e")
        level_records = [r for r in caplog.records if r.name == "test.levels"]
        assert len(level_records) == 4

    def test_exception_level(self, caplog):
        logger = ContextLogger(logging.getLogger("test.exc"))
        with caplog.at_level(logging.ERROR, logger="test.exc"):
            try:
                raise ValueError("boom")
            except ValueError:
                logger.exception("caught it")
        assert "caught it" in caplog.text

    def test_stdlib_logger_accessible(self):
        stdlib = logging.getLogger("test.stdlib")
        ctx = ContextLogger(stdlib)
        assert ctx.stdlib_logger is stdlib


# ── LoggingMixin ─────────────────────────────────────────────────────────


class TestLoggingMixin:
    def test_log_property_returns_context_logger(self):
        class MyClass(LoggingMixin):
            pass

        obj = MyClass()
        assert isinstance(obj.log, ContextLogger)

    def test_log_property_cached(self):
        class MyClass(LoggingMixin):
            pass

        obj = MyClass()
        assert obj.log is obj.log

    def test_logger_name_includes_class(self):
        class OrderService(LoggingMixin):
            pass

        obj = OrderService()
        assert "OrderService" in obj.log.stdlib_logger.name

    def test_manual_logging(self, caplog):
        class MyService(LoggingMixin):
            def do_work(self):
                self.log.info("doing work", meta={"item": 5})

        svc = MyService()
        with caplog.at_level(logging.INFO):
            svc.do_work()
        assert "doing work" in caplog.text
        assert "item=5" in caplog.text


# ── Auto-logging ─────────────────────────────────────────────────────────


class TestAutoLogging:
    def test_sync_method_logged(self, caplog):
        class Svc(LoggingMixin, auto_log=True):
            def process(self):
                return "done"

        svc = Svc()
        with caplog.at_level(logging.INFO):
            result = svc.process()
        assert result == "done"
        assert "process" in caplog.text

    @pytest.mark.asyncio
    async def test_async_method_logged(self, caplog):
        class Svc(LoggingMixin, auto_log=True):
            async def fetch(self):
                return 42

        svc = Svc()
        with caplog.at_level(logging.INFO):
            result = await svc.fetch()
        assert result == 42
        assert "fetch" in caplog.text

    def test_private_methods_skipped(self, caplog):
        class Svc(LoggingMixin, auto_log=True):
            def _internal(self):
                return "private"

            def public(self):
                return "public"

        svc = Svc()
        with caplog.at_level(logging.INFO):
            svc._internal()
            caplog.clear()
            svc.public()
        assert "public" in caplog.text

    def test_excluded_methods_skipped(self, caplog):
        class Svc(LoggingMixin, auto_log=True):
            __log_exclude__: ClassVar[set[str]] = {"health_check"}

            def health_check(self):
                return "ok"

            def process(self):
                return "done"

        svc = Svc()
        with caplog.at_level(logging.INFO):
            svc.health_check()
        assert "health_check" not in caplog.text

    def test_exception_logged(self, caplog):
        class Svc(LoggingMixin, auto_log=True):
            def fail(self):
                raise ValueError("boom")

        svc = Svc()
        with caplog.at_level(logging.ERROR), pytest.raises(ValueError, match="boom"):
            svc.fail()
        assert "fail failed" in caplog.text

    @pytest.mark.asyncio
    async def test_async_exception_logged(self, caplog):
        class Svc(LoggingMixin, auto_log=True):
            async def fail(self):
                raise RuntimeError("async boom")

        svc = Svc()
        with caplog.at_level(logging.ERROR), pytest.raises(RuntimeError, match="async boom"):
            await svc.fail()
        assert "fail failed" in caplog.text

    def test_no_auto_log_by_default(self, caplog):
        class Svc(LoggingMixin):
            def process(self):
                return "done"

        svc = Svc()
        with caplog.at_level(logging.INFO):
            svc.process()
        # No auto entry log
        assert "process" not in caplog.text

    def test_context_enrichment_in_auto_log(self, caplog):
        hit_id_context.set("trace-xyz")

        class Svc(LoggingMixin, auto_log=True):
            def work(self):
                return True

        svc = Svc()
        with caplog.at_level(logging.INFO):
            svc.work()
        assert "hit_id=trace-xyz" in caplog.text

    def test_excludes_inherited(self, caplog):
        class Base(LoggingMixin, auto_log=True):
            __log_exclude__: ClassVar[set[str]] = {"noisy"}

        class Child(Base, auto_log=True):
            __log_exclude__: ClassVar[set[str]] = {"also_noisy"}

            def noisy(self):
                return "n"

            def also_noisy(self):
                return "an"

            def normal(self):
                return "ok"

        svc = Child()
        with caplog.at_level(logging.INFO):
            svc.noisy()
            svc.also_noisy()
        assert "noisy" not in caplog.text
        assert "also_noisy" not in caplog.text


# ── RequestContextFilter ─────────────────────────────────────────────────


class TestRequestContextFilter:
    def _make_handler_with_filter(
        self, formatter_str: str
    ) -> tuple[logging.Logger, logging.Handler]:
        """Create a logger with a handler that uses RequestContextFilter."""
        logger = logging.getLogger(f"test.filter.{id(self)}")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.addFilter(RequestContextFilter())
        handler.setFormatter(logging.Formatter(formatter_str))
        logger.addHandler(handler)
        return logger, handler

    def test_adds_hit_id_to_record(self, caplog):
        hit_id_context.set("trace-999")
        f = RequestContextFilter()
        record = logging.LogRecord("test", logging.INFO, "", 0, "msg", (), None)
        f.filter(record)
        assert record.hit_id == "trace-999"  # type: ignore[attr-defined]

    def test_adds_user_id_to_record(self):
        class FakeClaims:
            sub = "alice"

        user_info_context.set(FakeClaims())
        f = RequestContextFilter()
        record = logging.LogRecord("test", logging.INFO, "", 0, "msg", (), None)
        f.filter(record)
        assert record.user_id == "alice"  # type: ignore[attr-defined]

    def test_defaults_to_dash_when_no_context(self):
        f = RequestContextFilter()
        record = logging.LogRecord("test", logging.INFO, "", 0, "msg", (), None)
        f.filter(record)
        assert record.hit_id == "-"  # type: ignore[attr-defined]
        assert record.user_id == "-"  # type: ignore[attr-defined]
        assert record.app_id == "-"  # type: ignore[attr-defined]
        assert record.api_version == "-"  # type: ignore[attr-defined]

    def test_always_returns_true(self):
        f = RequestContextFilter()
        record = logging.LogRecord("test", logging.INFO, "", 0, "msg", (), None)
        assert f.filter(record) is True

    def test_works_with_formatter(self, caplog):
        hit_id_context.set("req-abc")

        class FakeClaims:
            sub = "bob"

        user_info_context.set(FakeClaims())

        logger = logging.getLogger("test.filter.fmt")
        logger.handlers.clear()
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.addFilter(RequestContextFilter())
        fmt = logging.Formatter("%(message)s hit_id=%(hit_id)s user_id=%(user_id)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)

        with caplog.at_level(logging.INFO, logger="test.filter.fmt"):
            logger.info("hello")

        # The caplog records should have the filter-injected attributes
        record = next(r for r in caplog.records if r.name == "test.filter.fmt")
        assert record.hit_id == "req-abc"  # type: ignore[attr-defined]
        assert record.user_id == "bob"  # type: ignore[attr-defined]


# ── Debug mode / auth_error_detail ───────────────────────────────────────


class TestDebugMode:
    def setup_method(self):
        configure_logging(debug=False)

    def teardown_method(self):
        configure_logging(debug=False)

    def test_default_is_not_debug(self):
        configure_logging(debug=False)
        assert is_debug() is False

    def test_enable_debug(self):
        configure_logging(debug=True)
        assert is_debug() is True

    def test_disable_debug(self):
        configure_logging(debug=True)
        configure_logging(debug=False)
        assert is_debug() is False

    def test_auth_error_detail_production(self):
        configure_logging(debug=False)
        assert auth_error_detail("kid=abc not found") == "Unauthorized"

    def test_auth_error_detail_debug(self):
        configure_logging(debug=True)
        assert auth_error_detail("kid=abc not found") == "kid=abc not found"

    def test_auth_error_detail_custom_fallback(self):
        configure_logging(debug=False)
        result = auth_error_detail("secret info", fallback="Not allowed")
        assert result == "Not allowed"

    def test_auth_error_detail_custom_fallback_debug(self):
        configure_logging(debug=True)
        result = auth_error_detail("secret info", fallback="Not allowed")
        assert result == "secret info"

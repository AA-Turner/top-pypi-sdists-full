"""Logging extension for capturing full job logs into the shared collector."""

from __future__ import annotations

import logging

from scrapy import signals

from ..collector import ensure_collector
from ..config.settings import Settings
from ..utils.updates import update_available
from .log_handler import (
    IngestLogHandler,
    capture_prints,
    configure_logging_for_ingest,
    drain_early,
    ingest_capture_level,
    level_from_setting,
    stop_prints,
)


class LoggingExtension:
    """
    Capture full job logs (startup → crawl → stats dump → closed)
    plus print() spider lines into the shared collector.
    """

    def __init__(self, crawler, *, capture_level, console_level):
        self.crawler = crawler
        self.settings = Settings(crawler.settings)
        self.collector = ensure_collector(crawler)
        self.console_level = console_level
        drain_early(self.collector, min_level=capture_level)
        self.handler = IngestLogHandler(self.collector, level=capture_level)
        root = logging.getLogger()
        if self.handler not in root.handlers:
            root.addHandler(self.handler)
        configure_logging_for_ingest(self.handler, capture_level, console_level)
        capture_prints(self.collector)
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(self.engine_stopped, signal=signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        if getattr(crawler, "_ingest_logging_ext", None) is not None:
            return crawler._ingest_logging_ext

        update_available()
        console_level = level_from_setting(crawler.settings.get("LOG_LEVEL"), logging.INFO)
        capture_level = ingest_capture_level(crawler.settings)
        ext = cls(crawler, capture_level=capture_level, console_level=console_level)
        crawler._ingest_logging_ext = ext
        return ext

    def spider_opened(self, spider):
        capture = self.handler.level
        for name in (spider.name, getattr(spider, "__module__", None)):
            if not name:
                continue
            log = logging.getLogger(name)
            log.propagate = True
            if log.level == logging.NOTSET or log.level > capture:
                log.setLevel(capture)
        from ..database.flusher import get_flusher

        get_flusher(self.crawler, self.settings).start(spider)

    def engine_stopped(self):
        def _done():
            root = logging.getLogger()
            if self.handler in root.handlers:
                root.removeHandler(self.handler)
            stop_prints()

        try:
            from twisted.internet import reactor

            reactor.addSystemEventTrigger("before", "shutdown", _done)
        except Exception:
            _done()

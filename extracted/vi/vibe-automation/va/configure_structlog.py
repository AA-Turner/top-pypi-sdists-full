import logging
import sys
from typing import List

import structlog
from structlog.contextvars import bind_contextvars


# JSON logging configuration built on structlog.


# configures all logs (from both stdlib and structlog) to contain execution_id,
# timestamp, level, logger name, and any other extra fields passed to the log call
_PRE_CHAIN: List[structlog.types.Processor] = [
    structlog.stdlib.add_logger_name,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.stdlib.ExtraAdder(),
]


# This setup helper is called in workflow.py, in the _setup_execution function
def configure_structlog(level: int = logging.INFO) -> None:  # noqa: D401
    """Configure stdlib *logging* to route through *structlog* and emit JSON.

    After calling this once at process start-up **every** log call – whether it
    goes through :pymod:`logging` or :pymod:`structlog` – will produce a
    JSON line on *stdout* with at least the following keys::

        {
            "timestamp": "2025-07-29T19:15:30.123Z",
            "level": "info",
            "logger": "va.store.orby_store",
            "event": "mark_start",
            ...
        }
    """

    # 1. Stdlib root logger → StreamHandler → ProcessorFormatter
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear any existing handlers and install a single ProcessorFormatter
    root_logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=_PRE_CHAIN,
        )
    )
    root_logger.addHandler(handler)

    # 2. structlog configuration (stdlib bridge)
    structlog.configure(
        processors=_PRE_CHAIN + [structlog.processors.JSONRenderer()],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


# ---------------------------------------------------------------------------
# Execution-ID helpers


def bind_execution_id_to_root_logger(execution_id: str) -> None:  # noqa: D401
    """Expose *execution_id* to all loggers via contextvars.

    Because :func:`setup_json_logging` adds
    :pyfunc:`structlog.contextvars.merge_contextvars` to every log call, simply
    binding the variable once is enough – all subsequent log records will
    contain it automatically.
    """

    bind_contextvars(execution_id=execution_id)

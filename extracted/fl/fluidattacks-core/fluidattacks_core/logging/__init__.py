from __future__ import annotations

import logging
import logging.config
import sys
from typing import TYPE_CHECKING

from fluidattacks_core.logging.presets import DATE_FORMAT, PRODUCT_LOGGING
from fluidattacks_core.logging.sources.utils import (
    set_commit_ref_name,
    set_commit_sha,
    set_product_environment,
    set_product_id,
    set_product_version,
)
from fluidattacks_core.logging.utils import set_telemetry_metadata

if TYPE_CHECKING:
    from logging.config import _DictConfigArgs
    from types import TracebackType


def init_uncaught_exception_logging() -> None:
    logger = logging.getLogger("unhandled")

    def handle_uncaught_exception(
        exception_type: type[BaseException],
        msg: BaseException,
        traceback: TracebackType | None,
    ) -> None:
        if issubclass(exception_type, KeyboardInterrupt):
            sys.__excepthook__(exception_type, msg, traceback)
            return

        logger.critical(
            "Uncaught exception",
            exc_info=(exception_type, msg, traceback),
        )

    sys.excepthook = handle_uncaught_exception


def init_logging(preset: _DictConfigArgs | None = None) -> None:
    logging.config.dictConfig(preset or PRODUCT_LOGGING)
    init_uncaught_exception_logging()


__all__ = [
    "DATE_FORMAT",
    "PRODUCT_LOGGING",
    "init_logging",
    "init_uncaught_exception_logging",
    "set_commit_ref_name",
    "set_commit_sha",
    "set_product_environment",
    "set_product_id",
    "set_product_version",
    "set_telemetry_metadata",
]

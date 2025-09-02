#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

from pendingai.abc import Singleton

LOGGER_NAME: str = "pendingai"
LOGGER_FORMATTER: str = (
    "[%(name)s] %(asctime)s - %(levelname)s "
    "[%(filename)s:%(funcName)s:%(lineno)s] %(message)s"
)


class Logger(Singleton):
    _logfile: str = "pai.log"
    _logfile_size: int = int(5 * 1e6)
    _logfile_backups: int = 3
    _console_handler: logging.StreamHandler | None = None

    def _initialize(self, level: int | str = logging.WARNING) -> None:
        """
        Initialize singleton logger configuration called on setup.
        """
        self._logger: logging.Logger = logging.getLogger(LOGGER_NAME)
        self._logger.setLevel(level)
        self._logger.propagate = False

        # setup rotating file logger for debugging purposes and helping
        # when a user encounters runtime errors and need to submit bug reports
        if not self._logger.handlers:
            formatter = logging.Formatter(LOGGER_FORMATTER)

            # Create console handler but do not add it by default.
            self._console_handler = logging.StreamHandler()
            self._console_handler.setFormatter(formatter)

            # Create and add the file handler.
            log_file_path = Path.home() / ".pendingai" / self._logfile
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=self._logfile_size,
                backupCount=self._logfile_backups,
            )
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    def enable_console_logging(self) -> None:
        """Adds the console handler to the logger."""
        if self._console_handler and self._console_handler not in self._logger.handlers:
            self._logger.addHandler(self._console_handler)

    def get_logger(self) -> logging.Logger:
        """
        Retrieve singleton formatter logger instance.
        """
        return self._logger

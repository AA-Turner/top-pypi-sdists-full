import importlib.metadata
import platform
from bisect import bisect
import json
import logging
from logging import Formatter, LogRecord
import sys
from typing import Any, Dict, Callable
import time

from .commands.global_options import GlobalOptions
from .ui import is_interactive


_namespace: str | None = None


def set_namespace(namespace: str | None) -> None:
    global _namespace
    _namespace = namespace


_table: str | None = None


def set_table(table: str | None) -> None:
    global _table
    _table = table


class LevelFormatter(Formatter):
    def __init__(self, formats: Dict[int, str], **kwargs: Any) -> None:
        super().__init__()

        if "fmt" in kwargs:
            raise ValueError("format string to be passed to level-surrogate formatters")

        self.formats = sorted(
            (level, Formatter(fmt, **kwargs)) for level, fmt in formats.items()
        )

    def format(self, record: LogRecord) -> str:
        idx = bisect(self.formats, (record.levelno,), hi=len(self.formats) - 1)
        level, formatter = self.formats[idx]
        return formatter.format(record)


class JsonFormatter(Formatter):
    def __init__(self, datefmt: str = "%Y-%m-%dT%H:%M:%SZ") -> None:
        super().__init__()
        self.datefmt = datefmt
        self.converter = time.gmtime  # Use UTC for time conversion

    def format(self, record: LogRecord) -> str:
        log_record_dict = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
            "logger_name": record.name,
            "filename": record.filename,
            "module": record.module,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "dap_namespace": getattr(record, "dap_namespace", None),
            "dap_table": getattr(record, "dap_table", None),
            "dap_client_id": getattr(record, "dap_client_id", None),
        }
        if record.exc_text:
            log_record_dict["exc_text"] = record.exc_text
        if record.exc_info:
            log_record_dict["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_record_dict["stack_info"] = self.formatStack(record.stack_info)
        return json.dumps(log_record_dict)


def create_dap_logger_factory(global_options: GlobalOptions) -> Callable[..., logging.LogRecord]:
    """
    Create a custom log record factory where we add custom attributes to the log record.
    """
    default_factory = logging.getLogRecordFactory()
    def dap_record_factory(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> logging.LogRecord:
        record = default_factory(*args, **kwargs)
        record.dap_namespace = _namespace
        record.dap_table = _table
        record.dap_client_id = getattr(global_options, "client_id", None)
        return record
    return dap_record_factory

def create_log_formatter(global_options: GlobalOptions) -> logging.Formatter:
    if global_options.logformat == "json":
        return JsonFormatter()
    else:
        default_format = "%(asctime)s - %(levelname)s - %(message)s"
        debug_format = default_format + " (%(filename)s:%(lineno)d)"
        return LevelFormatter(
            {
                logging.DEBUG: debug_format,
                logging.INFO: default_format,
            }
        )

def setup_logging(global_options: GlobalOptions) -> None:
    logging.setLogRecordFactory(create_dap_logger_factory(global_options))
    logging.basicConfig(level=getattr(logging, global_options.loglevel.upper(), logging.INFO))
    log_formatter = create_log_formatter(global_options)
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    root_logger.addHandler(logging.NullHandler())
    if not is_interactive() and global_options.log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)
    if global_options.logfile:
        file_handler = logging.FileHandler(global_options.logfile, "a")
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

def configure_logging(level: str = "INFO", format: str = "plain",
                      file: str | None = None, log_to_console: bool = True,
                      namespace: str | None = None, table: str | None = None, client_id: str | None = None) -> None:
    setup_logging(GlobalOptions(loglevel=level, logformat=format, logfile=file, log_to_console=log_to_console,
                                namespace=namespace, table=table, client_id=client_id))


def log_system_info() -> None:
    logger = logging.getLogger("dap")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.uname().system} {platform.uname().release} {platform.uname().machine}")
    installed_packages = importlib.metadata.distributions()
    filter_packages = [
        "instructure-dap-client",
        "aiohttp",
        "aiohttp-retry",
        "aiofiles",
        "types-aiofiles",
        "json_strong_typing",
        "pysqlsync",
        "PyJWT",
        "tsv2py",
    ]
    dependency_versions = {
        pkg.metadata["Name"]: pkg.version
        for pkg in installed_packages
        if pkg.metadata["Name"] in filter_packages
    }
    logger.info(f"Package versions: {dependency_versions}")

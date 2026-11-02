"""Core functionality for Logscope."""

import logging
import sqlite3
from datetime import datetime

from typing import Callable

from logscope.handlers import SQLiteHandler
from logscope.formatter import LogscopeFormatter
from logscope.utils import CallingDetailsFilter

def logger(
    db_path: str = 'logscope.db',
    style: str = 'colorful',
    name: str = None,
    level: int = logging.DEBUG
) -> Callable:
    """
    Create a logger with SQLite storage and pretty console output.
    
    Args:
        db_path: Path to SQLite database file
        style: Output style ('colorful' or 'plain')
        name: Optional logger name (defaults to timestamped name)
        level: Logging level (defaults to DEBUG)
        
    Returns:
        Logging function that takes arbitrary arguments
    """
    logger_name = name or f"Logscope_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.handlers = []
    
    # Add the filter that adds calling details to records
    calling_details_filter = CallingDetailsFilter()
    logger.addFilter(calling_details_filter)

    if db_path:
        sqlite_handler = SQLiteHandler(db_path)
        logger.addHandler(sqlite_handler)

    console_handler = logging.StreamHandler()
    console_formatter = LogscopeFormatter(style=style)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    def log(*args):
        logger.debug(" ".join(map(str, args)))

    log._logger = logger
    log._db_path = db_path
    return log

def query(sql: str = '', db_path: str = 'logscope.db') -> list[dict]:
    """
    Retrieve logscope logs from the SQLite database at `db_path`.
    """
    sql = sql or "SELECT * FROM logs"
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    return [dict(row) for row in rows]
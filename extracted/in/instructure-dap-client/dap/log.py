from bisect import bisect
from logging import Formatter, LogRecord
from typing import Any, Dict


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

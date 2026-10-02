from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

_RECORD_FIELDS = frozenset(logging.makeLogRecord({}).__dict__) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    """Emit one JSON object per line using fields recognized by Chalk's log collector."""

    def format(self, record: logging.LogRecord) -> str:
        fields: dict[str, Any] = {key: value for key, value in vars(record).items() if key not in _RECORD_FIELDS}
        fields.update(
            timestamp=datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            severity=record.levelname,
            logger=record.name,
            message=record.getMessage(),
        )
        # Keep tracebacks out of the message and escape their newlines so the collector sees one event.
        if record.exc_info:
            fields["exception.stacktrace"] = self.formatException(record.exc_info)
        elif record.exc_text:
            fields["exception.stacktrace"] = record.exc_text
        if record.stack_info:
            fields["stack_info"] = self.formatStack(record.stack_info)
        return json.dumps(fields, default=str)

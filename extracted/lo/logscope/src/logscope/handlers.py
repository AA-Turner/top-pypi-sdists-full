import logging
from logscope.database import LogscopeDatabase
from logscope.utils import format_timestamp_with_milliseconds

class SQLiteHandler(logging.Handler):
    """Handler that writes log records to a SQLite database."""
    
    def __init__(self, db_path='logscope.db'):
        super().__init__()
        self.db = LogscopeDatabase(db_path)

    def emit(self, record):
        self.db.write_log({
            'timestamp': format_timestamp_with_milliseconds(record),
            'message': record.getMessage(),
            'filename': record.pathname,
            'lineno': record.lineno,
            'source': getattr(record, 'source', None),
            'function': getattr(record, 'function', None),
            'event_type': getattr(record, 'event_type', 'log'),
        })

    def close(self):
        self.db.close()
        super().close()
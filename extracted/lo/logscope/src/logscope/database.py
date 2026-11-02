"""Database operations for Logscope."""

import sqlite3
import threading
from datetime import datetime
from typing import Any, Dict

class LogscopeDatabase:
    """Handles database operations for Logscope."""
    
    def __init__(self, db_path: str = 'logscope.db'):
        self.db_path = db_path
        self._local = threading.local()
        self.run_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    def _get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.cursor = self._local.connection.cursor()
            
            self._local.cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run TEXT,
                    timestamp TEXT,
                    message TEXT,
                    filename TEXT,
                    lineno INTEGER,
                    source TEXT,
                    function TEXT,
                    event_type TEXT
                )
            """)
            self._local.connection.commit()

        return self._local.connection, self._local.cursor

    def write_log(self, entry: Dict[str, Any]):
        """
        Write a log entry to the database.
        
        Args:
            entry: Dictionary containing log entry fields
        """
        connection, cursor = self._get_connection()
        
        cursor.execute(
            """INSERT INTO logs 
               (run, timestamp, message, filename, lineno, source, function, event_type) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                self.run_id,
                entry.get('timestamp'),
                entry.get('message'),
                entry.get('filename'),
                entry.get('lineno'),
                entry.get('source'),
                entry.get('function'),
                entry.get('event_type')
            )
        )
        connection.commit()

    def close(self):
        """Close the database connection."""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            del self._local.connection

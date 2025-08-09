# src/canonmap/logger.py

import json
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from rich.logging import RichHandler
from rich.text import Text

load_dotenv(override=True)

ENV = os.getenv("ENV", "dev").lower().strip()

# --- Configuration for Rich Handler ---
LEVEL_COLORS = {
    "debug": "cyan",
    "info": "green",
    "warning": "yellow",
    "error": "red",
    "critical": "bold red"
}
MAX_PATH_DISPLAY_LEN = 40

# --- Handler for Development (Human-Readable) ---
class TruncatingRichHandler(RichHandler):
    """
    RichHandler that truncates file paths intelligently for development consoles.
    """
    def render_message(self, record, message: str) -> Text:
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        level = f"{record.levelname:<8}"
        path = self.truncate_path(record.pathname)
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append(level, style="bold blue")
        text.append(" ")
        text.append_text(path)
        text.append(": ")
        level_key = record.levelname.lower()
        message_style = LEVEL_COLORS.get(level_key)
        if message_style:
            text.append(message, style=message_style)
        else:
            text.append(message)
        return text

    def truncate_path(self, full_path: str) -> Text:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        rel_path = os.path.relpath(full_path, start=project_root) if full_path.startswith(project_root) else full_path
        parts = rel_path.split(os.sep)
        text = Text()
        if len(parts) == 1:
            text.append(parts[0], style="bold magenta")
            return text
        first, last = parts[0], parts[-1]
        reserved = len(first) + len(last) + len("...") + 2
        kept, length = [], 0
        for p in parts[1:-1]:
            seg_len = len(p) + 1
            if length + seg_len + reserved > MAX_PATH_DISPLAY_LEN:
                break
            kept.append(p)
            length += seg_len
        text.append(first, style="bold cyan")
        for part in kept:
            text.append(f".{part}", style="cyan")
        text.append("...", style="dim")
        text.append(f".{last}", style="bold magenta")
        return text

# --- Formatter for Production (Machine-Readable JSON) ---
class JsonFormatter(logging.Formatter):
    """Formats log records as a single-line JSON string for Cloud Logging."""
    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": self.formatTime(record, self.datefmt),
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger_name": record.name,
            "pathname": record.pathname,
            "lineno": record.lineno,
        }
        if record.exc_info:
            log_object['exception'] = self.formatException(record.exc_info)
        
        # This handles messages that are already JSON strings (from structured logging calls)
        try:
            # If the message is a valid JSON string, parse it and merge it
            msg_data = json.loads(record.getMessage())
            if isinstance(msg_data, dict):
                log_object['message'] = msg_data.pop('message', record.getMessage())
                log_object.update(msg_data)
        except (json.JSONDecodeError, TypeError):
            pass # Message is just a plain string

        return json.dumps(log_object)

# --- Handler Factory with Conditional Logic ---
def make_console_handler(level: str = "INFO", set_root: bool = False) -> logging.Handler:
    """
    Factory that returns a RichHandler for 'dev' environments
    and a JSON handler for the 'prod' environment.
    """
    # Check the environment variable to decide the format
    if ENV == "prod":
        # ☁️ In Production: Use the JSON formatter for Google Cloud Logging
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
    else:
        # 💻 In Development (or if ENV is not set): Use the nice Rich handler
        handler = TruncatingRichHandler(show_time=False, markup=True)

    handler.setLevel(level)
    if set_root:
        root = logging.getLogger()
        root.handlers.clear()
        root.addHandler(handler)
        root.setLevel(level)

    return handler
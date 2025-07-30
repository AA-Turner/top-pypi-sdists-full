# canonmap/utils/logger.py

import logging
import os
from rich.logging import RichHandler
from rich.text import Text
from datetime import datetime

LEVEL_COLORS = {
    "debug": "cyan",
    "info": "green",
    "warning": "yellow",
    "error": "red",
    "critical": "bold red"
}

MAX_PATH_DISPLAY_LEN = 40  # max characters for dotted paths

class TruncatingRichHandler(RichHandler):
    """
    RichHandler that truncates file paths intelligently and styles them:
    - First segment in bold cyan
    - Middle segments in cyan
    - Ellipsis in dim
    - Final segment (filename) in bold magenta
    """
    def render_message(self, record, message: str) -> Text:
        # Format timestamp and level
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        level = f"{record.levelname:<8}"

        # Build the styled log message
        path = self.truncate_path(record.pathname)
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append(level, style="bold blue")
        text.append(" ")
        text.append_text(path)
        text.append(": ")
        # apply level-based style to message
        level_key = record.levelname.lower()
        message_style = LEVEL_COLORS.get(level_key)
        if message_style:
            text.append(message, style=message_style)
        else:
            text.append(message)
        return text

    def truncate_path(self, full_path: str) -> Text:
        # Compute project root two levels above this file
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        rel_path = os.path.relpath(full_path, start=project_root) if full_path.startswith(project_root) else full_path

        parts = rel_path.split(os.sep)
        text = Text()
        if len(parts) == 1:
            text.append(parts[0], style="bold magenta")
            return text

        # Otherwise, truncate middle segments
        first, last = parts[0], parts[-1]
        reserved = len(first) + len(last) + len("...") + 2  # two dots around ellipsis

        kept, length = [], 0
        for p in parts[1:-1]:
            seg_len = len(p) + 1
            if length + seg_len + reserved > MAX_PATH_DISPLAY_LEN:
                break
            kept.append(p)
            length += seg_len

        # Build styled truncated path
        text.append(first, style="bold cyan")
        for part in kept:
            text.append(f".{part}", style="cyan")
        text.append("...", style="dim")
        text.append(f".{last}", style="bold magenta")
        return text

def make_console_handler(level: str = "INFO", set_root: bool = False) -> logging.Handler:
    """
    Factory for TruncatingRichHandler. Application code should:
        import logging
        from canonmap.utils.logger import make_console_handler

        handler = make_console_handler("DEBUG", set_root=True)
    """
    handler = TruncatingRichHandler(show_time=False, markup=True)
    handler.setLevel(level)
    if set_root:
        root = logging.getLogger()
        root.handlers.clear()
        root.addHandler(handler)
        root.setLevel(level)
    return handler
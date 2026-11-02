import logging
import textwrap
from logscope.utils import get_calling_details, format_timestamp_with_milliseconds
from datetime import datetime


class LogscopeFormatter(logging.Formatter):
    """Formatter that creates detailed, optionally colored log output."""
    
    COLOR_MAP = {
        'white': "\033[37m",
        'yellow': "\033[33m",
        'cyan': "\033[36m",
        'faded_gray': "\033[90m",
        'faded_green': "\033[38;2;2;50;2m",
    }
    
    def __init__(self, style='colorful'):
        super().__init__()
        self.style = style
        self.last_logged_times = {}
    
    def color(self, name: str, text: str) -> str:
        """Apply ANSI color to text if style is 'colorful'."""
        if self.style != 'colorful':
            return text
        start_color = self.COLOR_MAP[name]
        reset = "\033[0m"
        return f"{start_color}{text}{reset}"
    
    def format(self, record: logging.LogRecord) -> str:
        source, function, pathname, lineno = get_calling_details(record)
        timestamp = format_timestamp_with_milliseconds(record)
        message = record.getMessage()

        # Calculate the time difference
        current_time = datetime.fromtimestamp(record.created)
        last_time = self.last_logged_times.get(record.name, current_time)
        time_diff = (current_time - last_time).total_seconds()
        self.last_logged_times[record.name] = current_time

        time_diff_str = ""
        if 0 < time_diff < 1e-3:
            time_diff_str = f"(+{int(time_diff*1e6)}µs)"
        elif 1e-3 <= time_diff < 1:
            time_diff_str = f"(+{int(time_diff*1e3)}ms)"
        elif 1 <= time_diff < 60:
            time_diff_str = f"(+{time_diff:.3f}s)"
        elif 60 <= time_diff:
            time_diff_str = f"(+{time_diff/60:.3f}m)"
        timestamp_colored = self.color('faded_green', f"{timestamp} {time_diff_str}")
        if not message.endswith("\n"):
            message += "\n"
        message_colored = self.color('yellow', message)
        filename_colored = self.color('faded_gray', pathname)
        lineno_colored = self.color('faded_gray', str(lineno))
        function_colored = self.color('cyan', function)
        calling_expression = self.color('cyan', source)

        return message_colored + textwrap.dedent(f"""
              ⋅ {timestamp_colored}
              ⋅ {function_colored}:{calling_expression}
              ⋅ {filename_colored}:{lineno_colored}
        """).strip() + "\n"

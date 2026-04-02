import logging
import time

log_format = (
    "{"
    '"timestamp": "%(asctime)s", '
    '"level": "%(levelname)s", '
    '"message": "%(message)s", '
    '"method_path": "%(method_path)s", '
    '"mem_changes": "%(mem_changes)s", '
    '"time_spent": "%(time_spent)s", '
    '"log_source": "%(log_source)s", '
    '"cumulative_time_spent": "%(cumulative_time_spent)s"'
    "}"
)


class UTCFormatter(logging.Formatter):
    """Formatter that uses UTC time instead of local time."""

    converter = time.gmtime


class ConsoleFormatter(logging.Formatter):
    def format(self, record):
        base_message = f">>> {self.formatTime(record)} - {record.levelname} - {record.getMessage()}:\n"
        details = ""
        if getattr(record, "mem_changes", ""):
            details += f"  - Memory Changing: {record.mem_changes}\n"
        if getattr(record, "time_spent", ""):
            details += f"  - Time Spent in method itself: {record.time_spent}\n"
        if getattr(record, "cumulative_time_spent", ""):
            details += f"  - Cumulative Time Spent: {record.cumulative_time_spent}\n"
        if getattr(record, "method_path", ""):
            details += f"  - {record.method_path}"

        return base_message + details

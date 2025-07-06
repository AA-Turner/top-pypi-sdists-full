import logging
import sys
from typing import Optional


# Add SUCCESS level for custom logging
SUCCESS = 25  # Between INFO (20) and WARNING (30)
logging.addLevelName(SUCCESS, 'SUCCESS')


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter for canonmap loggers with colorized output and aligned columns.
    Only used for canonmap loggers, not the root logger or other libraries.
    """
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[90m',     # Gray
        'SUCCESS': '\033[92m',  # Bright Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m',     # Reset
        'NAME': '\033[94m',     # Blue for logger name
    }
    
    def format(self, record):
        # Get the original format
        log_message = super().format(record)
        
        # Add colors and pipe separators
        level_color = self.COLORS.get(record.levelname, '')
        name_color = self.COLORS['NAME']
        reset = self.COLORS['RESET']
        
        # Split the message and add colors
        parts = log_message.split(' - ')
        if len(parts) >= 4:
            timestamp, name, level, message = parts[0], parts[1], parts[2], ' - '.join(parts[3:])
            level_padded = level.ljust(9)  # Pad to 9 characters
            name_width = 30
            name_parts = name.split('.')
            if len(name_parts) > 2:
                first = name_parts[0]
                last = name_parts[-1]
                display = f"{first}...{last}"
                if len(display) > name_width:
                    # Truncate last part with ellipsis if needed
                    max_last_len = name_width - len(first) - 6  # 3 for ... and 3 for ...
                    if max_last_len > 0:
                        last_trunc = last[:max_last_len] + '...'
                        display = f"{first}...{last_trunc}"
                    else:
                        display = (first + '...')[:name_width]
                name_display = display.ljust(name_width)
            else:
                # 1 or 2 parts, just join and pad/ellipsis
                joined = '.'.join(name_parts)
                if len(joined) > name_width:
                    name_display = joined[:name_width-3] + '...'
                else:
                    name_display = joined.ljust(name_width)
            formatted = f"{level_color}{level_padded}{reset} {name_color}{name_display}{reset} | {message}"
        else:
            # Fallback if format doesn't match expected
            formatted = f"{level_color}{log_message}{reset}"
        
        return formatted


class SuccessLogger(logging.Logger):
    """
    Logger class for canonmap that adds a .success() method for SUCCESS level logs.
    """
    
    def success(self, msg, *args, **kwargs):
        """Log a success message."""
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)


# Register the custom logger class for canonmap loggers
logging.setLoggerClass(SuccessLogger)


def setup_logger(name: Optional[str] = None, level: Optional[int] = None) -> SuccessLogger:
    """
    Set up and return a canonmap logger with colored output and a SUCCESS log level.
    This function only attaches handlers/formatters to canonmap loggers (never the root logger).
    
    Args:
        name: Logger name (defaults to caller's module name if None)
        level: Optional log level to set for this logger (does not affect parent/root loggers)
    Returns:
        A canonmap SuccessLogger instance with custom formatting and SUCCESS support.
    
    Usage (in any canonmap module):
        from canonmap.logger import setup_logger
        logger = setup_logger(__name__)
    
    Best practice:
        - Do NOT use logging.basicConfig() in your library.
        - Do NOT attach handlers to the root logger in your library.
        - Let the application control the log level globally if desired:
            import logging
            logging.getLogger('canonmap').setLevel(logging.INFO)
    """
    if name is None:
        # Get the calling module's name
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'canonmap')
    
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # Prevent duplicate logs from root logger
    # Only set the level if explicitly requested
    if level is not None:
        logger.setLevel(level)
    
    return logger 
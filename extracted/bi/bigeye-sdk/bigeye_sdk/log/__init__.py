import logging
from typer import style


def get_logger(logger_name: str) -> logging.Logger:
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)

    # Only add handler if the logger doesn't already have one
    # This prevents duplicate log messages when get_logger is called multiple times
    if not log.handlers:
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # add formatter to ch
        ch.setFormatter(CustomFormatter())

        # add ch to logger
        log.addHandler(ch)

    return log


class CustomFormatter(logging.Formatter):
    msg_format = '%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s'

    FORMATS = {
        logging.DEBUG: style(msg_format, fg="cyan"),
        logging.INFO: msg_format,
        logging.WARNING: style(msg_format, fg="yellow"),
        logging.ERROR: style(msg_format, fg="red"),
        logging.CRITICAL: style(msg_format, fg="red", bold=True),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

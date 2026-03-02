import logging

SPAM: int = 5
VERBOSE: int = 15
NOTICE: int = 25
SUCCESS: int = 35

# noinspection PyTypeHints
logging.SPAM: int = SPAM  # type: ignore
# noinspection PyTypeHints
logging.VERBOSE: int = VERBOSE  # type: ignore
# noinspection PyTypeHints
logging.NOTICE: int = NOTICE  # type: ignore
# noinspection PyTypeHints
logging.SUCCESS: int = SUCCESS  # type: ignore

logging._levelToName[logging.SPAM] = "SPAM"  # type: ignore
logging._levelToName[logging.VERBOSE] = "VERBOSE"  # type: ignore
logging._levelToName[logging.NOTICE] = "NOTICE"  # type: ignore
logging._levelToName[logging.SUCCESS] = "SUCCESS"  # type: ignore

logging._nameToLevel["SPAM"] = logging.SPAM  # type: ignore
logging._nameToLevel["VERBOSE"] = logging.VERBOSE  # type: ignore
logging._nameToLevel["NOTICE"] = logging.NOTICE  # type: ignore
logging._nameToLevel["SUCCESS"] = logging.SUCCESS  # type: ignore


def get_log_level_from_str(log_level_str: str) -> int:
    """
    gets the log level as integer from a string


    >>> assert get_log_level_from_str('42') == 42
    >>> assert get_log_level_from_str('info') == 20
    >>> get_log_level_from_str('unknown')
    Traceback (most recent call last):
        ...
    ValueError: can not detect log level from string "unknown"

    """

    try:
        log_level = int(log_level_str)
        return log_level
    except ValueError:
        pass

    try:
        log_level = logging._nameToLevel[log_level_str.upper()]  # noqa
        return log_level
    except KeyError:
        raise ValueError(f'can not detect log level from string "{log_level_str}"')

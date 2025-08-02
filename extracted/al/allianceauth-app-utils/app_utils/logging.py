"""Utilities for logging."""

import logging


class LoggerAddTag(logging.LoggerAdapter):
    """adds a custom prefix to the given logger

    Example:

        .. code-block:: python

            import logging
            from app_utils.logging import LoggerAddTag

            logger = LoggerAddTag(logging.getLogger(__name__), __package__)

    """

    def __init__(self, my_logger, prefix):
        """:meta private:"""
        super().__init__(my_logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        """:meta private:"""
        return (
            "[%s] %s" % (self.prefix, msg),  # pylint: disable=consider-using-f-string
            kwargs,
        )


logger = LoggerAddTag(logging.getLogger(__name__), __package__)


def make_logger_prefix(tag: str):
    """creates a function to add logger prefixes, which returns tag when used empty"""
    return lambda text="": f'{tag}{(": " + text) if text else ""}'

"""Utility functions and classes for Eve Universe."""

import logging
import socket
from typing import Any, Optional

from django.conf import settings
from django.test import TestCase

# Format for output of datetime for this app
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class LoggerAddTag(logging.LoggerAdapter):
    """add custom tag to a logger"""

    def __init__(self, my_logger, prefix):
        super().__init__(my_logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return f"[{self.prefix}] {msg}", kwargs


logger = LoggerAddTag(logging.getLogger(__name__), __package__)


def chunks(lst, size):
    """Yield successive sized chunks from lst."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def clean_setting(
    name: str,
    default_value: Any,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    required_type: Optional[type] = None,
    choices: Optional[list] = None,
):
    """cleans the input for a custom setting

    Will use `default_value` if settings does not exit or has the wrong type
    or is outside define boundaries (for int only)

    Need to define `required_type` if `default_value` is `None`

    Will assume `min_value` of 0 for int (can be overridden)

    Returns cleaned value for setting
    """
    if default_value is None and not required_type:
        raise ValueError("You must specify a required_type for None defaults")

    if not required_type:
        required_type = type(default_value)

    if min_value is None and required_type == int:
        min_value = 0

    if not hasattr(settings, name):
        cleaned_value = default_value
    else:
        dirty_value = getattr(settings, name)
        # pylint: disable = too-many-boolean-expressions
        if (
            required_type
            and isinstance(dirty_value, required_type)
            and (min_value is None or dirty_value >= min_value)
            and (max_value is None or dirty_value <= max_value)
            and (choices is None or dirty_value in choices)
        ):
            cleaned_value = dirty_value
        else:
            logger.warning(
                "Your setting for %s it not valid. Please correct it. "
                "Using default for now: %s",
                name,
                default_value,
            )
            cleaned_value = default_value
    return cleaned_value


class SocketAccessError(Exception):
    """Custom exception for NoSocketsTestCase."""


class NoSocketsTestCase(TestCase):
    """Variation of TestCase class that prevents any use of sockets"""

    @classmethod
    def setUpClass(cls):
        """:private:"""
        cls.socket_original = socket.socket
        socket.socket = cls.guard
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """:private:"""
        socket.socket = cls.socket_original
        return super().tearDownClass()

    @staticmethod
    def guard(*args, **kwargs):
        """:private:"""
        raise SocketAccessError("Attempted to access network")

"""Improvement of the Django message class."""

from django.contrib import messages
from django.http import HttpRequest
from django.utils.safestring import mark_safe


# pylint: disable=invalid-name
class messages_plus:
    """Improvement of default Django messages with implicit HTML support."""

    @classmethod
    def debug(cls, request: HttpRequest, message: str, *args, **kwargs) -> None:
        """Send a debug message with HTML support. Use with safe strings only!"""
        messages.debug(request, mark_safe(message), *args, **kwargs)

    @classmethod
    def info(cls, request: HttpRequest, message: str, *args, **kwargs) -> None:
        """Send an info message with HTML support. Use with safe strings only!"""
        messages.info(request, mark_safe(message), *args, **kwargs)

    @classmethod
    def success(cls, request: HttpRequest, message: str, *args, **kwargs) -> None:
        """Send a success message with HTML support. Use with safe strings only!"""
        messages.success(request, mark_safe(message), *args, **kwargs)

    @classmethod
    def warning(cls, request: HttpRequest, message: str, *args, **kwargs) -> None:
        """Send a warning message with HTML support. Use with safe strings only!"""
        messages.warning(request, mark_safe(message), *args, **kwargs)

    @classmethod
    def error(cls, request: HttpRequest, message: str, *args, **kwargs) -> None:
        """Send an error message with HTML support. Use with safe strings only!"""
        messages.error(request, mark_safe(message), *args, **kwargs)

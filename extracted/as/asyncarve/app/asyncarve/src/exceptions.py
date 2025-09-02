"""Exceptions for Arve"""


class ArveError(Exception):
    """Generic Arve exception"""


class ArveConnectionError(ArveError):
    """Arve connection exception"""


class ArveUnathorizedError(ArveError):
    """Arve unauthorized exception"""

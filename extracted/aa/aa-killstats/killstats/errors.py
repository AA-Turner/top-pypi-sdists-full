"""Custom exceptions for Killstats."""


class ObjectNotFound(Exception):
    """Custom exception to indicate that an object was not found."""


class DownTimeError(Exception):
    """Custom exception to indicate ESI is in daily downtime."""

"""Exceptions for Efergy API Python client."""


class DataError(Exception):
    """When a data error is encountered."""


class ConnectError(Exception):
    """The request timed out while trying to connect to the remote server."""


class InvalidAuth(Exception):
    """The provided API token is invalid."""


class InvalidPeriod(Exception):
    """The provided duration period is invalid."""


class InvalidOffset(Exception):
    """The provided UTC offset is invalid."""


class InvalidCurrency(Exception):
    """The provided UTC offset is invalid."""


class ServiceError(Exception):
    """The was an error getting data from the hub."""


class APICallLimit(Exception):
    """The was an error getting data from the hub."""

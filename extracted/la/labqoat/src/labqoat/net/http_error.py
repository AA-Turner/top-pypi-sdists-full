"""A request that got no complete answer."""


class HttpError(Exception):
    """The connection could not be opened, broke, or answered with something that is not HTTP/1.1."""

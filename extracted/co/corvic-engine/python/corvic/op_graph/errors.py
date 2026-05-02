"""Corvic table specific errors."""

from corvic.result import Error


class OpParseError(Error):
    """Raised when parsing an op encounters a problem."""

"""Module for handling exceptions."""

from pydantic import ValidationError


class PydValErrInfo:
    """Extract information from pydantic ValidationError."""

    @staticmethod
    def error_msg(e: ValidationError) -> str:
        """Error message from pydantic ValidationError."""
        return e.errors()[0]["ctx"]["error"]

    @staticmethod
    def input(e: ValidationError) -> str:
        """Input value, as it is read by, pydantic ValidationError."""
        return e.errors()[0]["input"]

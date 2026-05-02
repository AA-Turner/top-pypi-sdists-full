# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["StreamChunk"]


class StreamChunk(BaseModel):
    """A single log line from the build process."""

    line: str
    """The log line content"""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["TimeIntervalObject"]


class TimeIntervalObject(BaseModel):
    confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the interval."""

    duration: Optional[float] = None
    """The duration (in seconds) of the time interval."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    start: Optional[float] = None
    """The starting point (in seconds) of the time interval."""

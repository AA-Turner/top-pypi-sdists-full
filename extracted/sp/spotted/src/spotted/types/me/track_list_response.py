# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel
from ..shared.track_object import TrackObject

__all__ = ["TrackListResponse"]


class TrackListResponse(BaseModel):
    added_at: Optional[datetime] = None
    """
    The date and time the track was saved. Timestamps are returned in ISO 8601
    format as Coordinated Universal Time (UTC) with a zero offset:
    YYYY-MM-DDTHH:MM:SSZ. If the time is imprecise (for example, the date/time of an
    album release), an additional field indicates the precision; see for example,
    release_date in an album object.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    track: Optional[TrackObject] = None
    """Information about the track."""

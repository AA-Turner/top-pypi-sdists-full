# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .shared.audiobook_base import AudiobookBase
from .simplified_chapter_object import SimplifiedChapterObject

__all__ = ["AudiobookRetrieveResponse", "AudiobookRetrieveResponseChapters"]


class AudiobookRetrieveResponseChapters(BaseModel):
    """The chapters of the audiobook."""

    href: str
    """A link to the Web API endpoint returning the full result of the request"""

    limit: int
    """
    The maximum number of items in the response (as set in the query or by default).
    """

    next: Optional[str] = None
    """URL to the next page of items. ( `null` if none)"""

    offset: int
    """The offset of the items returned (as set in the query or by default)"""

    previous: Optional[str] = None
    """URL to the previous page of items. ( `null` if none)"""

    total: int
    """The total number of items available to return."""

    items: Optional[List[SimplifiedChapterObject]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class AudiobookRetrieveResponse(AudiobookBase):
    chapters: AudiobookRetrieveResponseChapters
    """The chapters of the audiobook."""

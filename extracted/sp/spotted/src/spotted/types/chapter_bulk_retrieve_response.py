# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .shared.image_object import ImageObject
from .shared.audiobook_base import AudiobookBase
from .shared.external_url_object import ExternalURLObject
from .shared.resume_point_object import ResumePointObject
from .shared.chapter_restriction_object import ChapterRestrictionObject

__all__ = ["ChapterBulkRetrieveResponse", "Chapter"]


class Chapter(BaseModel):
    id: str
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    chapter.
    """

    audio_preview_url: Optional[str] = None
    """A URL to a 30 second preview (MP3 format) of the chapter.

    `null` if not available.
    """

    audiobook: AudiobookBase
    """The audiobook for which the chapter belongs."""

    chapter_number: int
    """The number of the chapter"""

    description: str
    """A description of the chapter.

    HTML tags are stripped away from this field, use `html_description` field in
    case HTML tags are needed.
    """

    duration_ms: int
    """The chapter length in milliseconds."""

    explicit: bool
    """
    Whether or not the chapter has explicit content (true = yes it does; false = no
    it does not OR unknown).
    """

    external_urls: ExternalURLObject
    """External URLs for this chapter."""

    href: str
    """A link to the Web API endpoint providing full details of the chapter."""

    html_description: str
    """A description of the chapter. This field may contain HTML tags."""

    images: List[ImageObject]
    """The cover art for the chapter in various sizes, widest first."""

    is_playable: bool
    """True if the chapter is playable in the given market. Otherwise false."""

    languages: List[str]
    """
    A list of the languages used in the chapter, identified by their
    [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639) code.
    """

    name: str
    """The name of the chapter."""

    release_date: str
    """The date the chapter was first released, for example `"1981-12-15"`.

    Depending on the precision, it might be shown as `"1981"` or `"1981-12"`.
    """

    release_date_precision: Literal["year", "month", "day"]
    """The precision with which `release_date` value is known."""

    type: Literal["episode"]
    """The object type."""

    uri: str
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    chapter.
    """

    available_markets: Optional[List[str]] = None
    """
    A list of the countries in which the chapter can be played, identified by their
    [ISO 3166-1 alpha-2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    restrictions: Optional[ChapterRestrictionObject] = None
    """Included in the response when a content restriction is applied."""

    resume_point: Optional[ResumePointObject] = None
    """The user's most recent position in the chapter.

    Set if the supplied access token is a user token and has the scope
    'user-read-playback-position'.
    """


class ChapterBulkRetrieveResponse(BaseModel):
    chapters: List[Chapter]

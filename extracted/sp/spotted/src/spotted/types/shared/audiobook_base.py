# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .image_object import ImageObject
from .author_object import AuthorObject
from .narrator_object import NarratorObject
from .copyright_object import CopyrightObject
from .external_url_object import ExternalURLObject

__all__ = ["AudiobookBase"]


class AudiobookBase(BaseModel):
    id: str
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    audiobook.
    """

    authors: List[AuthorObject]
    """The author(s) for the audiobook."""

    available_markets: List[str]
    """
    A list of the countries in which the audiobook can be played, identified by
    their [ISO 3166-1 alpha-2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
    code.
    """

    copyrights: List[CopyrightObject]
    """The copyright statements of the audiobook."""

    description: str
    """A description of the audiobook.

    HTML tags are stripped away from this field, use `html_description` field in
    case HTML tags are needed.
    """

    explicit: bool
    """
    Whether or not the audiobook has explicit content (true = yes it does; false =
    no it does not OR unknown).
    """

    external_urls: ExternalURLObject
    """External URLs for this audiobook."""

    href: str
    """A link to the Web API endpoint providing full details of the audiobook."""

    html_description: str
    """A description of the audiobook. This field may contain HTML tags."""

    images: List[ImageObject]
    """The cover art for the audiobook in various sizes, widest first."""

    languages: List[str]
    """
    A list of the languages used in the audiobook, identified by their
    [ISO 639](https://en.wikipedia.org/wiki/ISO_639) code.
    """

    media_type: str
    """The media type of the audiobook."""

    name: str
    """The name of the audiobook."""

    narrators: List[NarratorObject]
    """The narrator(s) for the audiobook."""

    publisher: str
    """The publisher of the audiobook."""

    total_chapters: int
    """The number of chapters in this audiobook."""

    type: Literal["audiobook"]
    """The object type."""

    uri: str
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    audiobook.
    """

    edition: Optional[str] = None
    """The edition of the audiobook."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

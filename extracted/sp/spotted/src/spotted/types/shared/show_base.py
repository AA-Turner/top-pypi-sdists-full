# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .image_object import ImageObject
from .copyright_object import CopyrightObject
from .external_url_object import ExternalURLObject

__all__ = ["ShowBase"]


class ShowBase(BaseModel):
    id: str
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the show.
    """

    available_markets: List[str]
    """
    A list of the countries in which the show can be played, identified by their
    [ISO 3166-1 alpha-2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code.
    """

    copyrights: List[CopyrightObject]
    """The copyright statements of the show."""

    description: str
    """A description of the show.

    HTML tags are stripped away from this field, use `html_description` field in
    case HTML tags are needed.
    """

    explicit: bool
    """
    Whether or not the show has explicit content (true = yes it does; false = no it
    does not OR unknown).
    """

    external_urls: ExternalURLObject
    """External URLs for this show."""

    href: str
    """A link to the Web API endpoint providing full details of the show."""

    html_description: str
    """A description of the show. This field may contain HTML tags."""

    images: List[ImageObject]
    """The cover art for the show in various sizes, widest first."""

    is_externally_hosted: bool
    """True if all of the shows episodes are hosted outside of Spotify's CDN.

    This field might be `null` in some cases.
    """

    languages: List[str]
    """
    A list of the languages used in the show, identified by their
    [ISO 639](https://en.wikipedia.org/wiki/ISO_639) code.
    """

    media_type: str
    """The media type of the show."""

    name: str
    """The name of the episode."""

    publisher: str
    """The publisher of the show."""

    total_episodes: int
    """The total number of episodes in the show."""

    type: Literal["show"]
    """The object type."""

    uri: str
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    show.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

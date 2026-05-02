# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .image_object import ImageObject
from .followers_object import FollowersObject
from .external_url_object import ExternalURLObject

__all__ = ["ArtistObject"]


class ArtistObject(BaseModel):
    id: Optional[str] = None
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    artist.
    """

    external_urls: Optional[ExternalURLObject] = None
    """Known external URLs for this artist."""

    followers: Optional[FollowersObject] = None
    """Information about the followers of the artist."""

    genres: Optional[List[str]] = None
    """A list of the genres the artist is associated with.

    If not yet classified, the array is empty.
    """

    href: Optional[str] = None
    """A link to the Web API endpoint providing full details of the artist."""

    images: Optional[List[ImageObject]] = None
    """Images of the artist in various sizes, widest first."""

    name: Optional[str] = None
    """The name of the artist."""

    popularity: Optional[int] = None
    """The popularity of the artist.

    The value will be between 0 and 100, with 100 being the most popular. The
    artist's popularity is calculated from the popularity of all the artist's
    tracks.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    type: Optional[Literal["artist"]] = None
    """The object type."""

    uri: Optional[str] = None
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    artist.
    """

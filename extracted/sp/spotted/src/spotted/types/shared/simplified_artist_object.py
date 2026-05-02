# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .external_url_object import ExternalURLObject

__all__ = ["SimplifiedArtistObject"]


class SimplifiedArtistObject(BaseModel):
    id: Optional[str] = None
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    artist.
    """

    external_urls: Optional[ExternalURLObject] = None
    """Known external URLs for this artist."""

    href: Optional[str] = None
    """A link to the Web API endpoint providing full details of the artist."""

    name: Optional[str] = None
    """The name of the artist."""

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

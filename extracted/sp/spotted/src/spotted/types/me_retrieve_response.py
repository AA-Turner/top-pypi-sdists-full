# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .shared.image_object import ImageObject
from .shared.followers_object import FollowersObject
from .shared.external_url_object import ExternalURLObject

__all__ = ["MeRetrieveResponse", "ExplicitContent"]


class ExplicitContent(BaseModel):
    """The user's explicit content settings.

    _This field is only available when the current user has granted access to the [user-read-private](/documentation/web-api/concepts/scopes/#list-of-scopes) scope._
    """

    filter_enabled: Optional[bool] = None
    """When `true`, indicates that explicit content should not be played."""

    filter_locked: Optional[bool] = None
    """
    When `true`, indicates that the explicit content setting is locked and can't be
    changed by the user.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class MeRetrieveResponse(BaseModel):
    id: Optional[str] = None
    """
    The [Spotify user ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    user.
    """

    country: Optional[str] = None
    """The country of the user, as set in the user's account profile.

    An
    [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
    _This field is only available when the current user has granted access to the
    [user-read-private](/documentation/web-api/concepts/scopes/#list-of-scopes)
    scope._
    """

    display_name: Optional[str] = None
    """The name displayed on the user's profile. `null` if not available."""

    email: Optional[str] = None
    """The user's email address, as entered by the user when creating their account.

    _**Important!** This email address is unverified; there is no proof that it
    actually belongs to the user._ _This field is only available when the current
    user has granted access to the
    [user-read-email](/documentation/web-api/concepts/scopes/#list-of-scopes)
    scope._
    """

    explicit_content: Optional[ExplicitContent] = None
    """The user's explicit content settings.

    _This field is only available when the current user has granted access to the
    [user-read-private](/documentation/web-api/concepts/scopes/#list-of-scopes)
    scope._
    """

    external_urls: Optional[ExternalURLObject] = None
    """Known external URLs for this user."""

    followers: Optional[FollowersObject] = None
    """Information about the followers of the user."""

    href: Optional[str] = None
    """A link to the Web API endpoint for this user."""

    images: Optional[List[ImageObject]] = None
    """The user's profile image."""

    product: Optional[str] = None
    """The user's Spotify subscription level: "premium", "free", etc.

    (The subscription level "open" can be considered the same as "free".) _This
    field is only available when the current user has granted access to the
    [user-read-private](/documentation/web-api/concepts/scopes/#list-of-scopes)
    scope._
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    type: Optional[str] = None
    """The object type: "user" """

    uri: Optional[str] = None
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    user.
    """

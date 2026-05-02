# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.track_object import TrackObject

__all__ = ["RecommendationGetResponse", "Seed"]


class Seed(BaseModel):
    id: Optional[str] = None
    """The id used to select this seed.

    This will be the same as the string used in the `seed_artists`, `seed_tracks` or
    `seed_genres` parameter.
    """

    after_filtering_size: Optional[int] = FieldInfo(alias="afterFilteringSize", default=None)
    """
    The number of tracks available after min\\__\\** and max\\__\\** filters have been
    applied.
    """

    after_relinking_size: Optional[int] = FieldInfo(alias="afterRelinkingSize", default=None)
    """The number of tracks available after relinking for regional availability."""

    href: Optional[str] = None
    """A link to the full track or artist data for this seed.

    For tracks this will be a link to a Track Object. For artists a link to an
    Artist Object. For genre seeds, this value will be `null`.
    """

    initial_pool_size: Optional[int] = FieldInfo(alias="initialPoolSize", default=None)
    """The number of recommended tracks available for this seed."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    type: Optional[str] = None
    """The entity type of this seed. One of `artist`, `track` or `genre`."""


class RecommendationGetResponse(BaseModel):
    seeds: List[Seed]
    """An array of recommendation seed objects."""

    tracks: List[TrackObject]
    """An array of track objects ordered according to the parameters supplied."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

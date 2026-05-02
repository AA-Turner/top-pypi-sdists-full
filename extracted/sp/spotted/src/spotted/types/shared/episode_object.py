# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .show_base import ShowBase
from .image_object import ImageObject
from .external_url_object import ExternalURLObject
from .resume_point_object import ResumePointObject
from .episode_restriction_object import EpisodeRestrictionObject

__all__ = ["EpisodeObject"]


class EpisodeObject(BaseModel):
    id: str
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    episode.
    """

    audio_preview_url: Optional[str] = None
    """A URL to a 30 second preview (MP3 format) of the episode.

    `null` if not available.
    """

    description: str
    """A description of the episode.

    HTML tags are stripped away from this field, use `html_description` field in
    case HTML tags are needed.
    """

    duration_ms: int
    """The episode length in milliseconds."""

    explicit: bool
    """
    Whether or not the episode has explicit content (true = yes it does; false = no
    it does not OR unknown).
    """

    external_urls: ExternalURLObject
    """External URLs for this episode."""

    href: str
    """A link to the Web API endpoint providing full details of the episode."""

    html_description: str
    """A description of the episode. This field may contain HTML tags."""

    images: List[ImageObject]
    """The cover art for the episode in various sizes, widest first."""

    is_externally_hosted: bool
    """True if the episode is hosted outside of Spotify's CDN."""

    is_playable: bool
    """True if the episode is playable in the given market. Otherwise false."""

    languages: List[str]
    """
    A list of the languages used in the episode, identified by their
    [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639) code.
    """

    name: str
    """The name of the episode."""

    release_date: str
    """The date the episode was first released, for example `"1981-12-15"`.

    Depending on the precision, it might be shown as `"1981"` or `"1981-12"`.
    """

    release_date_precision: Literal["year", "month", "day"]
    """The precision with which `release_date` value is known."""

    show: ShowBase
    """The show on which the episode belongs."""

    type: Literal["episode"]
    """The object type."""

    uri: str
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    episode.
    """

    language: Optional[str] = None
    """
    The language used in the episode, identified by a
    [ISO 639](https://en.wikipedia.org/wiki/ISO_639) code. This field is deprecated
    and might be removed in the future. Please use the `languages` field instead.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    restrictions: Optional[EpisodeRestrictionObject] = None
    """Included in the response when a content restriction is applied."""

    resume_point: Optional[ResumePointObject] = None
    """The user's most recent position in the episode.

    Set if the supplied access token is a user token and has the scope
    'user-read-playback-position'.
    """

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ResumePointObject"]


class ResumePointObject(BaseModel):
    fully_played: Optional[bool] = None
    """Whether or not the episode has been fully played by the user."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    resume_position_ms: Optional[int] = None
    """The user's most recent position in the episode in milliseconds."""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["DeviceObject"]


class DeviceObject(BaseModel):
    id: Optional[str] = None
    """The device ID.

    This ID is unique and persistent to some extent. However, this is not guaranteed
    and any cached `device_id` should periodically be cleared out and refetched as
    necessary.
    """

    is_active: Optional[bool] = None
    """If this device is the currently active device."""

    is_private_session: Optional[bool] = None
    """If this device is currently in a private session."""

    is_restricted: Optional[bool] = None
    """Whether controlling this device is restricted.

    At present if this is "true" then no Web API commands will be accepted by this
    device.
    """

    name: Optional[str] = None
    """A human-readable name for the device.

    Some devices have a name that the user can configure (e.g. \"Loudest speaker\")
    and some devices have a generic name associated with the manufacturer or device
    model.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    supports_volume: Optional[bool] = None
    """If this device can be used to set the volume."""

    type: Optional[str] = None
    """Device type, such as "computer", "smartphone" or "speaker"."""

    volume_percent: Optional[int] = None
    """The current volume in percent."""

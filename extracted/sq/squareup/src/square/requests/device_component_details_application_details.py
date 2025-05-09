# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing_extensions
from ..types.application_type import ApplicationType
import typing


class DeviceComponentDetailsApplicationDetailsParams(typing_extensions.TypedDict):
    application_type: typing_extensions.NotRequired[ApplicationType]
    """
    The type of application.
    See [ApplicationType](#type-applicationtype) for possible values
    """

    version: typing_extensions.NotRequired[str]
    """
    The version of the application.
    """

    session_location: typing_extensions.NotRequired[typing.Optional[str]]
    """
    The location_id of the session for the application.
    """

    device_code_id: typing_extensions.NotRequired[typing.Optional[str]]
    """
    The id of the device code that was used to log in to the device.
    """

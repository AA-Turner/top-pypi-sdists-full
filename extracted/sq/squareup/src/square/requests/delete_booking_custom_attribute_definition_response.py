# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing_extensions
import typing
from .error import ErrorParams


class DeleteBookingCustomAttributeDefinitionResponseParams(typing_extensions.TypedDict):
    """
    Represents a [DeleteBookingCustomAttributeDefinition](api-endpoint:BookingCustomAttributes-DeleteBookingCustomAttributeDefinition) response
    containing error messages when errors occurred during the request. The successful response does not contain any payload.
    """

    errors: typing_extensions.NotRequired[typing.Sequence[ErrorParams]]
    """
    Any errors that occurred during the request.
    """

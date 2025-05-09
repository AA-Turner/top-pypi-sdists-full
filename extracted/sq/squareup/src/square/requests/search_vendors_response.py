# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing_extensions
import typing
from .error import ErrorParams
from .vendor import VendorParams


class SearchVendorsResponseParams(typing_extensions.TypedDict):
    """
    Represents an output from a call to [SearchVendors](api-endpoint:Vendors-SearchVendors).
    """

    errors: typing_extensions.NotRequired[typing.Sequence[ErrorParams]]
    """
    Errors encountered when the request fails.
    """

    vendors: typing_extensions.NotRequired[typing.Sequence[VendorParams]]
    """
    The [Vendor](entity:Vendor) objects matching the specified search filter.
    """

    cursor: typing_extensions.NotRequired[str]
    """
    The pagination cursor to be used in a subsequent request. If unset,
    this is the final response.
    
    See the [Pagination](https://developer.squareup.com/docs/working-with-apis/pagination) guide for more information.
    """

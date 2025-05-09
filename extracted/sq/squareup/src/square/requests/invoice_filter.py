# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing
import typing_extensions


class InvoiceFilterParams(typing_extensions.TypedDict):
    """
    Describes query filters to apply.
    """

    location_ids: typing.Sequence[str]
    """
    Limits the search to the specified locations. A location is required. 
    In the current implementation, only one location can be specified.
    """

    customer_ids: typing_extensions.NotRequired[typing.Optional[typing.Sequence[str]]]
    """
    Limits the search to the specified customers, within the specified locations. 
    Specifying a customer is optional. In the current implementation, 
    a maximum of one customer can be specified.
    """

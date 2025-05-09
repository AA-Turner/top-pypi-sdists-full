# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing_extensions
import typing
from .error import ErrorParams
from .merchant import MerchantParams


class GetMerchantResponseParams(typing_extensions.TypedDict):
    """
    The response object returned by the [RetrieveMerchant](api-endpoint:Merchants-RetrieveMerchant) endpoint.
    """

    errors: typing_extensions.NotRequired[typing.Sequence[ErrorParams]]
    """
    Information on errors encountered during the request.
    """

    merchant: typing_extensions.NotRequired[MerchantParams]
    """
    The requested `Merchant` object.
    """

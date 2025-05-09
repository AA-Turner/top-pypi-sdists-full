# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing
from .bulk_delete_merchant_custom_attributes_response_merchant_custom_attribute_delete_response import (
    BulkDeleteMerchantCustomAttributesResponseMerchantCustomAttributeDeleteResponseParams,
)
import typing_extensions
from .error import ErrorParams


class BulkDeleteMerchantCustomAttributesResponseParams(typing_extensions.TypedDict):
    """
    Represents a [BulkDeleteMerchantCustomAttributes](api-endpoint:MerchantCustomAttributes-BulkDeleteMerchantCustomAttributes) response,
    which contains a map of responses that each corresponds to an individual delete request.
    """

    values: typing.Dict[str, BulkDeleteMerchantCustomAttributesResponseMerchantCustomAttributeDeleteResponseParams]
    """
    A map of responses that correspond to individual delete requests. Each response has the
    same key as the corresponding request.
    """

    errors: typing_extensions.NotRequired[typing.Sequence[ErrorParams]]
    """
    Any errors that occurred during the request.
    """

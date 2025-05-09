# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .error import Error
import pydantic
from .gift_card import GiftCard
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class UnlinkCustomerFromGiftCardResponse(UncheckedBaseModel):
    """
    A response that contains the unlinked `GiftCard` object. If the request resulted in errors,
    the response contains a set of `Error` objects.
    """

    errors: typing.Optional[typing.List[Error]] = pydantic.Field(default=None)
    """
    Any errors that occurred during the request.
    """

    gift_card: typing.Optional[GiftCard] = pydantic.Field(default=None)
    """
    The gift card with the ID of the unlinked customer removed from the `customer_ids` field. 
    If no other customers are linked, the `customer_ids` field is also removed.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow

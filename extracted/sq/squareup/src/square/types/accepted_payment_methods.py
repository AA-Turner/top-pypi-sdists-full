# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class AcceptedPaymentMethods(UncheckedBaseModel):
    apple_pay: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether Apple Pay is accepted at checkout.
    """

    google_pay: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether Google Pay is accepted at checkout.
    """

    cash_app_pay: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether Cash App Pay is accepted at checkout.
    """

    afterpay_clearpay: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether Afterpay/Clearpay is accepted at checkout.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow

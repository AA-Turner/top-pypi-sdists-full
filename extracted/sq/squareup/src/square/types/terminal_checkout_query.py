# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .terminal_checkout_query_filter import TerminalCheckoutQueryFilter
import pydantic
from .terminal_checkout_query_sort import TerminalCheckoutQuerySort
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class TerminalCheckoutQuery(UncheckedBaseModel):
    filter: typing.Optional[TerminalCheckoutQueryFilter] = pydantic.Field(default=None)
    """
    Options for filtering returned `TerminalCheckout` objects.
    """

    sort: typing.Optional[TerminalCheckoutQuerySort] = pydantic.Field(default=None)
    """
    Option for sorting returned `TerminalCheckout` objects.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow

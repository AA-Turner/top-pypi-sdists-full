# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class SaveCardOptions(UncheckedBaseModel):
    """
    Describes save-card action fields.
    """

    customer_id: str = pydantic.Field()
    """
    The square-assigned ID of the customer linked to the saved card.
    """

    card_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The id of the created card-on-file.
    """

    reference_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    An optional user-defined reference ID that can be used to associate
    this `Card` to another entity in an external system. For example, a customer
    ID generated by a third-party system.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow

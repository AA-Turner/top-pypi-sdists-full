# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .error import Error
import pydantic
from .loyalty_reward import LoyaltyReward
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class SearchLoyaltyRewardsResponse(UncheckedBaseModel):
    """
    A response that includes the loyalty rewards satisfying the search criteria.
    """

    errors: typing.Optional[typing.List[Error]] = pydantic.Field(default=None)
    """
    Any errors that occurred during the request.
    """

    rewards: typing.Optional[typing.List[LoyaltyReward]] = pydantic.Field(default=None)
    """
    The loyalty rewards that satisfy the search criteria.
    These are returned in descending order by `updated_at`.
    """

    cursor: typing.Optional[str] = pydantic.Field(default=None)
    """
    The pagination cursor to be used in a subsequent 
    request. If empty, this is the final response.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow

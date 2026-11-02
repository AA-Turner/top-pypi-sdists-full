from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .affiliate_reward import AffiliateReward


class AffiliateRewardList(AppwriteModel):
    """
    Affiliate rewards list

    Attributes
    ----------
    total : float
        Total number of rewards that matched your query.
    rewards : List[AffiliateReward]
        List of rewards.
    """

    total: float = Field(..., alias='total')
    rewards: List[AffiliateReward] = Field(..., alias='rewards')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'rewards' not in data:
            data['rewards'] = []
        return data

from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class AffiliateReward(AppwriteModel):
    """
    AffiliateReward

    Attributes
    ----------
    id : str
        Reward ID.
    createdat : str
        Reward creation date in ISO 8601 format.
    updatedat : str
        Reward update date in ISO 8601 format.
    userid : str
        User ID of the reward owner.
    linkid : str
        Affiliate link ID that earned this reward.
    referralid : str
        Referral ID that earned this reward.
    amount : float
        Reward amount in USD.
    status : str
        Reward status. Can be one of `pending` or `claimed`.
    teamid : Optional[str]
        Organization ID the reward was claimed on.
    creditid : Optional[str]
        Credit document ID created when the reward was claimed.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    userid: str = Field(..., alias='userId')
    linkid: str = Field(..., alias='linkId')
    referralid: str = Field(..., alias='referralId')
    amount: float = Field(..., alias='amount')
    status: str = Field(..., alias='status')
    teamid: Optional[str] = Field(default=None, alias='teamId')
    creditid: Optional[str] = Field(default=None, alias='creditId')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if '$createdAt' not in data and 'createdat' not in data:
            data['$createdAt'] = ''
        if '$updatedAt' not in data and 'updatedat' not in data:
            data['$updatedAt'] = ''
        if 'userId' not in data and 'userid' not in data:
            data['userId'] = ''
        if 'linkId' not in data and 'linkid' not in data:
            data['linkId'] = ''
        if 'referralId' not in data and 'referralid' not in data:
            data['referralId'] = ''
        if 'amount' not in data:
            data['amount'] = 0
        if 'status' not in data:
            data['status'] = ''
        return data

from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .affiliate_referral import AffiliateReferral


class AffiliateReferralList(AppwriteModel):
    """
    Affiliate referrals list

    Attributes
    ----------
    total : float
        Total number of referrals that matched your query.
    referrals : List[AffiliateReferral]
        List of referrals.
    """

    total: float = Field(..., alias='total')
    referrals: List[AffiliateReferral] = Field(..., alias='referrals')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'referrals' not in data:
            data['referrals'] = []
        return data

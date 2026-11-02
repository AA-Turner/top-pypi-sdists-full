from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class AffiliateReferral(AppwriteModel):
    """
    AffiliateReferral

    Attributes
    ----------
    id : str
        Referral ID.
    createdat : str
        Referral creation date in ISO 8601 format.
    updatedat : str
        Referral update date in ISO 8601 format.
    linkid : str
        Affiliate link ID used for attribution.
    referredusermaskedid : str
        Privacy-safe truncated referred user ID.
    referredusercountry : str
        ISO 3166-1 alpha-2 country code of the referred user at signup, when available.
    status : str
        Referral status. Can be one of `pending`, `converted`, or `expired`. `expired` is derived from `expiresAt` when still pending.
    attributedat : str
        Attribution time in ISO 8601 format.
    expiresat : str
        Attribution expiry time in ISO 8601 format.
    convertedat : Optional[str]
        Conversion time in ISO 8601 format.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    linkid: str = Field(..., alias='linkId')
    referredusermaskedid: str = Field(..., alias='referredUserMaskedId')
    referredusercountry: str = Field(..., alias='referredUserCountry')
    status: str = Field(..., alias='status')
    attributedat: str = Field(..., alias='attributedAt')
    expiresat: str = Field(..., alias='expiresAt')
    convertedat: Optional[str] = Field(default=None, alias='convertedAt')

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
        if 'linkId' not in data and 'linkid' not in data:
            data['linkId'] = ''
        if 'referredUserMaskedId' not in data and 'referredusermaskedid' not in data:
            data['referredUserMaskedId'] = ''
        if 'referredUserCountry' not in data and 'referredusercountry' not in data:
            data['referredUserCountry'] = ''
        if 'status' not in data:
            data['status'] = ''
        if 'attributedAt' not in data and 'attributedat' not in data:
            data['attributedAt'] = ''
        if 'expiresAt' not in data and 'expiresat' not in data:
            data['expiresAt'] = ''
        return data

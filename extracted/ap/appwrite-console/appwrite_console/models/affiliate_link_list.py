from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .affiliate_link import AffiliateLink


class AffiliateLinkList(AppwriteModel):
    """
    Affiliate links list

    Attributes
    ----------
    total : float
        Total number of links that matched your query.
    links : List[AffiliateLink]
        List of links.
    """

    total: float = Field(..., alias='total')
    links: List[AffiliateLink] = Field(..., alias='links')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'links' not in data:
            data['links'] = []
        return data

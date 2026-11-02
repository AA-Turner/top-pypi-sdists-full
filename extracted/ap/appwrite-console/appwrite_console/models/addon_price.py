from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class AddonPrice(AppwriteModel):
    """
    AddonPrice

    Attributes
    ----------
    addonkey : str
        Addon key.
    name : str
        Addon display name.
    monthlyprice : float
        Full monthly price of the addon.
    proratedamount : float
        Calculated prorated amount for the current billing cycle.
    remainingdays : float
        Days remaining in the current billing cycle.
    totalcycledays : float
        Total days in the billing cycle.
    currency : str
        Currency code.
    billingcycleend : str
        When the current billing cycle ends.
    """

    addonkey: str = Field(..., alias='addonKey')
    name: str = Field(..., alias='name')
    monthlyprice: float = Field(..., alias='monthlyPrice')
    proratedamount: float = Field(..., alias='proratedAmount')
    remainingdays: float = Field(..., alias='remainingDays')
    totalcycledays: float = Field(..., alias='totalCycleDays')
    currency: str = Field(..., alias='currency')
    billingcycleend: str = Field(..., alias='billingCycleEnd')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'addonKey' not in data and 'addonkey' not in data:
            data['addonKey'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'monthlyPrice' not in data and 'monthlyprice' not in data:
            data['monthlyPrice'] = 0
        if 'proratedAmount' not in data and 'proratedamount' not in data:
            data['proratedAmount'] = 0
        if 'remainingDays' not in data and 'remainingdays' not in data:
            data['remainingDays'] = 0
        if 'totalCycleDays' not in data and 'totalcycledays' not in data:
            data['totalCycleDays'] = 0
        if 'currency' not in data:
            data['currency'] = 'USD'
        if 'billingCycleEnd' not in data and 'billingcycleend' not in data:
            data['billingCycleEnd'] = ''
        return data

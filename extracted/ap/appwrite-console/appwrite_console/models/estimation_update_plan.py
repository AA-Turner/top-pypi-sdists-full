from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .estimation_item import EstimationItem


class EstimationUpdatePlan(AppwriteModel):
    """
    UpdatePlan

    Attributes
    ----------
    amount : float
        Total amount
    grossamount : float
        Gross payable amount
    discount : Optional[float]
        Discount amount
    credits : float
        Credits amount
    items : List[EstimationItem]
        Estimation items
    discounts : List[EstimationItem]
        Estimation discount items
    trialdays : float
        Trial days
    trialenddate : Optional[str]
        Trial end date
    organizationcredits : float
        Organization&#039;s existing credits
    """

    amount: float = Field(..., alias='amount')
    grossamount: float = Field(..., alias='grossAmount')
    discount: Optional[float] = Field(default=None, alias='discount')
    credits: float = Field(..., alias='credits')
    items: List[EstimationItem] = Field(..., alias='items')
    discounts: List[EstimationItem] = Field(..., alias='discounts')
    trialdays: float = Field(..., alias='trialDays')
    trialenddate: Optional[str] = Field(default=None, alias='trialEndDate')
    organizationcredits: float = Field(..., alias='organizationCredits')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'amount' not in data:
            data['amount'] = 0
        if 'grossAmount' not in data and 'grossamount' not in data:
            data['grossAmount'] = 0
        if 'credits' not in data:
            data['credits'] = 0
        if 'items' not in data:
            data['items'] = []
        if 'discounts' not in data:
            data['discounts'] = []
        if 'trialDays' not in data and 'trialdays' not in data:
            data['trialDays'] = 0
        if 'organizationCredits' not in data and 'organizationcredits' not in data:
            data['organizationCredits'] = 0
        return data

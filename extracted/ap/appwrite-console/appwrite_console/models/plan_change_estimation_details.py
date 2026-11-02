from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class PlanChangeEstimationDetails(AppwriteModel):
    """
    PlanChangeEstimationDetails

    Attributes
    ----------
    currency : str
        Currency code
    grossamount : float
        Gross amount after all discounts and credits
    credits : float
        Credits applied from coupon
    organizationcredits : float
        Organization&#039;s existing credits applied
    discount : float
        Discount amount from prorated invoices
    amount : float
        Total amount before discounts and credits
    nextinvoicedate : str
        Next invoice date
    items : List[Any]
        Line items breakdown
    discounts : List[Any]
        Applied discounts breakdown
    """

    currency: str = Field(..., alias='currency')
    grossamount: float = Field(..., alias='grossAmount')
    credits: float = Field(..., alias='credits')
    organizationcredits: float = Field(..., alias='organizationCredits')
    discount: float = Field(..., alias='discount')
    amount: float = Field(..., alias='amount')
    nextinvoicedate: str = Field(..., alias='nextInvoiceDate')
    items: List[Any] = Field(..., alias='items')
    discounts: List[Any] = Field(..., alias='discounts')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'currency' not in data:
            data['currency'] = 'USD'
        if 'grossAmount' not in data and 'grossamount' not in data:
            data['grossAmount'] = 0
        if 'credits' not in data:
            data['credits'] = 0
        if 'organizationCredits' not in data and 'organizationcredits' not in data:
            data['organizationCredits'] = 0
        if 'discount' not in data:
            data['discount'] = 0
        if 'amount' not in data:
            data['amount'] = 0
        if 'nextInvoiceDate' not in data and 'nextinvoicedate' not in data:
            data['nextInvoiceDate'] = ''
        if 'items' not in data:
            data['items'] = []
        if 'discounts' not in data:
            data['discounts'] = []
        return data

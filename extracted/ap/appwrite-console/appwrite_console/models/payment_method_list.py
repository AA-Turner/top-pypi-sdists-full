from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .payment_method import PaymentMethod


class PaymentMethodList(AppwriteModel):
    """
    Payment methods list

    Attributes
    ----------
    total : float
        Total number of paymentMethods that matched your query.
    paymentmethods : List[PaymentMethod]
        List of paymentMethods.
    """

    total: float = Field(..., alias='total')
    paymentmethods: List[PaymentMethod] = Field(..., alias='paymentMethods')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'paymentMethods' not in data and 'paymentmethods' not in data:
            data['paymentMethods'] = []
        return data

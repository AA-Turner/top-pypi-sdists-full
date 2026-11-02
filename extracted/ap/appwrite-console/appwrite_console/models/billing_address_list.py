from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .billing_address import BillingAddress


class BillingAddressList(AppwriteModel):
    """
    Billing address list

    Attributes
    ----------
    total : float
        Total number of billingAddresses that matched your query.
    billingaddresses : List[BillingAddress]
        List of billingAddresses.
    """

    total: float = Field(..., alias='total')
    billingaddresses: List[BillingAddress] = Field(..., alias='billingAddresses')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'billingAddresses' not in data and 'billingaddresses' not in data:
            data['billingAddresses'] = []
        return data

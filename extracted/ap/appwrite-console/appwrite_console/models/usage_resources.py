from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class UsageResources(AppwriteModel):
    """
    Resource

    Attributes
    ----------
    name : str
        Invoice name
    value : float
        Invoice value
    amount : float
        Invoice amount
    rate : float
        Invoice rate
    desc : str
        Invoice description
    resourceid : str
        Resource ID
    type : str
        Dedicated database engine type for per-database line items (e.g. postgresql). Empty for other resources.
    specification : str
        Dedicated database specification slug for per-database line items (e.g. s-2vcpu-2gb). Empty for other resources.
    """

    name: str = Field(..., alias='name')
    value: float = Field(..., alias='value')
    amount: float = Field(..., alias='amount')
    rate: float = Field(..., alias='rate')
    desc: str = Field(..., alias='desc')
    resourceid: str = Field(..., alias='resourceId')
    type: str = Field(..., alias='type')
    specification: str = Field(..., alias='specification')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'name' not in data:
            data['name'] = ''
        if 'value' not in data:
            data['value'] = 0
        if 'amount' not in data:
            data['amount'] = 0
        if 'rate' not in data:
            data['rate'] = 0
        if 'desc' not in data:
            data['desc'] = ''
        if 'resourceId' not in data and 'resourceid' not in data:
            data['resourceId'] = ''
        if 'type' not in data:
            data['type'] = ''
        if 'specification' not in data:
            data['specification'] = ''
        return data

from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class InvoiceItem(AppwriteModel):
    """
    InvoiceItem

    Attributes
    ----------
    type : str
        Recorded line type: plan, usage, addon, discount, credit, rounding or legacy.
    description : str
        Description recorded when the line was priced.
    amount : float
        Signed amount in currency minor units, including any recorded tax allocation.
    resourceid : Optional[str]
        Usage resource identifier.
    projectid : Optional[str]
        Project identifier; null for organization charges.
    planid : Optional[str]
        Plan used to price this line.
    quantity : Optional[float]
        Recorded usage quantity, when available.
    xfrom : Optional[str]
        Beginning of the service period for this line.
    to : Optional[str]
        End of the service period for this line.
    """

    type: str = Field(..., alias='type')
    description: str = Field(..., alias='description')
    amount: float = Field(..., alias='amount')
    resourceid: Optional[str] = Field(default=None, alias='resourceId')
    projectid: Optional[str] = Field(default=None, alias='projectId')
    planid: Optional[str] = Field(default=None, alias='planId')
    quantity: Optional[float] = Field(default=None, alias='quantity')
    xfrom: Optional[str] = Field(default=None, alias='from')
    to: Optional[str] = Field(default=None, alias='to')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'type' not in data:
            data['type'] = ''
        if 'description' not in data:
            data['description'] = ''
        if 'amount' not in data:
            data['amount'] = 0
        return data

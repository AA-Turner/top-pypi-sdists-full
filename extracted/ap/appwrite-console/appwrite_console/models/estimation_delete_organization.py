from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .invoice import Invoice


class EstimationDeleteOrganization(AppwriteModel):
    """
    DeleteOrganization

    Attributes
    ----------
    unpaidinvoices : List[Invoice]
        List of unpaid invoices
    """

    unpaidinvoices: List[Invoice] = Field(..., alias='unpaidInvoices')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'unpaidInvoices' not in data and 'unpaidinvoices' not in data:
            data['unpaidInvoices'] = []
        return data

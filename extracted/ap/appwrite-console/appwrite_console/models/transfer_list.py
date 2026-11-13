from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .transfer import Transfer


class TransferList(AppwriteModel):
    """
    Transfers List

    Attributes
    ----------
    total : float
        Total number of transfers that matched your query.
    transfers : List[Transfer]
        List of transfers.
    """

    total: float = Field(..., alias='total')
    transfers: List[Transfer] = Field(..., alias='transfers')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'transfers' not in data:
            data['transfers'] = []
        return data

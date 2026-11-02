from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .console_region import ConsoleRegion


class ConsoleRegionList(AppwriteModel):
    """
    Regions list

    Attributes
    ----------
    total : float
        Total number of regions that matched your query.
    regions : List[ConsoleRegion]
        List of regions.
    """

    total: float = Field(..., alias='total')
    regions: List[ConsoleRegion] = Field(..., alias='regions')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'regions' not in data:
            data['regions'] = []
        return data

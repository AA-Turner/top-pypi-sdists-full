from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .schedule import Schedule


class ScheduleList(AppwriteModel):
    """
    Schedules List

    Attributes
    ----------
    total : float
        Total number of schedules that matched your query.
    schedules : List[Schedule]
        List of schedules.
    """

    total: float = Field(..., alias='total')
    schedules: List[Schedule] = Field(..., alias='schedules')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'schedules' not in data:
            data['schedules'] = []
        return data

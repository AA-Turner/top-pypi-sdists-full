from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .aggregation_team import AggregationTeam


class AggregationTeamList(AppwriteModel):
    """
    Aggregation team list

    Attributes
    ----------
    total : float
        Total number of aggregations that matched your query.
    aggregations : List[AggregationTeam]
        List of aggregations.
    """

    total: float = Field(..., alias='total')
    aggregations: List[AggregationTeam] = Field(..., alias='aggregations')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'aggregations' not in data:
            data['aggregations'] = []
        return data

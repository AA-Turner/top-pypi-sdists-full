from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .billing_plan import BillingPlan


class BillingPlanList(AppwriteModel):
    """
    Billing plan list

    Attributes
    ----------
    total : float
        Total number of plans that matched your query.
    plans : List[BillingPlan]
        List of plans.
    """

    total: float = Field(..., alias='total')
    plans: List[BillingPlan] = Field(..., alias='plans')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'plans' not in data:
            data['plans'] = []
        return data

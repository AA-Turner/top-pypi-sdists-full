from enum import Enum
from typing import Union

from pydantic import BaseModel, Field, model_validator

from galileo_core.schemas.shared.metric import MetricValueType


class RuleOperator(str, Enum):
    gt = "gt"
    lt = "lt"
    gte = "gte"
    lte = "lte"
    eq = "eq"
    neq = "neq"
    contains = "contains"
    all = "all"
    any = "any"
    empty = "empty"
    not_empty = "not_empty"


class Rule(BaseModel):
    metric: str = Field(description="Name of the metric.")
    operator: RuleOperator = Field(description="Operator to use for comparison.")
    target_value: Union[str, float, int, list, None] = Field(
        description="Value to compare with for this metric (right hand side)."
    )

    @model_validator(mode="before")
    @classmethod
    def add_default_target_value(cls, data: dict) -> dict:
        operator = data.get("operator")
        if operator in [RuleOperator.empty, RuleOperator.not_empty]:
            if "target_value" not in data:
                data["target_value"] = None
        return data

    def evaluate(self, value: MetricValueType) -> bool:
        if value is not None:
            if isinstance(value, (float, int)) and isinstance(self.target_value, (float, int)):
                if self.operator == RuleOperator.gt:
                    return value > self.target_value
                elif self.operator == RuleOperator.lt:
                    return value < self.target_value
                elif self.operator == RuleOperator.gte:
                    return value >= self.target_value
                elif self.operator == RuleOperator.lte:
                    return value <= self.target_value
                elif self.operator == RuleOperator.eq:
                    return value == self.target_value
                elif self.operator == RuleOperator.neq:
                    return value != self.target_value
            elif isinstance(value, str):
                if isinstance(self.target_value, (str)):
                    if self.operator == RuleOperator.eq:
                        return value == self.target_value
                    elif self.operator == RuleOperator.neq:
                        return value != self.target_value
                elif isinstance(self.target_value, list):
                    if self.operator == RuleOperator.any:
                        return any([t == value for t in self.target_value])
            elif isinstance(value, list):
                if isinstance(self.target_value, str):
                    if self.operator == RuleOperator.contains:
                        return self.target_value in value
                elif isinstance(self.target_value, list):
                    if self.operator == RuleOperator.all:
                        return all([v in value for v in self.target_value])
                    elif self.operator == RuleOperator.any:
                        return any([v in value for v in self.target_value])
                elif self.target_value is None:
                    if self.operator == RuleOperator.empty:
                        return len(value) == 0
                    elif self.operator == RuleOperator.not_empty:
                        return len(value) > 0

        return False

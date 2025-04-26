# -*- coding: utf-8 -*-
#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc. Confidential.
#
# This is unpublished proprietary source code of DataRobot, Inc.
# and its affiliates.
#
# The copyright notice above does not evidence any actual or intended
# publication of such source code.
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar

import trafaret as t

from datarobot.models.api_object import APIObject

T = TypeVar("T", bound="FairnessInsights")


@dataclass
class PerClassFairnessData:
    class_name: str
    value: float
    absolute_value: float
    entries_count: int
    is_statistically_significant: bool


@dataclass
class FairnessInsightData:
    fairness_metric: str
    fairness_threshold: str
    prediction_threshold: float
    protected_feature: str
    per_class_fairness: List[PerClassFairnessData]


class FairnessInsights(APIObject):
    """
    Bias & Fairness - Per-Class Fairness Insight computed data.

    Attributes
    ----------
    model_id: str
        The model ID for which the Fairness Insight is computed.

    count: int
        The number of per-class fairness insights data computed for the given model.

    insights: List[FairnessInsightData]
        A list of computed per-class fairness insights data.
    """

    _path = "/projects/{}/models/{}/fairnessInsights/"

    per_class_fairness_trafaret = t.Dict(
        {
            t.Key("class_name"): t.String(),
            t.Key("value"): t.Float(),
            t.Key("absolute_value"): t.Float(),
            t.Key("entries_count"): t.Int,
            t.Key("is_statistically_significant"): t.Bool,
        }
    )

    single_fairness_insight_trafaret = t.Dict(
        {
            t.Key("fairness_metric"): t.Or(t.String(), t.Null),
            t.Key("fairness_threshold", optional=True, default=0.8): t.Float(),
            t.Key("prediction_threshold"): t.Or(t.Float(), t.Null),
            t.Key("protected_feature"): t.Or(t.String(), t.Null),
            t.Key("per_class_fairness"): t.List(per_class_fairness_trafaret),
        }
    )

    _converter = t.Dict(
        {
            t.Key("data"): t.List(
                t.Dict({t.Key("model_id"): t.String()}).merge(single_fairness_insight_trafaret)
            )
        }
    )

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.model_id = [insight_data.pop("model_id") for insight_data in data][0]
        self.count = len(data)
        self.insights = [
            FairnessInsightData(**insight_data)
            for insight_data in data
            if self.single_fairness_insight_trafaret.check(insight_data)
        ]

    @classmethod
    def from_server_data(  # type: ignore[override]
        cls: Type[T],
        data: Dict[str, List[Dict[str, Any]]],
        keep_attrs: Optional[Iterable[str]] = None,
    ) -> FairnessInsights:
        if data.get("count"):
            data = {"data": data["data"]}
        return super().from_server_data(data=data, keep_attrs=keep_attrs)

    def __repr__(self) -> str:
        return f"FairnessInsights({self.model_id})"

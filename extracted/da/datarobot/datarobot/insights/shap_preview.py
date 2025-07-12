#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import Any, cast, Dict, List, Optional

import trafaret as t
from typing_extensions import Self

from datarobot.enums import INSIGHTS_SOURCES
from datarobot.insights.base import BaseInsight


class ShapPreview(BaseInsight):
    """Class for SHAP Preview calculations. Use the standard methods of BaseInsight to compute
    and retrieve: compute, create, list, get.
    """

    SHAP_PREVIEW_VALUE = t.Dict(
        {
            t.Key("feature_rank"): t.Int(),
            t.Key("feature_name"): t.String(),
            t.Key("feature_value"): t.String(),
            t.Key("shap_value"): t.Float(),
        }
    ).ignore_extra("*")

    SHAP_PREVIEW_ROW = t.Dict(
        {
            t.Key("row_index"): t.Int(),
            t.Key("total_preview_features"): t.Int(),
            t.Key("prediction_value"): t.Float(),
            t.Key("preview_values"): t.List(SHAP_PREVIEW_VALUE),
        }
    )

    INSIGHT_NAME = "shapPreview"
    INSIGHT_DATA = {
        t.Key("previews_count"): t.Int(),
        t.Key("previews"): t.List(SHAP_PREVIEW_ROW),
    }

    @property
    def previews(self) -> List[Dict[str, Any]]:
        """SHAP preview values.

        Returns
        -------
        preview : List[Dict[str, Any]]
            A list of the ShapPreview values for each row.
        """
        return cast(List[Dict[str, Any]], self.data["previews"])

    @property
    def previews_count(self) -> int:
        """The number of shap preview rows.

        Returns
        -------
        int
        """
        return cast(int, self.data["previews_count"])

    @classmethod
    def get(
        cls,
        entity_id: str,
        source: str = INSIGHTS_SOURCES.VALIDATION,
        quick_compute: Optional[bool] = None,
        prediction_filter_row_count: Optional[int] = None,
        prediction_filter_percentiles: Optional[int] = None,
        prediction_filter_operand_first: Optional[float] = None,
        prediction_filter_operand_second: Optional[float] = None,
        prediction_filter_operator: Optional[str] = None,
        feature_filter_count: Optional[int] = None,
        feature_filter_name: Optional[str] = None,
        **kwargs: Any,
    ) -> Self:
        """Return the first matching ShapPreview insight based on the entity id and kwargs.

        Parameters
        ----------
        entity_id: str
            The ID of the entity to retrieve generated insights.
        source: str
            The source type to use when retrieving the insight.
        quick_compute: Optional[bool]
            Sets whether to retrieve the insight that was computed using quick-compute. If not
            specified, quick_compute is not used for matching.
        prediction_filter_row_count: Optional[int]
            The maximum number of preview rows to return.
        prediction_filter_percentiles: Optional[int]
            The number of percentile intervals to select from the total number of rows.
            This field will supersede predictionFilterRowCount if both are present.
        prediction_filter_operand_first: Optional[float]
            The first operand to apply to filtered predictions.
        prediction_filter_operand_second: Optional[float]
            The second operand to apply to filtered predictions.
        prediction_filter_operator: Optional[str]
            The operator to apply to filtered predictions.
        feature_filter_count: Optional[int]
            The maximum number of features to return for each preview.
        feature_filter_name: Optional[str]
            The names of specific features to return for each preview.

        Returns
        -------
        List[Any]
            List of newly or already computed insights.
        """
        query_params = {**kwargs}
        if prediction_filter_row_count is not None:
            query_params["predictionFilterRowCount"] = prediction_filter_row_count
        if prediction_filter_percentiles is not None:
            query_params["predictionFilterPercentiles"] = prediction_filter_percentiles
        if prediction_filter_operand_first is not None:
            query_params["predictionFilterOperandFirst"] = prediction_filter_operand_first
        if prediction_filter_operand_second is not None:
            query_params["predictionFilterOperandSecond"] = prediction_filter_operand_second
        if prediction_filter_operator is not None:
            query_params["predictionFilterOperator"] = prediction_filter_operator
        if feature_filter_count is not None:
            query_params["featureFilterCount"] = feature_filter_count
        if feature_filter_name is not None:
            query_params["featureFilterName"] = feature_filter_name

        return super().get(
            entity_id=entity_id, source=source, quick_compute=quick_compute, **query_params
        )

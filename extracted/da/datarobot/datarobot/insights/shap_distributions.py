#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import Any, cast, Dict, List

import trafaret as t

from datarobot.insights.base import BaseInsight


class ShapDistributions(BaseInsight):
    """Class for SHAP Distributions calculations. Use the standard methods of BaseInsight to compute
    and retrieve: compute, create, list, get.
    """

    SHAP_DISTRIBUTION_VALUE = t.Dict(
        {
            t.Key("row_index"): t.Int(),
            t.Key("prediction_value"): t.Float(),
            t.Key("feature_rank"): t.Int(),
            t.Key("feature_value"): t.String(),
            t.Key("shap_value"): t.Float(),
        }
    ).ignore_extra("*")

    SHAP_DISTRIBUTIONS_ROW = t.Dict(
        {
            t.Key("feature"): t.String(),
            t.Key("shap_values"): t.List(SHAP_DISTRIBUTION_VALUE),
            t.Key("impact_unnormalized"): t.Float(),
            t.Key("impact_normalized"): t.Float(),
            t.Key("feature_type"): t.String(),
        }
    )

    INSIGHT_NAME = "shapDistributions"
    INSIGHT_DATA = {
        t.Key("total_features_count"): t.Int(),
        t.Key("features"): t.List(SHAP_DISTRIBUTIONS_ROW),
    }

    @property
    def features(self) -> List[Dict[str, Any]]:
        """SHAP feature values

        Returns
        -------
        features : List[Dict[str, Any]]
            A list of the ShapDistributions values for each row
        """
        return cast(List[Dict[str, Any]], self.data["features"])

    @property
    def total_features_count(self) -> int:
        """Number of shap distributions features

        Returns
        -------
        int
        """
        return cast(int, self.data["total_features_count"])

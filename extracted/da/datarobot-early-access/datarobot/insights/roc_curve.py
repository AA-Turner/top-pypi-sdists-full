#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import cast, Dict, List, Union

import trafaret as t

from datarobot.insights.base import BaseInsight


class RocCurve(BaseInsight):
    """Class for ROC Curve calculations. Use the standard methods of BaseInsight to compute
    and retrieve: compute, create, list, get.

    Usage example:

        ```python
        >>> from datarobot.insights import RocCurve
        >>> RocCurve.compute("67643b2d87bb4954d7917323", data_slice_id="6764389b4bdd48581485a58b")
        <datarobot.models.status_check_job.StatusCheckJob object at 0x7fc0b313cc40>
        >>> RocCurve.get("67643b2d87bb4954d7917323", data_slice_id="6764389b4bdd48581485a58b")
        <datarobot.insights.roc_curve.RocCurve object at 0x7fc0a7549d20>
        >>> RocCurve.list("67643b2d87bb4954d7917323")
        [<datarobot.insights.roc_curve.RocCurve object at 0x7fc0a7549f60>, ...]
        >>> RocCurve.list("67643b2d87bb4954d7917323")[0].roc_points
        [{'accuracy': 0.539375, 'f1_score': 0.0, 'false_negative_score': 737, 'true_negative_score': 863, ...}]
        ```
    """

    ROC_POINTS = t.Dict(
        {
            t.Key("accuracy"): t.Float(),
            t.Key("f1Score"): t.Float(),
            t.Key("falseNegativeScore"): t.Int(),
            t.Key("trueNegativeScore"): t.Int(),
            t.Key("falsePositiveScore"): t.Int(),
            t.Key("truePositiveScore"): t.Int(),
            t.Key("trueNegativeRate"): t.Float(),
            t.Key("falsePositiveRate"): t.Float(),
            t.Key("truePositiveRate"): t.Float(),
            t.Key("matthewsCorrelationCoefficient"): t.Float(),
            t.Key("positivePredictiveValue"): t.Float(),
            t.Key("negativePredictiveValue"): t.Float(),
            t.Key("threshold"): t.Float(),
            t.Key("fractionPredictedAsPositive"): t.Float(),
            t.Key("fractionPredictedAsNegative"): t.Float(),
            t.Key("liftPositive"): t.Float(),
            t.Key("liftNegative"): t.Float(),
        }
    ).ignore_extra("*")

    INSIGHT_NAME = "rocCurve"
    INSIGHT_DATA = {
        t.Key("rocPoints"): t.List(ROC_POINTS),
        t.Key("negativeClassPredictions"): t.List(t.Float()),
        t.Key("positiveClassPredictions"): t.List(t.Float()),
        t.Key("auc", optional=True): t.Float(),
        t.Key("kolmogorovSmirnovMetric", optional=True): t.Float(),
    }

    @property
    def kolmogorov_smirnov_metric(self) -> float:
        """Kolmogorov-Smirnov metric for the ROC curve values"""
        return cast(float, self.data["kolmogorov_smirnov_metric"])

    @property
    def auc(self) -> float:
        """AUC metric for the ROC curve values"""
        return cast(float, self.data["auc"])

    @property
    def positive_class_predictions(self) -> List[float]:
        """List of positive class prediction values for the ROC curve"""
        return cast(List[float], self.data["positive_class_predictions"])

    @property
    def negative_class_predictions(self) -> List[float]:
        """List of negative class prediction values for the ROC curve"""
        return cast(List[float], self.data["negative_class_predictions"])

    @property
    def roc_points(self) -> List[Dict[str, Union[int, float]]]:
        """List of ROC values for the ROC curve"""
        return cast(List[Dict[str, Union[int, float]]], self.data["roc_points"])

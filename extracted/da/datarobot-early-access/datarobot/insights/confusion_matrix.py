#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, List, cast

import trafaret as t

from datarobot.insights.base import BaseInsight


class ConfusionMatrix(BaseInsight):
    """Class for Confusion Matrix calculations. Use the standard methods of BaseInsight to compute
    and retrieve: compute, create, list, get.

    Usage example:

        ```python
        >>> from datarobot.insights import Residuals
        >>> ConfusionMatrix.list("672e32de69b0b676ced54d9c")
        [<datarobot.insights.residuals.Residuals object at 0x7fbce8305ae0>]
        >>> ConfusionMatrix.compute("672e32de69b0b676ced54d9c", data_slice_id="677ae1249695103ba9feff97")
        <datarobot.models.status_check_job.StatusCheckJob object at 0x7fbcf4054b80>
        >>> ConfusionMatrix.list("672e32de69b0b676ced54d9c")
        <datarobot.insights.residuals.ConfusionChart object at 0x7fbce8305690>]
        >>> ConfusionMatrix.get("672e32de69b0b676ced54d9c", data_slice_id="677ae1249695103ba9feff97")
        <datarobot.insights.residuals.Residuals object at 0x7fbce83057b0>
        ```
    """

    GLOBAL_METRICS = t.Dict({
        t.Key("f1"): t.Float(),
        t.Key("precision"): t.Float(),
        t.Key("recall"): t.Float(),
    })

    CONFUSION_MATRIX_DATA = t.Dict({
        t.Key("row_classes"): t.List(t.Any),
        t.Key("col_classes"): t.List(t.Any),
        t.Key("confusion_matrix"): t.List(t.List(t.Float())),
        t.Key("class_metrics"): t.List(t.Any),
    })

    INSIGHT_NAME = "confusionMatrix"

    INSIGHT_DATA = {
        t.Key("confusion_matrix_data"): CONFUSION_MATRIX_DATA,
        t.Key("total_matrix_sum"): t.Int(),
        t.Key("global_metrics"): GLOBAL_METRICS,
        t.Key("number_of_classes"): t.Int(),
        t.Key("rows"): t.List(t.Int()),
        t.Key("columns"): t.List(t.Int()),
    }

    @property
    def confusion_matrix_data(self) -> Dict[str, Any]:
        return cast(Dict[str, Any], self.data["confusion_matrix_data"])

    @property
    def total_matrix_sum(self) -> int:
        return cast(int, self.data["total_matrix_sum"])

    @property
    def global_metrics(self) -> Dict[str, float]:
        return cast(Dict[str, float], self.data["global_metrics"])

    @property
    def number_of_classes(self) -> int:
        return cast(int, self.data["number_of_classes"])

    @property
    def rows(self) -> List[int]:
        return cast(List[int], self.data["rows"])

    @property
    def columns(self) -> List[int]:
        return cast(List[int], self.data["columns"])

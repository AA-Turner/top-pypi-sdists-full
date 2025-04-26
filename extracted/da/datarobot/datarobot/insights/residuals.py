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


class Residuals(BaseInsight):
    """Class for Residuals calculations. Use the standard methods of BaseInsight to compute
    and retrieve: compute, create, list, get.

    Usage example:

        ```python
        >>> from datarobot.insights import Residuals
        >>> Residuals.list("672e32de69b0b676ced54d9c")
        [<datarobot.insights.residuals.Residuals object at 0x7fbce8305ae0>]
        >>> Residuals.compute("672e32de69b0b676ced54d9c", data_slice_id="677ae1249695103ba9feff97")
        <datarobot.models.status_check_job.StatusCheckJob object at 0x7fbcf4054b80>
        >>> Residuals.list("672e32de69b0b676ced54d9c")
        [<datarobot.insights.residuals.Residuals object at 0x7fbce8305870>,
        <datarobot.insights.residuals.Residuals object at 0x7fbce8305690>]
        >>> Residuals.get("672e32de69b0b676ced54d9c", data_slice_id="677ae1249695103ba9feff97")
        <datarobot.insights.residuals.Residuals object at 0x7fbce83057b0>
        >>> Residuals.get("672e32de69b0b676ced54d9c", data_slice_id="677ae1249695103ba9feff97").histogram
        [{'interval_start': -33.37288135593221, 'interval_end': -32.525000000000006, 'occurrences': 1}, ...]
        ```
    """

    HISTOGRAM_BIN = t.Dict(
        {
            t.Key("interval_start"): t.Float(),
            t.Key("interval_end"): t.Float(),
            t.Key("occurrences"): t.Int(),
        }
    ).ignore_extra("*")

    INSIGHT_NAME = "residuals"
    INSIGHT_DATA = {
        t.Key("histogram"): t.List(HISTOGRAM_BIN),
        t.Key("coefficient_of_determination"): t.Float(),
        t.Key("residual_mean"): t.Float(),
        t.Key("standard_deviation"): t.Float(),
        t.Key("data"): t.List(t.List(t.Float())),
    }

    @property
    def histogram(self) -> List[Dict[str, Union[int, float]]]:
        """Residuals histogram."""
        return cast(List[Dict[str, Union[int, float]]], self.data["histogram"])

    @property
    def coefficient_of_determination(self) -> float:
        """Coefficient of determination."""
        return cast(float, self.data["coefficient_of_determination"])

    @property
    def residual_mean(self) -> float:
        """Residual mean."""
        return cast(float, self.data["residual_mean"])

    @property
    def standard_deviation(self) -> float:
        """Standard deviation."""
        return cast(float, self.data["standard_deviation"])

    @property
    def chart_data(self) -> List[List[float]]:
        """The rows of Residuals chart data in [actual, predicted, residual, row number] form."""
        return cast(List[List[float]], self.data["data"])

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
from typing import Any, cast, Dict, List

import trafaret as t

from datarobot.insights.base import BaseInsight


class LiftChart(BaseInsight):
    """Class for Lift Chart calculations. Use the standard methods of BaseInsight to compute
    and retrieve: compute, create, list, get.

    Usage example:

        ```python
        >>> from datarobot.insights import LiftChart
        >>> LiftChart.compute("67643b2d87bb4954d7917323", data_slice_id="6764389b4bdd48581485a58b")
        <datarobot.models.status_check_job.StatusCheckJob object at 0x7fa7f5ba20b0>
        >>> LiftChart.list("67643b2d87bb4954d7917323")
        [<datarobot.insights.lift_chart.LiftChart object at 0x7fe242eeaa10>, ... ]
        >>> LiftChart.get("67643b2d87bb4954d7917323", data_slice_id="6764389b4bdd48581485a58b").bins
        [{'actual': 0.4, 'predicted': 0.22727272727272724, 'bin_weight': 5.0}, ... ]
        ```
    """

    LIFT_CHART_BINS = t.Dict(
        {t.Key("actual"): t.Float(), t.Key("predicted"): t.Float(), t.Key("bin_weight"): t.Float()}
    ).ignore_extra("*")

    INSIGHT_NAME = "liftChart"
    INSIGHT_DATA = {t.Key("bins"): t.List(LIFT_CHART_BINS)}

    @property
    def bins(self) -> List[Dict[str, Any]]:
        """Lift chart bins."""
        return cast(List[Dict[str, Any]], self.data["bins"])

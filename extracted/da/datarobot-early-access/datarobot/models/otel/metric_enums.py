#
# Copyright 2025 DataRobot, Inc. and its affiliates.
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

from enum import Enum


class MetricAggregation(str, Enum):
    """Metric aggregation options."""

    AVERAGE = "average"
    MAX = "max"
    MIN = "min"
    SUM = "sum"


class MetricResolution(str, Enum):
    ONE_MINUTE = "PT1M"
    FIVE_MINUTES = "PT5M"
    ONE_HOUR = "PT1H"
    ONE_DAY = "P1D"

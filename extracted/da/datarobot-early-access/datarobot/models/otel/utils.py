#
# Copyright 2026 DataRobot, Inc. and its affiliates.
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

from datetime import date, datetime, timezone
from typing import Union


def to_datetime_param(value: Union[datetime, date, str]) -> str:
    """Convert to a potential datetime parameter string."""
    if isinstance(value, datetime):
        # set the timezone, so it produces a legit ISO string
        dt = value.replace(tzinfo=timezone.utc) if not value.tzinfo else value
        return dt.isoformat()

    if isinstance(value, date):
        return value.isoformat()

    # no real error checking here -- assume it is a legit datetime string
    return value

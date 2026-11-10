# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["SessionLogsParams"]


class SessionLogsParams(TypedDict, total=False):
    end_time: Annotated[Union[str, datetime], PropertyInfo(alias="endTime", format="iso8601")]

    event_types: Annotated[SequenceNotStr[str], PropertyInfo(alias="eventTypes")]

    limit: int

    namespace: str

    offset: int

    start_time: Annotated[Union[str, datetime], PropertyInfo(alias="startTime", format="iso8601")]

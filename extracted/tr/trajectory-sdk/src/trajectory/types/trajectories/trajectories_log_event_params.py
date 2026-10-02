# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict


class TrajectoriesLogEventParams(TypedDict, total=False):
  event_id: Required[str]
  """
  Caller-owned id used to dedupe retries of the same event. Stored as {trajectory_id}:{event_id}
  in a 128-character column.
  """
  name: Required[str]
  """
  Harness event name.
  """
  payload: Mapping[str, Any]
  """
  Optional structured event payload. Does not affect training reward.
  """

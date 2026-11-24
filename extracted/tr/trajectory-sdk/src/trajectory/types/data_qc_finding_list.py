# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.specs.diagnostics.findings.data_qc_finding import DataQcFinding


class DataQcFindingList(SyncPage[DataQcFinding]):
  items: list[DataQcFinding]

  next_cursor: str | None = None

  has_more: bool

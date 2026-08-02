# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Job planning types for plan mode."""

from __future__ import annotations

from typing import Literal

import attrs


@attrs.define(frozen=True)
class _BasePlan:
    """Common fields shared by all job plans."""

    table_name: str
    version: int
    has_work: bool
    total_tasks: int
    total_rows_pending: int
    skipped_fragments: int
    skipped_rows: int
    total_fragments: int
    total_rows: int


@attrs.define(frozen=True)
class BackfillPlan(_BasePlan):
    """Result of planning a backfill job without executing it."""

    job_type: Literal["backfill"] = attrs.field(init=False, default="backfill")
    column_name: str = ""
    where: str | None = None
    udf_mismatch: bool = False
    srcfiles_mismatch: bool = False


@attrs.define(frozen=True)
class RefreshPlan(_BasePlan):
    """Result of planning a refresh job without executing it."""

    job_type: Literal["refresh"] = attrs.field(init=False, default="refresh")
    new_source_fragments: int = 0
    stale_rows: int = 0
    invalidated_fragments: int = 0


JobPlan = BackfillPlan | RefreshPlan

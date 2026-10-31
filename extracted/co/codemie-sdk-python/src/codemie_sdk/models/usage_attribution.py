# Copyright 2026 EPAM Systems, Inc. ("EPAM")
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Usage Attribution analytics models for the CodeMie SDK."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .analytics import PaginationMetadata


class UsageAttributionQueryParams(BaseModel):
    """Period parameters shared by the Usage Attribution read endpoints.

    The endpoints take no project or user filter: they always attribute all usage.
    """

    model_config = ConfigDict(extra="ignore")

    time_period: str | None = Field(
        None,
        description='Time period: "last_hour", "last_6_hours", "last_24_hours", "last_7_days", "last_30_days", "last_60_days", "last_year"',
    )
    start_date: str | None = Field(
        None, description="ISO 8601 start date (use with end_date)"
    )
    end_date: str | None = Field(
        None, description="ISO 8601 end date (use with start_date)"
    )


class UsageAttributionRange(BaseModel):
    """The effective range of a response; ranges longer than the maximum are clamped."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    from_: str = Field(alias="from", description="Effective start")
    to: str = Field(description="Effective end")
    days: float = Field(description="Length of the effective range in days")
    clamped: bool = Field(description="The requested range was cut to the maximum")
    requested_from: str | None = Field(None, description="Requested start")
    requested_to: str | None = Field(None, description="Requested end")
    evidence_from: str | None = Field(
        None, description="Start of the evidence window used for categories"
    )


class UsageAttributionAnalysisSettings(BaseModel):
    """The analysis settings behind a response."""

    model_config = ConfigDict(extra="ignore")

    hash: str | None = None
    defaults_hash: str | None = None
    schema_version: int | None = None
    overridden: list[str] = Field(default_factory=list)
    tier: str | None = None


class UsageAttributionAnalysis(BaseModel):
    """When and how the cached analysis behind a response was computed."""

    model_config = ConfigDict(extra="ignore")

    computed_at: str | None = None
    duration_ms: float | None = None
    cache: str = Field(description="hit, miss, shared or stale")
    stale: bool = False
    refreshing: bool = Field(False, description="A newer analysis is being computed")
    error: str | None = None
    ttl_s: int | None = None
    window: dict[str, Any] | None = None
    evidence_window: dict[str, Any] | None = None
    coverage: dict[str, Any] | None = None
    unclassified_reasons: dict[str, Any] | None = None
    allocated: float | None = None
    timings: dict[str, Any] = Field(default_factory=dict)
    settings: UsageAttributionAnalysisSettings | None = None


class UsageAttributionResponse(BaseModel):
    """A composite view: totals, tiles, charts, a popup or How It Works."""

    model_config = ConfigDict(extra="ignore")

    data: dict[str, Any]
    range: UsageAttributionRange | None = None
    analysis: UsageAttributionAnalysis | None = Field(
        None, description="Absent for the fast totals, which skip the analysis"
    )


class UsageAttributionTableResponse(BaseModel):
    """A table page: rows of the page, totals over every matching row and filter counts."""

    model_config = ConfigDict(extra="ignore")

    data: dict[str, Any] = Field(description="rows and totals")
    pagination: PaginationMetadata
    counts: dict[str, int] = Field(default_factory=dict)
    threshold: float | None = None
    display: dict[str, float] | None = None
    range: UsageAttributionRange
    analysis: UsageAttributionAnalysis


class UsageAttributionSettingsResponse(BaseModel):
    """The tunable settings schema, the defaults and whether the caller may tune."""

    model_config = ConfigDict(extra="ignore")

    data: dict[str, Any]

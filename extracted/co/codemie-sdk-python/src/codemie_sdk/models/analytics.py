"""Models for analytics-related data structures."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ResponseMetadata(BaseModel):
    """Metadata for analytics responses."""

    model_config = ConfigDict(extra="ignore")

    timestamp: str = Field(description="ISO 8601 timestamp when response generated")
    data_as_of: str = Field(description="ISO 8601 timestamp of data freshness")
    filters_applied: dict[str, Any] = Field(description="Applied filters")
    execution_time_ms: float = Field(description="Query execution time in milliseconds")


class PaginationMetadata(BaseModel):
    """Pagination metadata for tabular responses."""

    model_config = ConfigDict(extra="ignore")

    page: int = Field(description="Zero-indexed page number")
    per_page: int = Field(description="Items per page")
    total_count: int = Field(description="Total items available")
    has_more: bool = Field(description="Whether more pages exist")


class ColumnDefinition(BaseModel):
    """Column metadata for tabular data."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Column identifier")
    label: str = Field(description="Human-readable label")
    type: str = Field(description='Data type: "string", "number", "date"')
    format: str | None = Field(
        None, description='Format hint: "currency", "percentage", "timestamp"'
    )
    description: str | None = Field(None, description="Column description")


class Metric(BaseModel):
    """Individual metric in summary responses."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Metric identifier")
    label: str = Field(description="Human-readable label")
    type: str = Field(description="Data type")
    value: Any = Field(description="Metric value (int, float, str, etc.)")
    format: str | None = Field(
        None, description='Format hint: "currency", "percentage", "number"'
    )
    description: str | None = Field(None, description="Metric description")


class SummariesData(BaseModel):
    """Container for summary metrics."""

    model_config = ConfigDict(extra="ignore")

    metrics: list[Metric] = Field(description="Array of metrics")


class TabularData(BaseModel):
    """Container for tabular data with dynamic columns."""

    model_config = ConfigDict(extra="ignore")

    columns: list[ColumnDefinition] = Field(description="Column definitions")
    rows: list[dict[str, Any]] = Field(description="Data rows (dict per row)")
    totals: dict[str, Any] | None = Field(None, description="Optional totals row")


class UserListItem(BaseModel):
    """Individual user item."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="User ID")
    name: str = Field(description="User name")


class UsersListData(BaseModel):
    """Container for users list."""

    model_config = ConfigDict(extra="ignore")

    users: list[UserListItem] = Field(description="List of users")
    total_count: int = Field(description="Total number of users")


class SummariesResponse(BaseModel):
    """Response for summary endpoints (summaries, cli-summary)."""

    model_config = ConfigDict(extra="ignore")

    data: SummariesData = Field(description="Summary data")
    metadata: ResponseMetadata = Field(description="Response metadata")


class TabularResponse(BaseModel):
    """Response for tabular endpoints (19 endpoints)."""

    model_config = ConfigDict(extra="ignore")

    data: TabularData = Field(description="Tabular data")
    metadata: ResponseMetadata = Field(description="Response metadata")
    pagination: PaginationMetadata | None = Field(
        None, description="Optional pagination metadata"
    )


class UsersListResponse(BaseModel):
    """Response for users list endpoint."""

    model_config = ConfigDict(extra="ignore")

    data: UsersListData = Field(description="Users list data")
    metadata: ResponseMetadata = Field(description="Response metadata")


class AnalyticsQueryParams(BaseModel):
    """Query parameters for analytics endpoints."""

    model_config = ConfigDict(extra="ignore")

    time_period: str | None = Field(
        None,
        description='Time period: "last_hour", "last_6_hours", "last_24_hours", "last_7_days", "last_30_days", "last_90_days", "last_year"',
    )
    start_date: str | None = Field(
        None, description="ISO 8601 format start date (use with end_date)"
    )
    end_date: str | None = Field(
        None, description="ISO 8601 format end date (use with start_date)"
    )
    users: str | None = Field(None, description="Comma-separated user IDs")
    projects: str | None = Field(None, description="Comma-separated project names")


class PaginatedAnalyticsQueryParams(AnalyticsQueryParams):
    """Query parameters with pagination."""

    page: int = Field(0, description="Zero-indexed page number")
    per_page: int = Field(20, description="Items per page")

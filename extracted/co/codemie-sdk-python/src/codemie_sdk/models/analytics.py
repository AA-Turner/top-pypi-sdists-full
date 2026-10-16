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


# ── CLI Analytics: /v1/analytics/cli-analytics/* ─────────────────────────────


class CliAnalyticsQueryParams(AnalyticsQueryParams):
    """Filters shared by the /v1/analytics/cli-analytics/* read endpoints."""

    repositories: str | None = Field(
        None, description="Comma-separated repository names"
    )


class CliAnalyticsSessionsQueryParams(CliAnalyticsQueryParams):
    """Query parameters of the CLI Analytics session list."""

    page: int | None = Field(None, description="Zero-indexed page number")
    per_page: int | None = Field(None, description="Items per page")
    is_unattributed: bool | None = Field(
        None, description="Only sessions with no attributed repository"
    )


class CliAnalyticsMetadata(BaseModel):
    """Metadata of CLI Analytics responses."""

    model_config = ConfigDict(extra="ignore")

    timestamp: str = Field(description="ISO 8601 timestamp when response generated")
    data_as_of: str = Field(description="ISO 8601 date/datetime of the newest data")
    execution_time_ms: float = Field(description="Query execution time in milliseconds")


class CliAnalyticsCostKpis(BaseModel):
    """Totals of the CLI Analytics cost breakdown."""

    model_config = ConfigDict(extra="ignore")

    total_sessions: int
    total_cost_usd: float
    total_tokens: int
    avg_cost_per_session: float


class CliAnalyticsCostByUser(BaseModel):
    """Cost of one user."""

    model_config = ConfigDict(extra="ignore")

    developer_name: str
    cost_usd: float


class CliAnalyticsCostByModel(BaseModel):
    """Cost of one model."""

    model_config = ConfigDict(extra="ignore")

    model_name: str
    cost_usd: float


class CliAnalyticsCostData(BaseModel):
    """Cost breakdown data."""

    model_config = ConfigDict(extra="ignore")

    kpis: CliAnalyticsCostKpis
    cost_by_user: list[CliAnalyticsCostByUser] = Field(default_factory=list)
    cost_by_model: list[CliAnalyticsCostByModel] = Field(default_factory=list)


class CliAnalyticsCostResponse(BaseModel):
    """Response of GET /v1/analytics/cli-analytics/cost."""

    model_config = ConfigDict(extra="ignore")

    data: CliAnalyticsCostData
    metadata: CliAnalyticsMetadata


class CliAnalyticsUserRow(BaseModel):
    """One user of the CLI Analytics user leaderboard."""

    model_config = ConfigDict(extra="ignore")

    developer_name: str = Field(description="Resolved user email")
    session_count: int
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_creation_tokens: int
    cost_usd: float


class CliAnalyticsUsersData(BaseModel):
    """User leaderboard data."""

    model_config = ConfigDict(extra="ignore")

    rows: list[CliAnalyticsUserRow]
    avg_session_duration_ms: int | None = None
    total_count: int | None = None


class CliAnalyticsUsersResponse(BaseModel):
    """Response of GET /v1/analytics/cli-analytics/users."""

    model_config = ConfigDict(extra="ignore")

    data: CliAnalyticsUsersData
    metadata: CliAnalyticsMetadata


class CliAnalyticsSessionRow(BaseModel):
    """One CLI session."""

    model_config = ConfigDict(extra="ignore")

    trace_id: str = Field(description="Session id")
    developer_name: str = Field(description="Resolved user email")
    repository: str | None = Field(None, description="None when unattributed")
    branch: str | None = None
    start_time: str = Field(description="ISO 8601 session start")
    duration_ms: int = Field(description="Session start to its last event")
    model_name: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    cost_usd: float


class CliAnalyticsSessionsData(BaseModel):
    """Session list data."""

    model_config = ConfigDict(extra="ignore")

    sessions: list[CliAnalyticsSessionRow]
    page: int
    per_page: int
    total: int


class CliAnalyticsSessionsResponse(BaseModel):
    """Response of GET /v1/analytics/cli-analytics/sessions."""

    model_config = ConfigDict(extra="ignore")

    data: CliAnalyticsSessionsData
    metadata: CliAnalyticsMetadata


class CliAnalyticsSessionDetailResponse(BaseModel):
    """Response of GET /v1/analytics/cli-analytics/sessions/{trace_id}."""

    model_config = ConfigDict(extra="ignore")

    data: CliAnalyticsSessionRow
    metadata: CliAnalyticsMetadata


class CliAnalyticsRepositoryRow(BaseModel):
    """One repository (or repository branch) of the CLI Analytics breakdown."""

    model_config = ConfigDict(extra="ignore")

    repository: str | None = Field(None, description="None for unattributed sessions")
    branch: str | None = None
    session_count: int
    cost_usd: float
    project_name: str | None = None


class CliAnalyticsRepositoriesData(BaseModel):
    """Repository breakdown data."""

    model_config = ConfigDict(extra="ignore")

    rows: list[CliAnalyticsRepositoryRow]
    pagination: PaginationMetadata


class CliAnalyticsRepositoriesResponse(BaseModel):
    """Response of GET /v1/analytics/cli-analytics/repositories."""

    model_config = ConfigDict(extra="ignore")

    data: CliAnalyticsRepositoriesData
    metadata: CliAnalyticsMetadata

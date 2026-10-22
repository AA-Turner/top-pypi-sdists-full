"""Analytics service implementation."""

import json

from ..models.analytics import (
    AnalyticsQueryParams,
    CliAnalyticsCostResponse,
    CliAnalyticsQueryParams,
    CliAnalyticsRepositoriesResponse,
    CliAnalyticsSessionDetailResponse,
    CliAnalyticsSessionsQueryParams,
    CliAnalyticsSessionsResponse,
    CliAnalyticsUsersResponse,
    PaginatedAnalyticsQueryParams,
    SummariesResponse,
    TabularResponse,
    UsersListResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class AnalyticsService:
    """Service for managing CodeMie analytics."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the analytics service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_summaries(
        self, params: AnalyticsQueryParams | None = None
    ) -> SummariesResponse:
        """Get overall platform summary metrics.

        Args:
            params: Query parameters (time filters, user/project filters)

        Returns:
            SummariesResponse with metrics array including total input tokens,
            cached input tokens, output tokens, and money spent
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/summaries",
            SummariesResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_cli_summary(
        self, params: AnalyticsQueryParams | None = None
    ) -> SummariesResponse:
        """Get CLI-specific summary metrics.

        Args:
            params: Query parameters (time filters, user/project filters)

        Returns:
            SummariesResponse with CLI metrics including unique users, repos,
            sessions, file operations, and code statistics
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/cli-summary",
            SummariesResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_assistants_chats(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get assistants chats analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with assistant performance metrics including chat statistics,
            error rates, token consumption, and costs
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/assistants-chats",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_workflows(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get workflows analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with workflow execution metrics including total runs,
            success/failure rates, costs, and performance statistics
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/workflows",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_tools_usage(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get tool usage analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with tool usage metrics including invocation counts,
            user adoption, agent usage, and error tracking
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/tools-usage",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_webhooks_invocation(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get webhooks invocation statistics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with webhook usage patterns showing invocation counts
            per user and webhook alias
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/webhooks-invocation",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_mcp_servers(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get top MCP servers analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with MCP server usage distribution showing
            percentage share of each server
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/mcp-servers",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_mcp_servers_by_users(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get MCP servers usage by users.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with individual user adoption and usage of MCP servers
            showing which users are utilizing which servers
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/mcp-servers-by-users",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_projects_spending(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get money spent by projects.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with project-level spending ranked by amount
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/projects-spending",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_llms_usage(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get top LLMs usage analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with LLM model usage distribution showing
            preference patterns across different models
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/llms-usage",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_users_spending(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get money spent by users.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with individual user spending ranked by amount
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/users-spending",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_budget_soft_limit(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get soft budget limit violations.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with users who have exceeded soft budget limits
            (warning threshold)
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/budget-soft-limit",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_budget_hard_limit(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get hard budget limit violations.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with users who have reached or exceeded hard budget
            limits (enforcement threshold)
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/budget-hard-limit",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_users_activity(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get most active users analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with comprehensive user activity metrics including
            spending, recent projects, and token consumption
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/users-activity",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_projects_activity(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get most active projects analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with project activity metrics including spending,
            active user counts, and token consumption
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/projects-activity",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_agents_usage(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get top agents usage analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with agent usage analytics including invocations,
            spending, user adoption, tool usage, and error tracking
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/agents-usage",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_cli_agents(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get top CLI agents analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with CLI agent usage distribution showing
            percentage share of each agent
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/cli-agents",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_cli_llms(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get top CLI LLMs analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with LLM model usage distribution in CLI context
            showing percentage share
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/cli-llms",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_cli_users(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get most active CLI users analytics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with CLI user activity showing total invocation
            counts per user
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/cli-users",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_cli_errors(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get top error codes for CLI.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with most common CLI error codes with occurrence
            counts for troubleshooting
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/cli-errors",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_cli_repositories(
        self, params: PaginatedAnalyticsQueryParams | None = None
    ) -> TabularResponse:
        """Get repository statistics.

        Args:
            params: Query parameters (filters + pagination)

        Returns:
            TabularResponse with repository-level metrics including code changes,
            token consumption, and branch activity
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/cli-repositories",
            TabularResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_users(
        self, params: AnalyticsQueryParams | None = None
    ) -> UsersListResponse:
        """Get users list.

        Args:
            params: Query parameters (time filters, user/project filters)

        Returns:
            UsersListResponse with list of unique users
        """
        query_params = params.model_dump(exclude_none=True) if params else {}
        return self._api.get(
            "/v1/analytics/users",
            UsersListResponse,
            params=query_params,
            wrap_response=False,
        )

    def get_leaderboard_summary(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/summary — summary metrics card."""
        return self._api.get(
            "/v1/analytics/leaderboard/summary",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def get_leaderboard_scores(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/scores — score distribution."""
        return self._api.get(
            "/v1/analytics/leaderboard/scores",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def get_leaderboard_tiers(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/tiers — tier distribution."""
        return self._api.get(
            "/v1/analytics/leaderboard/tiers",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def get_leaderboard_top_performers(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/top-performers — top performers panel."""
        return self._api.get(
            "/v1/analytics/leaderboard/top-performers",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def get_leaderboard_dimensions(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/dimensions — average scores by dimension."""
        return self._api.get(
            "/v1/analytics/leaderboard/dimensions",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def get_leaderboard_entries(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/entries — ranked users table."""
        return self._api.get(
            "/v1/analytics/leaderboard/entries",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def get_leaderboard_seasons(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/seasons — seasons list."""
        return self._api.get(
            "/v1/analytics/leaderboard/seasons",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def get_leaderboard_projects(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/projects — project filter list."""
        return self._api.get(
            "/v1/analytics/leaderboard/projects",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def get_leaderboard_framework(self, **kwargs) -> dict:
        """GET /v1/analytics/leaderboard/framework — dimension definitions."""
        return self._api.get(
            "/v1/analytics/leaderboard/framework",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    def send_cli_hook_events(
        self, events: list[dict], project: str | None = None
    ) -> dict:
        """POST /v1/analytics/cli-analytics/event-hooks — ingest CLI plugin hook events.

        The events are sent as NDJSON (one JSON object per line), the format the
        codemie-code analytics plugin uses. The authenticated user becomes the
        events' sender. Events with an ``event_id`` already stored are skipped.

        Args:
            events: Hook events, e.g. ``{"type": "agent.session.start", "session_id": ...}``
            project: Project name sent as ``X-CodeMie-Project``; the server discards
                the batch (HTTP 200) when it is missing, unknown or has CLI analytics
                disabled. None sends no header.

        Returns:
            Ingest response body: an empty object on success, or the discard body
            ``{"accepted": 0, "dropped": N, "reason": ...}`` (never raised on)
        """
        body = "\n".join(json.dumps(event) for event in events) + "\n"
        headers = {"Content-Type": "application/x-ndjson"}
        if project is not None:
            headers["X-CodeMie-Project"] = project
        return self._api.post(
            "/v1/analytics/cli-analytics/event-hooks",
            dict,
            data=body.encode("utf-8"),
            extra_headers=headers,
            wrap_response=False,
        )

    def get_cli_sessions(self, **kwargs) -> dict:
        """GET /v1/analytics/cli-analytics/sessions — CLI Analytics session list.

        Args:
            **kwargs: Query parameters (time_period, start_date, end_date, users,
                projects, page, per_page, sort_by, search, framework, branch)

        Returns:
            Response with ``data.sessions`` (one row per session) and paging fields
        """
        return self._api.get(
            "/v1/analytics/cli-analytics/sessions",
            dict,
            params=kwargs if kwargs else None,
            wrap_response=False,
        )

    # ── CLI Analytics: /v1/analytics/cli-analytics/* ─────────────────────────

    def ingest_cli_analytics_event_hooks(
        self, events: list[dict], project: str | None = None
    ) -> None:
        """POST /v1/analytics/cli-analytics/event-hooks — send CLI hook events.

        The endpoint takes NDJSON (one event per line); each event is posted as
        its own single-line body.

        Args:
            events: Hook events, e.g. ``agent.session.start``, ``agent.usage.request``
            project: Project name sent as ``X-CodeMie-Project``. The server stores the
                batch only for an existing project with CLI analytics enabled that the
                sender may use; otherwise it answers HTTP 200 and discards it.
        """
        headers = {"Content-Type": "application/x-ndjson"}
        if project is not None:
            headers["X-CodeMie-Project"] = project
        for event in events:
            self._api.post(
                "/v1/analytics/cli-analytics/event-hooks",
                dict,
                json_data=event,
                wrap_response=False,
                extra_headers=headers,
            )

    def ingest_cli_analytics_logs(
        self, payload: dict, project: str | None = None
    ) -> None:
        """POST /v1/analytics/cli-analytics/logs — send OTLP logs as JSON.

        Args:
            payload: An OTLP ``ExportLogsServiceRequest`` in its JSON form
            project: Project name sent as ``X-CodeMie-Project`` (see
                ``ingest_cli_analytics_event_hooks`` for the server behaviour)
        """
        headers = {"X-CodeMie-Project": project} if project is not None else None
        self._api.post(
            "/v1/analytics/cli-analytics/logs",
            dict,
            json_data=payload,
            extra_headers=headers,
            wrap_response=False,
        )

    def get_cli_analytics_cost(
        self, params: CliAnalyticsQueryParams | None = None
    ) -> CliAnalyticsCostResponse:
        """GET /v1/analytics/cli-analytics/cost — session, token and cost totals."""
        return self._api.get(
            "/v1/analytics/cli-analytics/cost",
            CliAnalyticsCostResponse,
            params=params.model_dump(exclude_none=True) if params else {},
            wrap_response=False,
        )

    def get_cli_analytics_users(
        self, params: CliAnalyticsQueryParams | None = None
    ) -> CliAnalyticsUsersResponse:
        """GET /v1/analytics/cli-analytics/users — per-user sessions and tokens."""
        return self._api.get(
            "/v1/analytics/cli-analytics/users",
            CliAnalyticsUsersResponse,
            params=params.model_dump(exclude_none=True) if params else {},
            wrap_response=False,
        )

    def get_cli_analytics_sessions(
        self, params: CliAnalyticsSessionsQueryParams | None = None
    ) -> CliAnalyticsSessionsResponse:
        """GET /v1/analytics/cli-analytics/sessions — paginated session list."""
        return self._api.get(
            "/v1/analytics/cli-analytics/sessions",
            CliAnalyticsSessionsResponse,
            params=params.model_dump(exclude_none=True) if params else {},
            wrap_response=False,
        )

    def get_cli_analytics_session(
        self, trace_id: str
    ) -> CliAnalyticsSessionDetailResponse:
        """GET /v1/analytics/cli-analytics/sessions/{trace_id} — session detail."""
        return self._api.get(
            f"/v1/analytics/cli-analytics/sessions/{trace_id}",
            CliAnalyticsSessionDetailResponse,
            wrap_response=False,
        )

    def get_cli_analytics_repositories(
        self, params: CliAnalyticsQueryParams | None = None
    ) -> CliAnalyticsRepositoriesResponse:
        """GET /v1/analytics/cli-analytics/repositories — per-repository breakdown.

        Without pagination parameters the endpoint returns every repository branch.
        """
        return self._api.get(
            "/v1/analytics/cli-analytics/repositories",
            CliAnalyticsRepositoriesResponse,
            params=params.model_dump(exclude_none=True) if params else {},
            wrap_response=False,
        )

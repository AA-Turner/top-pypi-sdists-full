from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_analytics_family import GetAnalyticsFamily
from ...models.get_analytics_granularity import GetAnalyticsGranularity
from ...models.get_analytics_outcome import GetAnalyticsOutcome
from ...models.get_analytics_scope import GetAnalyticsScope
from ...models.managed_agents_analytics_response import ManagedAgentsAnalyticsResponse
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    family: GetAnalyticsFamily,
    *,
    scope: GetAnalyticsScope | Unset = GetAnalyticsScope.WORKSPACE,
    workspace_id: str | Unset = UNSET,
    from_: str | Unset = UNSET,
    to: str | Unset = UNSET,
    granularity: GetAnalyticsGranularity | Unset = UNSET,
    launched_agent_id: str | Unset = UNSET,
    executing_agent_id: str | Unset = UNSET,
    executing_agent_version_id: str | Unset = UNSET,
    model: str | Unset = UNSET,
    project_source: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    tool_name: str | Unset = UNSET,
    outcome: GetAnalyticsOutcome | Unset = UNSET,
    sandbox_provider: str | Unset = UNSET,
    environment_id: str | Unset = UNSET,
    compute_class: str | Unset = UNSET,
    machine_type: str | Unset = UNSET,
    target_agent_id: str | Unset = UNSET,
    target_agent_version_id: str | Unset = UNSET,
    evaluator_agent_id: str | Unset = UNSET,
    evaluator_agent_version_id: str | Unset = UNSET,
    criterion_key: str | Unset = UNSET,
    archetype: str | Unset = UNSET,
    size_bucket: str | Unset = UNSET,
    series_group_by: str | Unset = UNSET,
    limit: int | Unset = 25,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_scope: str | Unset = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    params["workspace_id"] = workspace_id

    params["from"] = from_

    params["to"] = to

    json_granularity: str | Unset = UNSET
    if not isinstance(granularity, Unset):
        json_granularity = granularity.value

    params["granularity"] = json_granularity

    params["launched_agent_id"] = launched_agent_id

    params["executing_agent_id"] = executing_agent_id

    params["executing_agent_version_id"] = executing_agent_version_id

    params["model"] = model

    params["project_source"] = project_source

    params["project_id"] = project_id

    params["tool_name"] = tool_name

    json_outcome: str | Unset = UNSET
    if not isinstance(outcome, Unset):
        json_outcome = outcome.value

    params["outcome"] = json_outcome

    params["sandbox_provider"] = sandbox_provider

    params["environment_id"] = environment_id

    params["compute_class"] = compute_class

    params["machine_type"] = machine_type

    params["target_agent_id"] = target_agent_id

    params["target_agent_version_id"] = target_agent_version_id

    params["evaluator_agent_id"] = evaluator_agent_id

    params["evaluator_agent_version_id"] = evaluator_agent_version_id

    params["criterion_key"] = criterion_key

    params["archetype"] = archetype

    params["size_bucket"] = size_bucket

    params["series_group_by"] = series_group_by

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/analytics/{family}".format(family=quote(str(family), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsAnalyticsResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiError.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiError.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = ManagedAgentsApiError.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ManagedAgentsApiError.from_dict(response.json())



        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = ManagedAgentsApiError.from_dict(response.json())



        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    family: GetAnalyticsFamily,
    *,
    client: AuthenticatedClient | Client,
    scope: GetAnalyticsScope | Unset = GetAnalyticsScope.WORKSPACE,
    workspace_id: str | Unset = UNSET,
    from_: str | Unset = UNSET,
    to: str | Unset = UNSET,
    granularity: GetAnalyticsGranularity | Unset = UNSET,
    launched_agent_id: str | Unset = UNSET,
    executing_agent_id: str | Unset = UNSET,
    executing_agent_version_id: str | Unset = UNSET,
    model: str | Unset = UNSET,
    project_source: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    tool_name: str | Unset = UNSET,
    outcome: GetAnalyticsOutcome | Unset = UNSET,
    sandbox_provider: str | Unset = UNSET,
    environment_id: str | Unset = UNSET,
    compute_class: str | Unset = UNSET,
    machine_type: str | Unset = UNSET,
    target_agent_id: str | Unset = UNSET,
    target_agent_version_id: str | Unset = UNSET,
    evaluator_agent_id: str | Unset = UNSET,
    evaluator_agent_version_id: str | Unset = UNSET,
    criterion_key: str | Unset = UNSET,
    archetype: str | Unset = UNSET,
    size_bucket: str | Unset = UNSET,
    series_group_by: str | Unset = UNSET,
    limit: int | Unset = 25,

) -> Response[ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout]:
    """ Read pre-aggregated session, usage, and environment analytics

     Returns totals, a time series, and default breakdowns for one metric family over a time window.
    Figures come from a maintained projection rather than from session events, so the cost of a request
    depends on the window rather than on how much history the organization has, and every response
    reports its own freshness through as_of and lag_seconds. Percentiles are approximate: they are
    merged from a fixed-bin histogram, which is what lets them combine across shards, buckets, and
    scopes at all. scope defaults to the caller's own workspace. tenant aggregates every workspace in
    the parent tenant organization and requires both a Tenant Admin role and an identity that carries a
    tenant id, so it is reachable by a service credential but not yet from a browser session. global is
    not reachable with this operation at all.

    Args:
        family (GetAnalyticsFamily): Metric family to read: managed_agent_usage for tool, token,
            and cost figures, managed_agent_turn for turn counts and turn duration percentiles,
            managed_agent_environment for sandbox startup latency, managed_agent_completion for first
            successful root-session completions, and managed_agent_quality for immutable evaluation
            and criterion verdicts.
        scope (GetAnalyticsScope | Unset): Read locality. workspace is the caller's own
            organization; tenant aggregates every workspace in the parent tenant organization and
            requires a Tenant Admin role. Default: GetAnalyticsScope.WORKSPACE.
        workspace_id (str | Unset): With scope=tenant, narrow to one workspace of the tenant.
            Ignored at workspace scope, where the authenticated organization is authoritative.
        from_ (str | Unset): RFC 3339 start of the window. Defaults to seven days before to.
            Widened outward to a bucket boundary.
        to (str | Unset): RFC 3339 exclusive end of the window. Defaults to now.
        granularity (GetAnalyticsGranularity | Unset): Series bucket width. Defaults to hourly for
            windows up to two days and daily beyond that.
        launched_agent_id (str | Unset): Filter to work under sessions launched from this agent,
            including its subagents.
        executing_agent_id (str | Unset): Filter to work performed by this agent, whether it was
            launched directly or delegated to.
        executing_agent_version_id (str | Unset): Filter to one immutable agent version.
        model (str | Unset): Filter to one provider model id.
        project_source (str | Unset): Filter by the system a project or external source belongs
            to, e.g. slack_thread.
        project_id (str | Unset): Filter to one project or external source id within
            project_source.
        tool_name (str | Unset): Filter to one tool. Note that token and cost figures are model
            spend and are not attributable to a tool, so filtering by one reports only that tool's own
            direct cost.
        outcome (GetAnalyticsOutcome | Unset): Filter by outcome: tool call state for usage,
            startup result for environments, or immutable verdict for quality.
        sandbox_provider (str | Unset): Filter environment analytics to one sandbox provider, e.g.
            runs or docker. self_hosted is accepted for historical queries.
        environment_id (str | Unset): Filter environment analytics to one environment.
        compute_class (str | Unset): Filter environment analytics by compute kind: cpu, or an
            accelerator type and name such as gpu:a100.
        machine_type (str | Unset): Filter environment analytics to one machine type, or to the
            requested CPU and memory shape when the provider names none.
        target_agent_id (str | Unset): Filter quality analytics to evaluations of one target
            agent.
        target_agent_version_id (str | Unset): Filter quality analytics to one immutable target-
            agent version.
        evaluator_agent_id (str | Unset): Filter quality analytics to verdicts produced by one
            evaluator agent.
        evaluator_agent_version_id (str | Unset): Filter quality analytics to one immutable
            evaluator-agent version.
        criterion_key (str | Unset): Filter quality analytics to one stable rubric criterion key.
        archetype (str | Unset): Filter quality analytics by the target task archetype frozen on
            the evaluation.
        size_bucket (str | Unset): Filter quality analytics by the target size bucket frozen on
            the evaluation.
        series_group_by (str | Unset): Return the series split into one line per value of this
            dimension, for a stacked chart, alongside the combined series. Capped at the top eight
            groups by the family's ranking measure. Omit for the combined series only.
        limit (int | Unset): Rows per breakdown. Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout]
     """


    kwargs = _get_kwargs(
        family=family,
scope=scope,
workspace_id=workspace_id,
from_=from_,
to=to,
granularity=granularity,
launched_agent_id=launched_agent_id,
executing_agent_id=executing_agent_id,
executing_agent_version_id=executing_agent_version_id,
model=model,
project_source=project_source,
project_id=project_id,
tool_name=tool_name,
outcome=outcome,
sandbox_provider=sandbox_provider,
environment_id=environment_id,
compute_class=compute_class,
machine_type=machine_type,
target_agent_id=target_agent_id,
target_agent_version_id=target_agent_version_id,
evaluator_agent_id=evaluator_agent_id,
evaluator_agent_version_id=evaluator_agent_version_id,
criterion_key=criterion_key,
archetype=archetype,
size_bucket=size_bucket,
series_group_by=series_group_by,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    family: GetAnalyticsFamily,
    *,
    client: AuthenticatedClient | Client,
    scope: GetAnalyticsScope | Unset = GetAnalyticsScope.WORKSPACE,
    workspace_id: str | Unset = UNSET,
    from_: str | Unset = UNSET,
    to: str | Unset = UNSET,
    granularity: GetAnalyticsGranularity | Unset = UNSET,
    launched_agent_id: str | Unset = UNSET,
    executing_agent_id: str | Unset = UNSET,
    executing_agent_version_id: str | Unset = UNSET,
    model: str | Unset = UNSET,
    project_source: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    tool_name: str | Unset = UNSET,
    outcome: GetAnalyticsOutcome | Unset = UNSET,
    sandbox_provider: str | Unset = UNSET,
    environment_id: str | Unset = UNSET,
    compute_class: str | Unset = UNSET,
    machine_type: str | Unset = UNSET,
    target_agent_id: str | Unset = UNSET,
    target_agent_version_id: str | Unset = UNSET,
    evaluator_agent_id: str | Unset = UNSET,
    evaluator_agent_version_id: str | Unset = UNSET,
    criterion_key: str | Unset = UNSET,
    archetype: str | Unset = UNSET,
    size_bucket: str | Unset = UNSET,
    series_group_by: str | Unset = UNSET,
    limit: int | Unset = 25,

) -> ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | None:
    """ Read pre-aggregated session, usage, and environment analytics

     Returns totals, a time series, and default breakdowns for one metric family over a time window.
    Figures come from a maintained projection rather than from session events, so the cost of a request
    depends on the window rather than on how much history the organization has, and every response
    reports its own freshness through as_of and lag_seconds. Percentiles are approximate: they are
    merged from a fixed-bin histogram, which is what lets them combine across shards, buckets, and
    scopes at all. scope defaults to the caller's own workspace. tenant aggregates every workspace in
    the parent tenant organization and requires both a Tenant Admin role and an identity that carries a
    tenant id, so it is reachable by a service credential but not yet from a browser session. global is
    not reachable with this operation at all.

    Args:
        family (GetAnalyticsFamily): Metric family to read: managed_agent_usage for tool, token,
            and cost figures, managed_agent_turn for turn counts and turn duration percentiles,
            managed_agent_environment for sandbox startup latency, managed_agent_completion for first
            successful root-session completions, and managed_agent_quality for immutable evaluation
            and criterion verdicts.
        scope (GetAnalyticsScope | Unset): Read locality. workspace is the caller's own
            organization; tenant aggregates every workspace in the parent tenant organization and
            requires a Tenant Admin role. Default: GetAnalyticsScope.WORKSPACE.
        workspace_id (str | Unset): With scope=tenant, narrow to one workspace of the tenant.
            Ignored at workspace scope, where the authenticated organization is authoritative.
        from_ (str | Unset): RFC 3339 start of the window. Defaults to seven days before to.
            Widened outward to a bucket boundary.
        to (str | Unset): RFC 3339 exclusive end of the window. Defaults to now.
        granularity (GetAnalyticsGranularity | Unset): Series bucket width. Defaults to hourly for
            windows up to two days and daily beyond that.
        launched_agent_id (str | Unset): Filter to work under sessions launched from this agent,
            including its subagents.
        executing_agent_id (str | Unset): Filter to work performed by this agent, whether it was
            launched directly or delegated to.
        executing_agent_version_id (str | Unset): Filter to one immutable agent version.
        model (str | Unset): Filter to one provider model id.
        project_source (str | Unset): Filter by the system a project or external source belongs
            to, e.g. slack_thread.
        project_id (str | Unset): Filter to one project or external source id within
            project_source.
        tool_name (str | Unset): Filter to one tool. Note that token and cost figures are model
            spend and are not attributable to a tool, so filtering by one reports only that tool's own
            direct cost.
        outcome (GetAnalyticsOutcome | Unset): Filter by outcome: tool call state for usage,
            startup result for environments, or immutable verdict for quality.
        sandbox_provider (str | Unset): Filter environment analytics to one sandbox provider, e.g.
            runs or docker. self_hosted is accepted for historical queries.
        environment_id (str | Unset): Filter environment analytics to one environment.
        compute_class (str | Unset): Filter environment analytics by compute kind: cpu, or an
            accelerator type and name such as gpu:a100.
        machine_type (str | Unset): Filter environment analytics to one machine type, or to the
            requested CPU and memory shape when the provider names none.
        target_agent_id (str | Unset): Filter quality analytics to evaluations of one target
            agent.
        target_agent_version_id (str | Unset): Filter quality analytics to one immutable target-
            agent version.
        evaluator_agent_id (str | Unset): Filter quality analytics to verdicts produced by one
            evaluator agent.
        evaluator_agent_version_id (str | Unset): Filter quality analytics to one immutable
            evaluator-agent version.
        criterion_key (str | Unset): Filter quality analytics to one stable rubric criterion key.
        archetype (str | Unset): Filter quality analytics by the target task archetype frozen on
            the evaluation.
        size_bucket (str | Unset): Filter quality analytics by the target size bucket frozen on
            the evaluation.
        series_group_by (str | Unset): Return the series split into one line per value of this
            dimension, for a stacked chart, alongside the combined series. Capped at the top eight
            groups by the family's ranking measure. Omit for the combined series only.
        limit (int | Unset): Rows per breakdown. Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout
     """


    return sync_detailed(
        family=family,
client=client,
scope=scope,
workspace_id=workspace_id,
from_=from_,
to=to,
granularity=granularity,
launched_agent_id=launched_agent_id,
executing_agent_id=executing_agent_id,
executing_agent_version_id=executing_agent_version_id,
model=model,
project_source=project_source,
project_id=project_id,
tool_name=tool_name,
outcome=outcome,
sandbox_provider=sandbox_provider,
environment_id=environment_id,
compute_class=compute_class,
machine_type=machine_type,
target_agent_id=target_agent_id,
target_agent_version_id=target_agent_version_id,
evaluator_agent_id=evaluator_agent_id,
evaluator_agent_version_id=evaluator_agent_version_id,
criterion_key=criterion_key,
archetype=archetype,
size_bucket=size_bucket,
series_group_by=series_group_by,
limit=limit,

    ).parsed

async def asyncio_detailed(
    family: GetAnalyticsFamily,
    *,
    client: AuthenticatedClient | Client,
    scope: GetAnalyticsScope | Unset = GetAnalyticsScope.WORKSPACE,
    workspace_id: str | Unset = UNSET,
    from_: str | Unset = UNSET,
    to: str | Unset = UNSET,
    granularity: GetAnalyticsGranularity | Unset = UNSET,
    launched_agent_id: str | Unset = UNSET,
    executing_agent_id: str | Unset = UNSET,
    executing_agent_version_id: str | Unset = UNSET,
    model: str | Unset = UNSET,
    project_source: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    tool_name: str | Unset = UNSET,
    outcome: GetAnalyticsOutcome | Unset = UNSET,
    sandbox_provider: str | Unset = UNSET,
    environment_id: str | Unset = UNSET,
    compute_class: str | Unset = UNSET,
    machine_type: str | Unset = UNSET,
    target_agent_id: str | Unset = UNSET,
    target_agent_version_id: str | Unset = UNSET,
    evaluator_agent_id: str | Unset = UNSET,
    evaluator_agent_version_id: str | Unset = UNSET,
    criterion_key: str | Unset = UNSET,
    archetype: str | Unset = UNSET,
    size_bucket: str | Unset = UNSET,
    series_group_by: str | Unset = UNSET,
    limit: int | Unset = 25,

) -> Response[ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout]:
    """ Read pre-aggregated session, usage, and environment analytics

     Returns totals, a time series, and default breakdowns for one metric family over a time window.
    Figures come from a maintained projection rather than from session events, so the cost of a request
    depends on the window rather than on how much history the organization has, and every response
    reports its own freshness through as_of and lag_seconds. Percentiles are approximate: they are
    merged from a fixed-bin histogram, which is what lets them combine across shards, buckets, and
    scopes at all. scope defaults to the caller's own workspace. tenant aggregates every workspace in
    the parent tenant organization and requires both a Tenant Admin role and an identity that carries a
    tenant id, so it is reachable by a service credential but not yet from a browser session. global is
    not reachable with this operation at all.

    Args:
        family (GetAnalyticsFamily): Metric family to read: managed_agent_usage for tool, token,
            and cost figures, managed_agent_turn for turn counts and turn duration percentiles,
            managed_agent_environment for sandbox startup latency, managed_agent_completion for first
            successful root-session completions, and managed_agent_quality for immutable evaluation
            and criterion verdicts.
        scope (GetAnalyticsScope | Unset): Read locality. workspace is the caller's own
            organization; tenant aggregates every workspace in the parent tenant organization and
            requires a Tenant Admin role. Default: GetAnalyticsScope.WORKSPACE.
        workspace_id (str | Unset): With scope=tenant, narrow to one workspace of the tenant.
            Ignored at workspace scope, where the authenticated organization is authoritative.
        from_ (str | Unset): RFC 3339 start of the window. Defaults to seven days before to.
            Widened outward to a bucket boundary.
        to (str | Unset): RFC 3339 exclusive end of the window. Defaults to now.
        granularity (GetAnalyticsGranularity | Unset): Series bucket width. Defaults to hourly for
            windows up to two days and daily beyond that.
        launched_agent_id (str | Unset): Filter to work under sessions launched from this agent,
            including its subagents.
        executing_agent_id (str | Unset): Filter to work performed by this agent, whether it was
            launched directly or delegated to.
        executing_agent_version_id (str | Unset): Filter to one immutable agent version.
        model (str | Unset): Filter to one provider model id.
        project_source (str | Unset): Filter by the system a project or external source belongs
            to, e.g. slack_thread.
        project_id (str | Unset): Filter to one project or external source id within
            project_source.
        tool_name (str | Unset): Filter to one tool. Note that token and cost figures are model
            spend and are not attributable to a tool, so filtering by one reports only that tool's own
            direct cost.
        outcome (GetAnalyticsOutcome | Unset): Filter by outcome: tool call state for usage,
            startup result for environments, or immutable verdict for quality.
        sandbox_provider (str | Unset): Filter environment analytics to one sandbox provider, e.g.
            runs or docker. self_hosted is accepted for historical queries.
        environment_id (str | Unset): Filter environment analytics to one environment.
        compute_class (str | Unset): Filter environment analytics by compute kind: cpu, or an
            accelerator type and name such as gpu:a100.
        machine_type (str | Unset): Filter environment analytics to one machine type, or to the
            requested CPU and memory shape when the provider names none.
        target_agent_id (str | Unset): Filter quality analytics to evaluations of one target
            agent.
        target_agent_version_id (str | Unset): Filter quality analytics to one immutable target-
            agent version.
        evaluator_agent_id (str | Unset): Filter quality analytics to verdicts produced by one
            evaluator agent.
        evaluator_agent_version_id (str | Unset): Filter quality analytics to one immutable
            evaluator-agent version.
        criterion_key (str | Unset): Filter quality analytics to one stable rubric criterion key.
        archetype (str | Unset): Filter quality analytics by the target task archetype frozen on
            the evaluation.
        size_bucket (str | Unset): Filter quality analytics by the target size bucket frozen on
            the evaluation.
        series_group_by (str | Unset): Return the series split into one line per value of this
            dimension, for a stacked chart, alongside the combined series. Capped at the top eight
            groups by the family's ranking measure. Omit for the combined series only.
        limit (int | Unset): Rows per breakdown. Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout]
     """


    kwargs = _get_kwargs(
        family=family,
scope=scope,
workspace_id=workspace_id,
from_=from_,
to=to,
granularity=granularity,
launched_agent_id=launched_agent_id,
executing_agent_id=executing_agent_id,
executing_agent_version_id=executing_agent_version_id,
model=model,
project_source=project_source,
project_id=project_id,
tool_name=tool_name,
outcome=outcome,
sandbox_provider=sandbox_provider,
environment_id=environment_id,
compute_class=compute_class,
machine_type=machine_type,
target_agent_id=target_agent_id,
target_agent_version_id=target_agent_version_id,
evaluator_agent_id=evaluator_agent_id,
evaluator_agent_version_id=evaluator_agent_version_id,
criterion_key=criterion_key,
archetype=archetype,
size_bucket=size_bucket,
series_group_by=series_group_by,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    family: GetAnalyticsFamily,
    *,
    client: AuthenticatedClient | Client,
    scope: GetAnalyticsScope | Unset = GetAnalyticsScope.WORKSPACE,
    workspace_id: str | Unset = UNSET,
    from_: str | Unset = UNSET,
    to: str | Unset = UNSET,
    granularity: GetAnalyticsGranularity | Unset = UNSET,
    launched_agent_id: str | Unset = UNSET,
    executing_agent_id: str | Unset = UNSET,
    executing_agent_version_id: str | Unset = UNSET,
    model: str | Unset = UNSET,
    project_source: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    tool_name: str | Unset = UNSET,
    outcome: GetAnalyticsOutcome | Unset = UNSET,
    sandbox_provider: str | Unset = UNSET,
    environment_id: str | Unset = UNSET,
    compute_class: str | Unset = UNSET,
    machine_type: str | Unset = UNSET,
    target_agent_id: str | Unset = UNSET,
    target_agent_version_id: str | Unset = UNSET,
    evaluator_agent_id: str | Unset = UNSET,
    evaluator_agent_version_id: str | Unset = UNSET,
    criterion_key: str | Unset = UNSET,
    archetype: str | Unset = UNSET,
    size_bucket: str | Unset = UNSET,
    series_group_by: str | Unset = UNSET,
    limit: int | Unset = 25,

) -> ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | None:
    """ Read pre-aggregated session, usage, and environment analytics

     Returns totals, a time series, and default breakdowns for one metric family over a time window.
    Figures come from a maintained projection rather than from session events, so the cost of a request
    depends on the window rather than on how much history the organization has, and every response
    reports its own freshness through as_of and lag_seconds. Percentiles are approximate: they are
    merged from a fixed-bin histogram, which is what lets them combine across shards, buckets, and
    scopes at all. scope defaults to the caller's own workspace. tenant aggregates every workspace in
    the parent tenant organization and requires both a Tenant Admin role and an identity that carries a
    tenant id, so it is reachable by a service credential but not yet from a browser session. global is
    not reachable with this operation at all.

    Args:
        family (GetAnalyticsFamily): Metric family to read: managed_agent_usage for tool, token,
            and cost figures, managed_agent_turn for turn counts and turn duration percentiles,
            managed_agent_environment for sandbox startup latency, managed_agent_completion for first
            successful root-session completions, and managed_agent_quality for immutable evaluation
            and criterion verdicts.
        scope (GetAnalyticsScope | Unset): Read locality. workspace is the caller's own
            organization; tenant aggregates every workspace in the parent tenant organization and
            requires a Tenant Admin role. Default: GetAnalyticsScope.WORKSPACE.
        workspace_id (str | Unset): With scope=tenant, narrow to one workspace of the tenant.
            Ignored at workspace scope, where the authenticated organization is authoritative.
        from_ (str | Unset): RFC 3339 start of the window. Defaults to seven days before to.
            Widened outward to a bucket boundary.
        to (str | Unset): RFC 3339 exclusive end of the window. Defaults to now.
        granularity (GetAnalyticsGranularity | Unset): Series bucket width. Defaults to hourly for
            windows up to two days and daily beyond that.
        launched_agent_id (str | Unset): Filter to work under sessions launched from this agent,
            including its subagents.
        executing_agent_id (str | Unset): Filter to work performed by this agent, whether it was
            launched directly or delegated to.
        executing_agent_version_id (str | Unset): Filter to one immutable agent version.
        model (str | Unset): Filter to one provider model id.
        project_source (str | Unset): Filter by the system a project or external source belongs
            to, e.g. slack_thread.
        project_id (str | Unset): Filter to one project or external source id within
            project_source.
        tool_name (str | Unset): Filter to one tool. Note that token and cost figures are model
            spend and are not attributable to a tool, so filtering by one reports only that tool's own
            direct cost.
        outcome (GetAnalyticsOutcome | Unset): Filter by outcome: tool call state for usage,
            startup result for environments, or immutable verdict for quality.
        sandbox_provider (str | Unset): Filter environment analytics to one sandbox provider, e.g.
            runs or docker. self_hosted is accepted for historical queries.
        environment_id (str | Unset): Filter environment analytics to one environment.
        compute_class (str | Unset): Filter environment analytics by compute kind: cpu, or an
            accelerator type and name such as gpu:a100.
        machine_type (str | Unset): Filter environment analytics to one machine type, or to the
            requested CPU and memory shape when the provider names none.
        target_agent_id (str | Unset): Filter quality analytics to evaluations of one target
            agent.
        target_agent_version_id (str | Unset): Filter quality analytics to one immutable target-
            agent version.
        evaluator_agent_id (str | Unset): Filter quality analytics to verdicts produced by one
            evaluator agent.
        evaluator_agent_version_id (str | Unset): Filter quality analytics to one immutable
            evaluator-agent version.
        criterion_key (str | Unset): Filter quality analytics to one stable rubric criterion key.
        archetype (str | Unset): Filter quality analytics by the target task archetype frozen on
            the evaluation.
        size_bucket (str | Unset): Filter quality analytics by the target size bucket frozen on
            the evaluation.
        series_group_by (str | Unset): Return the series split into one line per value of this
            dimension, for a stacked chart, alongside the combined series. Capped at the top eight
            groups by the family's ranking measure. Omit for the combined series only.
        limit (int | Unset): Rows per breakdown. Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAnalyticsResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout
     """


    return (await asyncio_detailed(
        family=family,
client=client,
scope=scope,
workspace_id=workspace_id,
from_=from_,
to=to,
granularity=granularity,
launched_agent_id=launched_agent_id,
executing_agent_id=executing_agent_id,
executing_agent_version_id=executing_agent_version_id,
model=model,
project_source=project_source,
project_id=project_id,
tool_name=tool_name,
outcome=outcome,
sandbox_provider=sandbox_provider,
environment_id=environment_id,
compute_class=compute_class,
machine_type=machine_type,
target_agent_id=target_agent_id,
target_agent_version_id=target_agent_version_id,
evaluator_agent_id=evaluator_agent_id,
evaluator_agent_version_id=evaluator_agent_version_id,
criterion_key=criterion_key,
archetype=archetype,
size_bucket=size_bucket,
series_group_by=series_group_by,
limit=limit,

    )).parsed

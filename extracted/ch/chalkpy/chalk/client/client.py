from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    TypeAlias,
    Union,
)

import requests

from chalk.client.models import (
    BranchDeployResponse,
    BranchIdParam,
    BulkOnlineQueryResponse,
    ChalkError,
    CreateModelTrainingJobResponse,
    FeatureDropResponse,
    FeatureObservationDeletionResponse,
    FeatureReference,
    FeatureStatisticsResponse,
    GetIncrementalProgressResponse,
    JobQueueItem,
    ListDatasetsResponse,
    ManualTriggerScheduledQueryResponse,
    ModelNamespaceResponse,
    ModelVersionResponse,
    NamedQueryMetadata,
    OfflineQueryDeadlineOptions,
    OfflineQueryInfo,
    OfflineQueryInputUri,
    OfflineQueryProfileSummary,
    OfflineQueryReport,
    OfflineStoreTable,
    OnlineQuery,
    OnlineQueryContext,
    PlanQueryResponse,
    RedeployResponse,
    RegisteredModelVersion,
    RegisterModelResponse,
    RegisterModelVersionResponse,
    ResolverRunResponse,
    ResourceRequests,
    ScheduledQueryRun,
    StreamResolverTestResponse,
    UnloadResolvers,
    WhoAmIResponse,
    WorkflowExecutionInfo,
)
from chalk.client.response import Dataset, OnlineQueryResult
from chalk.features import DataFrame, Feature
from chalk.ml.model_file_transfer import SourceConfig

if TYPE_CHECKING:
    import ssl

    import pandas as pd
    import polars as pl
    from pydantic import BaseModel

    from chalk.client._chalkdf_import import ChalkDfDataFrame
    from chalk.client.api import APINamespace
    from chalk.features._encoding.inputs import InputSchemaHint
    from chalk.queries.named_query import NamedQuery
    from chalk.scalinggroup.spec import (
        AutoScalingSpec,
        DeleteScalingGroupResponse,
        GrpcReadinessProbe,
        GrpcStartupProbe,
        ListScalingGroupsResponse,
        ScalingGroup,
        ScalingGroupResourceRequest,
    )
    from chalk.testing import FeatureAssertion, StreamMessage, UploadFeatures
    from chalk.workflows import WorkflowDefinition
    from chalk.workflows._remote import WorkflowRunHandle

    QueryInput = Mapping[FeatureReference, Any] | pd.DataFrame | pl.DataFrame | DataFrame

from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features.resolver import Resolver
from chalk.features.tag import BranchId, DeploymentId, EnvironmentId
from chalk.ml import ModelClass, ModelEncoding, ModelRunCriterion, ModelType
from chalk.parsed.branch_state import BranchGraphSummary
from chalk.prompts import Prompt


class ChalkClient:
    """The `ChalkClient` is the primary Python interface for interacting with Chalk.

    You can use it to query data, trigger resolver runs, gather offline data, and more.
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        environment: EnvironmentId | None = None,
        api_server: str | None = None,
        branch: BranchId | None | Literal[True] = None,
        deployment_tag: str | None = None,
        preview_deployment_id: DeploymentId | None = None,
        session: requests.Session | None = None,
        query_server: str | None = None,
        additional_headers: Mapping[str, str] | None = None,
        default_job_timeout: float | timedelta | None = None,
        default_request_timeout: float | timedelta | None = None,
        default_connect_timeout: float | timedelta | None = None,
        local: bool = False,
        ssl_context: ssl.SSLContext | None = None,
    ):
        """Create a `ChalkClient` with the given credentials.

        Parameters
        ----------
        client_id
            The client ID to use to authenticate. Can either be a
            service token id or a user token id.
        client_secret
            The client secret to use to authenticate. Can either be a
            service token secret or a user token secret.
        environment
            The ID or name of the environment to use for this client.
            Not necessary if your `client_id` and `client_secret`
            are for a service token scoped to a single environment.
            If not present, the client will use the environment variable
            `CHALK_ENVIRONMENT`.
        api_server
            The API server to use for this client. Required if you are
            using a Chalk Dedicated deployment. If not present, the client
            will check for the presence of the environment variable
            `CHALK_API_SERVER`, and use that if found.
        query_server
            The query server to use for this client. Required if you are
            using a standalone Chalk query engine deployment. If not present,
            the client will default to the value of api_server.
        branch
            If specified, Chalk will route all requests from this client
            instance to the relevant branch. Some methods allow you to
            override this instance-level branch configuration by passing
            in a `branch` argument.

            If `True`, the client will pick up the branch from the
            current git branch.
        deployment_tag
            If specified, Chalk will route all requests from this client
            instance to the relevant tagged deployment. This cannot be
            used with the `branch` argument.
        preview_deployment_id
            If specified, Chalk will route all requests from this client
            instance to the relevant preview deployment.
        session
            A `requests.Session` to use for all requests. If not provided,
            a new session will be created.
        additional_headers
            A map of additional HTTP headers to pass with each request.
        default_job_timeout:
            The default wait timeout, in seconds, to wait for long-running jobs to complete
            when accessing query results.
            Jobs will not time out if this timeout elapses. For no timeout, set to `None`.
            The default is no timeout.
        default_request_timeout:
            The default wait timeout, in seconds, to wait for network requests to complete.
            If not specified, the default is no timeout.
        default_connect_timeout:
            The default connection timeout, in seconds, to wait for establishing a connection.
            This is separate from the request timeout and controls only the connection phase.
            If not specified, the default is no timeout.
        local
            If `True`, point the client at a local version of the code.
        ssl_context
            A `ssl.SSLContext` that can be loaded with self-signed certificates so that
            `requests` requests to servers hosted with self-signed certificates succeed.

        Raises
        ------
        ChalkAuthException
            If `client_id` or `client_secret` are not provided, there
            is no `~/.chalk.yml` file with applicable credentials,
            and the environment variables `CHALK_CLIENT_ID` and
            `CHALK_CLIENT_SECRET` are not set.
        """
        super().__init__()
        ...

    @property
    def api(self) -> "APINamespace":
        """Access Chalk management APIs.

        Returns an :class:`APINamespace` with sub-clients such as
        ``client.api.datasources`` for programmatic data-source management.
        """
        ...

    def query(
        self,
        input: Mapping[FeatureReference, Any] | Any,
        output: Sequence[FeatureReference] = (),
        now: datetime | None = None,
        staleness: Mapping[FeatureReference, str] | None = None,
        environment: EnvironmentId | None = None,
        tags: list[str] | None = None,
        preview_deployment_id: str | None = None,
        branch: BranchId | None = ...,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Mapping[str, str] | None = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        encoding_options: FeatureEncodingOptions | None = None,
        required_resolver_tags: list[str] | None = None,
        planner_options: Mapping[str, Union[str, int, bool]] | None = None,
        request_timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        headers: Mapping[str, str] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        trace: bool = False,
        translate_fqns: bool = False,
        value_metrics_tag_by_features: Sequence[FeatureReference] = (),
        input_schema_hint: InputSchemaHint | None = None,
    ) -> OnlineQueryResult:
        """Compute features values using online resolvers.
        See https://docs.chalk.ai/docs/query-basics for more information.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
            For example, `{User.id: 1234}`. Features can also be expressed as snakecased strings,
            e.g. `{"user.id": 1234}`
        output
            Outputs are the features that you'd like to compute from the inputs.
            For example, `[User.age, User.name, User.email]`.

            If an empty sequence, the output will be set to all features on the namespace
            of the query. For example, if you pass as input `{"user.id": 1234}`, then the query
            is defined on the `User` namespace, and all features on the `User` namespace
            (excluding has-one and has-many relationships) will be used as outputs.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        required_resolver_tags
            If specified, *all* `required_resolver_tags` must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        branch
            If specified, Chalk will route your request to the relevant branch.
        preview_deployment_id
            If specified, Chalk will route your request to the relevant preview deployment.
        query_name
            The semantic name for the query you're making, for example, `"loan_application_model"`.
            Typically, each query that you make from your application should have a name.
            Chalk will present metrics and dashboard functionality grouped by 'query_name'.
            If your query name matches a `NamedQuery`, the query will automatically pull outputs
            and options specified in the matching `NamedQuery`.
        query_name_version
            If `query_name` is specified, this specifies the version of the named query you're making.
            This is only useful if you want your query to use a `NamedQuery` with a specific name and a
            specific version. If a `query_name` has not been supplied, then this parameter is ignored.
        include_meta
            Returns metadata about the query execution under `OnlineQueryResult.meta`.
            This could make the query slightly slower.
            For more information, see https://docs.chalk.ai/docs/query-basics.
        explain
            Log the query execution plan. Requests using `explain=True` will be slower
            than requests using `explain=False`.

            If `True`, 'include_meta' will be set to `True` as well.
        store_plan_stages
            If `True`, the output of each of the query plan stages will be stored.
            This option dramatically impacts the performance of the query,
            so it should only be used for debugging.
        correlation_id
            You can specify a correlation ID to be used in logs and web interfaces.
            This should be globally unique, i.e. a `uuid` or similar. Logs generated
            during the execution of your query will be tagged with this correlation id.
        now
            The time at which to evaluate the query. If not specified, the current time will be used.
            If provided, this should be a timezone-aware datetime (e.g.
            `datetime(2025, 1, 1, tzinfo=timezone.utc)`). Naive datetimes are converted
            to UTC using the system's local timezone, which can cause unexpected boundary
            behavior in windowed aggregations when the local timezone is not UTC.

            This parameter is complex in the context of online_query since the online store
            only stores the most recent value of an entity's features. If `now` is in the past,
            it is extremely likely that `None` will be returned for cache-only features.

            This parameter is primarily provided to support:
                - controlling the time window for aggregations over cached has-many relationships
                - controlling the time window for aggregations over has-many relationships loaded from an
                  external database

            If you are trying to perform an exploratory analysis of past feature values, prefer `offline_query`.
        query_context
            An immutable context that can be accessed from Python resolvers.
            This context wraps a JSON-compatible dictionary or JSON string with type restrictions.
            See https://docs.chalk.ai/api-docs#ChalkContext for more information.
        trace
            Force tracing on the query. Requests using `trace=True` will be slower
            than requests using `trace=False`. Requires `opentelemetry-api` and
            `opentelemetry-sdk` to be installed (for example via the `chalkpy[tracing]`
            extra) for this to have any effect. When enabled, the query is traced
            regardless of the server's default trace sampling rate, and the query run
            records a trace ID that you can filter for on the Online Queries page in
            the Chalk dashboard.
        translate_fqns
            If `True`, rewrite windowed feature names in the response from their internal
            FQN format (e.g. `user.login_count__86400__`) to a human-readable format
            (e.g. `user.login_count["1d"]`).
        value_metrics_tag_by_features
            If your environment has feature value metrics enabled, this parameter specifies a list
            of features by which to tag these metrics. For example, if
            `value_metrics_tag_by_features=["user.category_id"]`, then the feature value metrics
            stored for this query will be tagged with the corresponding user's category_id.
        input_schema_hint
            An optional mapping specifying the intended columns of has-many inputs, e.g.
            `{User.transactions: [Transaction.id, Transaction.amount]}`. This pins the
            input's schema even when it cannot be inferred from the values themselves
            (e.g. an empty list of rows), which keeps the schema consistent across
            queries so the server can re-use cached query plans.

        Other Parameters
        ----------------
        meta
            Arbitrary `key:value` pairs to associate with a query.
        planner_options
            Dictionary of additional options to pass to the Chalk query engine.
            Values may be provided as part of conversations with Chalk support
            to enable or disable specific functionality.
        request_timeout
            Float value indicating number of seconds that the request should wait before timing out
            at the network level. May not cancel resources on the server processing the query.
        connect_timeout
            Float value indicating number of seconds to wait for establishing a connection.
            This is separate from request_timeout and controls only the connection phase.
        headers
            Additional headers to provide with the request

        Returns
        -------
        OnlineQueryResult
            Wrapper around the output features and any query metadata
            and errors encountered while running the resolvers.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> result = ChalkClient().query(
        ...     input={
        ...         User.name: "Katherine Johnson"
        ...     },
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        >>> result.get_feature_value(User.fico_score)
        """
        ...

    def multi_query(
        self,
        queries: list[OnlineQuery],
        environment: EnvironmentId | None = None,
        preview_deployment_id: str | None = None,
        branch: BranchId | None = ...,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        meta: Mapping[str, str] | None = None,
        use_feather: bool | None = True,
        compression: str | None = "uncompressed",
    ) -> BulkOnlineQueryResponse:
        """
        Execute multiple queries (represented by `queries=` argument) in a single request. This is useful if the
        queries are "rooted" in different `@features` classes -- i.e. if you want to load features for `User` and
        `Merchant` and there is no natural relationship object which is related to both of these classes, `multi_query`
        allows you to submit two independent queries.

        Returns a `BulkOnlineQueryResponse`, which is functionally a list of query results. Each of these result
        can be accessed by index. Individual results can be further checked for errors and converted
        to pandas or polars DataFrames.

        In contrast, `query_bulk` executes a single query with multiple inputs/outputs.

        Parameters
        ----------
        queries
            A list of the `OnlineQuery` objects you'd like to execute.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        branch
            If specified, Chalk will route your request to the relevant branch.
        preview_deployment_id
            If specified, Chalk will route your request to the
            relevant preview deployment.

        Other Parameters
        ----------------
        query_name
            The name for class of query you're making, for example, `"loan_application_model"`.
        query_context
            An immutable context that can be accessed from Python resolvers.
            This context wraps a JSON-compatible dictionary or JSON string with type restrictions.
            See https://docs.chalk.ai/api-docs#ChalkContext for more information.
        correlation_id
            A globally unique ID for the query, used alongside logs and
            available in web interfaces.
        meta
            Arbitrary `key:value` pairs to associate with a query.
        compression
            Which compression scheme to use pyarrow. Options are: `"zstd"`, `"lz4"`, `"uncompressed"`.

        Returns
        -------
        BulkOnlineQueryResponse
            An output containing results as a `list[BulkOnlineQueryResult]`,
            where each result contains a `DataFrame` of the results of each
            query or any errors.

        Examples
        --------
        >>> from chalk.client import ChalkClient, OnlineQuery
        >>> queries = [
        ...     OnlineQuery(
        ...         input={User.name: ['Katherine Johnson']},
        ...         output=[User.fico_score],
        ...     ),
        ...     OnlineQuery(
        ...         input={Merchant.name: ['Eight Sleep']},
        ...         output=[Merchant.address],
        ...     ),
        ... ]
        >>> result = ChalkClient().multi_query(queries)
        >>> result[0].get_feature_value(User.fico_score)
        """
        ...

    def query_bulk(
        self,
        input: Mapping[FeatureReference, Sequence[Any]],
        output: Sequence[FeatureReference] = (),
        now: Sequence[datetime] | None = None,
        staleness: Mapping[FeatureReference, str] | None = None,
        context: OnlineQueryContext | None = None,  # Deprecated.
        environment: EnvironmentId | None = None,
        store_plan_stages: bool = False,
        tags: list[str] | None = None,
        required_resolver_tags: list[str] | None = None,
        preview_deployment_id: str | None = None,
        branch: BranchId | None = ...,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        meta: Mapping[str, str] | None = None,
        explain: bool = False,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | None = None,
        translate_fqns: bool = False,
        trace: bool = False,
    ) -> BulkOnlineQueryResponse:
        """Compute features values for many rows of inputs using online resolvers.
        See https://docs.chalk.ai/docs/query-basics for more information on online query.

        This method is similar to `query`, except it takes in `list` of inputs, and produces one
        output per row of inputs.

        This method is appropriate if you want to fetch the same set of features for many different
        input primary keys.

        This method contrasts with `multi_query`, which executes multiple fully independent queries.

        This endpoint is not available in all environments.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to a list
            of the values.
        output
            Outputs are the features that you'd like to compute from the inputs.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        branch
            If specified, Chalk will route your request to the relevant branch.
        preview_deployment_id
            If specified, Chalk will route your request to the
            relevant preview deployment.
        now
            The time at which to evaluate the query. If not specified, the current time will be used.
            The length of this list must be the same as the length of the values in `input`.
            Each datetime should be timezone-aware (e.g. `datetime(2025, 1, 1, tzinfo=timezone.utc)`).
            Naive datetimes are converted to UTC using the system's local timezone.

        Other Parameters
        ----------------
        query_name
            The semantic name for the query you're making, for example, `"loan_application_model"`.
            Typically, each query that you make from your application should have a name.
            Chalk will present metrics and dashboard functionality grouped by 'query_name'.
            If your query name matches a `NamedQuery`, the query will automatically pull outputs
            and options specified in the matching `NamedQuery`.
        query_name_version
            If `query_name` is specified, this specifies the version of the named query you're making.
            This is only useful if you want your query to use a `NamedQuery` with a specific name and a
            specific version. If a `query_name` has not been supplied, then this parameter is ignored.
        query_context
            An immutable context that can be accessed from Python resolvers.
            This context wraps a JSON-compatible dictionary or JSON string with type restrictions.
            See https://docs.chalk.ai/api-docs#ChalkContext for more information.
        correlation_id
            A globally unique ID for the query, used alongside logs and
            available in web interfaces.
        meta
            Arbitrary `key:value` pairs to associate with a query.
        context
            Deprecated in favor of `environment` and `tags`.
        request_timeout
            Float value indicating number of seconds that the request should wait before timing out
            at the network level. May not cancel resources on the server processing the query
        explain
            Log the query execution plan. Requests using `explain=True` will be slower
            than requests using `explain=False`.
        headers
            Additional headers to provide with the request
        translate_fqns
            If `True`, rewrite windowed feature column names in each result from their
            internal FQN format (e.g. `user.login_count__86400__`) to a human-readable
            format (e.g. `user.login_count["1d"]`).
        trace
            Force tracing on the query. Requests using `trace=True` will be slower
            than requests using `trace=False`. Requires `opentelemetry-api` and
            `opentelemetry-sdk` to be installed (for example via the `chalkpy[tracing]`
            extra) for this to have any effect. When enabled, the query is traced
            regardless of the server's default trace sampling rate, and the query run
            records a trace ID that you can filter for on the Online Queries page in
            the Chalk dashboard.


        Returns
        -------
        BulkOnlineQueryResponse
            An output containing results as a `list[BulkOnlineQueryResult]`,
            where each result contains a `DataFrame` of the results of each query.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        ... ChalkClient().query_bulk(
        ...     input={User.name: ["Katherine Johnson", "Eleanor Roosevelt"]},
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        """
        ...

    def plan_query(
        self,
        input: Sequence[FeatureReference] | None = None,
        output: Sequence[FeatureReference] | None = None,
        staleness: Mapping[FeatureReference, str] | None = None,
        environment: EnvironmentId | None = None,
        tags: list[str] | None = None,
        preview_deployment_id: str | None = None,
        branch: Union[BranchId, None] = ...,
        query_name: str | None = None,
        query_name_version: str | None = None,
        meta: Mapping[str, str] | None = None,
        store_plan_stages: bool = False,
        explain: bool = False,
        num_input_rows: Optional[int] = None,
        headers: Mapping[str, str] | None = None,
        planner_options: Mapping[str, Any] | None = None,
        named_query: NamedQuery | None = None,
    ) -> PlanQueryResponse:
        """Plan a query without executing it.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
            For example, `{User.id: 1234}`. Features can also be expressed as snakecased strings,
            e.g. `{"user.id": 1234}`.
            Optional if a `named_query` is provided; if both are provided, the value from
            the `named_query` is used and this argument is ignored (with a warning).
        output
            Outputs are the features that you'd like to compute from the inputs.
            For example, `[User.age, User.name, User.email]`.
            Optional if a `named_query` is provided; if both are provided, the value from
            the `named_query` is used and this argument is ignored (with a warning).
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        branch
            If specified, Chalk will route your request to the relevant branch.
        preview_deployment_id
            If specified, Chalk will route your request to the relevant preview deployment.
        query_name
            The semantic name for the query you're making, for example, `"loan_application_model"`.
            Typically, each query that you make from your application should have a name.
            Chalk will present metrics and dashboard functionality grouped by 'query_name'.
            If your query name matches a `NamedQuery`, the query will automatically pull outputs
            and options specified in the matching `NamedQuery`.
        query_name_version
            If `query_name` is specified, this specifies the version of the named query you're making.
            This is only useful if you want your query to use a `NamedQuery` with a specific name and a
            specific version. If a `query_name` has not been supplied, then this parameter is ignored.
        meta
            Arbitrary `key:value` pairs to associate with a query.
        store_plan_stages
            If `True`, the plan will store the intermediate values at each stage in the plan
        explain
            If `True`, the plan will emit additional output to assist with debugging.
        num_input_rows:
            The number of input rows that this plan will be run with. If unknown, specify `None`.
        headers
            Additional headers to provide with the request
        planner_options
            Dictionary of additional options to pass to the Chalk query engine.
            Values may be provided as part of conversations with Chalk support
            to enable or disable specific functionality.
        named_query
            A `NamedQuery` to plan. When provided, the `NamedQuery` takes precedence
            over `input`, `output`, `staleness`, `tags`, `query_name`, `query_name_version`,
            `meta`, and `planner_options`.

        Returns
        -------
        PlanQueryResponse
            The query plan, including the resolver execution order and the
            resolver execution plan for each resolver.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> result = ChalkClient().plan_query(
        ...     input=[User.id],
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        >>> result.rendered_plan
        >>> result.output_schema

        You can also plan a `NamedQuery` directly:

        >>> from chalk import NamedQuery
        >>> from chalk.client import ChalkClient
        >>> nq = NamedQuery(name="fraud_model", input=[User.id], output=[User.fico_score])
        >>> result = ChalkClient().plan_query(named_query=nq)
        >>> result.errors
        """
        ...

    def check_stream_scenario(
        self,
        *messages: StreamMessage | FeatureAssertion | UploadFeatures,
        seed_online_store: Mapping[FeatureReference, Any] | None = None,
        branch: Union[BranchId, ellipsis, None] = ...,
        environment: EnvironmentId | None = None,
        float_rel_tolerance: float = 1e-6,
        float_abs_tolerance: float = 1e-12,
        show_table: bool = False,
    ) -> None:
        """Test complex stream workflows that update materialized aggregates or depend on cached state.

        `messages` is a sequence of `StreamMessage`, `FeatureAssertion`, and `UploadFeatures`
        objects, processed in order. For each `StreamMessage`, the bytes are parsed locally using
        `stream_resolver`'s parser (the same pipeline as `check_stream_parsing`) and the resulting
        feature values are uploaded via `upload_features` against `branch`. For each
        `FeatureAssertion`, an online query is run using the set fields of `assertion.input` as
        input, and the resulting feature values are compared against the set fields of
        `assertion.output`. A mismatch raises `AssertionError`. `Windowed[...]` fields are
        supported on either side: pass a ``{window: value}`` dict
        (e.g. ``transaction_count={"1d": 2, "30d": 7}``) and each bucket is checked independently.

        Use `UploadFeatures(...)` (or the `seed_online_store` keyword) to prime the branch online
        store with static feature data (e.g. candidate rows looked up by a join inside a windowed
        expression) — useful when the resolvers under test depend on existing online state. The
        upload runs through the same gRPC `upload_features` path as a regular
        `ChalkClient.upload_features` call (no materialized-aggregate refresh).

        Use the `timestamp` field on `StreamMessage` to control the feature time of the uploaded
        features (useful for out-of-order processing tests).

        Parameters
        ----------
        messages
            The scenario steps, processed left-to-right.
        seed_online_store
            Equivalent to prepending a single ``UploadFeatures(seed_online_store)`` step at the
            head of the scenario. Convenient for the common upfront-priming case. If both this
            kwarg and positional ``UploadFeatures`` steps are provided, the kwarg runs first.
        branch
            The branch to upload features into and run assertion queries against.
        environment
            The environment under which to run the scenario.
        float_rel_tolerance
            Relative tolerance for float comparisons in `FeatureAssertion` checks. Default is 1e-6.
        float_abs_tolerance
            Absolute tolerance for float comparisons in `FeatureAssertion` checks. Default is 1e-12.
            Values are considered equal if either tolerance is met.
        show_table
            If True, always print the `Chalk Feature Value Check Table` (Kind/Name/Value, modeled
            on `ChalkClient.check`) for each `FeatureAssertion` step — even on success. On a
            mismatch the table is always printed, regardless of this flag.

        Raises
        ------
        AssertionError
            If a `FeatureAssertion` mismatches the queried output.
        ValueError
            If a `StreamMessage` is missing `stream_resolver`, or if an `UploadFeatures` step
            has features with mismatched row counts.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> from chalk.testing import StreamMessage, FeatureAssertion, UploadFeatures
        >>> from datetime import datetime
        >>> ChalkClient().check_stream_scenario(
        ...     UploadFeatures({
        ...         Profile.id: [101, 102, 103],
        ...         Profile.embedding: [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        ...     }),
        ...     StreamMessage(
        ...         timestamp=datetime(2026, 1, 1, 12, 20),
        ...         message=b'{"id": 1, "user_id": 1, "amount": 10.0}',
        ...         stream_resolver=transaction_stream,
        ...     ),
        ...     StreamMessage(
        ...         timestamp=datetime(2026, 1, 1, 12, 20),
        ...         message=b'{"id": 1, "name": "Bartleby"}',
        ...         stream_resolver=create_user,
        ...     ),
        ...     FeatureAssertion(
        ...         input=User(id=1),
        ...         output=User(name="Bartleby", transaction_count={"1d": 1}),
        ...     ),
        ...     branch="my-branch",
        ... )
        """
        ...

    def check(
        self,
        input: Mapping[FeatureReference, Any] | Any,
        assertions: Mapping[FeatureReference, Any],
        cache_hits: Iterable[str | Any] | None = None,
        feature_errors: Mapping[str | Any, Any] | None = None,
        query_errors: Optional[Collection[ChalkError]] = None,
        now: datetime | None = None,
        staleness: Mapping[FeatureReference, str] | None = None,
        tags: list[str] | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        encoding_options: FeatureEncodingOptions | None = None,
        required_resolver_tags: list[str] | None = None,
        planner_options: Mapping[str, Union[str, int, bool]] | None = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        value_metrics_tag_by_features: Sequence[FeatureReference] = (),
        show_table: bool = False,
        float_rel_tolerance: float = 1e-6,
        float_abs_tolerance: float = 1e-12,
        prefix: bool = True,
        show_matches: bool = True,
    ):
        """Check whether expected results of a query match Chalk query ouputs.
        This function should be used in integration tests.
        If you're using `pytest`, `pytest.fail` will be executed on an error.
        Otherwise, an `AssertionError` will be raised.

        Parameters
        ----------
        input
            A feature set or a mapping of `{feature: value}` of givens.
            All values will be encoded to the json representation.
        assertions
            A feature set or a mapping of `{feature: value}` of expected outputs.
            For values where you do not care about the result, use an `...` for the
            feature value (i.e. when an error is expected).
        cache_hits
            A list of the features that you expect to be read from the online
            store, e.g.
            >>> cache_hits=[Actor.name, Actor.num_appearances]
        feature_errors
            A map from the expected feature name to the expected errors for that feature, e.g.
            >>> expected_feature_errors={
            ...     User.id: [ChalkError(...), ChalkError(...)]
            ... }
            >>> errors={
            ...     "user.id": [ChalkError(...), ChalkError(...)]
            ... }
        query_errors
            A list of the expected query error.
        now
            The time at which to evaluate the query. If not specified, the current time will be used.
            If provided, this should be a timezone-aware datetime (e.g.
            `datetime(2025, 1, 1, tzinfo=timezone.utc)`). Naive datetimes are converted
            to UTC using the system's local timezone, which can cause unexpected boundary
            behavior in windowed aggregations when the local timezone is not UTC.

            This parameter is complex in the context of `online_query` since the online store
            only stores the most recent value of an entity's features. If `now` is in the past,
            it is extremely likely that `None` will be returned for cache-only features.

            This parameter is primarily provided to support:
                - controlling the time window for aggregations over cached has-many relationships
                - controlling the time window for aggregations over has-many relationships loaded from an
                  external database

            If you are trying to perform an exploratory analysis of past feature values, prefer `offline_query`.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        query_name
            The semantic name for the query you're making, for example, `"loan_application_model"`.
            Typically, each query that you make from your application should have a name.
            Chalk will present metrics and dashboard functionality grouped by 'query_name'.
            If your query name matches a `NamedQuery`, the query will automatically pull outputs
            and options specified in the matching `NamedQuery`.
        query_name_version
            If `query_name` is specified, this specifies the version of the named query you're making.
            This is only useful if you want your query to use a `NamedQuery` with a specific name and a
            specific version. If a `query_name` has not been supplied, then this parameter is ignored.
        query_context
            An immutable context that can be accessed from Python resolvers.
            This context wraps a JSON-compatible dictionary or JSON string with type restrictions.
            See https://docs.chalk.ai/api-docs#ChalkContext for more information.
        required_resolver_tags
            If specified, *all* `required_resolver_tags` must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        show_table
            Print the feature value table even if no errors were found.
        show_matches
            If `True`, show the expected and actual values that match.
            If `False`, only show the expected and actual values that do not match.
        float_rel_tolerance
            The relative tolerenance to allow for float equality.
            If you specify both `float_rel_tolerance` and `float_abs_tolerance`,
            the numbers will be considered equal if either tolerance is met.
            Equivalent to:
            >>> abs(a - b) <= float_rel_tolerance * max(abs(a), abs(b))
        float_abs_tolerance
            The absolute tolerenance to allow for float equality.
            If you specify both `float_rel_tolerance` and `float_abs_tolerance`,
            the numbers will be considered equal if either tolerance is met.
            Equivalent to:
            >>> abs(a - b) <= float_abs_tolerance
        prefix
            Whether to show the prefix for feature names in the table.

        Other Parameters
        ----------------
        planner_options
            Dictionary of additional options to pass to the Chalk query engine.
            Values may be provided as part of conversations with Chalk support
            to enable or disable specific functionality.
        request_timeout
            Float value indicating number of seconds that the request should wait before timing out
            at the network level. May not cancel resources on the server processing the query.
        headers
            Additional headers to provide with the request

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> result = ChalkClient().check(
        ...     input={Actor.id: "nm0000001"},
        ...     assertions={Actor.num_movies: 40},
        ... )
        Chalk Feature Value Mismatch
        ┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
        ┃ Kind   ┃ Name                 ┃ Value     ┃
        ┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
        │ Expect │ actor.id             │ nm0000001 │
        │ Actual │ actor.id             │ nm0000001 │
        │ Expect │ actor.num_appearanc… │ 40        │
        │ Actual │ actor.num_appearanc… │ 41        │
        └────────┴──────────────────────┴───────────┘
        """
        ...

    def list_datasets(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        search: str | None = None,
    ) -> ListDatasetsResponse:
        """
        List datasets in the current environment.

        Returns a single page of datasets ordered by creation time, along
        with a cursor for fetching the next page if more results are
        available. Datasets are scoped to the active environment.

        cursor
            Opaque pagination token returned in the ``cursor`` field of a
            previous ``list_datasets`` response. Pass it back verbatim to
            fetch the next page. On the first call, leave as ``None``.
        limit
            Maximum number of datasets to return in this page. Defaults to
            ``100`` on the server when not provided.
        search
            Case-insensitive substring filter applied to dataset names.

        Returns
        -------
        ListDatasetsResponse
            A page of dataset metadata. The ``cursor`` field on the response
            will be empty when there are no further pages to fetch.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()

        List the most recent datasets:

        >>> response = client.list_datasets()
        >>> for dataset in response.datasets:
        ...     print(dataset.dataset_name, dataset.latest_status)

        Paginate through all datasets in pages of 10:

        >>> response = client.list_datasets(limit=10)
        >>> while response.cursor:
        ...     response = client.list_datasets(cursor=response.cursor, limit=10)
        """
        ...

    def get_dataset(
        self,
        dataset_name: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        *,
        dataset_id: str | uuid.UUID | None = None,
        revision_id: str | uuid.UUID | None = None,
        job_id: str | uuid.UUID | None = None,
    ) -> Dataset:
        """Get a Chalk `Dataset` containing data from a previously created dataset.

        If an offline query has been created with a dataset name, `.get_dataset` will
        return a Chalk `Dataset`.
        The `Dataset` wraps a lazily-loading Chalk `DataFrame` that enables us to analyze
        our data without loading all of it directly into memory.
        See https://docs.chalk.ai/docs/query-offline for more information.

        Parameters
        ----------
        dataset_name
            The name of the `Dataset` to return.
            Previously, you must have supplied a dataset name upon an offline query.
            Dataset names are unique for each environment.
            If 'dataset_name' is provided, then 'job_id' should not be provided.
        dataset_id
            A UUID returned in the `Dataset` object from an offline query.
            Dataset ids are unique for each environment.
            If 'dataset_id' is provided, then 'dataset_name' and 'revision_id' should not be provided.
        revision_id
            The unique id of the `DatasetRevision` to return.
            If a previously-created dataset did not have a name, you can look it
            up using its unique job id instead.
            If 'revision_id' is provided, then 'dataset_name' and 'dataset_id' should not be provided.
        environment
            The environment under which to execute the request.
            API tokens can be scoped to an environment.
            If no environment is specified in the request,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.

        Other Parameters
        ----------------
        job_id
            Same as revision id. Deprecated.

        Returns
        -------
        Dataset
            A `Dataset` that lazily loads your query data.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> uids = [1, 2, 3, 4]
        >>> at = datetime.now(timezone.utc)
        >>> X = ChalkClient().offline_query(
        ...     input={
        ...         User.id: uids,
        ...     },
        ...     input_times=[at] * len(uids),
        ...     output=[
        ...         User.id,
        ...         User.fullname,
        ...         User.email,
        ...         User.name_email_match_score,
        ...     ],
        ...     dataset='my_dataset_name'
        ... )

        Some time later...

        >>> dataset = ChalkClient().get_dataset(
        ...     dataset_name='my_dataset_name'
        ... )
        ...

        or

        >>> dataset = ChalkClient().get_dataset(
        ...     job_id='00000000-0000-0000-0000-000000000000'
        ... )
        ...

        If memory allows:

        >>> df: pd.DataFrame = dataset.get_data_as_pandas()
        """
        ...

    def create_dataset(
        self,
        input: QueryInput,
        dataset_name: str | None = None,
        environment: EnvironmentId | None = None,
        branch: BranchId | None = ...,
        wait: bool = False,
        show_progress: bool | ellipsis = ...,
        timeout: float | timedelta | ellipsis | None = ...,
    ) -> Dataset:
        """Create a Chalk `Dataset`.

        The `Dataset` wraps a lazily-loading Chalk `DataFrame` that enables us to analyze
        our data without loading all of it directly into memory.
        See https://docs.chalk.ai/docs/query-offline for more information.

        Parameters
        ----------
        input
            The features for which there are known values.
            It can be a mapping of features to a list of values for each
            feature, or an existing `DataFrame`.
        dataset_name
            A unique name that if provided will be used to generate and
            save a `Dataset` constructed from the inputs.
        environment
            The environment under which to execute the request.
            API tokens can be scoped to an environment.
            If no environment is specified in the request,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        wait
            Whether to wait for job completion.
        show_progress
            If `True`, progress bars will be shown while the query is running.
            Primarily intended for use in a Jupyter-like notebook environment.
            This flag will also be propagated to the methods of the resulting
            `Dataset`.
        timeout:
            How long to wait, in seconds, for job completion before raising a `TimeoutError`.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.

        Returns
        -------
        Dataset
            A Chalk `Dataset`.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> uids = [1, 2, 3, 4]
        >>> names = ['a', 'b', 'c', 'd']
        >>> dataset = ChalkClient().create_dataset(
        ...     input={
        ...         User.id: uids,
        ...         User.name: names,
        ...     },
        ...     dataset_name='my_dataset'
        ... )
        >>> df = dataset.get_data_as_pandas()
        """
        ...

    def offline_query(
        self,
        input: Union[QueryInput, OfflineQueryInputUri, ChalkDfDataFrame] | None = None,
        input_times: Sequence[datetime] | datetime | None = None,
        output: Sequence[FeatureReference] = (),
        required_output: Sequence[FeatureReference] = (),
        environment: EnvironmentId | None = None,
        dataset_name: str | None = None,
        branch: BranchId | None = ...,
        correlation_id: str | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        max_samples: int | None = None,
        wait: bool = False,
        show_progress: bool | ellipsis = ...,
        timeout: float | timedelta | ellipsis | None = ...,
        recompute_features: bool | list[FeatureReference] = False,
        sample_features: list[FeatureReference] | None = None,
        lower_bound: datetime | timedelta | str | None = None,
        upper_bound: datetime | timedelta | str | None = None,
        lower_bound_inserted_at: datetime | timedelta | str | None = None,
        upper_bound_inserted_at: datetime | timedelta | str | None = None,
        store_plan_stages: bool = False,
        explain: bool = False,
        tags: list[str] | None = None,
        required_resolver_tags: list[str] | None = None,
        planner_options: Mapping[str, Union[str, int, bool]] | None = None,
        spine_sql_query: str | None = None,
        resources: ResourceRequests | None = None,
        run_asynchronously: bool = False,
        store_online: bool = False,
        store_offline: bool = False,
        num_shards: int | None = None,
        num_workers: int | None = None,
        completion_deadline: Union[timedelta, OfflineQueryDeadlineOptions, None] = None,
        max_retries: int | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        *,  # Keyword-only: these were added later and must not be passed positionally.
        input_sql: str | None = None,
        use_metaplanner: bool | None = None,
        unload_resolvers: UnloadResolvers = None,
        feature_for_lower_upper_bound: FeatureReference | None = None,
        write_to: str | None = None,
    ) -> Dataset:
        """Compute feature values from the offline store or by running offline/online resolvers.
        See `Dataset` for more information.

        Parameters
        ----------
        input
            The features for which there are known values.
            It can be a mapping of features to a list of values for each
            feature, or an existing `DataFrame`.
            Each element in the `DataFrame` or list of values represents
            an observation in line with the timestamp in `input_times`.

            When `input` is a chalkdf DataFrame, the underlying plan is serialized
            and executed server-side. Use this for inputs referencing server-reachable data
            sources (e.g., `DataFrame.scan(...)`, `DataFrame.scan_glue_iceberg(...)`,
            `DataFrame.from_dataset(...)`, `DataFrame.from_catalog_table(...)`).
            Avoid using chalkdf DataFrames that embed large literal data via `DataFrame.from_dict(...)`
            or `DataFrame.from_arrow(...)`. Instead, pass that data through `input`
            directly (as a dict, pandas DataFrame, polars DataFrame, or pyarrow Table).
        spine_sql_query
            A SQL query that will query your offline store and use the result as input.
            See https://docs.chalk.ai/docs/query-offline#input for more information.
        input_times
            The time at which the given inputs should be observed for point-in-time correctness. If given a list of
            times, the list must match the length of the `input` lists. Each element of input_time corresponds with the
            feature values at the same index of the `input` lists.
            See https://docs.chalk.ai/docs/temporal-consistency for more information.
        input_sql
            An alternative to `input`: a ChalkSQL query that returns values
            to use as inputs.
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row) in
            the resulting `DataFrame`, its value will be `None`.
        recompute_features
            Used to control whether resolvers are allowed to run in order to compute feature values.

            If `True`, all output features will be recomputed by resolvers.
            If `False`, all output features will be sampled from the offline store.
            If a list, all output features in recompute_features will be recomputed,
            and all other output features will be sampled from the offline store.
        sample_features
            A list of features that will always be sampled, and thus always excluded from recompute.
            Should not overlap with any features used in `recompute_features` argument.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        dataset_name
            A unique name that if provided will be used to generate and
            save a `Dataset` constructed from the list of features computed
            from the inputs.
        max_samples
            The maximum number of samples to include in the `DataFrame`.
            If not specified, all samples will be returned.
        branch
            If specified, Chalk will route your request to the relevant branch.
            If `None`, Chalk will route your request to a non-branch deployment.
            If not specified, Chalk will use the current client's branch info.
        correlation_id
            You can specify a correlation ID to be used in logs and web interfaces.
            This should be globally unique, i.e. a `uuid` or similar. Logs generated
            during the execution of your query will be tagged with this correlation id.
        query_context
            An immutable context that can be accessed from Python resolvers.
            This context wraps a JSON-compatible dictionary or JSON string with type restrictions.
            See https://docs.chalk.ai/api-docs#ChalkContext for more information.
        wait
            Whether to wait for job completion.
        show_progress
            If `True`, progress bars will be shown while the query is running.
            Primarily intended for use in a Jupyter-like notebook environment.
            This flag will also be propagated to the methods of the resulting
            `Dataset`.
        timeout:
            How long to wait, in seconds, for job completion before raising a `TimeoutError`.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        lower_bound
            If specified, the query will only be run on data observed after this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        upper_bound
            If specified, the query will only be run on data observed before this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        lower_bound_inserted_at
            If specified, the query will only include rows whose `inserted_at` is at or after this
            timestamp — i.e. rows written to the offline store after this point in time. This is
            distinct from `lower_bound`, which compares against `observed_at`.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        upper_bound_inserted_at
            If specified, the query will only include rows whose `inserted_at` is at or before this
            timestamp — i.e. rows written to the offline store before this point in time. This is
            distinct from `upper_bound`, which compares against `observed_at`.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        feature_for_lower_upper_bound
            Override the feature whose values are filtered against `lower_bound` and `upper_bound`.
            By default, the bounds filter against the `FeatureTime` feature of each output's namespace.
            Must reference a scalar or `FeatureTime` feature.
        store_plan_stages
            If `True`, the output of each of the query plan stages will be stored
            in S3/GCS. This will dramatically impact the performance of the query,
            so it should only be used for debugging.
            These files will be visible in the web dashboard's query detail view, and
            can be downloaded in full by clicking on a plan node in the query plan visualizer.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        required_resolver_tags
            If specified, *all* `required_resolver_tags` must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        resources
            Override resource requests for processes with isolated resources, e.g., offline queries and cron jobs.
            See `ResourceRequests` for more information.
        run_asynchronously
            Boots a Kubernetes job to run the queries in their own pods, separate from the engine and branch servers.
            This is useful for large datasets and jobs that require a long time to run.
        store_online
            If `True`, the output of the query will be stored in the online store.
        store_offline
            If `True`, the output of the query will be stored in the offline store.
        num_shards
            If specified, the query will be run asynchronously, splitting the input across `num_shards` shards.
        num_workers
            If specified, the query will be run asynchronously across a maximum `num_workers` pod workers at any time.
            This parameter is useful if you have a large number of shards and would like to limit the number of pods running at once.
        completion_deadline
            If specified as a timedelta, applies a completion deadline to each shard; each shard of the query will fail (without being retried) if not completed within the duration.
            If specified as an OfflineQueryDeadlineOptions, allows more fine-grained control of shard- or query-level deadlines, with options to retry on shard failure or not.
            If not specified, defaults to an 18-hour deadline for each shard with no retries.
        max_retries
            Number of times failed offline query shards can be retried. The maximum number of attempts is 1 higher than this number and each shard has an independent retry budget.
            Errors that appear to be deterministic will not provoke retries.
            By default, this is set to 2, which is at most 3 attempts.
        query_name
            The name of the query to execute. If provided, will create a new named query or fill in missing parameters from a preexisting execution.
        query_name_version
            The version of the named query to execute.
        use_metaplanner
            Controls whether the query will use the metaplanner: https://docs.chalk.ai/docs/metaplanning
        unload_resolvers
            Specifies resolvers to unload, optionally with partition expressions.
            Can be a list of resolver FQNs or `Resolver` objects (no partitioning),
            or a dict mapping resolvers to a tuple of partition expressions.
            Partition expressions can be strings (raw FQNs), `Filter` objects
            (e.g., ``Bean.jar_id == Jar.id``), or ``Underscore`` expressions.
        write_to
            A storage URI (e.g. `s3://bucket/path`) to which the engine should write
            the query's output rows directly.

        Other Parameters
        ----------------
        required_output
            The features that you'd like to sample and must exist
            in each resulting row. Rows where a `required_output`
            was never stored in the offline store will be skipped.
            This differs from specifying the feature in `output`,
            where instead the row would be included, but the feature
            value would be `None`.

        Returns
        -------
        Dataset
            A Chalk `Dataset`.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> uids = [1, 2, 3, 4]
        >>> at = datetime.now(tz=timezone.utc)
        >>> dataset = ChalkClient().offline_query(
        ...     input={
        ...         User.id: uids,
        ...     },
        ...     input_times=[at] * len(uids),
        ...     output=[
        ...         User.id,
        ...         User.fullname,
        ...         User.email,
        ...         User.name_email_match_score,
        ...     ],
        ...     run_asynchronously=True,
        ...     resources={'cpu': '8', 'memory': '15Gi'},
        ...     dataset_name='my_dataset'
        ... )
        >>> df = dataset.get_data_as_pandas()
        """
        ...

    def cancel_offline_query(
        self,
        offline_query_id: str,
    ) -> None:
        """Cancel an in-progress async offline query by its ID.

        Parameters
        ----------
        offline_query_id
            The ID of the offline query to cancel. Returns an error if the query
            is not found or is not in a cancellable state (i.e. not WORKING or QUEUED).

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().cancel_offline_query(
        ...     offline_query_id="oq_1234567890abcdef",
        ... )
        """
        ...

    def run_scheduled_query(
        self,
        name: str,
        planner_options: Optional[Mapping[str, Any]],
        incremental_resolvers: Optional[Sequence[str]],
        max_samples: Optional[int],
        env_overrides: Optional[Mapping[str, str]],
        *,  # Keyword-only: these were added later and must not be passed positionally.
        unload_resolvers: UnloadResolvers = None,
    ) -> ManualTriggerScheduledQueryResponse:
        """
        Manually trigger a scheduled query request.

        Parameters
        ----------
        name
            The name of the scheduled query to be triggered.
        incremental_resolvers
            If set to `None`, Chalk will incrementalize resolvers in the query's root namespaces.
            If set to a list of resolvers, this set will be used for incrementalization.
            Incremental resolvers must return a feature time in its output, and must return a `DataFrame`.
            Most commonly, this will be the name of a SQL file resolver. Chalk will ingest all new data
            from these resolvers and propagate changes to values in the root namespace.
        max_samples
            The maximum number of samples to compute.
        env_overrides:
            A dictionary of environment values to override during this specific triggered query.

        Other Parameters
        ----------------
        planner_options
            A dictionary of options to pass to the planner.
            These are typically provided by Chalk Support for specific use cases.

        Returns
        -------
        ManualTriggerScheduledQueryResponse
            A response message containing metadata around the triggered run.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> ChalkGRPCClient().run_scheduled_query(
        ...     name="my_scheduled_query",
        ... )
        """
        ...

    def get_scheduled_query_run_history(
        self, name: str, limit: int = 10, include_run_details: bool = False
    ) -> List[ScheduledQueryRun]:
        """
        Get the run history for a scheduled query.

        Parameters
        ----------
        name
            The name of the scheduled query.
        limit
            The maximum number of runs to return. Defaults to 10.
        include_run_details
            Whether or not to populate the metadata fields of each run.

        Returns
        -------
        list[ScheduledQueryRun]
            A response message containing the list of scheduled query runs.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_scheduled_query_run_history(
        ...     name="my_scheduled_query",
        ...     limit=20,
        ... )
        """
        ...

    def get_scheduled_query_run_details(
        self, scheduled_run: ScheduledQueryRun
    ) -> Union[WorkflowExecutionInfo, OfflineQueryInfo, None]:
        """Fetch the offline query or workflow execution metadata underlying a scheduled query run.

        Parameters
        ----------
        scheduled_run
            The scheduled query run to enrich with metadata.
        """
        ...

    def list_jobs(
        self,
        state: Optional[
            Literal["scheduled", "running", "completed", "failed", "canceled", "not_ready", "waiting"]
        ] = None,
        kind: Optional[
            Literal["async_offline_query", "scheduled_query", "script_task", "chalksql_run", "dataframe_run"]
        ] = None,
        operation_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[JobQueueItem]:
        """
        List jobs in the data plane job queue.

        Parameters
        ----------
        state
            Filter by job state (scheduled, running, completed, failed, canceled, not_ready).
        kind
            Filter by job kind (async_offline_query, scheduled_query, script_task, chalksql_run, dataframe_run).
        operation_id
            Filter by operation ID.
        limit
            Maximum number of jobs to return. Defaults to 50.
        offset
            Offset for pagination. Defaults to 0.

        Returns
        -------
        List[JobQueueItem]
            The list of jobs.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().list_jobs(state="running", limit=10)
        """
        ...

    def get_offline_query_report(self, offline_query_id: str) -> Optional[OfflineQueryReport]:
        """
        Get the batch report associated with the offline query in environment.

        Parameters
        ----------
        offline_query_id
            Offline query's ID.

        environment_id
            Environment ID of offline query.

        Returns
        -------
        Optional[OfflineQueryReport]
            The OfflineQueryReport object if it exists.
        """
        ...

    def get_offline_query_profile_summary(self, offline_query_id: str) -> OfflineQueryProfileSummary:
        """Get the profile metrics summary for an offline query.

        Parameters
        ----------
        offline_query_id
            Offline query's ID.

        Returns
        -------
        OfflineQueryProfileSummary
            Aggregated profile metrics and warnings for the offline query.
        """
        ...

    def get_online_query_input_values(
        self,
        query: Union[OnlineQueryResult, str],
        query_timestamp: datetime | None = None,
    ) -> List[Dict[str, Any]]:
        """Fetch the inputs that were sent to a past online query.

        Retrieves the stored input feature values for an online query run from the
        offline store and returns them as a list of row dicts (one dict per input row,
        keyed by feature fqn). This is the same data shown in the inputs pane of a
        query run's detail page in the dashboard.

        Inputs are only available when online-query value persistence is enabled for the
        environment:

        - ``CHALK_PLANNER_PERSIST_VALUES_OFFLINE_STORE=1`` is required for online queries to
          persist their inputs/outputs to the value tables. It is off by default; without it
          this returns an empty list.
        - ``CHALK_PERSIST_TO_OFFLINE_STORE_QUERY_LOG`` controls whether the run is written to
          the query log at all; without it the query run cannot be found.

        (Offline queries always persist their inputs; this method is for online queries.)

        Parameters
        ----------
        query
            Either the operation id of the online query (a string), or the ``OnlineQueryResult``
            returned by a prior ``query(...)`` call. When a result is passed, both the operation
            id and the query timestamp are read from ``result.meta``, so the query must have been
            run with ``include_meta=True``.
        query_timestamp
            The approximate time the query ran. Without it the query run is only looked up within
            the last 24 hours; pass it to fetch inputs for older queries. It is taken automatically
            from ``result.meta.query_timestamp`` when an ``OnlineQueryResult`` is passed.

        Returns
        -------
        List[Dict[str, Any]]
            The query's inputs, one dict per row keyed by feature fqn. Returns an empty
            list if the query did not persist its values (see the env vars above).

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> result = client.query(input={User.id: 1}, output=[User.name], include_meta=True)
        >>> client.get_online_query_input_values(result)
        [{"user.id": 1}]
        """
        ...

    def get_named_query_metadata(
        self,
        name: str,
        query_version: str | None = None,
        branch: str | None = None,
    ) -> List[NamedQueryMetadata]:
        """
        Get the metadata associated with named queries.

        Parameters
        ----------
        name
            The name of the named query.
        query_version
            The query version of the named query. Returns all versions of the named query by default.
        branch
            The branch name to get the named query from. By default will use the mainline deployment.

        Returns
        -------
        list[ScheduledQueryRun]
            A response message containing the list of metadata of named queries.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_named_query_metadata(
        ...     name="my_named_query",
        ...     query_version="1.1.0",
        ... )
        """
        ...

    def get_offline_store_table_name(
        self,
        feature: Any,
        include_historical: bool = False,
    ) -> "str | list[str]":
        """Get the offline store table name(s) for a feature.

        Parameters
        ----------
        feature
            The feature to look up. Can be a feature class attribute (e.g. ``User.fico_score``)
            or a string FQN (e.g. ``"user.fico_score"``).
        include_historical
            If ``False`` (default), returns the current active table name as a string.
            If ``True``, returns all historical table names ordered by internal version
            (oldest to newest).

        Returns
        -------
        str | list[str]
            The table name string, or a list of table name strings if ``include_historical=True``.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_offline_store_table_name(User.fico_score)
        >>> ChalkClient().get_offline_store_table_name("user.fico_score", include_historical=True)
        """
        ...

    def get_all_offline_store_table_names(
        self,
        deployment_id: str | None = None,
    ) -> "list[OfflineStoreTable]":
        """Get the offline store table name for every feature and internal version in a deployment.

        Useful for reverse-mapping a ``feat_<hash>`` offline store table name back to its feature.

        Parameters
        ----------
        deployment_id
            The deployment to look up. If ``None``, uses the environment's active deployment.

        Returns
        -------
        list[OfflineStoreTable]
            One entry per feature and internal version, each with ``fqn``, ``internal_version``, and ``table_name``.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_all_offline_store_table_names()
        """
        ...

    def get_feature_from_offline_store_table_name(
        self,
        table_name: str,
        deployment_id: str | None = None,
    ) -> "OfflineStoreTable | None":
        """Find the feature for a given offline store table name (reverse lookup).

        Parameters
        ----------
        table_name
            The ``feat_<hash>`` offline store table name to look up.
        deployment_id
            The deployment to search. If ``None``, uses the environment's active deployment.

        Returns
        -------
        OfflineStoreTable | None
            The matching table (with ``fqn`` and ``internal_version``), or ``None`` if no feature maps to that table name.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_feature_from_offline_store_table_name("feat_5c00ed88...")
        """
        ...

    def prompt_evaluation(
        self,
        prompts: list[Prompt | str],
        dataset_name: str | None = None,
        dataset_id: str | None = None,
        revision_id: str | None = None,
        reference_output: FeatureReference | None = None,
        evaluators: list[str] | None = None,
        meta: Mapping[str, str] | None = None,
        input: QueryInput | None = None,
        input_times: Sequence[datetime] | datetime | None = None,
        output: Sequence[FeatureReference] = (),
        required_output: Sequence[FeatureReference] = (),
        environment: EnvironmentId | None = None,
        branch: BranchId | None = ...,
        correlation_id: str | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        max_samples: int | None = None,
        wait: bool = False,
        show_progress: bool | ellipsis = ...,
        timeout: float | timedelta | ellipsis | None = ...,
        recompute_features: bool | list[FeatureReference] = False,
        sample_features: list[FeatureReference] | None = None,
        lower_bound: datetime | timedelta | str | None = None,
        upper_bound: datetime | timedelta | str | None = None,
        store_plan_stages: bool = False,
        explain: bool = False,
        tags: list[str] | None = None,
        required_resolver_tags: list[str] | None = None,
        planner_options: Mapping[str, Union[str, int, bool]] | None = None,
        spine_sql_query: str | None = None,
        resources: ResourceRequests | None = None,
        run_asynchronously: bool = False,
        store_online: bool = False,
        store_offline: bool = False,
        num_shards: int | None = None,
        num_workers: int | None = None,
        completion_deadline: timedelta | None = None,
        max_retries: int | None = None,
        *,  # Keyword-only: these were added later and must not be passed positionally.
        feature_for_lower_upper_bound: FeatureReference | None = None,
    ) -> Dataset:
        """Runs an evaluation on a set of prompts.
        See https://docs.chalk.ai/docs/prompts#prompt-evaluation for more information.

        Parameters
        ----------
        prompts
            The list of prompts to use for the evaluation.
            This can be a list of `Prompt` objects or a list of named prompts.
        dataset_name
            The name of the `Dataset` to use for the evaluation.
            Dataset names are unique for each environment.
            If 'dataset_name' is provided, then 'dataset_id' should not be provided.
            If 'dataset_name' is provided along with 'inputs', then it will be used to
            generate save a `Dataset` constructed from the list of features computed
            from the inputs.
        dataset_id
            The UUID of the `Dataset` to use for the evaluation.
            Dataset ids are unique for each environment.
            If 'dataset_id' is provided, then 'dataset_name' and 'revision_id' should not be provided.
        revision_id
            The unique id of the `DatasetRevision` to use for the evaluation.
            If a previously-created dataset did not have a name, you can look it
            up using its unique job id instead.
            If 'revision_id' is provided, then 'dataset_name' and 'dataset_id' should not be provided.
        reference_output
            The name of the feature to use as the reference output for the evaluation.
        evaluators
            The list of evaluation functions to use for the evaluation.
            See https://docs.chalk.ai/docs/prompts#prompt-evaluation for more information.
        meta
            Arbitrary `key:value` pairs to associate with a query.
        input
            The features for which there are known values.
            It can be a mapping of features to a list of values for each
            feature, or an existing `DataFrame`.
            Each element in the `DataFrame` or list of values represents
            an observation in line with the timestamp in `input_times`.
        spine_sql_query
            A SQL query that will query your offline store and use the result as input.
            See https://docs.chalk.ai/docs/query-offline#input for more information.
        input_times
            The time at which the given inputs should be observed for point-in-time correctness. If given a list of
            times, the list must match the length of the `input` lists. Each element of input_time corresponds with the
            feature values at the same index of the `input` lists.
            See https://docs.chalk.ai/docs/temporal-consistency for more information.
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row) in
            the resulting `DataFrame`, its value will be `None`.
        recompute_features
            Used to control whether resolvers are allowed to run in order to compute feature values.

            If `True`, all output features will be recomputed by resolvers.
            If `False`, all output features will be sampled from the offline store.
            If a list, all output features in recompute_features will be recomputed,
            and all other output features will be sampled from the offline store.
        sample_features
            A list of features that will always be sampled, and thus always excluded from recompute.
            Should not overlap with any features used in `recompute_features` argument.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        max_samples
            The maximum number of samples to include in the `DataFrame`.
            If not specified, all samples will be returned.
        branch
            If specified, Chalk will route your request to the relevant branch.
            If `None`, Chalk will route your request to a non-branch deployment.
            If not specified, Chalk will use the current client's branch info.
        correlation_id
            You can specify a correlation ID to be used in logs and web interfaces.
            This should be globally unique, i.e. a `uuid` or similar. Logs generated
            during the execution of your query will be tagged with this correlation id.
        query_context
            An immutable context that can be accessed from Python resolvers.
            This context wraps a JSON-compatible dictionary or JSON string with type restrictions.
            See https://docs.chalk.ai/api-docs#ChalkContext for more information.
        wait
            Whether to wait for job completion.
        show_progress
            If `True`, progress bars will be shown while the query is running.
            Primarily intended for use in a Jupyter-like notebook environment.
            This flag will also be propagated to the methods of the resulting
            `Dataset`.
        timeout:
            How long to wait, in seconds, for job completion before raising a `TimeoutError`.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        lower_bound
            If specified, the query will only be run on data observed after this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        upper_bound
            If specified, the query will only be run on data observed before this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        feature_for_lower_upper_bound
            Override the feature whose values are filtered against `lower_bound` and `upper_bound`.
            By default, the bounds filter against the `FeatureTime` feature of each output's namespace.
            Must reference a scalar or `FeatureTime` feature.
        store_plan_stages
            If `True`, the output of each of the query plan stages will be stored
            in S3/GCS. This will dramatically impact the performance of the query,
            so it should only be used for debugging.
            These files will be visible in the web dashboard's query detail view, and
            can be downloaded in full by clicking on a plan node in the query plan visualizer.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        required_resolver_tags
            If specified, *all* `required_resolver_tags` must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        resources
            Override resource requests for processes with isolated resources, e.g., offline queries and cron jobs.
            See `ResourceRequests` for more information.
        run_asynchronously
            Boots a Kubernetes job to run the queries in their own pods, separate from the engine and branch servers.
            This is useful for large datasets and jobs that require a long time to run.
        store_online
            If `True`, the output of the query will be stored in the online store.
        store_offline
            If `True`, the output of the query will be stored in the offline store.
        num_shards
            If specified, the query will be run asynchronously, splitting the input across `num_shards` shards.
        num_workers
            If specified, the query will be run asynchronously across a maximum `num_workers` pod workers at any time.
            This parameter is useful if you have a large number of shards and would like to limit the number of pods running at once.
        completion_deadline
            If specified as a timedelta, applies a completion deadline to each shard; each shard of the query will fail (allowing retries) if not completed within the duration.
            If specified as an OfflineQueryDeadlineOptions, allows more fine-grained control of shard- or query-level deadlines, with options to retry on shard failure or not.
        max_retries
            Number of times failed offline query shards can be retried. The maximum number of attempts is 1 higher than this number and each shard has an independent retry budget.
            Errors that appear to be deterministic will not provoke retries.
            By default, this is set to 2, which is at most 3 attempts.

        Other Parameters
        ----------------
        required_output
            The features that you'd like to sample and must exist
            in each resulting row. Rows where a `required_output`
            was never stored in the offline store will be skipped.
            This differs from specifying the feature in `output`,
            where instead the row would be included, but the feature
            value would be `None`.

        Returns
        -------
        Dataset
            A Chalk `Dataset`.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> from chalk.prompts import Prompt, Message
        >>> dataset = ChalkClient().prompt_evaluation(
        ...     dataset_name='my_dataset',
        ...     reference_output='reference_output_column',
        ...     evaluators=['exact_match'],
        ...     prompts=[
        ...         Prompt(model='my_model', messages=[
        ...             Message(role='user', content='what is my name?'),
        ...         ]),
        ...     ]
        ... )
        >>> df = dataset.get_data_as_pandas()
        """
        ...

    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        environment: EnvironmentId | None = None,
        preview_deployment_id: str | None = None,
        branch: BranchId | None = ...,
        upper_bound: datetime | str | None = None,
        lower_bound: datetime | str | None = None,
        store_online: bool = True,
        store_offline: bool = True,
        timestamping_mode: Literal["feature_time", "online_store_write_time"] = "feature_time",
        idempotency_key: Optional[str] = None,
    ) -> ResolverRunResponse:
        """Triggers a resolver to run.
        See https://docs.chalk.ai/docs/runs for more information.

        Parameters
        ----------
        resolver_fqn
            The fully qualified name of the resolver to trigger.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        preview_deployment_id
            If specified, Chalk will route your request to the
            relevant preview deployment.
        upper_bound
            If specified, the resolver will only ingest data observed before this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        lower_bound
            If specified, the resolver will only ingest data observed after this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        store_online
            If `True`, the resolver run output will be stored in the online store.
        store_offline
            If `True`, the resolver run output will be stored in the offline store.
        idempotency_key
            If specified, the resolver run will be idempotent with respect to the key.
        branch

        Returns
        -------
        ResolverRunResponse
            Status of the resolver run and the run ID.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().trigger_resolver_run(
        ...     resolver_fqn="mymodule.fn"
        ... )
        """
        ...

    def get_run_status(
        self,
        run_id: str,
        environment: EnvironmentId | None = None,
        preview_deployment_id: str | None = None,
        branch: BranchId | None = ...,
    ) -> ResolverRunResponse:
        """Retrieves the status of a resolver run.
        See https://docs.chalk.ai/docs/runs for more information.

        Parameters
        ----------
        run_id
            ID of the resolver run to check.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        preview_deployment_id
            If specified, Chalk will route your request to the
            relevant preview deployment.
        branch

        Returns
        -------
        ResolverRunResponse
            Status of the resolver run and the run ID.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_run_status(
        ...     run_id="3",
        ... )
        ResolverRunResponse(
            id="3",
            status=ResolverRunStatus.SUCCEEDED
        )
        """
        ...

    def whoami(self) -> WhoAmIResponse:
        """Checks the identity of your client.

        Useful as a sanity test of your configuration.

        Returns
        -------
        WhoAmIResponse
            The identity of your client.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().whoami()
        WhoAmIResponse(user="...", environment_id='...', team_id='...')
        """
        ...

    def delete_features(
        self,
        namespace: str,
        features: list[str] | None,
        tags: list[str] | None,
        primary_keys: list[str],
        environment: Optional[EnvironmentId] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        retain_offline: bool = False,
        retain_online: bool = False,
    ) -> FeatureObservationDeletionResponse:
        """Targets feature observation values for deletion and performs deletion online and offline.

        Parameters
        ----------
        namespace
            The namespace in which the target features reside.
        features
            An optional list of the feature names of the features that should be deleted
            for the targeted primary keys. Not specifying this and not specifying the "tags" field
            will result in all features being targeted for deletion for the specified primary keys.
            Note that this parameter and the "tags" parameter are mutually exclusive.
        tags
            An optional list of tags that specify features that should be targeted for deletion.
            If a feature has a tag in this list, its observations for the primary keys you listed
            will be targeted for deletion. Not specifying this and not specifying the "features"
            field will result in all features being targeted for deletion for the specified primary
            keys. Note that this parameter and the "features" parameter are mutually exclusive.
        primary_keys
            The primary keys of the observations that should be targeted for deletion.
        retain_offline
            If `True`, the given observations will not be dropped from the offline store
        retain_online
            If `True`, the given observations will not be dropped from the online store

        Returns
        -------
        FeatureObservationDeletionResponse
            Holds any errors (if any) that occurred during the drop request.
            Deletion of a feature may partially-succeed.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().delete_features(
        ...     namespace="user",
        ...     features=["name", "email", "age"],
        ...     primary_keys=[1, 2, 3]
        ... )
        """
        ...

    def drop_features(
        self,
        namespace: str,
        features: list[str],
        environment: Optional[EnvironmentId] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        retain_offline: bool = False,
        retain_online: bool = False,
    ) -> FeatureDropResponse:
        """
        Performs a drop on features, which involves a deletes all their data
        (both online and offline). Once the feature is reset in this manner,
        its type can be changed.

        Parameters
        ----------
        namespace
            The namespace in which the target features reside.
        features
            A list of the feature names of the features that should be dropped.
        retain_offline
            If `True`, features will not be dropped from the offline store
        retain_online
            If `True`, features will not be dropped from the online store


        Returns
        -------
        FeatureDropResponse
            Holds any errors (if any) that occurred during the drop request.
            Dropping a feature may partially-succeed.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().drop_features(
        ...     namespace="user",
        ...     features=["name", "email", "age"],
        ... )
        """
        ...

    def upload_features(
        self,
        input: Mapping[FeatureReference, Any],
        branch: BranchId | None = ...,
        environment: EnvironmentId | None = None,
        preview_deployment_id: str | None = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        meta: Mapping[str, str] | None = None,
    ) -> list[ChalkError] | None:
        """Upload data to Chalk for use in offline resolvers or to prime a cache.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        preview_deployment_id
            If specified, Chalk will route your request to the relevant preview deployment
        query_name
            Optionally associate this upload with a query name. See `.query` for more information.

        Other Parameters
        ----------------
        correlation_id
            A globally unique ID for this operation, used alongside logs and
            available in web interfaces.
        meta
            Arbitrary `key:value` pairs to associate with a query.
        branch
            If specified, Chalk will route your request to the relevant branch.

        Returns
        -------
        list[ChalkError] | None
            The errors encountered from uploading features.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().upload_features(
        ...     input={
        ...         User.id: 1,
        ...         User.name: "Katherine Johnson"
        ...     }
        ... )
        """
        ...

    def multi_upload_features(
        self,
        input: Union[
            list[Mapping[str | Feature | Any, Any]],
            Mapping[str | Feature | Any, list[Any]],
            pd.DataFrame,
            pl.DataFrame,
            DataFrame,
        ],
        branch: BranchId | None = ...,
        environment: EnvironmentId | None = None,
        preview_deployment_id: str | None = None,
        correlation_id: str | None = None,
        meta: Mapping[str, str] | None = None,
    ) -> list[ChalkError] | None:
        """Upload data to Chalk for use in offline resolvers or to prime a cache.

        Parameters
        ----------
        input
            One of three types:
                - A list of mappings, each of which includes the features for which there are known values mapped to
                  those values. Each mapping can have different keys, but each mapping must have the same root features
                  class.
                - A mapping where each feature key is mapped to a list of the values for that feature.
                  You can consider this a mapping that describes columns (keys, i.e. features) and rows
                  (the list of values in the map for each feature). Each list must be the same length.
                - A `pandas`, `polars`, or `chalk.DataFrame`.
        branch
        environment
            The environment under which to run the upload.
            API tokens can be scoped to an environment.
            If no environment is specified in the upload,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        preview_deployment_id
            If specified, Chalk will route your request to the relevant preview deployment

        Other Parameters
        ----------------
        correlation_id
            A globally unique ID for this operation, used alongside logs and
            available in web interfaces. If `None`, a correlation ID will be
            generated for you and returned on the response.
        meta
            Arbitrary `key:value` pairs to associate with an upload.

        Returns
        -------
        list[ChalkError] | None
            The errors encountered from uploading features.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().multi_upload_features(
        ...     input=[
        ...         {
        ...             User.id: 1,
        ...             User.name: "Katherine Johnson"
        ...         },
        ...         {
        ...             User.id: 2,
        ...             User.name: "Eleanor Roosevelt"
        ...         }
        ...     ]
        ... )
        """
        ...

    def load_features(self, branch: BranchIdParam = ...):
        """Load Chalk features into notebook context. By default, uses the client's
        current branch (if that isn't specified then the main deployment is used).

        Parameters
        ----------
        branch
            If specified, Chalk will route your request to the relevant branch.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient(branch='fraud-model')
        ... client.load_features()
        """
        ...

    def sample(
        self,
        output: Sequence[FeatureReference] = (),
        required_output: Sequence[FeatureReference] = (),
        output_id: bool = False,
        output_ts: Union[bool, str] = False,
        max_samples: int | None = None,
        dataset: str | None = None,
        branch: BranchId | None = None,
        environment: EnvironmentId | None = None,
        tags: list[str] | None = None,
    ) -> pd.DataFrame:
        """Get the most recent feature values from the offline store.

        See https://docs.chalk.ai/docs/query-offline for more information.

        Parameters
        ----------
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row)
            in the resulting `DataFrame`, its value will be `None`.
        max_samples
            The maximum number of rows to return.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        dataset
            The `Dataset` name under which to save the output.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.

        Other Parameters
        ----------------
        required_output
            The features that you'd like to sample and must exist
            in each resulting row. Rows where a `required_output`
            was never stored in the offline store will be skipped.
            This differs from specifying the feature in `output`,
            where instead the row would be included, but the feature
            value would be `None`.
        output_ts
            Whether to return the input-time feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `DataFrame`.
            If set to a non-empty `str`, used as the input-time column name.
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.
        branch

        Returns
        -------
        pd.DataFrame
            A `pandas.DataFrame` with columns equal to the names of the features in output,
            and values representing the value of the most recent observation.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> sample_df = ChalkClient().sample(
        ...     output=[
        ...         Account.id,
        ...         Account.title,
        ...         Account.user.full_name
        ...     ],
        ...     max_samples=10
        ... )
        """
        ...

    def create_branch(
        self,
        branch_name: str,
        create_only: bool = False,
        switch: bool = True,
        source_deployment_id: str | None = None,
        environment: EnvironmentId | None = None,
    ) -> BranchDeployResponse:
        """
        Create a new branch based off of a deployment from the server.
        By default, uses the latest live deployment.

        Parameters
        ----------
        branch_name
            The name of the new branch to create.
        create_only
            If `True`, will raise an error if a branch with the given
            name already exists. If `False` and the branch exists, then
            that branch will be deployed to.
        switch
            If `True`, will switch the client to the newly created branch.
            Defaults to `True`.
        source_deployment_id
            The specific deployment ID to use for the branch.
            If not specified, the latest live deployment on the
            server will be used. You can see which deployments
            are available by clicking on the 'Deployments' tab on
            the project page in the Chalk dashboard.
        environment
            The environment under which to create the branch. API
            tokens can be scoped to an environment. If no environment
            is specified in the query, the environment will be taken
            from the client's cached token.

        Returns
        -------
        BranchDeployResponse
            A response object containing metadata about the branch.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.create_branch("my-new-branch")
        """
        ...

    def redeploy(
        self,
        deployment_id: Optional[str] = None,
        build_profile: Optional[Literal["o3_no_profiling", "o3_profiling", "o2_no_profiling", "o2_profiling"]] = None,
        deployment_tags: Optional[List[str]] = None,
        base_image_override: Optional[str] = None,
        force_rebuild_dockerfile: bool = False,
        display_description: Optional[str] = None,
    ) -> RedeployResponse:
        """
        Full rebuild and deploy using this deployment's source.

        Parameters
        ----------
        deployment_id
            The ID of the existing deployment to rebuild and deploy.
            If omitted, the environment's active deployment is used.
        build_profile
            Build optimization level. One of ``'o3_no_profiling'``, ``'o3_profiling'``,
            ``'o2_no_profiling'``, ``'o2_profiling'``.
        deployment_tags
            Blue-green routing tags to assign to the new deployment.
        base_image_override
            Override the base Docker image used for the build.
        force_rebuild_dockerfile
            Force a Dockerfile rebuild even if it has not changed.
        display_description
            Human-readable description for the new deployment.

        Returns
        -------
        RedeployResponse
            ``deployment_id`` is populated with the new deployment's ID.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.redeploy("dep_abc123")
        """
        ...

    def rollback_deployment(self, deployment_id: str) -> RedeployResponse:
        """
        Instantly redeploy using this deployment's pre-built image.

        Parameters
        ----------
        deployment_id
            The ID of the existing deployment whose image will be activated.

        Returns
        -------
        RedeployResponse

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().rollback_deployment("dep_abc123")
        """
        ...

    def suspend_environment(self, environment_id: EnvironmentId) -> None:
        """
        Suspend an environment, spinning down its cloud resources.

        Query servers, jobs, and in-cluster databases are spun down until the
        environment is resumed.

        .. warning::
            This tears down the environment's cloud resources. Double-check that
            ``environment_id`` is the one you intend to suspend before calling.

        Parameters
        ----------
        environment_id
            The id of the environment to suspend. Required, and intentionally not
            defaulted to the client's environment: naming the target explicitly
            avoids suspending the wrong environment by accident.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().suspend_environment(environment_id="my-staging-env")
        """
        ...

    def resume_environment(self, environment_id: EnvironmentId) -> None:
        """
        Resume a suspended environment, spinning its cloud resources back up.

        .. warning::
            This spins the environment's cloud resources back up. Double-check that
            ``environment_id`` is the one you intend to resume before calling.

        Parameters
        ----------
        environment_id
            The id of the environment to resume. Required, and intentionally not
            defaulted to the client's environment: naming the target explicitly
            avoids resuming the wrong environment by accident.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().resume_environment(environment_id="my-staging-env")
        """
        ...

    def rebuild_deployment(
        self,
        deployment_id: str,
        new_image_tag: str,
        build_profile: Optional[Literal["o3_no_profiling", "o3_profiling", "o2_no_profiling", "o2_profiling"]] = None,
        base_image_override: Optional[str] = None,
        force_rebuild_dockerfile: bool = False,
    ) -> RedeployResponse:
        """
        Build a new image from this deployment's source without deploying.

        Parameters
        ----------
        deployment_id
            The ID of the existing deployment to use as the build source.
        new_image_tag
            The image tag to apply to the rebuilt image.
        build_profile
            Build optimization level. One of ``'o3_no_profiling'``, ``'o3_profiling'``,
            ``'o2_no_profiling'``, ``'o2_profiling'``.
        base_image_override
            Override the base Docker image used for the build.
        force_rebuild_dockerfile
            Force a Dockerfile rebuild even if it has not changed.

        Returns
        -------
        RedeployResponse
            ``build_id`` is populated with the resulting build/job ID.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().rebuild_deployment("dep_abc123", new_image_tag="v1.2.3")
        """
        ...

    def patch_deployment(self, deployment_id: Optional[str] = None) -> RedeployResponse:
        """
        Patch deployment config and restart pods without a new build.

        Parameters
        ----------
        deployment_id
            The ID of the existing deployment to patch.
            If omitted, the environment's active deployment is used.

        Returns
        -------
        RedeployResponse
            ``nonfatal_errors`` is populated with any non-fatal errors encountered.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().patch_deployment("dep_abc123")
        """
        ...

    def get_or_create_branch(
        self,
        branch_name: str,
        source_branch_name: Optional[str] = None,
        source_deployment_id: Optional[str] = None,
    ):
        """
        Create a new branch named `branch_name` based off of an existing branch or deployment id.
        By default, the latest mainline deployment is used as the branch source.

        If the provided branch name already exists, the client will be updated to point
        to the latest deployment for the already existsing branch (no new deployment
        will be created).

        Parameters
        ----------
        branch_name
            The name to give the newly created branch.
        source_branch_name
            The branch to source the new branch from.
        source_deployment_id
            The specific deployment ID to source the new branch from.
        """

    def get_branches(self) -> list[str]:
        """Lists the current branches for this environment.

        Returns
        -------
        list[str]
            A list of the names of branches available on this environment.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_branches()
        ["testing", "feat/new-feature"]
        """
        ...

    def get_branch(self) -> str | None:
        """Displays the current branch this client is pointed at.

        If the current environment does not support branch deployments
        or no branch is set, this method returns `None`.

        Returns
        -------
        str | None
            The name of the current branch or `None`.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient(branch="my-branch")
        >>> assert client.get_branch() == "my-branch"
        """
        ...

    def set_branch(self, branch_name: Optional[str]):
        """Point the `ChalkClient` at the given branch.
        If `branch_name` is None, this points the client at the
        active non-branch deployment.

        If the branch does not exist or if branch deployments
        are not enabled for the current environment, this
        method raises an error.

        Parameters
        ----------
        branch_name
            The name of the branch to use, or None

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.create_branch("my-new-branch")
        >>> client.set_branch("my-new-branch")
        >>> client.set_branch(None)
        """
        ...

    def reset_branch(self, branch: BranchIdParam = ..., environment: EnvironmentId | None = None): ...

    def branch_state(
        self,
        branch: BranchId | ellipsis = ...,
        environment: EnvironmentId | None = None,
    ) -> BranchGraphSummary:
        """
        Returns a `BranchGraphSummary` object that contains the
        state of the branch server: Which resolver/features are
        defined, and the history of live notebook updates on the
        server.

        Parameters
        ----------
        branch
            The branch to query. If not specified, the branch is
            expected to be included in the constructor for `ChalkClient`.
        environment
            Optionally override the environment under which to query the branch state.
        """
        ...

    def set_incremental_cursor(
        self,
        *,
        resolver: str | Resolver | None = None,
        scheduled_query: str | None = None,
        max_ingested_timestamp: datetime | None = None,
        last_execution_timestamp: datetime | None = None,
    ) -> None:
        """
        Sets the incremental cursor for a resolver or scheduled query.

        Parameters
        ---------
        resolver
            The resolver. Can be a function or the string name of a function.
            Exactly one of `resolver` and `scheduled_query` is required.
        scheduled_query
            The name of the scheduled query. Exactly one of `resolver` and `scheduled_query`
            is required.
        max_ingested_timestamp
            Set the maximum timestamp of the data ingested by the resolver.
        last_execution_timestamp
            Override the last execution timestamp of the resolver.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.set_incremental_cursor(
        ...     resolver="my_resolver",
        ...     max_ingested_timestamp=datetime.now(),
        ... )
        """
        ...

    def get_incremental_cursor(
        self,
        *,
        resolver: str | Resolver | None = None,
        scheduled_query: str | None = None,
    ) -> GetIncrementalProgressResponse:
        """
        Gets the incremental cursor for a resolver or scheduled query.

        Parameters
        ---------
        resolver
            The resolver. Can be a function or the string name of a function.
            Exactly one of `resolver` and `scheduled_query` is required.
        scheduled_query
            If updating incremental status of a resolver in the context of a
            scheduled query, the name of the scheduled query.
            Exactly one of `resolver` and `scheduled_query` is required.

        Returns
        ------
        IncrementalStatus
            An object containing the `max_ingested_timestamp` and `incremental_timestamp`.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.get_incremental_cursor(resolver="my_resolver")
        """
        ...

    def test_streaming_resolver(
        self,
        resolver: str | Resolver,
        num_messages: int | None = None,
        message_filepath: str | None = None,
        message_keys: list[str | None] | None = None,
        message_bodies: "list[str | bytes | BaseModel] | None" = None,
        message_headers: list[list[tuple[str, bytes]]] | None = None,
        message_timestamps: list[str | datetime] | None = None,
        branch: BranchId | ellipsis = ...,
        environment: EnvironmentId | None = None,
        kafka_auto_offset_reset: Optional[Literal["earliest", "latest"]] = "earliest",
    ) -> StreamResolverTestResponse:
        """
        Tests a streaming resolver and its ability to parse and resolve messages.
        See https://docs.chalk.ai/docs/streams for more information.

        Parameters
        ----------
        resolver
            The streaming resolver or its string name.
        num_messages
            The number of messages to digest from the stream source.
            As messages may not be incoming into the stream, this action may time out.
        message_filepath
            A filepath from which test messages will be ingested.
            This file should be newline delimited json as follows:

            >>> {"message_key": "my-key", "message_body": {"field1": "value1", "field2": "value2"}}
            >>> {"message_key": "my-key", "message_body": {"field1": "value1", "field2": "value2"}}

            Each line may optionally contain a timezone string as a value to the key "message_timestamp".
        message_keys
            Alternatively, keys can be supplied in code along with the "test_message_bodies" argument.
            Both arguments must be the same length.
        message_bodies
            Message bodies can be supplied in code as strings, bytes, or Pydantic models along with the "test_message_keys" argument.
            Both arguments must be the same length.
        message_timestamps
            Optionally, timestamps can be provided for each message,

        Other Parameters
        ----------
        branch
            If specified, Chalk will route your request to the relevant branch.
        environment
            The environment under which to create the branch. API
            tokens can be scoped to an environment. If no environment
            is specified in the query, the environment will be taken
            from the client's cached token.
        kafka_auto_offset_reset
            The offset to start reading from when consuming messages from a Kafka source for testing.
            If not specified, the default is "earliest".

        Returns
        -------
        StreamResolverTestResponse
            A simple wrapper around a status and optional error message.
            Inspecting `StreamResolverTestResponse.features` will return the test results, if they exist.
            Otherwise, check `StreamResolverTestResponse.errors` and `StreamResolverTestResponse.message` for errors.

        Examples
        --------
        >>> from chalk.streams import stream, KafkaSource
        >>> from chalk.client import ChalkClient
        >>> from chalk.features import Features, features
        >>> from pydantic import BaseModel
        >>> # This code is an example of a simple streaming feature setup. Define the source
        >>> stream_source=KafkaSource(...)
        >>> # Define the features
        >>> @features(etl_offline_to_online=True, max_staleness="7d")
        >>> class StreamingFeature:
        >>>     id: str
        >>>     user_id: str
        >>>     card_id: str
        >>> # Define the streaming message model
        >>> class StreamingMessage(BaseModel):
        >>>     card_id: str
        >>>     user_id: str
        >>> # Define the mapping resolver
        >>> @stream(source=stream_source)
        >>> def our_stream_resolver(
        >>>     m: StreamingMessage,
        >>> ) -> Features[StreamingFeature.id, StreamingFeature.card_id, StreamingFeature.user_id]:
        >>>    return StreamingFeature(
        >>>        id=f"{m.card_id}-{m.user_id}",
        >>>        card_id=m.card_id,
        >>>        user_id=m.user_id,
        >>>    )
        >>> # Once you have done a `chalk apply`, you can test the streaming resolver with custom messages as follows
        >>> client = ChalkClient()
        >>> keys = ["my_key"] * 10
        >>> messages = [StreamingMessage(card_id="1", user_id=str(i)).json() for i in range(10)]
        >>> resp = client.test_streaming_resolver(
        >>>     resolver="our_stream_resolver",
        >>>     message_keys=keys,
        >>>     message_bodies=messages,
        >>> )
        >>> print(resp.features)
        """
        ...

    def ping_engine(self, num: Optional[int] = None) -> int:
        """
        Ping the engine to check if it is alive.

        Parameters
        ----------
        num
            A random number to send to the engine. If not provided, a random number is generated.
            This number will be returned as the response.

        Returns
        -------
        int
            The number sent to the engine.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.ping_engine(3)
        3
        """
        ...

    def get_operation_feature_statistics(self, operation_id: uuid.UUID) -> FeatureStatisticsResponse: ...

    def get_model(
        self,
        name: str,
        version: Optional[int] = None,
    ) -> Union[ModelNamespaceResponse, ModelVersionResponse]:
        """Retrieve a model from the Chalk model registry.

        .. deprecated::
            Use `get_model_namespace` for namespace-level info, or `get_model_version`
            to retrieve a version (only a version exposes ``.remote()``).

        Parameters
        ----------
        name
            Name of the model to retrieve.
        version
            Specific version to retrieve. If omitted, returns namespace-level info.

        Returns
        -------
        Union[ModelNamespaceResponse, ModelVersionResponse]
            Without a version, a `ModelNamespaceResponse` (info only). With a version, a
            `ModelVersionResponse` — see `get_model_version`.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> risk_model_namespace = client.get_model(name="RiskScoreModel")   # info
        >>> risk_model_v1 = client.get_model(name="RiskScoreModel", version=1)
        """
        ...

    def get_model_namespace(
        self,
        name: str,
    ) -> ModelNamespaceResponse:
        """Retrieve namespace-level info for a model.

        Parameters
        ----------
        name
            Name of the model to retrieve.

        Returns
        -------
        ModelNamespaceResponse
            Namespace-level info. This does not expose ``.remote()`` — use
            `get_model_version` to invoke a deployed model.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> risk_model = client.get_model_namespace(name="RiskScoreModel")
        """
        ...

    def get_model_version(
        self,
        name: str,
        version: Optional[int] = None,
    ) -> ModelVersionResponse:
        """Retrieve a single model version (latest when ``version`` is omitted).

        Returns a `DeployedModelVersion` when the version is deployed to a scaling group —
        its ``.remote(*args, **kwargs)`` invokes the model directly — otherwise a
        `RegisteredModelVersion`, whose ``.remote()`` raises until it is deployed.

        >>> from chalk.client import ChalkClient
        >>> latest_risk_model = ChalkClient().get_model_version("RiskScoreModel")
        >>> latest_risk_model.remote(txn_amount=42.0, account_age_days=365)
        """
        ...

    def register_model_namespace(
        self,
        name: str,
        description: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> RegisterModelResponse:
        """
        Register a model in the Chalk model registry.

        Parameters
        ----------
        name : str
            Unique name for the model
        description : str
            Description of the model's purpose and functionality
        metadata : Mapping[str, Any], optional
            Additional metadata dictionary containing framework info,
            training details, performance metrics, etc.

        Returns
        -------
        RegisterModelResponse
            The response object from the model registration

        Examples
        --------
        Register a new model:

        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.register_model_namespace(
        ...     name="RiskModel",
        ...     description="Credit risk assessment model using transaction history",
        ...     metadata={
        ...         "accuracy": 0.94,
        ...         "training_date": "2024-01-15"
        ...     }
        ... )
        """
        ...

    def register_model_version(
        self,
        name: str,
        model_type: Optional[ModelType] = None,
        model_class: Optional[ModelClass] = None,
        model_encoding: Optional[ModelEncoding] = None,
        aliases: Optional[List[str]] = None,
        model: Optional[Any] = None,
        additional_files: Optional[List[str]] = None,
        model_paths: Optional[List[str]] = None,
        input_schema: Optional[Any] = None,
        output_schema: Optional[Any] = None,
        metadata: Optional[Mapping[str, Any]] = None,
        input_features: Optional[list[str]] = None,
        output_features: Optional[list[str]] = None,
        source_config: Optional[SourceConfig] = None,
        dependencies: Optional[List[str]] = None,
        model_image: Optional[str] = None,
        skip_volume_upload: bool = False,
    ) -> RegisterModelVersionResponse:
        """Register a model in the Chalk model registry.

        Parameters
        ----------
        name
            Unique name for the model.
        model_image
            Docker image for model serving (must have chalk-remote-call-python installed).
            If provided, the model can be deployed to a scaling group via deploy_scaling_group().
        aliases
            List of version aliases (e.g., `["v1.0", "latest"]`).
        model
            Python model object (for object-based registration).
        model_paths
            Paths to model files (for file-based registration).
        additional_files
            Additional files needed for inference (tokenizers, configs, etc.)
        model_type
            Type of model framework.
        model_class
            Task the model solves.
        model_encoding
            Serialization format.
        input_schema
            Definition of the input schema. Can be:
            - `dict`: Dictionary mapping column names to dtypes for tabular data
            - `list`: List of `(shape, dtype)` tuples for tensor data
        output_schema
            Definition of the output schema. Can be:
            - `dict`: Dictionary mapping column names to dtypes for tabular data
            - `list`: List of `(shape, dtype)` tuples for tensor data
        metadata
            Additional metadata dictionary containing framework info,
            training details, performance metrics, etc.
        input_features
            The features to be used as inputs to the model.
            For example, `[User.message]`. Features can also be expressed as snakecased strings,
            e.g. `["user.message"]`.
        output_features
            The features to be used as outputs to the model.
            For example, `[User.is_spam]`. Features can also be expressed as snakecased strings,
            e.g. `["user.is_spam"]`.
        source_config
            Config to pass credentials to access files from a remote source.
        dependencies
            List of package dependencies needed to run this model.
            e.g. `["torch==2.7.1", "numpy==1.26.4"]`.
        skip_volume_upload
            If ``True``, skip uploading model artifacts to a volume during
            registration. Defaults to ``False``.

        Returns
        -------
        ModelVersion
           The registered model version object

        Examples
        --------

        Register from Python object (for engine deployment):

        >>> from chalk.client import ChalkClient
        >>> import pyarrow as pa
        >>> client = ChalkClient()
        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model=trained_pytorch_model,
        ...     model_type=ModelType.PYTORCH,
        ... )

        Register from local files (for engine deployment):

        >>> from chalk.client import ChalkClient
        >>> import pyarrow as pa
        >>> client = ChalkClient()
        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model_paths=["./model.pth"],
        ...     model_type=ModelType.PYTORCH,
        ...     input_schema={"content": pa.large_string()},
        ...     output_schema={"prob": pa.float64()},
        ... )

        Register with a Docker image (for scaling group deployment):

        >>> from chalk.client import ChalkClient
        >>> import pyarrow as pa
        >>> client = ChalkClient()
        >>> client.register_model_version(
        ...     name="ner-model",
        ...     input_schema={"text": pa.large_string()},
        ...     output_schema={"entities": pa.large_string()},
        ...     model_image="ghcr.io/my-org/ner-model:latest",
        ... )

        """
        ...

    def delete_model_namespace(
        self,
        name: str,
    ) -> ModelNamespaceResponse:
        """Delete a model namespace from the Chalk model registry.

        This archives the model and all of its versions. **The underlying model
        artifact data for those versions is permanently deleted from storage**
        (any artifact not still referenced by another version). A model cannot
        be deleted while it is referenced by the active deployment or a scaling
        group.

        Parameters
        ----------
        name
            Name of the model namespace to delete.

        Returns
        -------
        ModelNamespaceResponse
            The archived model.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.delete_model_namespace(name="RiskModel")
        """
        ...

    def delete_model_version(
        self,
        name: str,
        version: int,
    ) -> RegisteredModelVersion:
        """Delete a single model version from the Chalk model registry.

        This archives the given version. **The underlying model artifact data is
        permanently deleted from storage** (unless the artifact is still
        referenced by another version). A version cannot be deleted while it is
        referenced by the active deployment or a scaling group.

        Parameters
        ----------
        name
            Name of the model the version belongs to.
        version
            Version number to delete.

        Returns
        -------
        RegisteredModelVersion
            The archived model version.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.delete_model_version(name="RiskModel", version=1)
        """
        ...

    def deploy_model_version_to_scaling_group(
        self,
        name: str,
        model_name: str,
        model_version: int,
        scaling: Optional["AutoScalingSpec"] = None,
        resources: Optional["ScalingGroupResourceRequest"] = None,
        handler: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        secrets: Optional[List[Any]] = None,
        readiness_probe: Optional["GrpcReadinessProbe"] = None,
        startup_probe: Optional["GrpcStartupProbe"] = None,
    ) -> dict[str, Any]:
        """Deploy a registered model version as a scaling group.

        Parameters
        ----------
        name
            Name for the scaling group.
        model_name
            Name of the registered model.
        model_version
            Version number of the model to deploy.
        scaling
            Autoscaling configuration (min/max replicas, CPU target).
        resources
            Resource requests (CPU, memory, GPU).
        handler
            Dotted path to handler function (default: "model.handler").
        env_vars
            Extra environment variables to inject into the container.
        secrets
            List of Secret Registry secrets to be injected into the Scaling Group
        readiness_probe
            Optional gRPC readiness probe configuration. Model deployments only
            support gRPC readiness checks.
        startup_probe
            Optional gRPC startup probe configuration. Model deployments only
            support gRPC startup checks; if omitted, defaults to the standard
            gRPC health check method.

        Examples
        --------
        >>> from chalk.scalinggroup import AutoScalingSpec, ScalingGroupResourceRequest
        >>> model_version = client.register_model_version(
        ...     name="ner-model",
        ...     input_schema={"text": pa.large_string()},
        ...     output_schema={"entities": pa.large_string()},
        ...     model_image="ghcr.io/my-org/ner-model:latest",
        ... )
        >>> client.deploy_model_version_to_scaling_group(
        ...     name="my-ner-sg",
        ...     model_name="ner-model",
        ...     model_version=model_version.model_version,
        ...     scaling=AutoScalingSpec(min_replicas=1, max_replicas=2),
        ...     resources=ScalingGroupResourceRequest(cpu="2", memory="4Gi"),
        ... )
        """
        ...

    def list_scaling_groups(self) -> "ListScalingGroupsResponse":
        """List all scaling groups in the current environment.

        Returns
        -------
        ListScalingGroupsResponse
            Response containing a list of scaling groups.
        """
        ...

    def get_scaling_group(self, name: Optional[str] = None, id: Optional[str] = None) -> "ScalingGroup":
        """Get a scaling group by name or id.

        Parameters
        ----------
        name
            Name of the scaling group.
        id
            ID of the scaling group.

        Returns
        -------
        ScalingGroup
            The scaling group details.
        """
        ...

    def delete_scaling_group(
        self, name: Optional[str] = None, id: Optional[str] = None
    ) -> "DeleteScalingGroupResponse":
        """Delete a scaling group by name or id.

        Parameters
        ----------
        name
            Name of the scaling group to delete.
        id
            ID of the scaling group to delete.

        Returns
        -------
        DeleteScalingGroupResponse
            Response containing the deleted scaling group details.
        """
        ...

    def promote_model_artifact(
        self,
        name: str,
        model_artifact_id: Optional[str] = None,
        run_id: Optional[str] = None,
        run_name: Optional[str] = None,
        criterion: Optional[ModelRunCriterion] = None,
        aliases: Optional[List[str]] = None,
    ) -> RegisterModelVersionResponse:
        """
        Register a model in the Chalk model registry.

        Parameters
        ----------
        name : str
            Name of the model namespace to promote into.
        model_artifact_id: str, optional
            Artifact UUID to promote to a model version.
        run_id: str, optional
            run id that produce the artifact to promote.
        run_name: str, optional
            run name used in the checkpointer for artifact to promote.
        criterion: ModelRunCriterion, optional
            criterion on which to select the artifact from the training run.
            If none provided, the latest artifact in the run will be selected.
        aliases: list of str, optional
            List of version aliases (e.g., ["v1.0", "latest"])

        Example
        --------
        Register from Python object:

        >>> client.promote_model_artifact(
        ...     name="RiskModel",
        ...     model_artifact_id=model_artifact_id,
        ...     aliases=["latest"],
        ... )
        """
        ...

    def train_model(
        self,
        experiment_name: str,
        train_fn: Optional[Callable[[], None]] = None,
        config: Optional[Mapping[str, float | str | bool | int]] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        resources: Optional[ResourceRequests] = None,
        env_overrides: Optional[Mapping[str, str]] = None,
        enable_profiling: bool = False,
        max_retries: int = 0,
        train_script: Optional[str] = None,
        entrypoint: Optional[str] = None,
    ) -> CreateModelTrainingJobResponse:
        """Train a model using a provided training function or self-contained script.

        Parameters
        ----------
        experiment_name : str
            The name of the experiment for this training run.
        train_fn : Optional[Callable[[], None]]
            A callable training function. Use this in Jupyter notebooks or when importing
            a function from a script. Either ``train_fn`` or ``train_script`` must be provided.
        train_script : Optional[str]
            A self-contained Python script string. May be supplied alone, in which case
            the entrypoint is the script's single top-level function (use ``entrypoint``
            to disambiguate when multiple are defined). May also be supplied alongside
            ``train_fn`` to override the source that would otherwise be reconstructed
            from the notebook or read from the function's defining ``.py`` file; the
            script must then define a top-level function matching ``train_fn.__name__``.
        entrypoint : Optional[str]
            The name of the top-level function in ``train_script`` to use as the entrypoint.
            Required when ``train_script`` defines more than one top-level function.
            Only valid with ``train_script``.
        config: Optional[Mapping[str, float | str | bool | int]]
            Optional configuration parameters for the training job. If this is supplied, then
            the train function must take one argument.
        branch : Optional[Union[BranchId, ellipsis]]
            The branch to use for the training job.
        resources : Optional[ResourceRequests]
            Optional resource requirements for the training job.
        resource_group : Optional[str]
            Optional resource group for the training job.
        env_overrides : Optional[Mapping[str, str]]
            Optional environment variable overrides.
        enable_profiling : bool
            Whether to enable profiling for the training job.
        max_retries : int
            Maximum number of retries for the training job.

        Returns
        -------
        CreateModelTrainingJobResponse
            Response containing information about the created training job.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> def my_training_function():
        ...     # Training logic here
        ...     return True
        >>> client = ChalkClient()
        >>> response = client.train_model(
        ...     experiment_name="exp1",
        ...     train_fn=my_training_function
        ... )
        """
        ...

    def trigger_aggregate_backfill(
        self,
        features: list[str],
        lower_bound: datetime | None = None,
        upper_bound: datetime | None = None,
        resolver: str | None = None,
        query_tags: list[str] | None = None,
        store_offline: bool | None = None,
        allow_empty_tiles: bool = True,
        exact: bool = False,
        enable_profiling: bool = False,
        resource_group: str | None = None,
        input_sql: str | None = None,
        plan_only: bool = False,
    ) -> Any:
        """Trigger one or more aggregate backfill jobs.

        Parameters
        ----------
        features : list[str]
            The fully-qualified names of the aggregate features to backfill.
        lower_bound : datetime, optional
            The lower bound of the time range to backfill.
        upper_bound : datetime, optional
            The upper bound of the time range to backfill.
        resolver : str, optional
            The resolver to use for the backfill.
        query_tags : list[str], optional
            Resolver tags to prefer when running the backfill.
        store_offline : bool, optional
            If `True`, store materialized aggregate values in the offline store.
            Requires both `lower_bound` and `upper_bound`.
        allow_empty_tiles : bool
            If `True`, empty tile spans are skipped instead of raising an error.
            Defaults to `True`. Set to `False` to raise an error when a backfill produces no tile files.
        exact : bool, optional
            If `True`, execute the underlying SQL source to determine the exact
            number of rows that need to migrate.
        enable_profiling : bool, optional
            If `True`, enable profiling while running the backfill jobs.
        resource_group : str, optional
            Resource group to use for the created backfill jobs.
        input_sql : str, optional
            Chalk SQL query to use to resolve event data. Mutually exclusive with `resolver`.
        plan_only : bool, optional
            If `True`, return the aggregate backfill plan without creating jobs.

        Returns
        -------
        list | PlanAggregateBackfillResponse
            A list of aggregate backfill job responses, one per planned backfill job,
            or the plan when `plan_only=True`.
        """
        ...

    def trigger_workflow(
        self,
        workflow: WorkflowDefinition | str,
        input: Optional[Mapping[str, Any]] = None,
        *,
        workflow_id: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        wait: bool = False,
    ) -> Union[WorkflowRunHandle, Any]:
        """Start a `@workflow` on this environment's workflow orchestrator.

        The workflow must be part of the environment's active deployment: its tasks
        execute on the deployment's workflow workers. To execute a workflow defined
        in a local file that has not been deployed, use `run_workflow` instead.

        Requires the `temporalio` package (`pip install chalkpy[workflows]`).

        Parameters
        ----------
        workflow
            The workflow to run: a `@workflow`-decorated function or its name.
        input
            Keyword arguments for the workflow function. Values must be
            JSON-serializable.
        workflow_id
            Idempotency key identifying this run. Defaults to a generated id.
        environment
            The environment under which to run the workflow.
        wait
            If `True`, block until the workflow completes and return its result.

        Returns
        -------
        Union[WorkflowRunHandle, Any]
            A handle for the started run, or the workflow's return value if
            `wait=True`.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.trigger_workflow("nightly_scoring", input={"segment": "us"})
        """
        ...

    def run_workflow(
        self,
        workflow: WorkflowDefinition,
        input: Optional[Mapping[str, Any]] = None,
        *,
        workflow_id: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
    ) -> Any:
        """Run a locally defined `@workflow` against this environment's workflow
        orchestrator, and block until it completes.

        Coordination (durable state, retries, timers) happens on the environment's
        workflow orchestrator, while the workflow and its tasks execute in this
        process — the workflow does not need to be deployed first. This is intended
        for local development; use `trigger_workflow` to run deployed workflows on
        the environment's workflow workers.

        Requires the `temporalio` package (`pip install chalkpy[workflows]`).

        Parameters
        ----------
        workflow
            A `@workflow`-decorated function defined in this process.
        input
            Keyword arguments for the workflow function. Values must be
            JSON-serializable.
        workflow_id
            Idempotency key identifying this run. Defaults to a generated id.
        environment
            The environment under which to run the workflow.

        Returns
        -------
        Any
            The workflow's return value.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> from chalk.workflows import task, workflow
        >>> @task
        ... def add(x: int, y: int) -> int:
        ...     return x + y
        >>> @workflow
        ... async def add_workflow(x: int, y: int) -> int:
        ...     return await add(x, y)
        >>> client = ChalkClient()
        >>> client.run_workflow(add_workflow, input={"x": 1, "y": 2})
        """
        ...

    def __new__(cls, *args: Any, **kwargs: Any):
        from chalk.client.client_impl import ChalkAPIClientImpl

        return ChalkAPIClientImpl(*args, **kwargs)


ChalkAPIClientProtocol: TypeAlias = ChalkClient
"""Deprecated. Use `ChalkClient` instead."""

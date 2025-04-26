from __future__ import annotations

import types
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Mapping, Optional, Sequence, Union
from uuid import UUID

from chalk import DataFrame
from chalk.client.models import (
    BulkOnlineQueryResponse,
    FeatureReference,
    FeatureStatisticsResponse,
    OfflineQueryInputUri,
    OnlineQuery,
    OnlineQueryContext,
    ResourceRequests,
    UploadFeaturesResponse,
    WhoAmIResponse,
)
from chalk.client.response import Dataset, OnlineQueryResult
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features.tag import BranchId, DeploymentId, EnvironmentId
from chalk.prompts import Prompt

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

    QueryInput = Mapping[FeatureReference, Any] | pd.DataFrame | pl.DataFrame | DataFrame | str


class AsyncChalkClient:
    """The `AsyncChalkClient` is an asynchronous Python interface for interacting with Chalk.

    You can use it to query data, trigger resolver runs, gather offline data, and more, and all calls are asynchronous.
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        api_server: Optional[str] = None,
        query_server: Optional[str] = None,
        branch: Optional[BranchId] = None,
        preview_deployment_id: Optional[DeploymentId] = None,
        additional_headers: Optional[Mapping[str, str]] = None,
        default_job_timeout: float | timedelta | None = None,
        default_request_timeout: float | timedelta | None = None,
        executor: Optional[ThreadPoolExecutor] = None,
        pool_maxsize: Optional[int] = None,
    ):
        """Create an `AsyncChalkClient` with the given credentials.

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
            the client will default to the value of `api_server`.
        branch
            If specified, Chalk will route all requests from this client
            instance to the relevant branch. Some methods allow you to
            override this instance-level branch configuration by passing
            in a `branch` argument.
        preview_deployment_id
            If specified, Chalk will route all requests from this client
            instance to the relevant preview deployment.
        additional_headers
            A map of additional HTTP headers to pass with each request.
        default_job_timeout
            The default wait timeout, in seconds, to wait for long-running jobs to complete
            when accessing query results.
            Jobs will not time out if this timeout elapses. For no timeout, set to `None`.
            The default timeout is 10 minutes.
        default_request_timeout:
            The default wait timeout, in seconds, to wait for network requests to complete.
            If not specified, the default is no timeout.
        executor
            A custom `ThreadPoolExecutor` to use for running asynchronous tasks.
            If not provided, will use Chalk's default thread pool.
        pool_maxsize
            The maximum number of connections the HTTP session is configured to handle.
            If not provided, will use the default pool size.

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

    def __new__(cls, *args: Any, **kwargs: Any):
        from chalk.client.client_async_impl import AsyncChalkClientImpl

        return AsyncChalkClientImpl(*args, **kwargs)

    async def whoami(self) -> WhoAmIResponse:
        """Checks the identity of your client.

        Useful as a sanity test of your configuration.

        Returns
        -------
        WhoAmIResponse
            The identity of your client.

        Examples
        --------
        >>> from chalk.client import AsyncChalkClient
        >>> await AsyncChalkClient().whoami()
        WhoAmIResponse(user="...", environment_id='...', team_id='...')
        """
        ...

    async def query(
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
        headers: Mapping[str, str] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
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
            If specified, *all* required_resolver_tags must be present on a resolver for it to be
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
        headers
            Additional headers to provide with the request.

        Returns
        -------
        Awaitable[OnlineQueryResult]
            Coroutine that returns a wrapper around the output features and any query metadata,
            plus errors encountered while running the resolvers.

        Examples
        --------
        >>> from chalk.client import AsyncChalkClient
        >>> result = await AsyncChalkClient().query(
        ...     input={
        ...         User.name: "Katherine Johnson"
        ...     },
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        >>> result.get_feature_value(User.fico_score)
        """
        ...

    async def multi_query(
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

        Returns a BulkOnlineQueryResponse, which is functionally a list of query results. Each of these result
        can be accessed by index. Individual results can be further checked for errors and converted
        to pandas or polars DataFrames.

        In contrast, `query_bulk` executes a single query with multiple inputs/outputs.

        Parameters
        ----------
        queries
            A list of the OnlineQueries you'd like to execute.
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
        query_context
            An immutable context that can be accessed from Python resolvers.
            This context wraps a JSON-compatible dictionary or JSON string with type restrictions.
            See https://docs.chalk.ai/api-docs#ChalkContext for more information.
        compression
            Which compression scheme to use pyarrow. Options are: {"zstd", "lz4", "uncompressed"}.

        Returns
        -------
        Awaitable[BulkOnlineQueryResponse]
            Coroutine that returns object containing results: list[BulkOnlineQueryResult], where each result contains
            dataframes of the results of each query or any errors.

        Examples
        --------
        >>> from chalk.client import AsyncChalkClient, OnlineQuery
        >>> queries =[
        ...     OnlineQuery(input={User.name: ['Katherine Johnson'], output=[User.fico_score]}),
        ...     OnlineQuery(input={Merchant.name: ['Myrrh Chant'], output=['Merchant.address']}),
        ...     OnlineQuery(input={NonFeature.wrong: ['Wrong!'], output=['NonFeature.wrong']}),
        ... ]
        >>> result = await AsyncChalkClient().multi_query(
        ...     queries=queries,
        ... )
        >>> result[0].get_feature_value(User.fico_score)
        >>> queries_with_errors = [q for q, r in zip(queries, result) if r.errors is not None]
        """
        ...

    async def query_bulk(
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

        Returns
        -------
        Awaitable[BulkOnlineQueryResponse]
            Coroutine of a list[BulkOnlineQueryResult], where each result contains dataframes of the
            results of each query.

        Examples
        --------
        >>> from chalk.client import AsyncChalkClient
        >>> await AsyncChalkClient().query_bulk(
        ...     input={User.name: ["Katherine Johnson", "Eleanor Roosevelt"]},
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        """
        ...

    async def offline_query(
        self,
        input: Union[QueryInput, OfflineQueryInputUri] | None = None,
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
        show_progress: bool = True,
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
        input_times
            A list of the times of the observations from `input`.
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row) in
            the resulting `DataFrame`, its value will be `None`.
        recompute_features
            Used to control whether resolvers are allowed to run in order to compute feature values.

            If True, all output features will be recomputed by resolvers.
            If False, all output features will be sampled from the offline store.
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
            If None, Chalk will route your request to a non-branch deployment.
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
            Whether to wait for job completion
        show_progress
            If True, progress bars will be shown while the query is running.
            Primarily intended for use in a Jupyter-like notebook environment.
            This flag will also be propagated to the methods of the resulting
            `Dataset`.
        timeout:
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        lower_bound
            If specified, the query will only be run on data observed after this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        upper_bound
            If specified, the query will only be run on data observed before this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        store_plan_stages
            If True, the output of each of the query plan stages will be stored
            in S3/GCS. This will dramatically impact the performance of the query,
            so it should only be used for debugging.
            These files will be visible in the web dashboard's query detail view, and
            can be downloaded in full by clicking on a plan node in the query plan visualizer.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        required_resolver_tags
            If specified, *all* required_resolver_tags must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        store_online
            If True, the output of the query will be stored in the online store.
        store_offline
            If True, the output of the query will be stored in the offline store.
        num_shards
            If specified, the query will be run asynchronously, splitting the input across `num_shards` shards.
        num_workers
            If specified, the query will be run asynchronously across a maximum `num_workers` pod workers at any time.
            This parameter is useful if you have a large number of shards and would like to limit the number of pods running at once.

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
        >>> from chalk.client import AsyncChalkClient
        >>> uids = [1, 2, 3, 4]
        >>> at = datetime.now(tz=timezone.utc)
        >>> dataset = await AsyncChalkClient().offline_query(
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
        ...     dataset_name='my_dataset'
        ... )
        >>> df = dataset.get_data_as_pandas()
        """
        ...

    async def create_dataset(
        self,
        input: QueryInput,
        dataset_name: str | None = None,
        environment: EnvironmentId | None = None,
        branch: BranchId | None = ...,
        wait: bool = False,
        show_progress: bool = True,
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
            If True, progress bars will be shown while the query is running.
            Primarily intended for use in a Jupyter-like notebook environment.
            This flag will also be propagated to the methods of the resulting
            `Dataset`.
        timeout:
            How long to wait, in seconds, for job completion before raising a TimeoutError.
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

    async def prompt_evaluation(
        self,
        prompts: list[Prompt | str],
        dataset_id: str | None = None,
        dataset_name: str | None = None,
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
        show_progress: bool = True,
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
    ) -> Dataset:
        """Runs an evaluation on a set of prompts.
        See https://docs.chalk.ai/docs/prompts#prompt-evaluation for more information.

        Parameters
        ----------
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
        prompts
            The list of prompts to use for the evaluation.
            This can be a list of `Prompt` objects or a list of named prompts.
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

            If True, all output features will be recomputed by resolvers.
            If False, all output features will be sampled from the offline store.
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
            If None, Chalk will route your request to a non-branch deployment.
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
            If True, progress bars will be shown while the query is running.
            Primarily intended for use in a Jupyter-like notebook environment.
            This flag will also be propagated to the methods of the resulting
            `Dataset`.
        timeout:
            How long to wait, in seconds, for job completion before raising a TimeoutError.
            Jobs will continue to run in the background if they take longer than this timeout.
            For no timeout, set to `None`. If no timeout is specified, the client's default
            timeout is used.
        lower_bound
            If specified, the query will only be run on data observed after this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        upper_bound
            If specified, the query will only be run on data observed before this timestamp.
            Accepts strings in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        store_plan_stages
            If True, the output of each of the query plan stages will be stored
            in S3/GCS. This will dramatically impact the performance of the query,
            so it should only be used for debugging.
            These files will be visible in the web dashboard's query detail view, and
            can be downloaded in full by clicking on a plan node in the query plan visualizer.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        required_resolver_tags
            If specified, *all* required_resolver_tags must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        resources
            Override resource requests for processes with isolated resources, e.g., offline queries and cron jobs.
            See `ResourceRequests` for more information.
        run_asynchronously
            Boots a kubernetes job to run the queries in their own pods, separate from the engine and branch servers.
            This is useful for large datasets and jobs that require a long time to run.
        store_online
            If True, the output of the query will be stored in the online store.
        store_offline
            If True, the output of the query will be stored in the offline store.
        num_shards
            If specified, the query will be run asynchronously, splitting the input across `num_shards` shards.
        num_workers
            If specified, the query will be run asynchronously across a maximum `num_workers` pod workers at any time.
            This parameter is useful if you have a large number of shards and would like to limit the number of pods running at once.
        completion_deadline
            If specified, shards must complete within 'completion_deadline' duration, or they will be terminated.
            Terminated shards can be tried.
        max_retries
            If specified, failed offline query shards will be retried. The retry budget is shared across all shards.
            By default, max_retries=num_shards/

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

    async def upload_features(
        self,
        input: Mapping[FeatureReference, Any],
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        environment: Optional[EnvironmentId] = None,
    ) -> UploadFeaturesResponse:
        ...

    async def get_operation_feature_statistics(self, operation_id: UUID) -> FeatureStatisticsResponse:
        """
        Fetches statistics for an operation's outputs.

        """
        ...

    async def __aenter__(self) -> AsyncChalkClient:
        ...

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exception: BaseException | None, tb: types.TracebackType | None
    ) -> None:
        ...

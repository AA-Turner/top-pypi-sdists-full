from __future__ import annotations

import inspect
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Collection

from chalk.queries._schedule_entity_name import validate_schedule_entity_name
from chalk.utils.duration import CronTab, Duration

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference, ResourceRequests, UnloadResolvers


class ScheduledQuery:
    def __init__(
        self,
        name: str,
        schedule: CronTab | Duration,
        output: Collection[FeatureReference],
        recompute_features: bool | Collection[FeatureReference] = True,
        max_samples: int | None = None,
        lower_bound: datetime | timedelta | None = None,
        upper_bound: datetime | timedelta | None = None,
        tags: Collection[str] | None = None,
        dataset_name: str | None = None,
        required_resolver_tags: Collection[str] | None = None,
        store_online: bool = True,
        store_offline: bool = True,
        incremental_resolvers: Collection[str] | None = None,
        planner_options: dict[str, str] | None = None,
        resource_group: str | None = None,
        completion_deadline: timedelta | None = None,
        num_shards: int | None = None,
        num_workers: int | None = None,
        input_sql: str | None = None,
        unload_resolvers: UnloadResolvers = None,
        max_retries: int | None = None,
        resources: ResourceRequests | None = None,
        environment: str | None = None,
        write_to: str | None = None,
    ):
        """Create an offline query which runs on a schedule.

        Scheduled queries do not produce datasets, but persist their results in the
        online and/or offline feature stores.

        By default, scheduled queries use incrementalization to only ingest data that
        has been updated since the last run.

        Parameters
        ----------
        name
            A unique name for the scheduled query. The name of the scheduled query
            will show up in the dashboard and will be uset to set the incremetalization
            metadata.
        schedule
            A cron schedule or a `Duration` object representing the interval at which
            the query should run.
        output
            The features that this query will compute. Namespaces are exploded into all
            features in the namespace.
        recompute_features
            Whether to recompute all features or load from the feature store.
            If `True`, all features will be recomputed.
            If `False`, all features will be loaded from the feature store.
            If a list of features, only those features will be recomputed, and the rest
            will be loaded from the feature store.
        max_samples
            The maximum number of samples to compute.
        lower_bound
            A lower bound for the query. If set, the query will not use incrementalization.
            A `datetime` is a fixed bound; a `timedelta` is resolved relative to each run
            (e.g. `-timedelta(days=7)` is the last 7 days as of the run).
        upper_bound
            An upper bound for the query. If set, the query will not use incrementalization.
            A `datetime` is a fixed bound; a `timedelta` is resolved relative to each run.
        tags
            Allows selecting resolvers with these tags.
        dataset_name
            Associated dataset name for the scheduled query. If set, each run's output is
            persisted as a revision of this dataset, independently of `store_online` and
            `store_offline`.
        required_resolver_tags
            Requires that resolvers have these tags.
        store_online
            Whether to store the results of this query in the online store.
        store_offline
            Whether to store the results of this query in the offline store.
        incremental_resolvers
            If set to None, Chalk will incrementalize resolvers in the query's root namespaces.
            If set to a list of resolvers, this set will be used for incrementalization.
            Incremental resolvers must return a feature time in its output, and must return a `DataFrame`.
            Most commonly, this will be the name of a SQL file resolver. Chalk will ingest all new data
            from these resolvers and propagate changes to values in the root namespace.
        planner_options
            A dictionary of options to pass to the planner. These are typically provided by Chalk Support
            for specific use cases.
        resource_group
            The resource group to use for the query. If not set, the default resource group will be used.
        write_to
            A storage URI (e.g. `s3://bucket/path/`) to which each run's output rows
            are written directly, in addition to online/offline store persistence.

        Returns
        -------
        ScheduledQuery
            A scheduled query object.

        Examples
        --------
        >>> from chalk.queries import ScheduledQuery
        >>> # this scheduled query will automatically run every 5 minutes after `chalk apply`
        >>> ScheduledQuery(
        ...     name="ingest_users",
        ...     schedule="*/5 * * * *",
        ...     output=[User],
        ...     store_online=True,
        ...     store_offline=True,
        ... )
        """
        super().__init__()
        self.errors = []

        name_err = validate_schedule_entity_name(name, entity_noun="Scheduled query")
        if name_err is not None:
            self.errors.append(name_err)

        if name in CRON_QUERY_REGISTRY:
            self.errors.append(
                f"A scheduled query with name '{name}' already exists. Scheduled query names must be unique."
            )

        if len(output) == 0:
            self.errors.append(
                f"Scheduled query '{name}' was instantiated with an empty set of outputs. At least one output is required."
            )

        if isinstance(lower_bound, datetime):
            lower_bound = lower_bound.astimezone(tz=timezone.utc)
        if isinstance(upper_bound, datetime):
            upper_bound = upper_bound.astimezone(tz=timezone.utc)

        caller_filename = None
        frame = inspect.currentframe()
        assert frame is not None, "Failed to get current frame"
        caller_frame = frame.f_back
        assert caller_frame is not None, "Failed to get caller frame"
        caller_filename = caller_frame.f_code.co_filename
        del frame

        # Capture the call-site AST so that, during `chalk apply` / `chalk lint`, we
        # can surface lint diagnostics that point directly at this `ScheduledQuery(...)`
        # call (e.g. an `incremental_resolvers` entry that isn't actually incremental).
        from chalk._lsp.error_builder import FunctionCallErrorBuilder, get_function_caller_info

        self._error_builder = FunctionCallErrorBuilder(get_function_caller_info(frame_offset=1))

        # A `write_to` destination or a `dataset_name` makes a run meaningful even without
        # online/offline store persistence: the output rows are written to the destination
        # directly, or persisted as a revision of the named dataset.
        if not store_offline and not store_online and write_to is None and dataset_name is None:
            self.errors.append(
                f"Scheduled query '{name}' was instantiated with `store_offline=False` and `store_online=False`, and no `write_to` destination or `dataset_name`. Running it will have no effect, as it does not store any data."
            )

        self.input_sql = input_sql
        self.name = name
        self.cron = schedule
        self.output = [str(f) for f in output]
        self.max_samples = max_samples
        self.recompute_features = (
            recompute_features
            if recompute_features is True or recompute_features is False
            else [str(f) for f in recompute_features]
        )
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.tags = tags
        self.dataset_name = dataset_name
        self.required_resolver_tags = required_resolver_tags
        self.filename = caller_filename
        self.store_online = store_online
        self.store_offline = store_offline
        if incremental_resolvers is not None and isinstance(incremental_resolvers, str):
            self.errors.append(
                f"Scheduled query '{name}' was instantiated with `incremental_resolvers={incremental_resolvers}`, but `{incremental_resolvers}` must be a list of resolver names."
            )
        self.incremental_resolvers = incremental_resolvers
        self.planner_options = {k: str(v) for k, v in planner_options.items()} if planner_options else None
        self.resource_group = resource_group

        self.completion_deadline = completion_deadline
        self.max_retries = max_retries
        self.resources = resources
        self.environment = environment

        self.num_shards = num_shards
        self.num_workers = num_workers
        self.write_to = write_to
        from chalk.client.client_impl import encode_unload_resolvers

        self.unload_resolvers = encode_unload_resolvers(unload_resolvers)

        CRON_QUERY_REGISTRY[name] = self


CRON_QUERY_REGISTRY: dict[str, ScheduledQuery] = {}


def lint_incremental_resolvers(cron: ScheduledQuery, resolver_registry: object) -> None:
    """Warn when a scheduled query lists `incremental_resolvers` that aren't actually
    incremental.
    """
    incremental_resolvers = cron.incremental_resolvers
    if not incremental_resolvers:
        return
    builder = getattr(cron, "_error_builder", None)
    get_resolver = getattr(resolver_registry, "get_resolver", None)
    if builder is None or get_resolver is None:
        return

    from chalk.features.resolver import resolver_is_incremental
    from chalk.parsed.duplicate_input_gql import DiagnosticSeverityGQL, PositionGQL, RangeGQL

    base_range = builder.function_arg_range_by_name("incremental_resolvers")
    if base_range is None:
        line = max((builder.caller_info.lineno or 1) - 1, 0)
        base_range = RangeGQL(
            start=PositionGQL(line=line, character=0),
            end=PositionGQL(line=line, character=1),
        )

    # Need to offset by 1 to match the CLI renderer convention
    diagnostic_range = RangeGQL(
        start=PositionGQL(line=base_range.start.line + 1, character=base_range.start.character),
        end=PositionGQL(line=base_range.end.line + 1, character=base_range.end.character),
    )

    for resolver_name in incremental_resolvers:
        resolver = get_resolver(resolver_name)
        if resolver is None:
            builder.add_diagnostic(
                message=(
                    f"Scheduled query '{cron.name}' lists '{resolver_name}' in `incremental_resolvers`, "
                    f"but no resolver named '{resolver_name}' could be found. The scheduled query cannot "
                    f"incrementalize through a resolver that does not exist."
                ),
                label="unknown incremental resolver",
                code="214",
                range=diagnostic_range,
                severity=DiagnosticSeverityGQL.Warning,
            )
        elif not resolver_is_incremental(resolver):
            builder.add_diagnostic(
                message=(
                    f"Scheduled query '{cron.name}' lists '{resolver_name}' in `incremental_resolvers`, "
                    f"but '{resolver_name}' is not configured to be incremental, so it will not be "
                    f"incrementalized. Chalk can only incrementalize a scheduled query through resolvers "
                    f"that are themselves incremental. Add incremental settings to the resolver (an "
                    f"`incremental:` block for a SQL file resolver, or `incremental=...` for a Python resolver)."
                ),
                label="non-incremental incremental resolver",
                code="213",
                range=diagnostic_range,
                severity=DiagnosticSeverityGQL.Warning,
            )

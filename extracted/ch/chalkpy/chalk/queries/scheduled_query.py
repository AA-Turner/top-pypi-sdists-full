from __future__ import annotations

import inspect
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Collection

from chalk.utils.duration import CronTab, Duration

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference


class ScheduledQuery:
    def __init__(
        self,
        name: str,
        schedule: CronTab | Duration,
        output: Collection[FeatureReference],
        recompute_features: bool | Collection[FeatureReference] = True,
        max_samples: int | None = None,
        lower_bound: datetime | None = None,
        upper_bound: datetime | None = None,
        tags: Collection[str] | None = None,
        required_resolver_tags: Collection[str] | None = None,
        store_online: bool = True,
        store_offline: bool = True,
        incremental_resolvers: Collection[str] | None = None,
        planner_options: dict[str, str] | None = None,
        resource_group: str | None = None,
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
            A hard-coded lower bound for the query. If set, the query will not use
            incrementalization.
        upper_bound
            A hard-coded upper bound for the query. If set, the query will not use
            incrementalization.
        tags
            Allows selecting resolvers with these tags.
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


        Returns
        -------
        ScheduledQuery
            A scheduled query object.

        Examples
        --------
        >>> from chalk.features import ScheduledQuery
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

        if name in CRON_QUERY_REGISTRY:
            self.errors.append(
                f"A scheduled query with name '{name}' already exists. Scheduled query names must be unique."
            )

        if len(output) == 0:
            self.errors.append(
                f"Scheduled query '{name}' was instantiated with an empty set of outputs. At least one output is required."
            )

        if lower_bound is not None:
            lower_bound = lower_bound.astimezone(tz=timezone.utc)
        if upper_bound is not None:
            upper_bound = upper_bound.astimezone(tz=timezone.utc)

        caller_filename = inspect.stack()[1].filename

        if not store_offline and not store_online:
            self.errors.append(
                f"Scheduled query '{name}' was instantiated with `store_offline=False` and `store_online=False`. Running it will have no effect, as it does not store any data."
            )

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

        CRON_QUERY_REGISTRY[name] = self


CRON_QUERY_REGISTRY: dict[str, ScheduledQuery] = {}

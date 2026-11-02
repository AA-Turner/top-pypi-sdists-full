from ..service import Service
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Union
from ..exception import AppwriteException
from appwrite_console.utils.deprecated import deprecated
from ..enums.usage_interval import UsageInterval
from ..enums.usage_event_dimension import UsageEventDimension
from ..enums.usage_order_by import UsageOrderBy
from ..enums.usage_order_direction import UsageOrderDirection
from ..models.usage_event_list import UsageEventList
from ..enums.usage_gauge_dimension import UsageGaugeDimension
from ..models.usage_gauge_list import UsageGaugeList


class Usage(Service):

    def __init__(self, client) -> None:
        super(Usage, self).__init__(client)

    def list_events(
        self,
        metrics: List[str],
        queries: Optional[List[str]] = None,
        interval: Optional[UsageInterval] = None,
        dimensions: Optional[List[UsageEventDimension]] = None,
        start_at: Optional[str] = None,
        end_at: Optional[str] = None,
        order_by: Optional[UsageOrderBy] = None,
        order_dir: Optional[UsageOrderDirection] = None,
        limit: Optional[float] = None,
        offset: Optional[float] = None,
    ) -> UsageEventList:
        """
        Aggregate usage event metrics. `metrics[]` (1-10) is required; the response always contains one entry per requested metric, each with its own `points[]` time series.

        **Two response shapes**:
        - Omit `interval` for a flat top-N table — one point per dimension combination, no time axis. Useful for "top 10 paths by bandwidth in the last 7 days".
        - Pass `interval` (`1m`, `15m`, `30m`, `1h`, `1d`) for a time series — one point per (time bucket × dimension combination).

        `dimensions[]` breaks each point down by one or more attributes (service, path, status, country, …). `queries[]` filters the underlying events using the standard Utopia query syntax — `equal("path", ["/v1/storage/files"])`, `equal("resourceType", ["bucket"])`, `equal("resourceId", ["abc123"])`, `startsWith("path", ["/v1/storage"])`, `equal("status", ["200", "201"])`, `isNotNull("resourceId")`. Supported attributes: see `queries[]` param. Supported methods: `equal`, `notEqual`, `contains`, `startsWith`, `endsWith`, `isNull`, `isNotNull`. Pass multiple metrics to render stacked charts in one round-trip. `orderBy=value`+`orderDir=desc`+`limit=N` returns the top-N by aggregated value. When `startAt` is omitted, the default window adapts to `interval` (or 7d when interval is omitted).

        Parameters
        ----------
        metrics : List[str]
            One to ten metric names. Single-metric callers pass a one-element array. Example: `metrics[]=executions` or `metrics[]=executions&metrics[]=executions.compute` for stacked charts. On console: `metrics[]=affiliates.clicks`.
        queries : Optional[List[str]]
            Up to 10 filter queries in Utopia syntax. Allowed attributes, also published as the `UsageEventDimension` enum: path, method, status, service, resourceType, resourceId, teamId, country, continentCode, city, region, hostname, ip, osName, clientType, clientName, deviceName, sdk, sdkVersion, protocol, queryKeys, accept, acceptLanguage, postalCode, latitude, longitude, timeZone, weatherCode, isp, autonomousSystemNumber, autonomousSystemOrganization, connectionType, connectionUsageType, connectionOrganization. Allowed methods: equal, notEqual, contains, startsWith, endsWith, isNull, isNotNull. Example: `queries[]=equal("resourceType", ["bucket"])`.
        interval : Optional[UsageInterval]
            Time interval size. Omit (null) for a flat aggregate over the whole window. Allowed: 1m, 15m, 30m, 1h, 1d.
        dimensions : Optional[List[UsageEventDimension]]
            Break-down dimensions (max 10). Allowed: path, method, status, service, resourceType, country, continentCode, city, region, hostname, ip, osName, clientType, clientName, deviceName, sdk, sdkVersion, teamId, resourceId, protocol, queryKeys, accept, acceptLanguage, postalCode, latitude, longitude, timeZone, weatherCode, isp, autonomousSystemNumber, autonomousSystemOrganization, connectionType, connectionUsageType, connectionOrganization.
        start_at : Optional[str]
            Range start in ISO 8601. Defaults adapt to interval (7d for the no-interval aggregate).
        end_at : Optional[str]
            Range end in ISO 8601. Defaults to the current time.
        order_by : Optional[UsageOrderBy]
            Column to order by. Allowed: time, value. Default time when an interval is set; otherwise value.
        order_dir : Optional[UsageOrderDirection]
            Sort direction: asc or desc. Default desc — paired with the default limit, returns the most recent / highest-value groups first.
        limit : Optional[float]
            Maximum rows to return (1-5000).
        offset : Optional[float]
            Pagination offset (0-100000).
        Returns
        -------
        UsageEventList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/usage/events'
        api_params = {}
        if metrics is None:
            raise AppwriteException('Missing required parameter: "metrics"')
        api_params['metrics'] = self._normalize_value(metrics)
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if interval is not None:
            api_params['interval'] = self._normalize_value(interval)
        if dimensions is not None:
            api_params['dimensions'] = self._normalize_value(dimensions)
        if start_at is not None:
            api_params['startAt'] = self._normalize_value(start_at)
        if end_at is not None:
            api_params['endAt'] = self._normalize_value(end_at)
        if order_by is not None:
            api_params['orderBy'] = self._normalize_value(order_by)
        if order_dir is not None:
            api_params['orderDir'] = self._normalize_value(order_dir)
        if limit is not None:
            api_params['limit'] = self._normalize_value(limit)
        if offset is not None:
            api_params['offset'] = self._normalize_value(offset)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=UsageEventList)

    def list_gauges(
        self,
        metrics: List[str],
        queries: Optional[List[str]] = None,
        interval: Optional[UsageInterval] = None,
        dimensions: Optional[List[UsageGaugeDimension]] = None,
        start_at: Optional[str] = None,
        end_at: Optional[str] = None,
        order_by: Optional[UsageOrderBy] = None,
        order_dir: Optional[UsageOrderDirection] = None,
        limit: Optional[float] = None,
        offset: Optional[float] = None,
        aggregate: Optional[str] = None,
    ) -> UsageGaugeList:
        """
        Aggregate usage gauge snapshots. Gauges are point-in-time values (storage totals, resource counts, …); each point carries the latest snapshot in its interval via `argMax(value, time)`. `metrics[]` (1-10) is required; the response always contains one entry per requested metric, each with its own `points[]` time series.

        A metric with no stored samples in the window returns an empty `points[]`. A metric that really did read zero returns a point whose `value` is `0`, so "no such series" and "a genuine zero" are different answers.

        **Two response shapes**:
        - Omit `interval` for a flat top-N table — `argMax(value, time)` per dimension combination over the whole window, no time axis. Useful for "top 10 resources by current storage".
        - Pass `interval` (`1m`, `15m`, `30m`, `1h`, `1d`) for a time series — one snapshot per (time bucket × dimension combination).

        `dimensions[]` breaks each point down further. Supported on gauges: `resourceId`, `teamId`, `service`, `resourceType`, `ordinal`. `service` and `resourceType` enable per-service / per-resource-type panels (e.g. storage-by-service: group `files.storage`, `deployments.storage`, `builds.storage`, `databases.storage` by `service`). `ordinal` separates per-node series for multi-node resources such as dedicated databases. It is a stable per-node identity, not a role — ordinal 0 is the first member created, and a failover can leave the primary on any ordinal, so read the role from the database's replicas endpoint rather than inferring it here. `queries[]` filters the underlying rows using the standard Utopia query syntax — `equal("resourceType", ["bucket"])`, `equal("resourceId", ["abc123"])`, `equal("teamId", ["team_x"])`, `equal("ordinal", ["0"])`, `isNotNull("teamId")`. Supported attributes: see `queries[]` param. Supported methods: `equal`, `notEqual`, `isNull`, `isNotNull`. Pass multiple metrics to render stacked charts in one round-trip. `orderBy=value`+`orderDir=desc`+`limit=N` returns the top-N. When `startAt` is omitted, the default window adapts to interval (or 7d when interval is omitted).

        `aggregate` selects how the samples in a bucket are combined: `last` (default) is the latest reading — correct for a snapshot such as storage — while `max` is the highest reading. Use `max` for a sampled level series: peak concurrent realtime connections is `metrics[]=realtime.connections&aggregate=max`, at whatever `interval` the chart needs, since the peak of a set of samples is just the max of their per-bucket maxima. `realtime.connections` is served only here - it is a concurrency level, not a countable event, so `/v1/usage/events` rejects it.

        Parameters
        ----------
        metrics : List[str]
            One to ten metric names. Single-metric callers pass a one-element array. Example: `metrics[]=files.storage` or `metrics[]=files.storage&metrics[]=deployments.storage` for stacked charts.
        queries : Optional[List[str]]
            Up to 10 filter queries in Utopia syntax. Allowed attributes, also published as the `UsageGaugeDimension` enum: service, resourceType, resourceId, teamId, ordinal. Allowed methods: equal, notEqual, isNull, isNotNull. Example: `queries[]=equal("resourceType", ["bucket"])`.
        interval : Optional[UsageInterval]
            Time interval size. Omit (null) for a flat aggregate over the whole window. Allowed: 1m, 15m, 30m, 1h, 1d.
        dimensions : Optional[List[UsageGaugeDimension]]
            Break-down dimensions. Allowed: resourceId, teamId, service, resourceType, ordinal.
        start_at : Optional[str]
            Range start in ISO 8601. Defaults to endAt - 7d.
        end_at : Optional[str]
            Range end in ISO 8601. Defaults to the current time.
        order_by : Optional[UsageOrderBy]
            Column to order by. Allowed: time, value. Default time.
        order_dir : Optional[UsageOrderDirection]
            Sort direction: asc or desc. Default desc — paired with the default limit, this returns the most recent groups first. Pass asc for chronological charting.
        limit : Optional[float]
            Maximum rows to return (1-5000).
        offset : Optional[float]
            Pagination offset (0-100000).
        aggregate : Optional[str]
            How to combine the samples in each bucket. `last` (default) returns the latest reading — the right answer for a snapshot such as storage. `max` returns the highest reading, which is what a sampled level series needs: peak concurrent realtime connections is the max of `realtime.connections` over the window.
        Returns
        -------
        UsageGaugeList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/usage/gauges'
        api_params = {}
        if metrics is None:
            raise AppwriteException('Missing required parameter: "metrics"')
        api_params['metrics'] = self._normalize_value(metrics)
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if interval is not None:
            api_params['interval'] = self._normalize_value(interval)
        if dimensions is not None:
            api_params['dimensions'] = self._normalize_value(dimensions)
        if start_at is not None:
            api_params['startAt'] = self._normalize_value(start_at)
        if end_at is not None:
            api_params['endAt'] = self._normalize_value(end_at)
        if order_by is not None:
            api_params['orderBy'] = self._normalize_value(order_by)
        if order_dir is not None:
            api_params['orderDir'] = self._normalize_value(order_dir)
        if limit is not None:
            api_params['limit'] = self._normalize_value(limit)
        if offset is not None:
            api_params['offset'] = self._normalize_value(offset)
        if aggregate is not None:
            api_params['aggregate'] = self._normalize_value(aggregate)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=UsageGaugeList)

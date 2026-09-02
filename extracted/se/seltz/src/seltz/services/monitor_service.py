"""Monitor CRUD and the two read cursors, over the generated gRPC stubs."""

# The enum types are EnumTypeWrapper instances at runtime, not classes, so the
# annotations naming them must not be evaluated.
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, AsyncIterator, Iterable, Iterator, List, Union

import grpc
from grpc import aio

from .._types import OMIT, Omit, is_given
from ..exceptions import map_rpc_error
from . import DEFAULT_TIMEOUT_SECONDS, MonitorStatus, SearchRequest, SortOrder, Webhook
from seltz_public_api.proto.v1 import monitor_pb2, monitor_pb2_grpc

SearchRequestInput = Union[str, Mapping[str, Any], SearchRequest]
WebhookInput = Union[Webhook, Mapping[str, Any]]

# The fields of SearchRequest, less `api_key`. A monitor stores its search
# requests and replays them for months, so a key in one would be a credential
# written to the database; the server refuses the field rather than clearing
# it, and rejecting here keeps the key off the wire entirely.
_SEARCH_REQUEST_FIELDS = frozenset(SearchRequest.DESCRIPTOR.fields_by_name) - {
    "api_key"
}


def _search_requests(queries: Iterable[SearchRequestInput]) -> List[SearchRequest]:
    """Accept a bare query string, a mapping of SearchService.search()'s keyword
    arguments, or an already-built SearchRequest."""
    built = []
    for query in queries:
        if isinstance(query, str):
            built.append(SearchRequest(query=query))
        elif isinstance(query, Mapping):
            unexpected = sorted(set(query) - _SEARCH_REQUEST_FIELDS)
            if unexpected:
                raise TypeError(f"unexpected search request fields: {unexpected}")
            built.append(SearchRequest(**query))
        else:
            built.append(query)
    return built


def _webhook(webhook: WebhookInput) -> Webhook:
    if isinstance(webhook, Mapping):
        return Webhook(**webhook)
    return webhook


# Request builders, shared by the synchronous and asynchronous services.
#
# The two services cannot share method bodies. An aio stub returns an awaitable
# rather than a response, so any body that reads a field off the result, or that
# catches `grpc.RpcError` around the call, is wrong on the async side: the field
# access raises AttributeError before the RPC completes, and the error surfaces
# at the await, outside the except. Only the request shape is common, so only
# the request shape is shared.


def _create_request(
    api_key: str,
    name: str,
    cadence: str,
    search_requests: Iterable[SearchRequestInput],
    webhook: Union[WebhookInput, None, Omit],
    status: Union[MonitorStatus, None, Omit],
) -> Any:
    return monitor_pb2.CreateMonitorRequest(
        api_key=api_key,
        name=name,
        cadence=cadence,
        search_requests=_search_requests(search_requests),
        webhook=(
            _webhook(webhook) if is_given(webhook) and webhook is not None else None
        ),
        status=status if is_given(status) and status is not None else None,
    )


def _get_request(api_key: str, monitor_id: str) -> Any:
    return monitor_pb2.GetMonitorRequest(api_key=api_key, monitor_id=monitor_id)


def _list_request(
    api_key: str,
    name: Union[str, None, Omit],
    status: Union[MonitorStatus, None, Omit],
    since: Union[str, None, Omit],
    before: Union[str, None, Omit],
    limit: Union[int, None, Omit],
) -> Any:
    request = monitor_pb2.ListMonitorsRequest(api_key=api_key)
    if is_given(name) and name is not None:
        request.name = name
    if is_given(status) and status is not None:
        request.status = status
    if is_given(since) and since is not None:
        request.since = since
    if is_given(before) and before is not None:
        request.before = before
    if is_given(limit) and limit is not None:
        request.limit = limit
    return request


def _update_request(
    api_key: str,
    monitor_id: str,
    name: Union[str, None, Omit],
    status: Union[MonitorStatus, None, Omit],
    cadence: Union[str, None, Omit],
    search_requests: Union[Iterable[SearchRequestInput], None, Omit],
    webhook: Union[WebhookInput, None, Omit],
) -> Any:
    request = monitor_pb2.UpdateMonitorRequest(api_key=api_key, monitor_id=monitor_id)
    if is_given(name) and name is not None:
        request.name = name
    if is_given(status) and status is not None:
        request.status = status
    if is_given(cadence) and cadence is not None:
        request.cadence = cadence
    if is_given(search_requests) and search_requests is not None:
        built = _search_requests(search_requests)
        # An empty repeated field is indistinguishable from an absent one on the
        # wire, so the server reads it as "keep the existing list" and the call
        # succeeds having changed nothing. A monitor cannot hold zero search
        # requests -- create rejects that -- so an empty list is always a
        # mistake, and the server has no way to say so.
        if not built:
            raise ValueError(
                "search_requests must not be empty: pass at least one request to "
                "replace the list, or omit the argument to keep it"
            )
        request.search_requests.extend(built)
    if is_given(webhook):
        if webhook is None:
            # Present but empty is what clears it. Leaving the field unset would
            # keep the existing webhook, and passing None straight to protobuf
            # produces exactly that -- the same bytes as omitting the argument.
            request.webhook.SetInParent()
        else:
            request.webhook.CopyFrom(_webhook(webhook))
    return request


def _delete_request(api_key: str, monitor_id: str) -> Any:
    return monitor_pb2.DeleteMonitorRequest(api_key=api_key, monitor_id=monitor_id)


def _list_runs_request(
    api_key: str,
    monitor_id: str,
    since: Union[int, None, Omit],
    before: Union[int, None, Omit],
    limit: Union[int, None, Omit],
    sort: Union[SortOrder, None, Omit],
) -> Any:
    request = monitor_pb2.ListRunsRequest(api_key=api_key, monitor_id=monitor_id)
    if is_given(since) and since is not None:
        request.since = since
    if is_given(before) and before is not None:
        request.before = before
    if is_given(limit) and limit is not None:
        request.limit = limit
    if is_given(sort) and sort is not None:
        request.sort = sort
    return request


def _get_run_request(api_key: str, monitor_id: str, run_id: int) -> Any:
    return monitor_pb2.GetRunRequest(
        api_key=api_key, monitor_id=monitor_id, run_id=run_id
    )


def _list_run_requests_request(api_key: str, monitor_id: str, run_id: int) -> Any:
    return monitor_pb2.ListRunRequestsRequest(
        api_key=api_key, monitor_id=monitor_id, run_id=run_id
    )


def _list_records_request(
    api_key: str,
    monitor_id: str,
    since: Union[int, None, Omit],
    before: Union[int, None, Omit],
    limit: Union[int, None, Omit],
    include_content: Union[bool, None, Omit],
) -> Any:
    request = monitor_pb2.ListRecordsRequest(api_key=api_key, monitor_id=monitor_id)
    if is_given(since) and since is not None:
        request.since = since
    if is_given(before) and before is not None:
        request.before = before
    if is_given(limit) and limit is not None:
        request.limit = limit
    if is_given(include_content) and include_content is not None:
        request.include_content = include_content
    return request


def _list_run_records_request(
    api_key: str,
    monitor_id: str,
    run_id: int,
    since: Union[int, None, Omit],
    before: Union[int, None, Omit],
    limit: Union[int, None, Omit],
    include_content: Union[bool, None, Omit],
) -> Any:
    request = monitor_pb2.ListRunRecordsRequest(
        api_key=api_key, monitor_id=monitor_id, run_id=run_id
    )
    if is_given(since) and since is not None:
        request.since = since
    if is_given(before) and before is not None:
        request.before = before
    if is_given(limit) and limit is not None:
        request.limit = limit
    if is_given(include_content) and include_content is not None:
        request.include_content = include_content
    return request


def _stream_records_request(
    api_key: str, monitor_id: str, since: Union[int, None, Omit]
) -> Any:
    request = monitor_pb2.StreamRecordsRequest(api_key=api_key, monitor_id=monitor_id)
    if is_given(since) and since is not None:
        request.since = since
    return request


class MonitorService:
    """Synchronous monitor operations."""

    def __init__(self, channel: grpc.Channel, api_key: str):
        self._stub = monitor_pb2_grpc.MonitorServiceStub(channel)
        self._api_key = api_key

    def create(
        self,
        name: str,
        *,
        cadence: str,
        search_requests: Iterable[SearchRequestInput],
        webhook: Union[WebhookInput, None, Omit] = OMIT,
        status: Union[MonitorStatus, None, Omit] = OMIT,
    ) -> monitor_pb2.CreateMonitorResponse:
        """Create a monitor. Returns the CreateMonitorResponse."""
        request = _create_request(
            self._api_key, name, cadence, search_requests, webhook, status
        )
        try:
            return self._stub.CreateMonitor(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def get(self, monitor_id: str) -> monitor_pb2.GetMonitorResponse:
        """Read one monitor. Returns the GetMonitorResponse, which carries the
        monitor and its run_state."""
        request = _get_request(self._api_key, monitor_id)
        try:
            return self._stub.GetMonitor(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def list(
        self,
        *,
        name: Union[str, None, Omit] = OMIT,
        status: Union[MonitorStatus, None, Omit] = OMIT,
        since: Union[str, None, Omit] = OMIT,
        before: Union[str, None, Omit] = OMIT,
        limit: Union[int, None, Omit] = OMIT,
    ) -> monitor_pb2.ListMonitorsResponse:
        """A page of this org's live monitors, newest first. Filter by exact
        name, never by position. `since` and `before` are exclusive bounds
        naming a monitor_id; page forward with before = monitors[-1].monitor_id
        while the response's has_more is set."""
        request = _list_request(self._api_key, name, status, since, before, limit)
        try:
            return self._stub.ListMonitors(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def update(
        self,
        monitor_id: str,
        *,
        name: Union[str, None, Omit] = OMIT,
        status: Union[MonitorStatus, None, Omit] = OMIT,
        cadence: Union[str, None, Omit] = OMIT,
        search_requests: Union[Iterable[SearchRequestInput], None, Omit] = OMIT,
        webhook: Union[WebhookInput, None, Omit] = OMIT,
    ) -> monitor_pb2.UpdateMonitorResponse:
        """Edit a monitor. Returns the UpdateMonitorResponse."""
        request = _update_request(
            self._api_key,
            monitor_id,
            name,
            status,
            cadence,
            search_requests,
            webhook,
        )
        try:
            return self._stub.UpdateMonitor(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def delete(self, monitor_id: str) -> monitor_pb2.DeleteMonitorResponse:
        """Soft-delete a monitor. Every record becomes invisible at once.
        Returns the DeleteMonitorResponse."""
        request = _delete_request(self._api_key, monitor_id)
        try:
            return self._stub.DeleteMonitor(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def list_runs(
        self,
        monitor_id: str,
        *,
        since: Union[int, None, Omit] = OMIT,
        before: Union[int, None, Omit] = OMIT,
        limit: Union[int, None, Omit] = OMIT,
        sort: Union[SortOrder, None, Omit] = OMIT,
    ) -> monitor_pb2.ListRunsResponse:
        """A page of runs, newest first, so runs[0] is the latest. `since` and
        `before` are exclusive bounds naming a run_id; page back with
        before = runs[-1].run_id while the response's has_more is set.

        Pass `sort=SortOrder.SORT_ORDER_ASC` to walk forward from the oldest
        instead. Under that order `since` is the cursor, not `before`."""
        request = _list_runs_request(
            self._api_key, monitor_id, since, before, limit, sort
        )
        try:
            return self._stub.ListRuns(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def get_run(self, monitor_id: str, run_id: int) -> monitor_pb2.GetRunResponse:
        """One run: its status, its counts and its record range.
        Returns the GetRunResponse."""
        request = _get_run_request(self._api_key, monitor_id, run_id)
        try:
            return self._stub.GetRun(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def list_run_requests(
        self, monitor_id: str, run_id: int
    ) -> monitor_pb2.ListRunRequestsResponse:
        """That run's per-request outcomes. Returns the
        ListRunRequestsResponse.

        Where a caller separates "this query returned less this run" into a
        failure and a run with genuinely nothing new: requests_failed on the
        run says how many, and this says which.

        Unpaginated, and never a page: one entry per search request on the
        config the run executed."""
        request = _list_run_requests_request(self._api_key, monitor_id, run_id)
        try:
            return self._stub.ListRunRequests(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def list_records(
        self,
        monitor_id: str,
        *,
        since: Union[int, None, Omit] = OMIT,
        before: Union[int, None, Omit] = OMIT,
        limit: Union[int, None, Omit] = OMIT,
        include_content: Union[bool, None, Omit] = OMIT,
    ) -> monitor_pb2.ListRecordsResponse:
        """A page of records, oldest first. `since` is exclusive, so resume is
        safe: pass back the last record_id you handled."""
        request = _list_records_request(
            self._api_key, monitor_id, since, before, limit, include_content
        )
        try:
            return self._stub.ListRecords(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def list_run_records(
        self,
        monitor_id: str,
        run_id: int,
        *,
        since: Union[int, None, Omit] = OMIT,
        before: Union[int, None, Omit] = OMIT,
        limit: Union[int, None, Omit] = OMIT,
        include_content: Union[bool, None, Omit] = OMIT,
    ) -> monitor_pb2.ListRunRecordsResponse:
        """That run's records. Exists so no consumer does arithmetic on a record
        id: the range on a run is a bound, not a dense sequence.

        `since` and `before` are exclusive bounds on `record_id`, exactly as on
        `list_records`. A first run has no dedup history behind it, so it is the
        largest run a monitor will ever produce and the one most likely to
        exceed a page."""
        request = _list_run_records_request(
            self._api_key, monitor_id, run_id, since, before, limit, include_content
        )
        try:
            return self._stub.ListRunRecords(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def stream_records(
        self, monitor_id: str, *, since: Union[int, None, Omit] = OMIT
    ) -> Iterator[monitor_pb2.StreamRecordsResponse]:
        """Live-tail, yielding StreamRecordsResponse. Best-effort push over a
        durable pull: a dropped stream is recovered by resuming
        `list_records(since=...)` with the last id seen."""
        request = _stream_records_request(self._api_key, monitor_id, since)
        try:
            for response in self._stub.StreamRecords(request):
                yield response
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error


class AsyncMonitorService(MonitorService):
    """Asynchronous monitor operations.

    Every method awaits the RPC inside its own try, so a failure raises the same
    Seltz exception the synchronous twin raises. `stream_records` is an async
    generator and is consumed with `async for`.
    """

    def __init__(self, channel: aio.Channel, api_key: str):
        self._stub = monitor_pb2_grpc.MonitorServiceStub(channel)
        self._api_key = api_key

    async def create(  # type: ignore[override]
        self,
        name: str,
        *,
        cadence: str,
        search_requests: Iterable[SearchRequestInput],
        webhook: Union[WebhookInput, None, Omit] = OMIT,
        status: Union[MonitorStatus, None, Omit] = OMIT,
    ) -> monitor_pb2.CreateMonitorResponse:
        """Create a monitor. Returns the CreateMonitorResponse."""
        request = _create_request(
            self._api_key, name, cadence, search_requests, webhook, status
        )
        try:
            return await self._stub.CreateMonitor(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def get(self, monitor_id: str) -> monitor_pb2.GetMonitorResponse:  # type: ignore[override]
        """Read one monitor. Returns the GetMonitorResponse, which carries the
        monitor and its run_state."""
        request = _get_request(self._api_key, monitor_id)
        try:
            return await self._stub.GetMonitor(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def list(  # type: ignore[override]
        self,
        *,
        name: Union[str, None, Omit] = OMIT,
        status: Union[MonitorStatus, None, Omit] = OMIT,
        since: Union[str, None, Omit] = OMIT,
        before: Union[str, None, Omit] = OMIT,
        limit: Union[int, None, Omit] = OMIT,
    ) -> monitor_pb2.ListMonitorsResponse:
        """A page of this org's live monitors, newest first."""
        request = _list_request(self._api_key, name, status, since, before, limit)
        try:
            return await self._stub.ListMonitors(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def update(  # type: ignore[override]
        self,
        monitor_id: str,
        *,
        name: Union[str, None, Omit] = OMIT,
        status: Union[MonitorStatus, None, Omit] = OMIT,
        cadence: Union[str, None, Omit] = OMIT,
        search_requests: Union[Iterable[SearchRequestInput], None, Omit] = OMIT,
        webhook: Union[WebhookInput, None, Omit] = OMIT,
    ) -> monitor_pb2.UpdateMonitorResponse:
        """Edit a monitor. Returns the UpdateMonitorResponse."""
        request = _update_request(
            self._api_key,
            monitor_id,
            name,
            status,
            cadence,
            search_requests,
            webhook,
        )
        try:
            return await self._stub.UpdateMonitor(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def delete(self, monitor_id: str) -> monitor_pb2.DeleteMonitorResponse:  # type: ignore[override]
        """Soft-delete a monitor. Returns the DeleteMonitorResponse."""
        request = _delete_request(self._api_key, monitor_id)
        try:
            return await self._stub.DeleteMonitor(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def list_runs(  # type: ignore[override]
        self,
        monitor_id: str,
        *,
        since: Union[int, None, Omit] = OMIT,
        before: Union[int, None, Omit] = OMIT,
        limit: Union[int, None, Omit] = OMIT,
        sort: Union[SortOrder, None, Omit] = OMIT,
    ) -> monitor_pb2.ListRunsResponse:
        """A page of runs, newest first."""
        request = _list_runs_request(
            self._api_key, monitor_id, since, before, limit, sort
        )
        try:
            return await self._stub.ListRuns(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def get_run(self, monitor_id: str, run_id: int) -> monitor_pb2.GetRunResponse:  # type: ignore[override]
        """One run. Returns the GetRunResponse."""
        request = _get_run_request(self._api_key, monitor_id, run_id)
        try:
            return await self._stub.GetRun(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def list_run_requests(  # type: ignore[override]
        self, monitor_id: str, run_id: int
    ) -> monitor_pb2.ListRunRequestsResponse:
        """That run's per-request outcomes."""
        request = _list_run_requests_request(self._api_key, monitor_id, run_id)
        try:
            return await self._stub.ListRunRequests(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def list_records(  # type: ignore[override]
        self,
        monitor_id: str,
        *,
        since: Union[int, None, Omit] = OMIT,
        before: Union[int, None, Omit] = OMIT,
        limit: Union[int, None, Omit] = OMIT,
        include_content: Union[bool, None, Omit] = OMIT,
    ) -> monitor_pb2.ListRecordsResponse:
        """A page of records, oldest first."""
        request = _list_records_request(
            self._api_key, monitor_id, since, before, limit, include_content
        )
        try:
            return await self._stub.ListRecords(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def list_run_records(  # type: ignore[override]
        self,
        monitor_id: str,
        run_id: int,
        *,
        since: Union[int, None, Omit] = OMIT,
        before: Union[int, None, Omit] = OMIT,
        limit: Union[int, None, Omit] = OMIT,
        include_content: Union[bool, None, Omit] = OMIT,
    ) -> monitor_pb2.ListRunRecordsResponse:
        """That run's records."""
        request = _list_run_records_request(
            self._api_key, monitor_id, run_id, since, before, limit, include_content
        )
        try:
            return await self._stub.ListRunRecords(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def stream_records(  # type: ignore[override]
        self, monitor_id: str, *, since: Union[int, None, Omit] = OMIT
    ) -> AsyncIterator[monitor_pb2.StreamRecordsResponse]:
        """Live-tail, yielding StreamRecordsResponse, consumed with `async
        for`."""
        request = _stream_records_request(self._api_key, monitor_id, since)
        try:
            async for response in self._stub.StreamRecords(request):
                yield response
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

from __future__ import annotations

import abc
import collections
import threading
import time
import typing as t
import uuid

import grpc
from query_cache_common.constants import (
    CLOUD_RUN_ID_HEADER,
    INVOCATION_ID_HEADER,
    ORG_ID_HEADER,
    OS_NAME_HEADER,
    REQUEST_ID_HEADER,
    SESSION_ID_HEADER,
    SUBMITTED_AT_EPOCH_HEADER,
    SYSTEM_USER_ID_HEADER,
)
from query_cache_common.utils import current_epoch_millis
from typing_extensions import override

from dbt_state import events


class _ClientCallDetails(
    collections.namedtuple(
        "_ClientCallDetails",
        ("method", "timeout", "metadata", "credentials", "wait_for_ready", "compression"),
    ),
    grpc.ClientCallDetails,
):
    pass


class RpcErrorWithRequestId(grpc.RpcError):
    """A grpc.RpcError proxy that prefixes details/str() with request_id."""

    def __init__(self, original: grpc.RpcError, request_id: str) -> None:
        super().__init__()
        self._original = original
        self.request_id = request_id

    def code(self) -> grpc.StatusCode:
        return self._original.code()

    def details(self) -> str:
        try:
            base = self._original.details() or ""
        except Exception:
            base = ""
        prefix = f"[request_id={self.request_id}]"
        return f"{prefix} {base}".rstrip()

    def __str__(self) -> str:
        return f"dbt State: {self.details()}"

    def __getattr__(self, name: str) -> t.Any:
        return getattr(self._original, name)


class _CallIteratorProxy:
    """Proxy for objects that are both Call and iterator (unary-stream, stream-stream)."""

    def __init__(self, call_iter: t.Any, request_id: str) -> None:
        self._call_iter = call_iter
        self._rid = request_id

    def __iter__(self) -> _CallIteratorProxy:
        return self

    def __next__(self) -> t.Any:
        try:
            return next(self._call_iter)
        except grpc.RpcError as e:
            raise RpcErrorWithRequestId(e, self._rid) from e

    def __getattr__(self, name: str) -> t.Any:
        return getattr(self._call_iter, name)


class _CallFutureProxy:
    """Proxy for objects that are both Call and Future (stream-unary)."""

    def __init__(self, call_future: t.Any, request_id: str) -> None:
        self._call_future = call_future
        self._rid = request_id

    def result(self, timeout: t.Optional[float] = None) -> t.Any:
        try:
            return self._call_future.result(timeout)
        except grpc.RpcError as e:
            raise RpcErrorWithRequestId(e, self._rid) from e

    def exception(self, timeout: t.Optional[float] = None) -> t.Optional[BaseException]:
        exc = self._call_future.exception(timeout=timeout)
        if isinstance(exc, grpc.RpcError):
            return RpcErrorWithRequestId(exc, self._rid)
        return exc

    def __getattr__(self, name: str) -> t.Any:
        return getattr(self._call_future, name)


class _MetadataModifyingInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
    abc.ABC,
):
    @abc.abstractmethod
    def _modify_metadata(self, metadata: t.List[t.Tuple[str, t.Any]]) -> None: ...

    def _add_metadata(
        self,
        client_call_details: grpc.ClientCallDetails,
    ) -> grpc.ClientCallDetails:
        metadata = list(client_call_details.metadata or [])
        self._modify_metadata(metadata)
        return _ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=metadata,
            credentials=client_call_details.credentials,
            wait_for_ready=client_call_details.wait_for_ready,
            compression=client_call_details.compression,
        )

    def intercept_unary_unary(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Any], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request: t.Any,
    ) -> t.Any:
        return continuation(self._add_metadata(client_call_details), request)

    def intercept_unary_stream(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Any], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request: t.Any,
    ) -> t.Any:
        return continuation(self._add_metadata(client_call_details), request)

    def intercept_stream_unary(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Iterator[t.Any]], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request_iterator: t.Iterator[t.Any],
    ) -> t.Any:
        return continuation(self._add_metadata(client_call_details), request_iterator)

    def intercept_stream_stream(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Iterator[t.Any]], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request_iterator: t.Iterator[t.Any],
    ) -> t.Any:
        return continuation(self._add_metadata(client_call_details), request_iterator)


class RequestIdInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    """Client interceptor that adds x-request-id to all gRPC calls and enhances errors."""

    @staticmethod
    def _add_request_id_metadata(
        client_call_details: grpc.ClientCallDetails,
    ) -> t.Tuple[grpc.ClientCallDetails, str]:
        metadata = list(client_call_details.metadata or [])

        # Check if request ID already exists in metadata
        existing_request_id: t.Optional[t.Union[str, bytes]] = next(
            (v for k, v in metadata if k.lower() == REQUEST_ID_HEADER), None
        )

        if existing_request_id:
            # Ensure request_id is a string
            if isinstance(existing_request_id, bytes):
                request_id = existing_request_id.decode("utf-8")
            else:
                request_id = existing_request_id
        else:
            request_id = uuid.uuid4().hex
            metadata.append((REQUEST_ID_HEADER, request_id))

        new_details = _ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=metadata,
            credentials=client_call_details.credentials,
            wait_for_ready=client_call_details.wait_for_ready,
            compression=client_call_details.compression,
        )
        return new_details, request_id

    def intercept_unary_unary(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Any], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request: t.Any,
    ) -> t.Any:
        new_details, rid = self._add_request_id_metadata(client_call_details)
        call = continuation(new_details, request)
        return _CallFutureProxy(call, rid)

    def intercept_unary_stream(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Any], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request: t.Any,
    ) -> t.Any:
        new_details, rid = self._add_request_id_metadata(client_call_details)
        call_iter = continuation(new_details, request)
        return _CallIteratorProxy(call_iter, rid)

    def intercept_stream_unary(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Iterator[t.Any]], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request_iterator: t.Iterator[t.Any],
    ) -> t.Any:
        new_details, rid = self._add_request_id_metadata(client_call_details)
        call_future = continuation(new_details, request_iterator)
        return _CallFutureProxy(call_future, rid)

    def intercept_stream_stream(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Iterator[t.Any]], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request_iterator: t.Iterator[t.Any],
    ) -> t.Any:
        new_details, rid = self._add_request_id_metadata(client_call_details)
        call_iter = continuation(new_details, request_iterator)
        return _CallIteratorProxy(call_iter, rid)


class SessionIdInterceptor(_MetadataModifyingInterceptor):
    """Client interceptor that adds x-session-id to all gRPC calls.

    The session_id is generated once per client lifetime and persists across all requests,
    allowing tracking of a full dbt run.
    """

    def __init__(self, session_id: t.Optional[str] = None) -> None:
        self._session_id = session_id or uuid.uuid4().hex

    def _modify_metadata(self, metadata: t.List[t.Tuple[str, t.Any]]) -> None:
        metadata.append((SESSION_ID_HEADER, self._session_id))


class SubmittedAtEpochInterceptor(_MetadataModifyingInterceptor):
    """Client interceptor that adds x-submitted-at-epoch to all gRPC calls.

    The epoch is generated fresh for each request (milliseconds since Unix epoch).
    """

    @override
    def _modify_metadata(self, metadata: t.List[t.Tuple[str, t.Any]]) -> None:
        metadata.append((SUBMITTED_AT_EPOCH_HEADER, str(current_epoch_millis())))


class OrgIdInterceptor(_MetadataModifyingInterceptor):
    """Client interceptor that adds x-organization-id to all gRPC calls."""

    def __init__(self, org_id: str) -> None:
        if not org_id:
            raise ValueError("org_id cannot be empty")
        self._org_id = org_id

    def _modify_metadata(self, metadata: t.List[t.Tuple[str, t.Any]]) -> None:
        metadata.append((ORG_ID_HEADER, self._org_id))


class SystemInfoInterceptor(_MetadataModifyingInterceptor):
    """Client interceptor that adds x-system-user-id and x-os-name to all gRPC calls."""

    def __init__(self, system_user_id: str = "", os_name: str = "") -> None:
        self._system_user_id = system_user_id
        self._os_name = os_name

    def _modify_metadata(self, metadata: t.List[t.Tuple[str, t.Any]]) -> None:
        metadata.append((SYSTEM_USER_ID_HEADER, self._system_user_id))
        metadata.append((OS_NAME_HEADER, self._os_name))


class InvocationInfoInterceptor(_MetadataModifyingInterceptor):
    """Client interceptor that adds x-dbt-invocation-id and x-dbt-cloud-run-id to all gRPC calls.

    Both identifiers are constant for the lifetime of a single dbt invocation. The
    invocation_id is dbt's per-run UUID; the cloud_run_id is only present when running
    on the dbt platform (from the DBT_CLOUD_RUN_ID environment variable) and is omitted
    otherwise.
    """

    def __init__(self, invocation_id: str = "", cloud_run_id: str = "") -> None:
        self._invocation_id = invocation_id
        self._cloud_run_id = cloud_run_id

    def _modify_metadata(self, metadata: t.List[t.Tuple[str, t.Any]]) -> None:
        if self._invocation_id:
            metadata.append((INVOCATION_ID_HEADER, self._invocation_id))
        if self._cloud_run_id:
            metadata.append((CLOUD_RUN_ID_HEADER, self._cloud_run_id))


class ServerUnavailableError(grpc.RpcError):
    """Raised by QueryCacheGrpcClient for every RPC once ServerUnavailableInterceptor has marked
    the server unavailable.

    Subclasses grpc.RpcError so existing `except grpc.RpcError` handlers treat it as any other
    server failure.
    """

    def code(self) -> grpc.StatusCode:  # noqa: PLR6301
        return grpc.StatusCode.UNAVAILABLE

    def details(self) -> str:  # noqa: PLR6301
        return "dbt State disabled for the rest of this run"

    def __str__(self) -> str:
        return f"dbt State: {self.details()}"


COUNTED_STATUS_CODES = frozenset(
    {
        grpc.StatusCode.DEADLINE_EXCEEDED,
        grpc.StatusCode.UNAVAILABLE,
        grpc.StatusCode.UNAUTHENTICATED,
    }
)
"""Status codes that count toward marking the server unavailable: it can't be reached or
authenticated"""


class ServerUnavailableInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Marks the server unavailable for the rest of the run after repeated failed requests.

    It only tracks failures; QueryCacheGrpcClient checks is_server_available before each RPC and
    fails it immediately. It must come after RequestIdInterceptor so it sees grpc's own call
    rather than RequestIdInterceptor's wrapped error.

    A one-way circuit breaker: it never marks the server available again within the run (no
    half-open probing).

    Counts failures with a code in COUNTED_STATUS_CODES; overlapping failures count once. Marks
    the server unavailable once max_consecutive_failures are counted over at least
    min_failure_span_seconds. A success resets the count; other errors are ignored.
    """

    def __init__(
        self,
        max_consecutive_failures: int,
        min_failure_span_seconds: float,
    ) -> None:
        """
        Args:
            max_consecutive_failures: Counted failures after which the server is marked
                unavailable. A value of 0 or less never marks it unavailable.
            min_failure_span_seconds: How long counted failures must keep happening, from the
                start of the first one, before the server is marked unavailable.
        """
        self._max_consecutive_failures = max_consecutive_failures
        self._min_failure_span_seconds = min_failure_span_seconds
        self._lock = threading.Lock()
        self._consecutive_failures = 0
        self._last_counted_failure_end = float("-inf")
        self._first_counted_failure_start = 0.0
        self._is_server_available = True

    @property
    def is_server_available(self) -> bool:
        """Whether the server is still considered available. Once marked unavailable, it stays
        False for the rest of the run."""
        return self._is_server_available

    def intercept_unary_unary(
        self,
        continuation: t.Callable[[grpc.ClientCallDetails, t.Any], t.Any],
        client_call_details: grpc.ClientCallDetails,
        request: t.Any,
    ) -> t.Any:
        started = time.monotonic()
        call = continuation(client_call_details, request)
        exc = call.exception()
        ended = time.monotonic()

        # continuation returns non-gRPC exceptions as-is, and they have no code()
        code = exc.code() if isinstance(exc, grpc.RpcError) else None

        unavailable_after: t.Optional[int] = None
        with self._lock:
            if exc is None:
                self._consecutive_failures = 0
            elif (
                code in COUNTED_STATUS_CODES
                # a call that started before the last counted failure ended overlapped it
                and started >= self._last_counted_failure_end
            ):
                if self._consecutive_failures == 0:
                    self._first_counted_failure_start = started
                self._consecutive_failures += 1
                self._last_counted_failure_end = ended
                if (
                    0 < self._max_consecutive_failures <= self._consecutive_failures
                    and ended - self._first_counted_failure_start >= self._min_failure_span_seconds
                    and self._is_server_available
                ):
                    self._is_server_available = False
                    unavailable_after = self._consecutive_failures

        # fired outside the lock so other gRPC threads don't wait on dbt's event system
        if unavailable_after is not None and code is not None:
            events.fire_warn_event_with_cache_bypass(
                "dbt State disabled for the rest of this run after {} consecutive failed "
                "requests to the dbt State API (last error: {})",
                str(unavailable_after),
                code.name,
            )

        return call

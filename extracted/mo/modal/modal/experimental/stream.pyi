import collections.abc
import datetime
import modal.client
import modal.exception
import modal.sandbox._sandbox
import modal.sandbox.sandbox
import synchronicity
import typing
import typing_extensions

class StreamInfo:
    """A Stream's state: `last_seq` is the sequence number of its latest entry, or 0 while it is empty."""

    name: str
    last_seq: int
    sealed: bool
    created_at: datetime.datetime
    last_written_at: datetime.datetime
    expires_at: typing.Optional[datetime.datetime]

    def __init__(
        self,
        name: str,
        last_seq: int,
        sealed: bool,
        created_at: datetime.datetime,
        last_written_at: datetime.datetime,
        expires_at: typing.Optional[datetime.datetime],
    ) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

    def __setattr__(self, name, value):
        """Implement setattr(self, name, value)."""
        ...

    def __delattr__(self, name):
        """Implement delattr(self, name)."""
        ...

    def __hash__(self):
        """Return hash(self)."""
        ...

class AppendResult:
    """Where an appended value landed; `deduped` when its idempotency key had already been written."""

    seq: int
    deduped: bool

    def __init__(self, seq: int, deduped: bool) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

    def __setattr__(self, name, value):
        """Implement setattr(self, name, value)."""
        ...

    def __delattr__(self, name):
        """Implement delattr(self, name)."""
        ...

    def __hash__(self):
        """Return hash(self)."""
        ...

class Entry:
    """One entry read from a Stream: a value, or the final `seal` entry."""

    seq: int
    idempotency_key: str
    kind: typing.Literal["value", "seal"]
    value: typing.Any
    ts: datetime.datetime

    def __init__(
        self,
        seq: int,
        idempotency_key: str,
        kind: typing.Literal["value", "seal"],
        value: typing.Any,
        ts: datetime.datetime,
    ) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

    def __setattr__(self, name, value):
        """Implement setattr(self, name, value)."""
        ...

    def __delattr__(self, name):
        """Implement delattr(self, name)."""
        ...

    def __hash__(self):
        """Return hash(self)."""
        ...

class StreamToken:
    """An access token for one Stream, for use with `Stream.from_token` until `expires_at`."""

    token: str
    expires_at: datetime.datetime

    def __init__(self, token: str, expires_at: datetime.datetime) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

    def __setattr__(self, name, value):
        """Implement setattr(self, name, value)."""
        ...

    def __delattr__(self, name):
        """Implement delattr(self, name)."""
        ...

    def __hash__(self):
        """Return hash(self)."""
        ...

class IdempotencyConflict(modal.exception.ConflictError):
    """An idempotency key was reused with a different value; `seq` is where the original value landed."""

    idempotency_key: typing.Optional[str]
    seq: typing.Optional[int]

    def __init__(self, message: str, *, idempotency_key: typing.Optional[str], seq: typing.Optional[int]):
        """mdmd:hidden"""
        ...

class _Transient(modal.exception.ServiceError):
    """Raised when an error occurs in basic client/server communication."""

    ...

class _Fenced(modal.exception.ConflictError):
    """Raised when a resource conflict occurs between the request and current system state."""

    ...

def _service_url() -> str: ...
def _backoff(attempt: int) -> float: ...
def _check_name(name: str) -> None: ...
def _check_retention(retention: typing.Optional[datetime.timedelta]) -> None: ...
def _error_for(status: int, body: bytes, stream_name: str) -> Exception: ...
def _serialize(value: typing.Any) -> bytes: ...
def _identity_token() -> typing.Optional[str]:
    """This container's Modal identity token, if it has one; a token file is reread since it is rewritten
    as the token renews.
    """
    ...

def _entry(event: dict[str, typing.Any]) -> Entry: ...
def _utc(ts_us: int) -> datetime.datetime: ...
def _sse_messages(content: typing.Any) -> collections.abc.AsyncGenerator[tuple[str, str], None]:
    """The (event, data) of each server-sent event; lines are split by hand since values can exceed
    aiohttp's 64 KiB line limit.
    """
    ...

class _StreamManager:
    """Namespace with methods for managing named Streams."""
    async def delete(
        self,
        name: str,
        *,
        allow_missing: bool = False,
        environment_name: typing.Optional[str] = None,
        client: typing.Optional[modal.client._Client] = None,
    ) -> None:
        """Delete a named Stream and all of its entries.

        Deletion is irreversible; handles to the Stream then raise `NotFoundError`.

        Args:
            name: Name of the Stream to delete.
            allow_missing: If True, do nothing when the Stream does not exist.
            environment_name: Environment to delete from; defaults to the active environment.
            client: Modal client to use; defaults to `Client.from_env()` when omitted.

        Examples:
            ```python notest
            modal.experimental.Stream.objects.delete("my-stream")
            ```
        """
        ...

class StreamManager:
    """Namespace with methods for managing named Streams."""
    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    class __delete_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            name: str,
            *,
            allow_missing: bool = False,
            environment_name: typing.Optional[str] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> None:
            """Delete a named Stream and all of its entries.

            Deletion is irreversible; handles to the Stream then raise `NotFoundError`.

            Args:
                name: Name of the Stream to delete.
                allow_missing: If True, do nothing when the Stream does not exist.
                environment_name: Environment to delete from; defaults to the active environment.
                client: Modal client to use; defaults to `Client.from_env()` when omitted.

            Examples:
                ```python notest
                modal.experimental.Stream.objects.delete("my-stream")
                ```
            """
            ...

        async def aio(
            self,
            /,
            name: str,
            *,
            allow_missing: bool = False,
            environment_name: typing.Optional[str] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> None:
            """Delete a named Stream and all of its entries.

            Deletion is irreversible; handles to the Stream then raise `NotFoundError`.

            Args:
                name: Name of the Stream to delete.
                allow_missing: If True, do nothing when the Stream does not exist.
                environment_name: Environment to delete from; defaults to the active environment.
                client: Modal client to use; defaults to `Client.from_env()` when omitted.

            Examples:
                ```python notest
                modal.experimental.Stream.objects.delete("my-stream")
                ```
            """
            ...

    delete: __delete_spec

class _Stream:
    """A named, durable, append-only stream of JSON values.

    Each value gets a dense sequence number starting at 1. Readers can replay a stream from any point
    and follow it for new values until it is sealed. Any number of handles, in any
    process, may append to the same stream.

    Streams are in limited preview: other workspaces get a `PermissionDeniedError`.

    **Usage**

    ```python notest
    import modal

    stream = modal.experimental.Stream.from_name("my-stream", create_if_missing=True)
    stream.append({"role": "user", "content": "hi"}, idempotency_key="turn-1")
    for entry in stream.read(follow=True):
        print(entry.seq, entry.value)
    ```
    """
    def __init__(
        self,
        name: str,
        environment_name: str,
        create_if_missing: bool,
        retention: typing.Optional[datetime.timedelta],
        client: typing.Optional[modal.client._Client],
        token: typing.Optional[str] = None,
    ):
        """mdmd:hidden"""
        ...

    @synchronicity.classproperty
    @classmethod
    def objects(cls) -> _StreamManager: ...
    @staticmethod
    def from_name(
        name: str,
        *,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
        retention: typing.Optional[datetime.timedelta] = None,
        client: typing.Optional[modal.client._Client] = None,
    ) -> _Stream:
        """Reference a Stream by name; nothing is sent until its first use, which creates it if asked.

        `retention` sets how long a stream this call creates is kept after its last write, from one hour
        up to the service's maximum; without it the service's default applies. It has no effect on a
        stream that already exists.
        """
        ...

    @staticmethod
    def from_token(token: str, *, name: str) -> _Stream:
        """Reference the Stream named `name` with an access token from `Stream.create_token`, in place of Modal
        credentials.

        The handle supports the operations the token's access allows until it expires; others raise
        `PermissionDeniedError`, and an expired token raises `AuthError`. A handle inside the Sandbox a
        token was created for (`sandbox=`) instead replaces the expired token with a new one and continues;
        the Sandbox must be created with `include_oidc_identity_token=True`.
        """
        ...

    async def create_token(
        self,
        *,
        access: typing.Literal["read", "write"] = "write",
        ttl: datetime.timedelta = datetime.timedelta(seconds=3600),
        create_if_missing: bool = False,
        retention: typing.Optional[datetime.timedelta] = None,
        sandbox: typing.Optional[modal.sandbox._sandbox._Sandbox] = None,
    ) -> StreamToken:
        """Create an access token for this Stream, for code without Modal credentials such as a Sandbox
        or a browser; see `Stream.from_token`.

        A `read` token can read the stream, and a `write` token can also append to and seal it. The token
        is valid for `ttl`, at most one hour. `create_if_missing` and `retention` create the stream as
        `Stream.from_name` does.

        A token for a `sandbox` keeps working inside that Sandbox beyond `ttl`: a handle from
        `Stream.from_token` there replaces it when it expires, proving it runs in the Sandbox with the
        Sandbox's identity token. The Sandbox must be created with `include_oidc_identity_token=True`.
        """
        ...

    async def _headers(self) -> dict[str, str]: ...
    async def _call(
        self,
        method: str,
        path: str,
        body: typing.Any = None,
        params: typing.Optional[collections.abc.Mapping[str, typing.Any]] = None,
        retry: bool = True,
        headers: typing.Optional[collections.abc.Mapping[str, str]] = None,
        content: typing.Optional[bytes] = None,
        timeout: float = 30.0,
    ) -> tuple[bytes, collections.abc.Mapping[str, str]]:
        """One request to the streams service, or to an absolute `path`, retried on transient failures until
        `RETRY_DEADLINE_S` passes, if `retry`, and once with a refreshed token if its token has expired.
        `headers` replaces the handle's credentials.
        """
        ...

    async def _put_blob(self, data: bytes) -> str:
        """Upload `data` for this stream and return the reference an entry holds in its place."""
        ...

    async def _get_blob(self, ref: str) -> bytes: ...
    async def _transfer(
        self, method: str, url: str, headers: collections.abc.Mapping[str, str], content: typing.Optional[bytes] = None
    ) -> bytes: ...
    async def _payload(self, value: typing.Any) -> dict[str, typing.Any]:
        """The entry fields that carry `value`: the value, or a reference to its upload."""
        ...

    async def _resolve(self, event: dict[str, typing.Any]) -> Entry: ...
    async def _renew(self, stale: str) -> bool:
        """Whether the access token `stale` has been replaced, refreshing it if this handle can; concurrent
        callers share one refresh.
        """
        ...

    async def _refresh(self) -> bool: ...
    def _unreachable(self, exc: Exception) -> Exception: ...
    async def _create_locked(self) -> None:
        """Create the stream on this handle's first request if `create_if_missing` was set; the caller
        holds `_lock`, so concurrent first requests create it once.
        """
        ...

    async def _lease(self) -> int:
        """The lease number this client attaches to its writes. The service rejects a stale one, and since
        this client never takes a new lease, all handles share the current one.
        """
        ...

    async def _write(self, path: str, body: dict[str, typing.Any]) -> dict[str, typing.Any]:
        """A write under the stream's current generation, resent under the new one if it changes."""
        ...

    async def append(self, value: typing.Any, *, idempotency_key: typing.Optional[str] = None) -> AppendResult:
        """Append a JSON-serializable value of at most 1 GiB and return its sequence number. A value over
        64 KiB is uploaded before its entry is written; reads return it like any other.

        Appending again with the same `idempotency_key` and value returns the original result with
        `deduped=True`; the same key with a different value raises `IdempotencyConflict`.
        """
        ...

    async def append_many(
        self,
        values: collections.abc.Iterable[typing.Any],
        *,
        idempotency_keys: typing.Optional[collections.abc.Sequence[str]] = None,
    ) -> list[AppendResult]:
        """Append several values in one request, in order; see `append`. If any key conflicts, none
        of the values is written.
        """
        ...

    async def _append(self, entries: list[tuple[str, dict[str, typing.Any]]]) -> list[AppendResult]: ...
    async def info(self) -> StreamInfo:
        """The stream's latest sequence number, whether it is sealed, and when it was created, last written
        and is due to expire.
        """
        ...

    async def __getitem__(self, seq: int) -> Entry:
        """The entry at sequence number `seq`; raises `IndexError` past the end of the stream. Use `read` for
        a range of entries.
        """
        ...

    def read(self, start: int = 1, *, follow: bool = False) -> collections.abc.AsyncGenerator[Entry, None]:
        """Iterate over the stream's entries from sequence number `start`.

        With `follow=True`, keep waiting for new entries until the stream is sealed, reconnecting after the
        last entry when the connection drops.
        """
        ...

    def _replay(self, start: int) -> collections.abc.AsyncGenerator[Entry, None]: ...
    def _follow(self, start: int) -> collections.abc.AsyncGenerator[Entry, None]: ...
    async def fork(
        self, name: str, *, at: typing.Optional[int] = None, retention: typing.Optional[datetime.timedelta] = None
    ) -> _Stream:
        """Create a Stream named `name` that starts with this stream's entries through sequence number `at`,
        or all of them but a final `seal` by default, and continues independently from there.

        The fork reads those entries from this stream without copying them, and keeps them even if this
        stream is deleted or expires. `retention` applies to the fork as in `Stream.from_name`; without
        it the fork keeps this stream's retention.
        """
        ...

    async def seal(self) -> int:
        """Close the stream to writers and return the sequence number of its final `seal` entry."""
        ...

    def writer(
        self,
        *,
        on_written: typing.Optional[collections.abc.Callable[[str, AppendResult], None]] = None,
        on_conflict: typing.Optional[collections.abc.Callable[[IdempotencyConflict], None]] = None,
    ) -> _StreamWriter:
        """A writer that appends in the background, batching values that arrive while a write is in flight."""
        ...

class _StreamWriter:
    """Appends to a Stream from a background task, in order and in batches.

    `append` queues a value and returns at once, or waits while 1000 values are queued. Do not change a
    value after appending it. Each value written is reported to `on_written` with its idempotency key and
    result, and a reused key with a different value to `on_conflict`. A write that fails after retries, or
    a conflict without an `on_conflict` handler, stops the writer: the error is raised from the next
    `append`, `flush` or `close`, and values still queued are dropped. Use the writer as an async context
    manager or call `close`, so every value is written or the error is raised. Callbacks run on Modal's
    event loop thread, not the caller's, and should return quickly.
    """
    def __init__(
        self,
        stream: _Stream,
        on_written: typing.Optional[collections.abc.Callable[[str, AppendResult], None]],
        on_conflict: typing.Optional[collections.abc.Callable[[IdempotencyConflict], None]],
    ):
        """mdmd:hidden"""
        ...

    async def append(self, value: typing.Any, *, idempotency_key: typing.Optional[str] = None) -> None:
        """Queue a value to be appended; see `Stream.append` for the limits and idempotency. A value over
        64 KiB is uploaded before it is queued.
        """
        ...

    def _try_enqueue(self, payload: dict[str, typing.Any], idempotency_key: typing.Optional[str]) -> bool:
        """Queue the value's entry fields and return True, or return False while the queue is full."""
        ...

    def _start(self) -> None: ...
    async def flush(self) -> None:
        """Wait until every queued value is written."""
        ...

    async def close(self) -> None:
        """Flush and stop the background task; an `append` still waiting for room raises `InvalidError`."""
        ...

    async def __aenter__(self) -> _StreamWriter: ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...
    async def _run(self) -> None: ...
    async def _drain(self) -> None: ...
    async def _write(self, batch: list[tuple[str, dict[str, typing.Any]]]) -> None: ...
    def _report(self, callback: collections.abc.Callable[..., None], *args: typing.Any) -> None: ...

class Stream:
    """A named, durable, append-only stream of JSON values.

    Each value gets a dense sequence number starting at 1. Readers can replay a stream from any point
    and follow it for new values until it is sealed. Any number of handles, in any
    process, may append to the same stream.

    Streams are in limited preview: other workspaces get a `PermissionDeniedError`.

    **Usage**

    ```python notest
    import modal

    stream = modal.experimental.Stream.from_name("my-stream", create_if_missing=True)
    stream.append({"role": "user", "content": "hi"}, idempotency_key="turn-1")
    for entry in stream.read(follow=True):
        print(entry.seq, entry.value)
    ```
    """
    def __init__(
        self,
        name: str,
        environment_name: str,
        create_if_missing: bool,
        retention: typing.Optional[datetime.timedelta],
        client: typing.Optional[modal.client.Client],
        token: typing.Optional[str] = None,
    ):
        """mdmd:hidden"""
        ...

    @synchronicity.classproperty
    @classmethod
    def objects(cls) -> StreamManager: ...
    @staticmethod
    def from_name(
        name: str,
        *,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
        retention: typing.Optional[datetime.timedelta] = None,
        client: typing.Optional[modal.client.Client] = None,
    ) -> Stream:
        """Reference a Stream by name; nothing is sent until its first use, which creates it if asked.

        `retention` sets how long a stream this call creates is kept after its last write, from one hour
        up to the service's maximum; without it the service's default applies. It has no effect on a
        stream that already exists.
        """
        ...

    @staticmethod
    def from_token(token: str, *, name: str) -> Stream:
        """Reference the Stream named `name` with an access token from `Stream.create_token`, in place of Modal
        credentials.

        The handle supports the operations the token's access allows until it expires; others raise
        `PermissionDeniedError`, and an expired token raises `AuthError`. A handle inside the Sandbox a
        token was created for (`sandbox=`) instead replaces the expired token with a new one and continues;
        the Sandbox must be created with `include_oidc_identity_token=True`.
        """
        ...

    class __create_token_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            *,
            access: typing.Literal["read", "write"] = "write",
            ttl: datetime.timedelta = datetime.timedelta(seconds=3600),
            create_if_missing: bool = False,
            retention: typing.Optional[datetime.timedelta] = None,
            sandbox: typing.Optional[modal.sandbox.sandbox.Sandbox] = None,
        ) -> StreamToken:
            """Create an access token for this Stream, for code without Modal credentials such as a Sandbox
            or a browser; see `Stream.from_token`.

            A `read` token can read the stream, and a `write` token can also append to and seal it. The token
            is valid for `ttl`, at most one hour. `create_if_missing` and `retention` create the stream as
            `Stream.from_name` does.

            A token for a `sandbox` keeps working inside that Sandbox beyond `ttl`: a handle from
            `Stream.from_token` there replaces it when it expires, proving it runs in the Sandbox with the
            Sandbox's identity token. The Sandbox must be created with `include_oidc_identity_token=True`.
            """
            ...

        async def aio(
            self,
            /,
            *,
            access: typing.Literal["read", "write"] = "write",
            ttl: datetime.timedelta = datetime.timedelta(seconds=3600),
            create_if_missing: bool = False,
            retention: typing.Optional[datetime.timedelta] = None,
            sandbox: typing.Optional[modal.sandbox.sandbox.Sandbox] = None,
        ) -> StreamToken:
            """Create an access token for this Stream, for code without Modal credentials such as a Sandbox
            or a browser; see `Stream.from_token`.

            A `read` token can read the stream, and a `write` token can also append to and seal it. The token
            is valid for `ttl`, at most one hour. `create_if_missing` and `retention` create the stream as
            `Stream.from_name` does.

            A token for a `sandbox` keeps working inside that Sandbox beyond `ttl`: a handle from
            `Stream.from_token` there replaces it when it expires, proving it runs in the Sandbox with the
            Sandbox's identity token. The Sandbox must be created with `include_oidc_identity_token=True`.
            """
            ...

    create_token: __create_token_spec

    class ___headers_spec(typing_extensions.Protocol):
        def __call__(self, /) -> dict[str, str]: ...
        async def aio(self, /) -> dict[str, str]: ...

    _headers: ___headers_spec

    class ___call_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            method: str,
            path: str,
            body: typing.Any = None,
            params: typing.Optional[collections.abc.Mapping[str, typing.Any]] = None,
            retry: bool = True,
            headers: typing.Optional[collections.abc.Mapping[str, str]] = None,
            content: typing.Optional[bytes] = None,
            timeout: float = 30.0,
        ) -> tuple[bytes, collections.abc.Mapping[str, str]]:
            """One request to the streams service, or to an absolute `path`, retried on transient failures until
            `RETRY_DEADLINE_S` passes, if `retry`, and once with a refreshed token if its token has expired.
            `headers` replaces the handle's credentials.
            """
            ...

        async def aio(
            self,
            /,
            method: str,
            path: str,
            body: typing.Any = None,
            params: typing.Optional[collections.abc.Mapping[str, typing.Any]] = None,
            retry: bool = True,
            headers: typing.Optional[collections.abc.Mapping[str, str]] = None,
            content: typing.Optional[bytes] = None,
            timeout: float = 30.0,
        ) -> tuple[bytes, collections.abc.Mapping[str, str]]:
            """One request to the streams service, or to an absolute `path`, retried on transient failures until
            `RETRY_DEADLINE_S` passes, if `retry`, and once with a refreshed token if its token has expired.
            `headers` replaces the handle's credentials.
            """
            ...

    _call: ___call_spec

    class ___put_blob_spec(typing_extensions.Protocol):
        def __call__(self, /, data: bytes) -> str:
            """Upload `data` for this stream and return the reference an entry holds in its place."""
            ...

        async def aio(self, /, data: bytes) -> str:
            """Upload `data` for this stream and return the reference an entry holds in its place."""
            ...

    _put_blob: ___put_blob_spec

    class ___get_blob_spec(typing_extensions.Protocol):
        def __call__(self, /, ref: str) -> bytes: ...
        async def aio(self, /, ref: str) -> bytes: ...

    _get_blob: ___get_blob_spec

    class ___transfer_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            method: str,
            url: str,
            headers: collections.abc.Mapping[str, str],
            content: typing.Optional[bytes] = None,
        ) -> bytes: ...
        async def aio(
            self,
            /,
            method: str,
            url: str,
            headers: collections.abc.Mapping[str, str],
            content: typing.Optional[bytes] = None,
        ) -> bytes: ...

    _transfer: ___transfer_spec

    class ___payload_spec(typing_extensions.Protocol):
        def __call__(self, /, value: typing.Any) -> dict[str, typing.Any]:
            """The entry fields that carry `value`: the value, or a reference to its upload."""
            ...

        async def aio(self, /, value: typing.Any) -> dict[str, typing.Any]:
            """The entry fields that carry `value`: the value, or a reference to its upload."""
            ...

    _payload: ___payload_spec

    class ___resolve_spec(typing_extensions.Protocol):
        def __call__(self, /, event: dict[str, typing.Any]) -> Entry: ...
        async def aio(self, /, event: dict[str, typing.Any]) -> Entry: ...

    _resolve: ___resolve_spec

    class ___renew_spec(typing_extensions.Protocol):
        def __call__(self, /, stale: str) -> bool:
            """Whether the access token `stale` has been replaced, refreshing it if this handle can; concurrent
            callers share one refresh.
            """
            ...

        async def aio(self, /, stale: str) -> bool:
            """Whether the access token `stale` has been replaced, refreshing it if this handle can; concurrent
            callers share one refresh.
            """
            ...

    _renew: ___renew_spec

    class ___refresh_spec(typing_extensions.Protocol):
        def __call__(self, /) -> bool: ...
        async def aio(self, /) -> bool: ...

    _refresh: ___refresh_spec

    def _unreachable(self, exc: Exception) -> Exception: ...

    class ___create_locked_spec(typing_extensions.Protocol):
        def __call__(self, /) -> None:
            """Create the stream on this handle's first request if `create_if_missing` was set; the caller
            holds `_lock`, so concurrent first requests create it once.
            """
            ...

        async def aio(self, /) -> None:
            """Create the stream on this handle's first request if `create_if_missing` was set; the caller
            holds `_lock`, so concurrent first requests create it once.
            """
            ...

    _create_locked: ___create_locked_spec

    class ___lease_spec(typing_extensions.Protocol):
        def __call__(self, /) -> int:
            """The lease number this client attaches to its writes. The service rejects a stale one, and since
            this client never takes a new lease, all handles share the current one.
            """
            ...

        async def aio(self, /) -> int:
            """The lease number this client attaches to its writes. The service rejects a stale one, and since
            this client never takes a new lease, all handles share the current one.
            """
            ...

    _lease: ___lease_spec

    class ___write_spec(typing_extensions.Protocol):
        def __call__(self, /, path: str, body: dict[str, typing.Any]) -> dict[str, typing.Any]:
            """A write under the stream's current generation, resent under the new one if it changes."""
            ...

        async def aio(self, /, path: str, body: dict[str, typing.Any]) -> dict[str, typing.Any]:
            """A write under the stream's current generation, resent under the new one if it changes."""
            ...

    _write: ___write_spec

    class __append_spec(typing_extensions.Protocol):
        def __call__(self, /, value: typing.Any, *, idempotency_key: typing.Optional[str] = None) -> AppendResult:
            """Append a JSON-serializable value of at most 1 GiB and return its sequence number. A value over
            64 KiB is uploaded before its entry is written; reads return it like any other.

            Appending again with the same `idempotency_key` and value returns the original result with
            `deduped=True`; the same key with a different value raises `IdempotencyConflict`.
            """
            ...

        async def aio(self, /, value: typing.Any, *, idempotency_key: typing.Optional[str] = None) -> AppendResult:
            """Append a JSON-serializable value of at most 1 GiB and return its sequence number. A value over
            64 KiB is uploaded before its entry is written; reads return it like any other.

            Appending again with the same `idempotency_key` and value returns the original result with
            `deduped=True`; the same key with a different value raises `IdempotencyConflict`.
            """
            ...

    append: __append_spec

    class __append_many_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            values: collections.abc.Iterable[typing.Any],
            *,
            idempotency_keys: typing.Optional[collections.abc.Sequence[str]] = None,
        ) -> list[AppendResult]:
            """Append several values in one request, in order; see `append`. If any key conflicts, none
            of the values is written.
            """
            ...

        async def aio(
            self,
            /,
            values: collections.abc.Iterable[typing.Any],
            *,
            idempotency_keys: typing.Optional[collections.abc.Sequence[str]] = None,
        ) -> list[AppendResult]:
            """Append several values in one request, in order; see `append`. If any key conflicts, none
            of the values is written.
            """
            ...

    append_many: __append_many_spec

    class ___append_spec(typing_extensions.Protocol):
        def __call__(self, /, entries: list[tuple[str, dict[str, typing.Any]]]) -> list[AppendResult]: ...
        async def aio(self, /, entries: list[tuple[str, dict[str, typing.Any]]]) -> list[AppendResult]: ...

    _append: ___append_spec

    class __info_spec(typing_extensions.Protocol):
        def __call__(self, /) -> StreamInfo:
            """The stream's latest sequence number, whether it is sealed, and when it was created, last written
            and is due to expire.
            """
            ...

        async def aio(self, /) -> StreamInfo:
            """The stream's latest sequence number, whether it is sealed, and when it was created, last written
            and is due to expire.
            """
            ...

    info: __info_spec

    class ____getitem___spec(typing_extensions.Protocol):
        def __call__(self, /, seq: int) -> Entry:
            """The entry at sequence number `seq`; raises `IndexError` past the end of the stream. Use `read` for
            a range of entries.
            """
            ...

        async def aio(self, /, seq: int) -> Entry:
            """The entry at sequence number `seq`; raises `IndexError` past the end of the stream. Use `read` for
            a range of entries.
            """
            ...

    __getitem__: ____getitem___spec

    class __read_spec(typing_extensions.Protocol):
        def __call__(self, /, start: int = 1, *, follow: bool = False) -> typing.Generator[Entry, None, None]:
            """Iterate over the stream's entries from sequence number `start`.

            With `follow=True`, keep waiting for new entries until the stream is sealed, reconnecting after the
            last entry when the connection drops.
            """
            ...

        def aio(self, /, start: int = 1, *, follow: bool = False) -> collections.abc.AsyncGenerator[Entry, None]:
            """Iterate over the stream's entries from sequence number `start`.

            With `follow=True`, keep waiting for new entries until the stream is sealed, reconnecting after the
            last entry when the connection drops.
            """
            ...

    read: __read_spec

    class ___replay_spec(typing_extensions.Protocol):
        def __call__(self, /, start: int) -> typing.Generator[Entry, None, None]: ...
        def aio(self, /, start: int) -> collections.abc.AsyncGenerator[Entry, None]: ...

    _replay: ___replay_spec

    class ___follow_spec(typing_extensions.Protocol):
        def __call__(self, /, start: int) -> typing.Generator[Entry, None, None]: ...
        def aio(self, /, start: int) -> collections.abc.AsyncGenerator[Entry, None]: ...

    _follow: ___follow_spec

    class __fork_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            name: str,
            *,
            at: typing.Optional[int] = None,
            retention: typing.Optional[datetime.timedelta] = None,
        ) -> Stream:
            """Create a Stream named `name` that starts with this stream's entries through sequence number `at`,
            or all of them but a final `seal` by default, and continues independently from there.

            The fork reads those entries from this stream without copying them, and keeps them even if this
            stream is deleted or expires. `retention` applies to the fork as in `Stream.from_name`; without
            it the fork keeps this stream's retention.
            """
            ...

        async def aio(
            self,
            /,
            name: str,
            *,
            at: typing.Optional[int] = None,
            retention: typing.Optional[datetime.timedelta] = None,
        ) -> Stream:
            """Create a Stream named `name` that starts with this stream's entries through sequence number `at`,
            or all of them but a final `seal` by default, and continues independently from there.

            The fork reads those entries from this stream without copying them, and keeps them even if this
            stream is deleted or expires. `retention` applies to the fork as in `Stream.from_name`; without
            it the fork keeps this stream's retention.
            """
            ...

    fork: __fork_spec

    class __seal_spec(typing_extensions.Protocol):
        def __call__(self, /) -> int:
            """Close the stream to writers and return the sequence number of its final `seal` entry."""
            ...

        async def aio(self, /) -> int:
            """Close the stream to writers and return the sequence number of its final `seal` entry."""
            ...

    seal: __seal_spec

    def writer(
        self,
        *,
        on_written: typing.Optional[collections.abc.Callable[[str, AppendResult], None]] = None,
        on_conflict: typing.Optional[collections.abc.Callable[[IdempotencyConflict], None]] = None,
    ) -> StreamWriter:
        """A writer that appends in the background, batching values that arrive while a write is in flight."""
        ...

class StreamWriter:
    """Appends to a Stream from a background task, in order and in batches.

    `append` queues a value and returns at once, or waits while 1000 values are queued. Do not change a
    value after appending it. Each value written is reported to `on_written` with its idempotency key and
    result, and a reused key with a different value to `on_conflict`. A write that fails after retries, or
    a conflict without an `on_conflict` handler, stops the writer: the error is raised from the next
    `append`, `flush` or `close`, and values still queued are dropped. Use the writer as an async context
    manager or call `close`, so every value is written or the error is raised. Callbacks run on Modal's
    event loop thread, not the caller's, and should return quickly.
    """
    def __init__(
        self,
        stream: Stream,
        on_written: typing.Optional[collections.abc.Callable[[str, AppendResult], None]],
        on_conflict: typing.Optional[collections.abc.Callable[[IdempotencyConflict], None]],
    ):
        """mdmd:hidden"""
        ...

    class __append_spec(typing_extensions.Protocol):
        def __call__(self, /, value: typing.Any, *, idempotency_key: typing.Optional[str] = None) -> None:
            """Queue a value to be appended; see `Stream.append` for the limits and idempotency. A value over
            64 KiB is uploaded before it is queued.
            """
            ...

        async def aio(self, /, value: typing.Any, *, idempotency_key: typing.Optional[str] = None) -> None:
            """Queue a value to be appended; see `Stream.append` for the limits and idempotency. A value over
            64 KiB is uploaded before it is queued.
            """
            ...

    append: __append_spec

    def _try_enqueue(self, payload: dict[str, typing.Any], idempotency_key: typing.Optional[str]) -> bool:
        """Queue the value's entry fields and return True, or return False while the queue is full."""
        ...

    def _start(self) -> None: ...

    class __flush_spec(typing_extensions.Protocol):
        def __call__(self, /) -> None:
            """Wait until every queued value is written."""
            ...

        async def aio(self, /) -> None:
            """Wait until every queued value is written."""
            ...

    flush: __flush_spec

    class __close_spec(typing_extensions.Protocol):
        def __call__(self, /) -> None:
            """Flush and stop the background task; an `append` still waiting for room raises `InvalidError`."""
            ...

        async def aio(self, /) -> None:
            """Flush and stop the background task; an `append` still waiting for room raises `InvalidError`."""
            ...

    close: __close_spec

    def __enter__(self) -> StreamWriter: ...
    async def __aenter__(self) -> StreamWriter: ...
    def __exit__(self, exc_type, exc, tb) -> None: ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    class ___run_spec(typing_extensions.Protocol):
        def __call__(self, /) -> None: ...
        async def aio(self, /) -> None: ...

    _run: ___run_spec

    class ___drain_spec(typing_extensions.Protocol):
        def __call__(self, /) -> None: ...
        async def aio(self, /) -> None: ...

    _drain: ___drain_spec

    class ___write_spec(typing_extensions.Protocol):
        def __call__(self, /, batch: list[tuple[str, dict[str, typing.Any]]]) -> None: ...
        async def aio(self, /, batch: list[tuple[str, dict[str, typing.Any]]]) -> None: ...

    _write: ___write_spec

    def _report(self, callback: collections.abc.Callable[..., None], *args: typing.Any) -> None: ...

MAX_VALUE_BYTES: int

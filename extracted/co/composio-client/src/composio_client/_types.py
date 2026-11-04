"""Public compatibility types shared by the client and generated resources."""

from __future__ import annotations

import os
import typing
from collections.abc import AsyncIterator, Iterator, Mapping, Sequence
from typing import IO, TYPE_CHECKING, Any, TypeAlias, TypeVar, overload

import httpx
from typing_extensions import Protocol, SupportsIndex, TypedDict

NoneType = type(None)
Timeout = httpx.Timeout

DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=5.0)
DEFAULT_MAX_RETRIES = 2
DEFAULT_CONNECTION_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20)


class NotGiven:
    """Sentinel distinguishing an omitted argument from an explicit ``None``."""

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()
not_given = NOT_GIVEN


class Omit:
    """Sentinel used by generated optional request fields."""

    def __bool__(self) -> bool:
        return False


omit = Omit()

Headers: TypeAlias = Mapping[str, str | None]
Query: TypeAlias = Mapping[str, object]
Body: TypeAlias = Mapping[str, object]
AnyMapping: TypeAlias = Mapping[str, object]
BinaryTypes: TypeAlias = str | bytes | bytearray | memoryview
AsyncBinaryTypes: TypeAlias = BinaryTypes | AsyncIterator[bytes]
FileContent: TypeAlias = IO[bytes] | bytes | os.PathLike[str]
FileTypes: TypeAlias = (
    FileContent
    | tuple[str | None, FileContent]
    | tuple[str | None, FileContent, str | None]
    | tuple[str | None, FileContent, str | None, Mapping[str, str]]
)
RequestFiles: TypeAlias = Mapping[str, FileTypes] | Sequence[tuple[str, FileTypes]]

_T_co = TypeVar("_T_co", covariant=True)

if TYPE_CHECKING:

    class SequenceNotStr(Protocol[_T_co]):
        """A sequence protocol that excludes strings during static checking."""

        @overload
        def __getitem__(self, index: SupportsIndex, /) -> _T_co: ...

        @overload
        def __getitem__(self, index: slice, /) -> Sequence[_T_co]: ...

        def __contains__(self, value: object, /) -> bool: ...

        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[_T_co]: ...

        def __reversed__(self) -> Iterator[_T_co]: ...

else:
    SequenceNotStr = typing.Sequence


class PropertyInfo:
    """Metadata retained on Stainless-compatible request annotations."""

    def __init__(
        self,
        *,
        alias: str | None = None,
        format: str | None = None,
        format_template: str | None = None,
        discriminator: str | None = None,
    ) -> None:
        self.alias = alias
        self.format = format
        self.format_template = format_template
        self.discriminator = discriminator

    def __repr__(self) -> str:
        arguments = ", ".join(
            f"{name}={value!r}"
            for name in ("alias", "format", "format_template", "discriminator")
            if (value := getattr(self, name)) is not None
        )
        return f"{type(self).__name__}({arguments})"


class RequestOptions(TypedDict, total=False):
    """Per-request overrides accepted by the raw client methods.

    ``query`` is an additive alias retained for the first owned-client API;
    Stainless calls the same field ``params``.
    """

    headers: Headers
    max_retries: int
    timeout: float | httpx.Timeout | None
    params: Query
    query: Query
    extra_json: AnyMapping
    # Stainless options-bag compatibility: sent as the `Idempotency-Key`
    # request header. Server-side replay/dedup for Composio's write endpoints
    # is not guaranteed. This header does not opt a POST/PATCH into retries.
    idempotency_key: str
    follow_redirects: bool


class _DefaultHttpxClient(httpx.Client):
    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        kwargs.setdefault("limits", DEFAULT_CONNECTION_LIMITS)
        kwargs.setdefault("follow_redirects", True)
        super().__init__(**kwargs)


class _DefaultAsyncHttpxClient(httpx.AsyncClient):
    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        kwargs.setdefault("limits", DEFAULT_CONNECTION_LIMITS)
        kwargs.setdefault("follow_redirects", True)
        super().__init__(**kwargs)


DefaultHttpxClient = _DefaultHttpxClient

DefaultAsyncHttpxClient = _DefaultAsyncHttpxClient

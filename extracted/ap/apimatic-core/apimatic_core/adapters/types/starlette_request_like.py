from typing import Any, Mapping, Awaitable
from typing_extensions import Protocol, runtime_checkable

@runtime_checkable
class StarletteRequestLike(Protocol):
    method: str
    headers: Mapping[str, str]
    cookies: Mapping[str, str]
    query_params: Mapping[str, Any]
    url: Any
    def body(self) -> Awaitable[bytes]: ...
    def form(self) -> Awaitable[Any]: ...

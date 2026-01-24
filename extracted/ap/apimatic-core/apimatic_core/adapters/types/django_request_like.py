from typing import Any, Mapping
from typing_extensions import Protocol, runtime_checkable

@runtime_checkable
class DjangoRequestLike(Protocol):
    method: str
    headers: Mapping[str, str]
    COOKIES: Mapping[str, str]
    GET: Mapping[str, Any]
    POST: Mapping[str, Any]
    path: str
    body: bytes
    def build_absolute_uri(self) -> str: ...

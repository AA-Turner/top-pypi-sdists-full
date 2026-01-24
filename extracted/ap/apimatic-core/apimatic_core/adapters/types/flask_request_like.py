from typing import Any, Mapping
from typing_extensions import Protocol, runtime_checkable

@runtime_checkable
class FlaskRequestLike(Protocol):
    method: str
    headers: Mapping[str, str]
    cookies: Mapping[str, str]
    args: Mapping[str, Any]
    url: str
    path: str
    def get_data(self, cache: bool = ...) -> bytes: ...
    form: Mapping[str, Any]

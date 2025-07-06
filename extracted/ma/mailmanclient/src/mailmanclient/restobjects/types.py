import sys
from typing import Mapping, Any, Tuple, NewType
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    # mypy understnads version_info check better than ImportError. So for the
    # sake of static typing checks, we are for once going to do LBYL.
    from typing_extensions import Protocol

__all__ = [
    'HTTPClientProto',
    'ResponseType',
    'ContentType',
    'ConnectionProto',
]


ContentType = NewType('ContentType', Mapping[str, Any])


class ResponseType(Protocol):
    status_code: int
    content: ContentType


class HTTPClientProto(Protocol):
    """A type checking protocol for the HTTP client argument for AsyncClient"""
    async def request(self) -> ResponseType:
        ...


class ConnectionProto(Protocol):
    """A type checking procol for connection object to avoid circular import"""
    async def call(self,
                   path: str,
                   data: Mapping[str, Any] = None,
                   method: str = 'GET') -> Tuple[ResponseType, ContentType]:
        ...

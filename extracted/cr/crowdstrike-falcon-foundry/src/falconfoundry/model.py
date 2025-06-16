from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class FoundryRequestParams:
    header: Dict[str, List[str]] = field(default_factory=lambda: {})
    query: Dict[str, List[str]] = field(default_factory=lambda: {})


@dataclass
class FoundryAPIError:
    code: int = field(default=0)
    message: str = field(default='')


@dataclass
class FoundryRequest:
    access_token: str = field(default='')
    body: Dict[str, any] = field(default_factory=lambda: {})
    context: Dict[str, any] = field(default_factory=lambda: {})
    files: Dict[str, bytes] = field(default_factory=lambda: {})
    fn_id: str = field(default='')
    fn_version: int = field(default=0)
    method: str = field(default='')
    params: FoundryRequestParams = field(default_factory=lambda: FoundryRequestParams())
    trace_id: str = field(default='')
    url: str = field(default='')


@dataclass
class FoundryResponse:
    body: Dict[str, any] = field(default_factory=lambda: {})
    code: int = field(default=0)
    errors: List[FoundryAPIError] = field(default_factory=lambda: [])
    header: Dict[str, List[str]] = field(default_factory=lambda: {})


class FoundryFDKException(Exception):

    def __init__(self, code: int, message: str):
        Exception.__init__(self, message)
        self.code = code
        self.message = message

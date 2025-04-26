import dataclasses
from typing import Generic, Mapping, Optional, Type, TypeVar, get_args

import pyarrow as pa

T = TypeVar("T", str, bytes)


@dataclasses.dataclass
class HttpResponse(Generic[T]):
    """
     Feature annotation for HTTP responses, with a string body. HTTP responses are treated internally as
     structs, and you can treat them as such in code/expressions that involve this feature.

     The underlying pyarrow type of HttpStringResponse is
     pa.struct_([
         pa.field("status_code", pa.int64()),
         pa.field("headers", pa.map_(pa.large_string(), pa.large_string())),
         pa.field("body", pa.large_string()),
         pa.field("final_url", pa.large_string()),
     ])

    Examples
     --------
     >>> from chalk import _
     >>> import chalk.functions as F
     >>> from chalk.functions.http import HttpResponse
     >>> @features
     ... class User:
     ...    id: str
     ...    resp: HttpResponse[str] = F.http_request("https://example.com", "GET")
     ...    status_code: int = _.resp.status_code
     ...    resp_body: str = _.resp.body
    """

    status_code: Optional[int]
    headers: Optional[Mapping[str, str]]
    body: Optional[T]
    final_url: Optional[str]


def get_http_response_as_pyarrow(t: Type[HttpResponse]) -> pa.DataType:
    type_args = get_args(t)
    if len(type_args) != 1:
        raise TypeError(f"Unsupported http-response type: {t}")
    if issubclass(type_args[0], str):
        return pa.struct(
            [
                pa.field("status_code", pa.int64()),
                pa.field("headers", pa.map_(pa.large_utf8(), pa.large_utf8())),
                pa.field("body", pa.large_utf8()),
                pa.field("final_url", pa.large_utf8()),
            ]
        )
    if issubclass(type_args[0], bytes):
        return pa.struct(
            [
                pa.field("status_code", pa.int64()),
                pa.field("headers", pa.map_(pa.large_utf8(), pa.large_utf8())),
                pa.field("body", pa.large_binary()),
                pa.field("final_url", pa.large_utf8()),
            ]
        )
    raise TypeError(f"Unsupported http-response type: {t}")


__all__ = ["HttpResponse", "get_http_response_as_pyarrow"]

import dataclasses
import typing as t

import httpx


@dataclasses.dataclass
class MockedResponse:
    status_code: httpx.codes
    response_body: dict[str, t.Any] | list[t.Any] | str | None
    headers: dict[str, str] | None = None
    request_json_body: dict[
        str, t.Any
    ] | None = None  # for cases where we want to match the request body


ResponseBodyMap: t.TypeAlias = (
    t.Mapping[str, t.Mapping[str, MockedResponse] | list[MockedResponse]] | None
)
# ResponseBodyMap: t.TypeAlias = dict[str, dict[str, MockedResponse]] | None
RequestHandler: t.TypeAlias = t.Callable[[httpx.Request], httpx.Response]
ClientContextManager: t.TypeAlias = t.Callable[[str, str, RequestHandler], t.ContextManager[None]]

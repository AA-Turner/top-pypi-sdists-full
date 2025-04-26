import typing as t

import httpx
import pydantic

DTO = t.TypeVar("DTO", bound=pydantic.BaseModel)


def create_client_response(
    response: httpx.Response,
    dto: type[DTO],
) -> DTO:
    response.raise_for_status()
    response_body = response.json()
    if isinstance(response_body, list):
        return dto(root=response_body)
    else:
        return dto(**response_body)

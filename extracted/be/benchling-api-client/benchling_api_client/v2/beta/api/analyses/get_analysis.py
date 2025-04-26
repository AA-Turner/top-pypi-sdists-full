from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.analysis import Analysis
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    analysis_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/analyses/{analysis_id}".format(client.base_url, analysis_id=analysis_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Analysis, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = Analysis.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Analysis, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    analysis_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[Analysis, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        analysis_id=analysis_id,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    analysis_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[Analysis, ForbiddenError, NotFoundError]]:
    """Get an Analysis and the Data Framess and Files it contains. You can download the Analysis data with the corresponding
    [Get a data frame](#/Data%20Frames/getDataFrame) and [Get a file](#/Files/getFile) endpoints.

    For more details and examples on building Analysis integrations, see our [developer guide](https://docs.benchling.com/docs/analyses-api-developer-guide).
    """

    return sync_detailed(
        client=client,
        analysis_id=analysis_id,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    analysis_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[Analysis, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        analysis_id=analysis_id,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    analysis_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[Analysis, ForbiddenError, NotFoundError]]:
    """Get an Analysis and the Data Framess and Files it contains. You can download the Analysis data with the corresponding
    [Get a data frame](#/Data%20Frames/getDataFrame) and [Get a file](#/Files/getFile) endpoints.

    For more details and examples on building Analysis integrations, see our [developer guide](https://docs.benchling.com/docs/analyses-api-developer-guide).
    """

    return (
        await asyncio_detailed(
            client=client,
            analysis_id=analysis_id,
            returning=returning,
        )
    ).parsed

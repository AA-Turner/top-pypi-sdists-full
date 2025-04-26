from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.analysis import Analysis
from ...models.analysis_update import AnalysisUpdate
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    analysis_id: str,
    json_body: AnalysisUpdate,
) -> Dict[str, Any]:
    url = "{}/analyses/{analysis_id}".format(client.base_url, analysis_id=analysis_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    json_body: AnalysisUpdate,
) -> Response[Union[Analysis, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        analysis_id=analysis_id,
        json_body=json_body,
    )

    response = client.httpx_client.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    analysis_id: str,
    json_body: AnalysisUpdate,
) -> Optional[Union[Analysis, ForbiddenError, NotFoundError]]:
    """Update an analysis.

    This endpoint can be used to attach DataFrames and Files to an analysis by providing file and/or data frame
    ids inside the `dataFrameIds` and `fileIds` elements. This will append the dataFramess and files to the analysis.

    If attaching files:
    1. Upload the files with the [Create a file](#/Files/createFile) endpoint
    2. Use this endpoint to attach file ids via the `fileIds` array element

    If attaching data frames:
    1. Create the data frames from existing files using the [Create a data frame](#/Data%20Frames/createDataFrame)
    endpoint
    2. Use this endpoint to attach data frame ids via the `dataFrameIds` array element

    For more details and examples on building Analysis integrations, see our [developer guide](https://docs.benchling.com/docs/analyses-api-developer-guide).
    """

    return sync_detailed(
        client=client,
        analysis_id=analysis_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    analysis_id: str,
    json_body: AnalysisUpdate,
) -> Response[Union[Analysis, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        analysis_id=analysis_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    analysis_id: str,
    json_body: AnalysisUpdate,
) -> Optional[Union[Analysis, ForbiddenError, NotFoundError]]:
    """Update an analysis.

    This endpoint can be used to attach DataFrames and Files to an analysis by providing file and/or data frame
    ids inside the `dataFrameIds` and `fileIds` elements. This will append the dataFramess and files to the analysis.

    If attaching files:
    1. Upload the files with the [Create a file](#/Files/createFile) endpoint
    2. Use this endpoint to attach file ids via the `fileIds` array element

    If attaching data frames:
    1. Create the data frames from existing files using the [Create a data frame](#/Data%20Frames/createDataFrame)
    endpoint
    2. Use this endpoint to attach data frame ids via the `dataFrameIds` array element

    For more details and examples on building Analysis integrations, see our [developer guide](https://docs.benchling.com/docs/analyses-api-developer-guide).
    """

    return (
        await asyncio_detailed(
            client=client,
            analysis_id=analysis_id,
            json_body=json_body,
        )
    ).parsed

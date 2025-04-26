from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.assay_results_bulk_create_request import AssayResultsBulkCreateRequest
from ...models.assay_results_create_error_response import AssayResultsCreateErrorResponse
from ...models.assay_results_create_response import AssayResultsCreateResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultsBulkCreateRequest,
) -> Dict[str, Any]:
    url = "{}/result-transactions/{transaction_id}/results".format(
        client.base_url, transaction_id=transaction_id
    )

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AssayResultsCreateResponse, AssayResultsCreateErrorResponse]]:
    if response.status_code == 200:
        response_200 = AssayResultsCreateResponse.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = AssayResultsCreateErrorResponse.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AssayResultsCreateResponse, AssayResultsCreateErrorResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultsBulkCreateRequest,
) -> Response[Union[AssayResultsCreateResponse, AssayResultsCreateErrorResponse]]:
    kwargs = _get_kwargs(
        client=client,
        transaction_id=transaction_id,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultsBulkCreateRequest,
) -> Optional[Union[AssayResultsCreateResponse, AssayResultsCreateErrorResponse]]:
    """ Create results in a transaction """

    return sync_detailed(
        client=client,
        transaction_id=transaction_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultsBulkCreateRequest,
) -> Response[Union[AssayResultsCreateResponse, AssayResultsCreateErrorResponse]]:
    kwargs = _get_kwargs(
        client=client,
        transaction_id=transaction_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultsBulkCreateRequest,
) -> Optional[Union[AssayResultsCreateResponse, AssayResultsCreateErrorResponse]]:
    """ Create results in a transaction """

    return (
        await asyncio_detailed(
            client=client,
            transaction_id=transaction_id,
            json_body=json_body,
        )
    ).parsed

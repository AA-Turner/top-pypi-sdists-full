from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.convert_to_csv import ConvertToCSV
from ...models.convert_to_csv_response_200_item import ConvertToCSVResponse_200Item
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ConvertToCSV,
) -> Dict[str, Any]:
    url = "{}/connect/convert-to-csv".format(client.base_url)

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
) -> Optional[Union[List[ConvertToCSVResponse_200Item], BadRequestError]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ConvertToCSVResponse_200Item.from_dict(response_200_item_data, strict=False)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[List[ConvertToCSVResponse_200Item], BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ConvertToCSV,
) -> Response[Union[List[ConvertToCSVResponse_200Item], BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: ConvertToCSV,
) -> Optional[Union[List[ConvertToCSVResponse_200Item], BadRequestError]]:
    """Convert a blob or file containing ASM, JSON, or instrument data to CSV.

    If the file is ASM JSON, specify either no transform type (in which case all transform types will be returned),
    a matching transform type for the ASM schema, or a custom JSON mapper config.

    If the file non-ASM JSON, must provide a JSON mapper config argument, which specifies how to map the JSON to CSV.
    Reach out to Benchling Support for more information about how to create a JSON mapper config.

    If the file is an instrument file, must also specify an instrument vendor. The file will be converted first to
    ASM JSON and then to CSV. Only the CSV output will be returned.

    May provide an AutomationOutputFile with CSV transform arguments configured to read the transform type
    or mapper config from.

    May provide a connection ID associated with an instrument to read the vendor from.
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ConvertToCSV,
) -> Response[Union[List[ConvertToCSVResponse_200Item], BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: ConvertToCSV,
) -> Optional[Union[List[ConvertToCSVResponse_200Item], BadRequestError]]:
    """Convert a blob or file containing ASM, JSON, or instrument data to CSV.

    If the file is ASM JSON, specify either no transform type (in which case all transform types will be returned),
    a matching transform type for the ASM schema, or a custom JSON mapper config.

    If the file non-ASM JSON, must provide a JSON mapper config argument, which specifies how to map the JSON to CSV.
    Reach out to Benchling Support for more information about how to create a JSON mapper config.

    If the file is an instrument file, must also specify an instrument vendor. The file will be converted first to
    ASM JSON and then to CSV. Only the CSV output will be returned.

    May provide an AutomationOutputFile with CSV transform arguments configured to read the transform type
    or mapper config from.

    May provide a connection ID associated with an instrument to read the vendor from.
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed

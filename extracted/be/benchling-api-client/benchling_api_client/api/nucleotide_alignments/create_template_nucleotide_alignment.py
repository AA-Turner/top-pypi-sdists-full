from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.async_task_link import AsyncTaskLink
from ...models.nucleotide_template_alignment_create import NucleotideTemplateAlignmentCreate
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: NucleotideTemplateAlignmentCreate,
) -> Dict[str, Any]:
    url = "{}/nucleotide-alignments:create-template-alignment".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[AsyncTaskLink]:
    if response.status_code == 202:
        response_202 = AsyncTaskLink.from_dict(response.json(), strict=False)

        return response_202
    return None


def _build_response(*, response: httpx.Response) -> Response[AsyncTaskLink]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: NucleotideTemplateAlignmentCreate,
) -> Response[AsyncTaskLink]:
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
    json_body: NucleotideTemplateAlignmentCreate,
) -> Optional[AsyncTaskLink]:
    """ Create a template Nucleotide Alignment """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: NucleotideTemplateAlignmentCreate,
) -> Response[AsyncTaskLink]:
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
    json_body: NucleotideTemplateAlignmentCreate,
) -> Optional[AsyncTaskLink]:
    """ Create a template Nucleotide Alignment """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.read_docs_page_response_200 import ReadDocsPageResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    url_query: str,
    section: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["url"] = url_query

    params["section"] = section

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/docs/page",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ReadDocsPageResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ReadDocsPageResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ReadDocsPageResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    url_query: str,
    section: Union[Unset, None, str] = UNSET,
) -> Response[ReadDocsPageResponse200]:
    """Fetch the markdown of a single Windmill documentation page. Provide the `url` of a page found via
    searchDocs (its Source URL). If the page is large, this returns its list of section headings instead
    of the full content; call again with the `section` argument set to one of those headings to read
    that section.

    Args:
        url_query (str):
        section (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReadDocsPageResponse200]
    """

    kwargs = _get_kwargs(
        url_query=url_query,
        section=section,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    url_query: str,
    section: Union[Unset, None, str] = UNSET,
) -> Optional[ReadDocsPageResponse200]:
    """Fetch the markdown of a single Windmill documentation page. Provide the `url` of a page found via
    searchDocs (its Source URL). If the page is large, this returns its list of section headings instead
    of the full content; call again with the `section` argument set to one of those headings to read
    that section.

    Args:
        url_query (str):
        section (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReadDocsPageResponse200
    """

    return sync_detailed(
        client=client,
        url_query=url_query,
        section=section,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    url_query: str,
    section: Union[Unset, None, str] = UNSET,
) -> Response[ReadDocsPageResponse200]:
    """Fetch the markdown of a single Windmill documentation page. Provide the `url` of a page found via
    searchDocs (its Source URL). If the page is large, this returns its list of section headings instead
    of the full content; call again with the `section` argument set to one of those headings to read
    that section.

    Args:
        url_query (str):
        section (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReadDocsPageResponse200]
    """

    kwargs = _get_kwargs(
        url_query=url_query,
        section=section,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    url_query: str,
    section: Union[Unset, None, str] = UNSET,
) -> Optional[ReadDocsPageResponse200]:
    """Fetch the markdown of a single Windmill documentation page. Provide the `url` of a page found via
    searchDocs (its Source URL). If the page is large, this returns its list of section headings instead
    of the full content; call again with the `section` argument set to one of those headings to read
    that section.

    Args:
        url_query (str):
        section (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReadDocsPageResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            url_query=url_query,
            section=section,
        )
    ).parsed

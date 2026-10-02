from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_help_articles import CategoryHelpArticles
from ...models.category_help_articles_request import CategoryHelpArticlesRequest
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: CategoryHelpArticlesRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/marketplace-category-help-articles/{id}/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CategoryHelpArticles:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CategoryHelpArticles.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CategoryHelpArticles]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    body: CategoryHelpArticlesRequest,
) -> Response[CategoryHelpArticles]:
    """Update a category help article

     Updates an existing help article. Requires staff permissions.

    Args:
        id (int):
        body (CategoryHelpArticlesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryHelpArticles]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient,
    body: CategoryHelpArticlesRequest,
) -> CategoryHelpArticles:
    """Update a category help article

     Updates an existing help article. Requires staff permissions.

    Args:
        id (int):
        body (CategoryHelpArticlesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryHelpArticles
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    body: CategoryHelpArticlesRequest,
) -> Response[CategoryHelpArticles]:
    """Update a category help article

     Updates an existing help article. Requires staff permissions.

    Args:
        id (int):
        body (CategoryHelpArticlesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryHelpArticles]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient,
    body: CategoryHelpArticlesRequest,
) -> CategoryHelpArticles:
    """Update a category help article

     Updates an existing help article. Requires staff permissions.

    Args:
        id (int):
        body (CategoryHelpArticlesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryHelpArticles
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed

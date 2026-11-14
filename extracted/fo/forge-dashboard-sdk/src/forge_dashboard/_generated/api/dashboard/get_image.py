from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.get_image_forge import GetImageForge
from ...models.get_image_kind import GetImageKind
from ...models.get_image_width import GetImageWidth
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    forge: GetImageForge,
    url_query: str,
    full_name: str | Unset = UNSET,
    number: int | Unset = UNSET,
    tag: str | Unset = UNSET,
    comment: int | Unset = UNSET,
    kind: GetImageKind | Unset = UNSET,
    width: GetImageWidth | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_forge = forge.value
    params["forge"] = json_forge

    params["url"] = url_query

    params["fullName"] = full_name

    params["number"] = number

    params["tag"] = tag

    params["comment"] = comment

    json_kind: str | Unset = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value

    params["kind"] = json_kind

    json_width: int | Unset = UNSET
    if not isinstance(width, Unset):
        json_width = width.value

    params["width"] = json_width


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/images",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Error | None:
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())



        return response_415

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    forge: GetImageForge,
    url_query: str,
    full_name: str | Unset = UNSET,
    number: int | Unset = UNSET,
    tag: str | Unset = UNSET,
    comment: int | Unset = UNSET,
    kind: GetImageKind | Unset = UNSET,
    width: GetImageWidth | Unset = UNSET,

) -> Response[Error]:
    """ Read an image embedded in a forge's Markdown, through the server

     The details dialog shows the images in a description or comment by
    pointing its `<img>` here, never at the forge or a third party. The
    server fetches the image and returns the bytes, so the browser sends no
    request to another host, and a private repository's attachment loads
    without the forge token ever reaching the browser.

    Only the forge the item belongs to is reached. Forgejo: the saved
    instance, with the saved token sent to that host only. GitHub:
    `github.com` and its user-content hosts (`user-images`,
    `private-user-images`, `raw`, `gist`, `avatars` and `repository-images`
    under `githubusercontent.com`), without a
    token, since its attachment links are signed. A
    `github.com/user-attachments/...` link in a private repository is not
    served unsigned, so when `fullName` and `number` (or `tag`, or the
    `comment` it was posted in) name where it sits, the server reads that
    item's or comment's rendered HTML through the
    GitHub API with the saved token and fetches the signed address found
    there instead, without the token. If the lookup finds nothing or fails, or the signed address is on
    a host
    that isn't allowed or doesn't load, the link is fetched as written.
    Each such image costs one GitHub API request, which is never served from
    the ETag cache because the signature expires. Any other host, scheme or
    address answers 403 without a request. A redirect is followed only to
    another allowed host, and at most three times. GitHub's hosts are also
    refused at connect time if they resolve to a non-public address.

    The body must be a PNG, JPEG, GIF or WebP by its own bytes, not by the
    host's `Content-Type`, and at most 8 MiB (512 KiB with `kind=avatar`).
    SVG and anything else answers 415.

    The cost is bounded. At most 8 fetches run upstream at once; another
    request waits up to 5 seconds for a slot, then answers 503 with
    `Retry-After`. A fetched image is served again from a server-side cache
    for 5 minutes, without a new upstream fetch. The answer carries
    `nosniff` and a sandboxing `Content-Security-Policy`, and is cacheable
    by the browser for an hour.

    Args:
        forge (GetImageForge):
        url_query (str):
        full_name (str | Unset):
        number (int | Unset):
        tag (str | Unset):
        comment (int | Unset):
        kind (GetImageKind | Unset):
        width (GetImageWidth | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
     """


    kwargs = _get_kwargs(
        forge=forge,
url_query=url_query,
full_name=full_name,
number=number,
tag=tag,
comment=comment,
kind=kind,
width=width,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    forge: GetImageForge,
    url_query: str,
    full_name: str | Unset = UNSET,
    number: int | Unset = UNSET,
    tag: str | Unset = UNSET,
    comment: int | Unset = UNSET,
    kind: GetImageKind | Unset = UNSET,
    width: GetImageWidth | Unset = UNSET,

) -> Error | None:
    """ Read an image embedded in a forge's Markdown, through the server

     The details dialog shows the images in a description or comment by
    pointing its `<img>` here, never at the forge or a third party. The
    server fetches the image and returns the bytes, so the browser sends no
    request to another host, and a private repository's attachment loads
    without the forge token ever reaching the browser.

    Only the forge the item belongs to is reached. Forgejo: the saved
    instance, with the saved token sent to that host only. GitHub:
    `github.com` and its user-content hosts (`user-images`,
    `private-user-images`, `raw`, `gist`, `avatars` and `repository-images`
    under `githubusercontent.com`), without a
    token, since its attachment links are signed. A
    `github.com/user-attachments/...` link in a private repository is not
    served unsigned, so when `fullName` and `number` (or `tag`, or the
    `comment` it was posted in) name where it sits, the server reads that
    item's or comment's rendered HTML through the
    GitHub API with the saved token and fetches the signed address found
    there instead, without the token. If the lookup finds nothing or fails, or the signed address is on
    a host
    that isn't allowed or doesn't load, the link is fetched as written.
    Each such image costs one GitHub API request, which is never served from
    the ETag cache because the signature expires. Any other host, scheme or
    address answers 403 without a request. A redirect is followed only to
    another allowed host, and at most three times. GitHub's hosts are also
    refused at connect time if they resolve to a non-public address.

    The body must be a PNG, JPEG, GIF or WebP by its own bytes, not by the
    host's `Content-Type`, and at most 8 MiB (512 KiB with `kind=avatar`).
    SVG and anything else answers 415.

    The cost is bounded. At most 8 fetches run upstream at once; another
    request waits up to 5 seconds for a slot, then answers 503 with
    `Retry-After`. A fetched image is served again from a server-side cache
    for 5 minutes, without a new upstream fetch. The answer carries
    `nosniff` and a sandboxing `Content-Security-Policy`, and is cacheable
    by the browser for an hour.

    Args:
        forge (GetImageForge):
        url_query (str):
        full_name (str | Unset):
        number (int | Unset):
        tag (str | Unset):
        comment (int | Unset):
        kind (GetImageKind | Unset):
        width (GetImageWidth | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
     """


    return sync_detailed(
        client=client,
forge=forge,
url_query=url_query,
full_name=full_name,
number=number,
tag=tag,
comment=comment,
kind=kind,
width=width,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    forge: GetImageForge,
    url_query: str,
    full_name: str | Unset = UNSET,
    number: int | Unset = UNSET,
    tag: str | Unset = UNSET,
    comment: int | Unset = UNSET,
    kind: GetImageKind | Unset = UNSET,
    width: GetImageWidth | Unset = UNSET,

) -> Response[Error]:
    """ Read an image embedded in a forge's Markdown, through the server

     The details dialog shows the images in a description or comment by
    pointing its `<img>` here, never at the forge or a third party. The
    server fetches the image and returns the bytes, so the browser sends no
    request to another host, and a private repository's attachment loads
    without the forge token ever reaching the browser.

    Only the forge the item belongs to is reached. Forgejo: the saved
    instance, with the saved token sent to that host only. GitHub:
    `github.com` and its user-content hosts (`user-images`,
    `private-user-images`, `raw`, `gist`, `avatars` and `repository-images`
    under `githubusercontent.com`), without a
    token, since its attachment links are signed. A
    `github.com/user-attachments/...` link in a private repository is not
    served unsigned, so when `fullName` and `number` (or `tag`, or the
    `comment` it was posted in) name where it sits, the server reads that
    item's or comment's rendered HTML through the
    GitHub API with the saved token and fetches the signed address found
    there instead, without the token. If the lookup finds nothing or fails, or the signed address is on
    a host
    that isn't allowed or doesn't load, the link is fetched as written.
    Each such image costs one GitHub API request, which is never served from
    the ETag cache because the signature expires. Any other host, scheme or
    address answers 403 without a request. A redirect is followed only to
    another allowed host, and at most three times. GitHub's hosts are also
    refused at connect time if they resolve to a non-public address.

    The body must be a PNG, JPEG, GIF or WebP by its own bytes, not by the
    host's `Content-Type`, and at most 8 MiB (512 KiB with `kind=avatar`).
    SVG and anything else answers 415.

    The cost is bounded. At most 8 fetches run upstream at once; another
    request waits up to 5 seconds for a slot, then answers 503 with
    `Retry-After`. A fetched image is served again from a server-side cache
    for 5 minutes, without a new upstream fetch. The answer carries
    `nosniff` and a sandboxing `Content-Security-Policy`, and is cacheable
    by the browser for an hour.

    Args:
        forge (GetImageForge):
        url_query (str):
        full_name (str | Unset):
        number (int | Unset):
        tag (str | Unset):
        comment (int | Unset):
        kind (GetImageKind | Unset):
        width (GetImageWidth | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
     """


    kwargs = _get_kwargs(
        forge=forge,
url_query=url_query,
full_name=full_name,
number=number,
tag=tag,
comment=comment,
kind=kind,
width=width,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    forge: GetImageForge,
    url_query: str,
    full_name: str | Unset = UNSET,
    number: int | Unset = UNSET,
    tag: str | Unset = UNSET,
    comment: int | Unset = UNSET,
    kind: GetImageKind | Unset = UNSET,
    width: GetImageWidth | Unset = UNSET,

) -> Error | None:
    """ Read an image embedded in a forge's Markdown, through the server

     The details dialog shows the images in a description or comment by
    pointing its `<img>` here, never at the forge or a third party. The
    server fetches the image and returns the bytes, so the browser sends no
    request to another host, and a private repository's attachment loads
    without the forge token ever reaching the browser.

    Only the forge the item belongs to is reached. Forgejo: the saved
    instance, with the saved token sent to that host only. GitHub:
    `github.com` and its user-content hosts (`user-images`,
    `private-user-images`, `raw`, `gist`, `avatars` and `repository-images`
    under `githubusercontent.com`), without a
    token, since its attachment links are signed. A
    `github.com/user-attachments/...` link in a private repository is not
    served unsigned, so when `fullName` and `number` (or `tag`, or the
    `comment` it was posted in) name where it sits, the server reads that
    item's or comment's rendered HTML through the
    GitHub API with the saved token and fetches the signed address found
    there instead, without the token. If the lookup finds nothing or fails, or the signed address is on
    a host
    that isn't allowed or doesn't load, the link is fetched as written.
    Each such image costs one GitHub API request, which is never served from
    the ETag cache because the signature expires. Any other host, scheme or
    address answers 403 without a request. A redirect is followed only to
    another allowed host, and at most three times. GitHub's hosts are also
    refused at connect time if they resolve to a non-public address.

    The body must be a PNG, JPEG, GIF or WebP by its own bytes, not by the
    host's `Content-Type`, and at most 8 MiB (512 KiB with `kind=avatar`).
    SVG and anything else answers 415.

    The cost is bounded. At most 8 fetches run upstream at once; another
    request waits up to 5 seconds for a slot, then answers 503 with
    `Retry-After`. A fetched image is served again from a server-side cache
    for 5 minutes, without a new upstream fetch. The answer carries
    `nosniff` and a sandboxing `Content-Security-Policy`, and is cacheable
    by the browser for an hour.

    Args:
        forge (GetImageForge):
        url_query (str):
        full_name (str | Unset):
        number (int | Unset):
        tag (str | Unset):
        comment (int | Unset):
        kind (GetImageKind | Unset):
        width (GetImageWidth | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
     """


    return (await asyncio_detailed(
        client=client,
forge=forge,
url_query=url_query,
full_name=full_name,
number=number,
tag=tag,
comment=comment,
kind=kind,
width=width,

    )).parsed

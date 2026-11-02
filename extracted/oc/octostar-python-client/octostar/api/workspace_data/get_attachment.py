from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import quote
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET
from ... import errors

from ...types import UNSET, Unset
from ...models.get_attachment_response_401 import GetAttachmentResponse401
from typing import Union
from typing import cast
from typing import Optional
from ...models.get_attachment_response_200 import GetAttachmentResponse200
from typing import Dict


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    workspace: str,
    file_path: str,
    *,
    client: Client = None,
    no_redirect: Union[Unset, None, str] = UNSET,
    return_url: Union[Unset, None, bool] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    # API uses single {path} param that combines workspace and file_path
    full_path = f"{quote(workspace, safe='')}/{quote(file_path, safe='/')}"
    url = "{}/api/v1/files/attachments/{}".format(base_url, full_path)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    params: Dict[str, Any] = {}
    params["no_redirect"] = no_redirect
    params["return_url"] = return_url
    params["content_disposition"] = content_disposition
    params["content_type"] = content_type
    params["external_url"] = external_url

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        response_200 = GetAttachmentResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.MOVED_PERMANENTLY:
        response_301 = cast(Any, None)
        return response_301
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetAttachmentResponse401.from_dict(response.json())

        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    response_kwargs = {
        "status_code": HTTPStatus(response.status_code),
        "content": response.content,
        "headers": response.headers,
        "parsed": _parse_response(client=client, response=response),
    }
    return Response(**response_kwargs)


def _build_chunk_response(
    *, client: Client = None, response: httpx.Response, chunk: bytes
) -> Response[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    response_kwargs = {
        "status_code": HTTPStatus(response.status_code),
        "content": chunk,
        "headers": response.headers,
        "parsed": None,  # cannot parse incomplete chunks of data, we leave it to the user
    }
    return Response(**response_kwargs)


def sync_detailed(
    workspace: str,
    file_path: str,
    *,
    client: Client = None,
    no_redirect: Union[Unset, None, str] = UNSET,
    return_url: Union[Unset, None, bool] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]:
    """## Get S3 attachments operation

      This operation will get attachments given a workspace and file_path

    ### Args:
    * `workspace`: workspace (str):
    * `file_path`: file_path (str):
    * `no_redirect`: no_redirect (Union[Unset, None, str]):
    * `content_disposition`: content_disposition (Union[Unset, None, str]):
    * `content_type`: content_type (Union[Unset, None, str]):
    * `external_url`: external_url (Union[Unset, None, bool]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        workspace=workspace,
        file_path=file_path,
        client=client,
        no_redirect=no_redirect,
        return_url=return_url,
        content_disposition=content_disposition,
        content_type=content_type,
        external_url=external_url,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )
    if response.is_error:
        print(
            f"{str(response.status_code)} Error: {response.text} for request",
            str(kwargs),
        )
    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    file_path: str,
    *,
    client: Client = None,
    no_redirect: Union[Unset, None, str] = UNSET,
    return_url: Union[Unset, None, bool] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]:
    """## Get S3 attachments operation

      This operation will get attachments given a workspace and file_path

    ### Args:
    * `workspace`: workspace (str):
    * `file_path`: file_path (str):
    * `no_redirect`: no_redirect (Union[Unset, None, str]):
    * `content_disposition`: content_disposition (Union[Unset, None, str]):
    * `content_type`: content_type (Union[Unset, None, str]):
    * `external_url`: external_url (Union[Unset, None, bool]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]`
    """

    return sync_detailed(
        workspace=workspace,
        file_path=file_path,
        client=client,
        no_redirect=no_redirect,
        return_url=return_url,
        content_disposition=content_disposition,
        content_type=content_type,
        external_url=external_url,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    file_path: str,
    *,
    client: Client = None,
    no_redirect: Union[Unset, None, str] = UNSET,
    return_url: Union[Unset, None, bool] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]:
    """## Get S3 attachments operation

      This operation will get attachments given a workspace and file_path

    ### Args:
    * `workspace`: workspace (str):
    * `file_path`: file_path (str):
    * `no_redirect`: no_redirect (Union[Unset, None, str]):
    * `content_disposition`: content_disposition (Union[Unset, None, str]):
    * `content_type`: content_type (Union[Unset, None, str]):
    * `external_url`: external_url (Union[Unset, None, bool]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        workspace=workspace,
        file_path=file_path,
        client=client,
        no_redirect=no_redirect,
        return_url=return_url,
        content_disposition=content_disposition,
        content_type=content_type,
        external_url=external_url,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    file_path: str,
    *,
    client: Client = None,
    no_redirect: Union[Unset, None, str] = UNSET,
    return_url: Union[Unset, None, bool] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]]:
    """## Get S3 attachments operation

      This operation will get attachments given a workspace and file_path

    ### Args:
    * `workspace`: workspace (str):
    * `file_path`: file_path (str):
    * `no_redirect`: no_redirect (Union[Unset, None, str]):
    * `content_disposition`: content_disposition (Union[Unset, None, str]):
    * `content_type`: content_type (Union[Unset, None, str]):
    * `external_url`: external_url (Union[Unset, None, bool]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Any, GetAttachmentResponse200, GetAttachmentResponse401]`
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            file_path=file_path,
            client=client,
            no_redirect=no_redirect,
            return_url=return_url,
            content_disposition=content_disposition,
            content_type=content_type,
            external_url=external_url,
            accept=accept,
        )
    ).parsed

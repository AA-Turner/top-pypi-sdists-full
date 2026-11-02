from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET
from ... import errors

from ...models.get_permissions_response_400 import GetPermissionsResponse400
from ...types import UNSET, Unset
from ...models.get_permissions_response_401 import GetPermissionsResponse401
from typing import Union
from typing import cast
from typing import Optional
from ...models.get_permissions_response_500 import GetPermissionsResponse500
from ...models.get_permissions_response_200 import GetPermissionsResponse200
from typing import Dict


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    os_workspace: Union[Unset, None, str] = UNSET,
    os_workspaces: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/permissions/workspace-permissions".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    workspaces: list = []
    if not isinstance(os_workspace, Unset) and os_workspace is not None:
        workspaces.append(os_workspace)
    if not isinstance(os_workspaces, Unset) and os_workspaces is not None:
        workspaces.extend(os_workspaces.split(","))

    json_body: Dict[str, Any] = {}
    if workspaces:
        json_body["workspaces"] = workspaces

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_body,
    }


def _parse_response(*, client: Client = None, response: httpx.Response) -> Optional[
    Union[
        GetPermissionsResponse200,
        GetPermissionsResponse400,
        GetPermissionsResponse401,
        GetPermissionsResponse500,
    ]
]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        response_200 = GetPermissionsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetPermissionsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetPermissionsResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = GetPermissionsResponse500.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client = None, response: httpx.Response) -> Response[
    Union[
        GetPermissionsResponse200,
        GetPermissionsResponse400,
        GetPermissionsResponse401,
        GetPermissionsResponse500,
    ]
]:
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
) -> Response[
    Union[
        GetPermissionsResponse200,
        GetPermissionsResponse400,
        GetPermissionsResponse401,
        GetPermissionsResponse500,
    ]
]:
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
    *,
    client: Client = None,
    os_workspace: Union[Unset, None, str] = UNSET,
    os_workspaces: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[
    Union[
        GetPermissionsResponse200,
        GetPermissionsResponse400,
        GetPermissionsResponse401,
        GetPermissionsResponse500,
    ]
]:
    """## Get my permission for a workspace

      Get the highest permission I have for the workspace. 0=No permission, 1=Read, 2=Write, 4=Admin

    ### Args:
    * `os_workspace`: os_workspace (Union[Unset, None, str]):
    * `os_workspaces`: os_workspaces (Union[Unset, None, str]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[GetPermissionsResponse200, GetPermissionsResponse400, GetPermissionsResponse401, GetPermissionsResponse500]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        os_workspace=os_workspace,
        os_workspaces=os_workspaces,
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
    *,
    client: Client = None,
    os_workspace: Union[Unset, None, str] = UNSET,
    os_workspaces: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[
    Union[
        GetPermissionsResponse200,
        GetPermissionsResponse400,
        GetPermissionsResponse401,
        GetPermissionsResponse500,
    ]
]:
    """## Get my permission for a workspace

      Get the highest permission I have for the workspace. 0=No permission, 1=Read, 2=Write, 4=Admin

    ### Args:
    * `os_workspace`: os_workspace (Union[Unset, None, str]):
    * `os_workspaces`: os_workspaces (Union[Unset, None, str]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[GetPermissionsResponse200, GetPermissionsResponse400, GetPermissionsResponse401, GetPermissionsResponse500]`
    """

    return sync_detailed(
        client=client,
        os_workspace=os_workspace,
        os_workspaces=os_workspaces,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    os_workspace: Union[Unset, None, str] = UNSET,
    os_workspaces: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[
    Union[
        GetPermissionsResponse200,
        GetPermissionsResponse400,
        GetPermissionsResponse401,
        GetPermissionsResponse500,
    ]
]:
    """## Get my permission for a workspace

      Get the highest permission I have for the workspace. 0=No permission, 1=Read, 2=Write, 4=Admin

    ### Args:
    * `os_workspace`: os_workspace (Union[Unset, None, str]):
    * `os_workspaces`: os_workspaces (Union[Unset, None, str]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[GetPermissionsResponse200, GetPermissionsResponse400, GetPermissionsResponse401, GetPermissionsResponse500]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        os_workspace=os_workspace,
        os_workspaces=os_workspaces,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    os_workspace: Union[Unset, None, str] = UNSET,
    os_workspaces: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[
    Union[
        GetPermissionsResponse200,
        GetPermissionsResponse400,
        GetPermissionsResponse401,
        GetPermissionsResponse500,
    ]
]:
    """## Get my permission for a workspace

      Get the highest permission I have for the workspace. 0=No permission, 1=Read, 2=Write, 4=Admin

    ### Args:
    * `os_workspace`: os_workspace (Union[Unset, None, str]):
    * `os_workspaces`: os_workspaces (Union[Unset, None, str]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[GetPermissionsResponse200, GetPermissionsResponse400, GetPermissionsResponse401, GetPermissionsResponse500]`
    """

    return (
        await asyncio_detailed(
            client=client,
            os_workspace=os_workspace,
            os_workspaces=os_workspaces,
            accept=accept,
        )
    ).parsed

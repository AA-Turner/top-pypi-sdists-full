from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET
from ... import errors

from ...types import UNSET, Unset
from ...models.list_apps_response_401 import ListAppsResponse401
from typing import cast, List
from ...models.app_status import AppStatus
from typing import Union
from typing import cast
from ...models.list_apps_response_500 import ListAppsResponse500
from typing import Dict


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/apps/".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Union[ListAppsResponse401, ListAppsResponse500, List["AppStatus"]]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        apps_list = (
            _response_200.get("apps", _response_200)
            if isinstance(_response_200, dict)
            else _response_200
        )

        for componentsschemas_app_or_job_status_list_item_data in apps_list:
            componentsschemas_app_or_job_status_list_item = AppStatus.from_dict(
                componentsschemas_app_or_job_status_list_item_data
            )

            response_200.append(componentsschemas_app_or_job_status_list_item)

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ListAppsResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ListAppsResponse500.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[ListAppsResponse401, ListAppsResponse500, List["AppStatus"]]]:
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
) -> Response[Union[ListAppsResponse401, ListAppsResponse500, List["AppStatus"]]]:
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
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[ListAppsResponse401, ListAppsResponse500, List["AppStatus"]]]:
    """## List running apps

      list all the apps you are authorized to see. If you are an admin, you will see all the apps.

    ### Args:
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[ListAppsResponse401, ListAppsResponse500, List['AppStatus']]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
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
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[ListAppsResponse401, ListAppsResponse500, List["AppStatus"]]]:
    """## List running apps

      list all the apps you are authorized to see. If you are an admin, you will see all the apps.

    ### Args:
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[ListAppsResponse401, ListAppsResponse500, List['AppStatus']]`
    """

    return sync_detailed(
        client=client,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[ListAppsResponse401, ListAppsResponse500, List["AppStatus"]]]:
    """## List running apps

      list all the apps you are authorized to see. If you are an admin, you will see all the apps.

    ### Args:
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[ListAppsResponse401, ListAppsResponse500, List['AppStatus']]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[ListAppsResponse401, ListAppsResponse500, List["AppStatus"]]]:
    """## List running apps

      list all the apps you are authorized to see. If you are an admin, you will see all the apps.

    ### Args:
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[ListAppsResponse401, ListAppsResponse500, List['AppStatus']]`
    """

    return (
        await asyncio_detailed(
            client=client,
            accept=accept,
        )
    ).parsed

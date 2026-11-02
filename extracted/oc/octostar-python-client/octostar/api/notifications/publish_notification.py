from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET
from ... import errors

from ...models.os_notification import OsNotification


def wrap_list_as_object(items: List, key: str) -> Dict[str, Any]:
    """Wrap a list of items in an object with the given key.

    This bridges SDK list format to API object format.
    """
    return {
        key: [item.to_dict() if hasattr(item, "to_dict") else item for item in items]
    }


from ...types import UNSET, Unset
from typing import cast, List
from typing import Union
from typing import cast
from ...models.acknowledgement import Acknowledgement
from typing import Dict
from ...models.publish_notification_response_401 import PublishNotificationResponse401


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    json_body: List["OsNotification"],
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/notifications/".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    # Bridge SDK list format to API object format
    json_json_body = wrap_list_as_object(json_body, "notifications")

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Union[Acknowledgement, PublishNotificationResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        response_200 = Acknowledgement.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.CREATED:
        response_201 = Acknowledgement.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Acknowledgement.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = PublishNotificationResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Acknowledgement.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[Acknowledgement, PublishNotificationResponse401]]:
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
) -> Response[Union[Acknowledgement, PublishNotificationResponse401]]:
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
    json_body: List["OsNotification"],
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Acknowledgement, PublishNotificationResponse401]]:
    """## Get the list of notifications for the session

      Get the list of notifications for the session

    ### Args:
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List['OsNotification']):

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Acknowledgement, PublishNotificationResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
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
    json_body: List["OsNotification"],
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Acknowledgement, PublishNotificationResponse401]]:
    """## Get the list of notifications for the session

      Get the list of notifications for the session

    ### Args:
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List['OsNotification']):

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Acknowledgement, PublishNotificationResponse401]`
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    json_body: List["OsNotification"],
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Acknowledgement, PublishNotificationResponse401]]:
    """## Get the list of notifications for the session

      Get the list of notifications for the session

    ### Args:
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List['OsNotification']):

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Acknowledgement, PublishNotificationResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    json_body: List["OsNotification"],
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Acknowledgement, PublishNotificationResponse401]]:
    """## Get the list of notifications for the session

      Get the list of notifications for the session

    ### Args:
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List['OsNotification']):

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Acknowledgement, PublishNotificationResponse401]`
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            accept=accept,
        )
    ).parsed

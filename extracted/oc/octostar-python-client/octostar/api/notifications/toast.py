from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response, UNSET, Unset
from ... import errors
from ...models.toast_response_401 import ToastResponse401
from ...models.toast_level import ToastLevel
from ...models.acknowledgement import Acknowledgement


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    message: Union[Unset, None, str] = UNSET,
    result_url: Union[Unset, None, str] = UNSET,
    description: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, ToastLevel] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/notifications/toast".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    json_body: Dict[str, Any] = {}
    if not isinstance(message, Unset) and message is not None:
        json_body["message"] = message
    if not isinstance(result_url, Unset) and result_url is not None:
        json_body["result_url"] = result_url
    if not isinstance(description, Unset) and description is not None:
        json_body["description"] = description
    if not isinstance(level, Unset) and level is not None:
        json_body["level"] = level.value if level else None

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_body,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Union[Acknowledgement, Any, ToastResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    if response.status_code == HTTPStatus.OK:
        return Acknowledgement.from_dict(response.json())
    if response.status_code == HTTPStatus.CREATED:
        return Acknowledgement.from_dict(response.json())
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return ToastResponse401.from_dict(response.json())
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        return cast(Any, None)
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[Acknowledgement, Any, ToastResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client = None,
    message: Union[Unset, None, str] = UNSET,
    result_url: Union[Unset, None, str] = UNSET,
    description: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, ToastLevel] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Acknowledgement, Any, ToastResponse401]]:
    """## Show a desktop notification

      Show a desktop notification

    ### Args:
    * `message`: message (Union[Unset, None, str]):
    * `result_url`: result_url (Union[Unset, None, str]):
    * `description`: description (Union[Unset, None, str]):
    * `level`: level (Union[Unset, None, ToastLevel]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Acknowledgement, Any, ToastResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    kwargs = _get_kwargs(
        client=client,
        message=message,
        result_url=result_url,
        description=description,
        level=level,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )
    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client = None,
    message: Union[Unset, None, str] = UNSET,
    result_url: Union[Unset, None, str] = UNSET,
    description: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, ToastLevel] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Acknowledgement, Any, ToastResponse401]]:
    """## Show a desktop notification

      Show a desktop notification

    ### Args:
    * `message`: message (Union[Unset, None, str]):
    * `result_url`: result_url (Union[Unset, None, str]):
    * `description`: description (Union[Unset, None, str]):
    * `level`: level (Union[Unset, None, ToastLevel]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Acknowledgement, Any, ToastResponse401]`
    """

    return sync_detailed(
        client=client,
        message=message,
        result_url=result_url,
        description=description,
        level=level,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    message: Union[Unset, None, str] = UNSET,
    result_url: Union[Unset, None, str] = UNSET,
    description: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, ToastLevel] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Acknowledgement, Any, ToastResponse401]]:
    """## Show a desktop notification

      Show a desktop notification

    ### Args:
    * `message`: message (Union[Unset, None, str]):
    * `result_url`: result_url (Union[Unset, None, str]):
    * `description`: description (Union[Unset, None, str]):
    * `level`: level (Union[Unset, None, ToastLevel]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Acknowledgement, Any, ToastResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    kwargs = _get_kwargs(
        client=client,
        message=message,
        result_url=result_url,
        description=description,
        level=level,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    message: Union[Unset, None, str] = UNSET,
    result_url: Union[Unset, None, str] = UNSET,
    description: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, ToastLevel] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Acknowledgement, Any, ToastResponse401]]:
    """## Show a desktop notification

      Show a desktop notification

    ### Args:
    * `message`: message (Union[Unset, None, str]):
    * `result_url`: result_url (Union[Unset, None, str]):
    * `description`: description (Union[Unset, None, str]):
    * `level`: level (Union[Unset, None, ToastLevel]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Acknowledgement, Any, ToastResponse401]`
    """

    return (
        await asyncio_detailed(
            client=client,
            message=message,
            result_url=result_url,
            description=description,
            level=level,
            accept=accept,
        )
    ).parsed

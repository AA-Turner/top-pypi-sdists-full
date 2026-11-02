from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET, Unset
from ... import errors
from ...models.list_app_jobs_response_401 import ListAppJobsResponse401
from ...models.list_app_jobs_response_500 import ListAppJobsResponse500
from ...models.app_status import AppStatus


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    app_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/apps/jobs/by-app/{}".format(base_url, app_id)

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
) -> Optional[Union[ListAppJobsResponse401, ListAppJobsResponse500, List["AppStatus"]]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()

        # New API returns { "jobs": [...] }, extract the jobs list
        jobs_list = (
            _response_200.get("jobs", _response_200)
            if isinstance(_response_200, dict)
            else _response_200
        )

        for job_data in jobs_list:
            # Map new JobResponse format to old AppStatus format for backward compatibility
            # JobResponse: job_id, ancestor, status, namespace, creation_timestamp, start_time, completion_time, active, succeeded, failed
            # AppStatus: name, uid, namespace, app_state, state, active, ready, failed, succeeded, creation_timestamp, start_time, completion_time
            mapped_data = {
                "name": job_data.get("job_id", job_data.get("name")),
                "uid": job_data.get("job_id", job_data.get("uid")),
                "namespace": job_data.get("namespace"),
                "app_state": job_data.get("status", job_data.get("app_state")),
                "state": job_data.get("status", job_data.get("state")),
                "active": job_data.get("active"),
                "ready": job_data.get("ready", 0),
                "failed": job_data.get("failed"),
                "succeeded": job_data.get("succeeded"),
                "creation_timestamp": job_data.get("creation_timestamp"),
                "start_time": job_data.get("start_time"),
                "completion_time": job_data.get("completion_time"),
            }
            componentsschemas_app_or_job_status_list_item = AppStatus.from_dict(
                mapped_data
            )
            response_200.append(componentsschemas_app_or_job_status_list_item)

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ListAppJobsResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ListAppJobsResponse500.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[ListAppJobsResponse401, ListAppJobsResponse500, List["AppStatus"]]]:
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
) -> Response[Union[ListAppJobsResponse401, ListAppJobsResponse500, List["AppStatus"]]]:
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
    app_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[ListAppJobsResponse401, ListAppJobsResponse500, List["AppStatus"]]]:
    """## List running jobs for a given parent app

      List all active jobs that were created by this app.

    ### Args:
    * `app_id`: app_id (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[ListAppJobsResponse401, ListAppJobsResponse500, List['AppStatus']]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        app_id=app_id,
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
    app_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[ListAppJobsResponse401, ListAppJobsResponse500, List["AppStatus"]]]:
    """## List running jobs for a given parent app

      List all active jobs that were created by this app.

    ### Args:
    * `app_id`: app_id (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[ListAppJobsResponse401, ListAppJobsResponse500, List['AppStatus']]`
    """

    return sync_detailed(
        app_id=app_id,
        client=client,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    app_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[ListAppJobsResponse401, ListAppJobsResponse500, List["AppStatus"]]]:
    """## List running jobs for a given parent app

      List all active jobs that were created by this app.

    ### Args:
    * `app_id`: app_id (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[ListAppJobsResponse401, ListAppJobsResponse500, List['AppStatus']]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        app_id=app_id,
        client=client,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[ListAppJobsResponse401, ListAppJobsResponse500, List["AppStatus"]]]:
    """## List running jobs for a given parent app

      List all active jobs that were created by this app.

    ### Args:
    * `app_id`: app_id (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[ListAppJobsResponse401, ListAppJobsResponse500, List['AppStatus']]`
    """

    return (
        await asyncio_detailed(
            app_id=app_id,
            client=client,
            accept=accept,
        )
    ).parsed

import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.customer_user_o_enum import CustomerUserOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_uuid: UUID,
    *,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, CustomerUserOEnum] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_agreement_date: Union[Unset, str] = UNSET
    if not isinstance(agreement_date, Unset):
        json_agreement_date = agreement_date.isoformat()
    params["agreement_date"] = json_agreement_date

    params["civil_number"] = civil_number

    json_date_joined: Union[Unset, str] = UNSET
    if not isinstance(date_joined, Unset):
        json_date_joined = date_joined.isoformat()
    params["date_joined"] = json_date_joined

    params["description"] = description

    params["email"] = email

    params["full_name"] = full_name

    params["is_active"] = is_active

    params["job_title"] = job_title

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    params["native_name"] = native_name

    json_o: Union[Unset, str] = UNSET
    if not isinstance(o, Unset):
        json_o = o.value

    params["o"] = json_o

    params["organization"] = organization

    params["page"] = page

    params["page_size"] = page_size

    params["phone_number"] = phone_number

    params["registration_method"] = registration_method

    params["user_keyword"] = user_keyword

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": f"/api/projects/{project_uuid}/other_users/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, CustomerUserOEnum] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        project_uuid (UUID):
        agreement_date (Union[Unset, datetime.datetime]):
        civil_number (Union[Unset, str]):
        date_joined (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        full_name (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        job_title (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, CustomerUserOEnum]):
        organization (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        phone_number (Union[Unset, str]):
        registration_method (Union[Unset, str]):
        user_keyword (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
        agreement_date=agreement_date,
        civil_number=civil_number,
        date_joined=date_joined,
        description=description,
        email=email,
        full_name=full_name,
        is_active=is_active,
        job_title=job_title,
        modified=modified,
        native_name=native_name,
        o=o,
        organization=organization,
        page=page,
        page_size=page_size,
        phone_number=phone_number,
        registration_method=registration_method,
        user_keyword=user_keyword,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, CustomerUserOEnum] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        project_uuid (UUID):
        agreement_date (Union[Unset, datetime.datetime]):
        civil_number (Union[Unset, str]):
        date_joined (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        full_name (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        job_title (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, CustomerUserOEnum]):
        organization (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        phone_number (Union[Unset, str]):
        registration_method (Union[Unset, str]):
        user_keyword (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        project_uuid=project_uuid,
        client=client,
        agreement_date=agreement_date,
        civil_number=civil_number,
        date_joined=date_joined,
        description=description,
        email=email,
        full_name=full_name,
        is_active=is_active,
        job_title=job_title,
        modified=modified,
        native_name=native_name,
        o=o,
        organization=organization,
        page=page,
        page_size=page_size,
        phone_number=phone_number,
        registration_method=registration_method,
        user_keyword=user_keyword,
        username=username,
    ).parsed


async def asyncio_detailed(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, CustomerUserOEnum] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        project_uuid (UUID):
        agreement_date (Union[Unset, datetime.datetime]):
        civil_number (Union[Unset, str]):
        date_joined (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        full_name (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        job_title (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, CustomerUserOEnum]):
        organization (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        phone_number (Union[Unset, str]):
        registration_method (Union[Unset, str]):
        user_keyword (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
        agreement_date=agreement_date,
        civil_number=civil_number,
        date_joined=date_joined,
        description=description,
        email=email,
        full_name=full_name,
        is_active=is_active,
        job_title=job_title,
        modified=modified,
        native_name=native_name,
        o=o,
        organization=organization,
        page=page,
        page_size=page_size,
        phone_number=phone_number,
        registration_method=registration_method,
        user_keyword=user_keyword,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, CustomerUserOEnum] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        project_uuid (UUID):
        agreement_date (Union[Unset, datetime.datetime]):
        civil_number (Union[Unset, str]):
        date_joined (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        full_name (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        job_title (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, CustomerUserOEnum]):
        organization (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        phone_number (Union[Unset, str]):
        registration_method (Union[Unset, str]):
        user_keyword (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            project_uuid=project_uuid,
            client=client,
            agreement_date=agreement_date,
            civil_number=civil_number,
            date_joined=date_joined,
            description=description,
            email=email,
            full_name=full_name,
            is_active=is_active,
            job_title=job_title,
            modified=modified,
            native_name=native_name,
            o=o,
            organization=organization,
            page=page,
            page_size=page_size,
            phone_number=phone_number,
            registration_method=registration_method,
            user_keyword=user_keyword,
            username=username,
        )
    ).parsed

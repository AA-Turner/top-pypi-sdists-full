from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.open_stack_tenant_quota import OpenStackTenantQuota
from ...models.open_stack_tenant_quota_request import OpenStackTenantQuotaRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: OpenStackTenantQuotaRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/openstack-tenants/{uuid}/set_quotas/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OpenStackTenantQuota:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OpenStackTenantQuota.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OpenStackTenantQuota]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OpenStackTenantQuotaRequest,
) -> Response[OpenStackTenantQuota]:
    """Set tenant quotas

     A quota can be set for a particular tenant. Only staff users and service provider owners/managers
    can do that.
    In order to set quota submit POST request to /api/openstack-tenants/<uuid>/set_quotas/.
    The quota values are propagated to the backend.

    The following quotas are supported. All values are expected to be integers:

    - instances - maximal number of created instances.
    - ram - maximal size of ram for allocation. In MiB_.
    - storage - maximal size of storage for allocation. In MiB_.
    - vcpu - maximal number of virtual cores for allocation.
    - security_group_count - maximal number of created security groups.
    - security_group_rule_count - maximal number of created security groups rules.
    - volumes - maximal number of created volumes.
    - snapshots - maximal number of created snapshots.

    It is possible to update quotas by one or by submitting all the fields in one request.
    Waldur will attempt to update the provided quotas. Please note, that if provided quotas are
    conflicting with the backend (e.g. requested number of instances is below of the already existing
    ones),
    some quotas might not be applied.

    .. _MiB: http://en.wikipedia.org/wiki/Mebibyte

    Response code of a successful request is **202 ACCEPTED**.
    In case tenant is in a non-stable status, the response would be **409 CONFLICT**.
    In this case REST client is advised to repeat the request after some time.
    On successful completion the task will synchronize quotas with the backend.

    Args:
        uuid (UUID):
        body (OpenStackTenantQuotaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OpenStackTenantQuota]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OpenStackTenantQuotaRequest,
) -> OpenStackTenantQuota:
    """Set tenant quotas

     A quota can be set for a particular tenant. Only staff users and service provider owners/managers
    can do that.
    In order to set quota submit POST request to /api/openstack-tenants/<uuid>/set_quotas/.
    The quota values are propagated to the backend.

    The following quotas are supported. All values are expected to be integers:

    - instances - maximal number of created instances.
    - ram - maximal size of ram for allocation. In MiB_.
    - storage - maximal size of storage for allocation. In MiB_.
    - vcpu - maximal number of virtual cores for allocation.
    - security_group_count - maximal number of created security groups.
    - security_group_rule_count - maximal number of created security groups rules.
    - volumes - maximal number of created volumes.
    - snapshots - maximal number of created snapshots.

    It is possible to update quotas by one or by submitting all the fields in one request.
    Waldur will attempt to update the provided quotas. Please note, that if provided quotas are
    conflicting with the backend (e.g. requested number of instances is below of the already existing
    ones),
    some quotas might not be applied.

    .. _MiB: http://en.wikipedia.org/wiki/Mebibyte

    Response code of a successful request is **202 ACCEPTED**.
    In case tenant is in a non-stable status, the response would be **409 CONFLICT**.
    In this case REST client is advised to repeat the request after some time.
    On successful completion the task will synchronize quotas with the backend.

    Args:
        uuid (UUID):
        body (OpenStackTenantQuotaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OpenStackTenantQuota
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OpenStackTenantQuotaRequest,
) -> Response[OpenStackTenantQuota]:
    """Set tenant quotas

     A quota can be set for a particular tenant. Only staff users and service provider owners/managers
    can do that.
    In order to set quota submit POST request to /api/openstack-tenants/<uuid>/set_quotas/.
    The quota values are propagated to the backend.

    The following quotas are supported. All values are expected to be integers:

    - instances - maximal number of created instances.
    - ram - maximal size of ram for allocation. In MiB_.
    - storage - maximal size of storage for allocation. In MiB_.
    - vcpu - maximal number of virtual cores for allocation.
    - security_group_count - maximal number of created security groups.
    - security_group_rule_count - maximal number of created security groups rules.
    - volumes - maximal number of created volumes.
    - snapshots - maximal number of created snapshots.

    It is possible to update quotas by one or by submitting all the fields in one request.
    Waldur will attempt to update the provided quotas. Please note, that if provided quotas are
    conflicting with the backend (e.g. requested number of instances is below of the already existing
    ones),
    some quotas might not be applied.

    .. _MiB: http://en.wikipedia.org/wiki/Mebibyte

    Response code of a successful request is **202 ACCEPTED**.
    In case tenant is in a non-stable status, the response would be **409 CONFLICT**.
    In this case REST client is advised to repeat the request after some time.
    On successful completion the task will synchronize quotas with the backend.

    Args:
        uuid (UUID):
        body (OpenStackTenantQuotaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OpenStackTenantQuota]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OpenStackTenantQuotaRequest,
) -> OpenStackTenantQuota:
    """Set tenant quotas

     A quota can be set for a particular tenant. Only staff users and service provider owners/managers
    can do that.
    In order to set quota submit POST request to /api/openstack-tenants/<uuid>/set_quotas/.
    The quota values are propagated to the backend.

    The following quotas are supported. All values are expected to be integers:

    - instances - maximal number of created instances.
    - ram - maximal size of ram for allocation. In MiB_.
    - storage - maximal size of storage for allocation. In MiB_.
    - vcpu - maximal number of virtual cores for allocation.
    - security_group_count - maximal number of created security groups.
    - security_group_rule_count - maximal number of created security groups rules.
    - volumes - maximal number of created volumes.
    - snapshots - maximal number of created snapshots.

    It is possible to update quotas by one or by submitting all the fields in one request.
    Waldur will attempt to update the provided quotas. Please note, that if provided quotas are
    conflicting with the backend (e.g. requested number of instances is below of the already existing
    ones),
    some quotas might not be applied.

    .. _MiB: http://en.wikipedia.org/wiki/Mebibyte

    Response code of a successful request is **202 ACCEPTED**.
    In case tenant is in a non-stable status, the response would be **409 CONFLICT**.
    In this case REST client is advised to repeat the request after some time.
    On successful completion the task will synchronize quotas with the backend.

    Args:
        uuid (UUID):
        body (OpenStackTenantQuotaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OpenStackTenantQuota
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed

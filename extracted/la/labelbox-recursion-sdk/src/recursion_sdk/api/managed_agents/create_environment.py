from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_create_environment_request import ManagedAgentsCreateEnvironmentRequest
from ...models.managed_agents_environment import ManagedAgentsEnvironment
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    body: ManagedAgentsCreateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["verify"] = verify


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/environments",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEnvironment.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 409:
        response_409 = ManagedAgentsApiError.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = ManagedAgentsApiError.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

    if response.status_code == 422:
        response_422 = ManagedAgentsApiError.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = ManagedAgentsApiError.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ManagedAgentsApiError.from_dict(response.json())



        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = ManagedAgentsApiError.from_dict(response.json())



        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]:
    """ Create environment

     Defines the sandbox an agent session runs in and returns the stored environment, including its
    generated environment_id. The provider must be one this deployment reports from
    listSandboxProviders. Nothing is provisioned here unless ?verify=true is passed, in which case a
    manual setup run starts immediately and the response's setup_verification names it. Otherwise
    compute is allocated when a session that references the environment starts. An environment with a
    setup script must be verified (createEnvironmentSetupRun) before a session on the runs or docker
    provider will start.

    Args:
        verify (bool | Unset): When true, a manual setup run is started as soon as the environment
            is saved, so one call both writes the configuration and begins proving it. The response is
            the environment with setup_verification.active_setup_run_id naming the run to poll; the
            status reads running unless an earlier verified verdict is being kept while it re-
            verifies. Ignored when the environment has no setup script.
        body (ManagedAgentsCreateEnvironmentRequest): Request body for creating an environment:
            the sandbox image, setup, compute sizing, networking, and lifecycle a session's sandbox is
            provisioned from. Server-managed fields are not accepted. Example: {'computer_use': True,
            'config': {'key': 'example'}, 'description': 'example', 'env_vars': {'key': 'example'},
            'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key':
            'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
            name', 'network_policy': {'key': 'example'}, 'privileged': True, 'provider': 'example',
            'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name',
            'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
            'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
            'regions': ['example']}, 'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key':
            'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1},
            'stopped_delete_after_seconds': 1}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]
     """


    kwargs = _get_kwargs(
        body=body,
verify=verify,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment | None:
    """ Create environment

     Defines the sandbox an agent session runs in and returns the stored environment, including its
    generated environment_id. The provider must be one this deployment reports from
    listSandboxProviders. Nothing is provisioned here unless ?verify=true is passed, in which case a
    manual setup run starts immediately and the response's setup_verification names it. Otherwise
    compute is allocated when a session that references the environment starts. An environment with a
    setup script must be verified (createEnvironmentSetupRun) before a session on the runs or docker
    provider will start.

    Args:
        verify (bool | Unset): When true, a manual setup run is started as soon as the environment
            is saved, so one call both writes the configuration and begins proving it. The response is
            the environment with setup_verification.active_setup_run_id naming the run to poll; the
            status reads running unless an earlier verified verdict is being kept while it re-
            verifies. Ignored when the environment has no setup script.
        body (ManagedAgentsCreateEnvironmentRequest): Request body for creating an environment:
            the sandbox image, setup, compute sizing, networking, and lifecycle a session's sandbox is
            provisioned from. Server-managed fields are not accepted. Example: {'computer_use': True,
            'config': {'key': 'example'}, 'description': 'example', 'env_vars': {'key': 'example'},
            'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key':
            'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
            name', 'network_policy': {'key': 'example'}, 'privileged': True, 'provider': 'example',
            'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name',
            'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
            'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
            'regions': ['example']}, 'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key':
            'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1},
            'stopped_delete_after_seconds': 1}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment
     """


    return sync_detailed(
        client=client,
body=body,
verify=verify,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]:
    """ Create environment

     Defines the sandbox an agent session runs in and returns the stored environment, including its
    generated environment_id. The provider must be one this deployment reports from
    listSandboxProviders. Nothing is provisioned here unless ?verify=true is passed, in which case a
    manual setup run starts immediately and the response's setup_verification names it. Otherwise
    compute is allocated when a session that references the environment starts. An environment with a
    setup script must be verified (createEnvironmentSetupRun) before a session on the runs or docker
    provider will start.

    Args:
        verify (bool | Unset): When true, a manual setup run is started as soon as the environment
            is saved, so one call both writes the configuration and begins proving it. The response is
            the environment with setup_verification.active_setup_run_id naming the run to poll; the
            status reads running unless an earlier verified verdict is being kept while it re-
            verifies. Ignored when the environment has no setup script.
        body (ManagedAgentsCreateEnvironmentRequest): Request body for creating an environment:
            the sandbox image, setup, compute sizing, networking, and lifecycle a session's sandbox is
            provisioned from. Server-managed fields are not accepted. Example: {'computer_use': True,
            'config': {'key': 'example'}, 'description': 'example', 'env_vars': {'key': 'example'},
            'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key':
            'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
            name', 'network_policy': {'key': 'example'}, 'privileged': True, 'provider': 'example',
            'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name',
            'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
            'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
            'regions': ['example']}, 'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key':
            'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1},
            'stopped_delete_after_seconds': 1}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]
     """


    kwargs = _get_kwargs(
        body=body,
verify=verify,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment | None:
    """ Create environment

     Defines the sandbox an agent session runs in and returns the stored environment, including its
    generated environment_id. The provider must be one this deployment reports from
    listSandboxProviders. Nothing is provisioned here unless ?verify=true is passed, in which case a
    manual setup run starts immediately and the response's setup_verification names it. Otherwise
    compute is allocated when a session that references the environment starts. An environment with a
    setup script must be verified (createEnvironmentSetupRun) before a session on the runs or docker
    provider will start.

    Args:
        verify (bool | Unset): When true, a manual setup run is started as soon as the environment
            is saved, so one call both writes the configuration and begins proving it. The response is
            the environment with setup_verification.active_setup_run_id naming the run to poll; the
            status reads running unless an earlier verified verdict is being kept while it re-
            verifies. Ignored when the environment has no setup script.
        body (ManagedAgentsCreateEnvironmentRequest): Request body for creating an environment:
            the sandbox image, setup, compute sizing, networking, and lifecycle a session's sandbox is
            provisioned from. Server-managed fields are not accepted. Example: {'computer_use': True,
            'config': {'key': 'example'}, 'description': 'example', 'env_vars': {'key': 'example'},
            'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key':
            'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
            name', 'network_policy': {'key': 'example'}, 'privileged': True, 'provider': 'example',
            'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name',
            'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
            'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
            'regions': ['example']}, 'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key':
            'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1},
            'stopped_delete_after_seconds': 1}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment
     """


    return (await asyncio_detailed(
        client=client,
body=body,
verify=verify,

    )).parsed

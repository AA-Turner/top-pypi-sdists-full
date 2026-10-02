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
from ...models.managed_agents_environment import ManagedAgentsEnvironment
from ...models.managed_agents_update_environment_request import ManagedAgentsUpdateEnvironmentRequest
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    environment_id: UUID,
    *,
    body: ManagedAgentsUpdateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["verify"] = verify


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/managed-agents/v1/environments/{environment_id}".format(environment_id=quote(str(environment_id), safe=""),),
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

    if response.status_code == 404:
        response_404 = ManagedAgentsApiError.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = ManagedAgentsApiError.from_dict(response.json())



        return response_409

    if response.status_code == 412:
        response_412 = ManagedAgentsApiError.from_dict(response.json())



        return response_412

    if response.status_code == 413:
        response_413 = ManagedAgentsApiError.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

    if response.status_code == 422:
        response_422 = ManagedAgentsApiError.from_dict(response.json())



        return response_422

    if response.status_code == 428:
        response_428 = ManagedAgentsApiError.from_dict(response.json())



        return response_428

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
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]:
    """ Update environment

     Applies a partial update and returns the stored environment; omitted fields keep their current
    values. Changing from a non-Runs provider to Runs with an absent or {} stored policy requires an
    explicit network_policy: {"version":"v1","rules":[]} for deny-all or {} for unrestricted egress. A
    provider is validated only when the request actually names one. Sending setup with an empty script
    clears the script; omitting setup leaves it. Any change to provider, image, setup (script or
    timeout), resources, workspace disk size, provider config, variables, secret references, mounts,
    network policy, or effective Docker privilege marks the previous setup verification stale; name,
    description, metadata, and http_port do not. Pass ?verify=true to re-run setup in the same call;
    that half is authorized as createEnvironmentSetupRun is, in addition to the update itself. Sessions
    already running keep the spec they started with, so a change takes effect on the next session start.
    A Runs update that changes a nonempty network_policy or enables privileged Docker requires
    expected_access with the network_policy and privileged values from the last environment read. A
    missing access snapshot returns 428; a stale one returns 412. A concurrent placement edit may return
    409; reload and retry.

    Args:
        environment_id (UUID): Environment id (UUID) as returned by createEnvironment or
            listEnvironments.
        verify (bool | Unset): When true, a manual setup run is started as soon as the update is
            saved. Read setup_verification.active_setup_run_id from the response and poll
            getEnvironmentSetupRun; setup_verification.setup_run_id keeps naming an earlier verified
            run while it re-verifies. Ignored when the environment has no setup script. Starting the
            run is authorized exactly as createEnvironmentSetupRun is, so a caller who may update the
            environment but may not start a setup run is refused with 403 rather than saved without
            one.
        body (ManagedAgentsUpdateEnvironmentRequest): A sandbox environment a session executes in:
            its provider, resources, mounts, setup steps and idle/delete lifecycle. Created and
            started independently of any session. Example: {'computer_use': True, 'config': {'key':
            'example'}, 'created_at': '2026-02-18T09:30:00Z', 'description': 'example', 'env_vars':
            {'key': 'example'}, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'expected_access': {'network_policy': {'key': 'example'}, 'privileged': True},
            'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key':
            'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
            name', 'network_policy': {'key': 'example'}, 'organization_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'privileged': True, 'provider': 'example',
            'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name',
            'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
            'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
            'regions': ['example']}, 'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key':
            'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1}, 'setup_updated_at':
            '2026-02-18T09:30:00Z', 'setup_updated_by_user_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'setup_verification': {'active_setup_run_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'fingerprint':
            'example', 'image': {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z',
            'computeId': 'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example',
            'imageId': 'example', 'runnerImage': 'example', 'setupRunId': 'example', 'sizeBytes': 1,
            'usable': True, 'warmup': 'example', 'warmupMessage': 'example'}, 'imageCapture': {'at':
            '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId':
            'example', 'status': 'failed'}, 'last_run': {'duration_ms': 1, 'exit_code': 1,
            'failed_command': 'example', 'failed_line': 1, 'hint': 'example', 'hint_code': 'example',
            'message': 'example', 'phase': 'example', 'setup_run_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example', 'stderr_tail': 'example'},
            'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True, 'status':
            'example', 'verified_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
            'setup_warnings': [{'code': 'example', 'line': 1, 'message': 'example'}],
            'stopped_delete_after_seconds': 1, 'updated_at': '2026-02-18T09:30:00Z'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
body=body,
verify=verify,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment | None:
    """ Update environment

     Applies a partial update and returns the stored environment; omitted fields keep their current
    values. Changing from a non-Runs provider to Runs with an absent or {} stored policy requires an
    explicit network_policy: {"version":"v1","rules":[]} for deny-all or {} for unrestricted egress. A
    provider is validated only when the request actually names one. Sending setup with an empty script
    clears the script; omitting setup leaves it. Any change to provider, image, setup (script or
    timeout), resources, workspace disk size, provider config, variables, secret references, mounts,
    network policy, or effective Docker privilege marks the previous setup verification stale; name,
    description, metadata, and http_port do not. Pass ?verify=true to re-run setup in the same call;
    that half is authorized as createEnvironmentSetupRun is, in addition to the update itself. Sessions
    already running keep the spec they started with, so a change takes effect on the next session start.
    A Runs update that changes a nonempty network_policy or enables privileged Docker requires
    expected_access with the network_policy and privileged values from the last environment read. A
    missing access snapshot returns 428; a stale one returns 412. A concurrent placement edit may return
    409; reload and retry.

    Args:
        environment_id (UUID): Environment id (UUID) as returned by createEnvironment or
            listEnvironments.
        verify (bool | Unset): When true, a manual setup run is started as soon as the update is
            saved. Read setup_verification.active_setup_run_id from the response and poll
            getEnvironmentSetupRun; setup_verification.setup_run_id keeps naming an earlier verified
            run while it re-verifies. Ignored when the environment has no setup script. Starting the
            run is authorized exactly as createEnvironmentSetupRun is, so a caller who may update the
            environment but may not start a setup run is refused with 403 rather than saved without
            one.
        body (ManagedAgentsUpdateEnvironmentRequest): A sandbox environment a session executes in:
            its provider, resources, mounts, setup steps and idle/delete lifecycle. Created and
            started independently of any session. Example: {'computer_use': True, 'config': {'key':
            'example'}, 'created_at': '2026-02-18T09:30:00Z', 'description': 'example', 'env_vars':
            {'key': 'example'}, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'expected_access': {'network_policy': {'key': 'example'}, 'privileged': True},
            'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key':
            'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
            name', 'network_policy': {'key': 'example'}, 'organization_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'privileged': True, 'provider': 'example',
            'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name',
            'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
            'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
            'regions': ['example']}, 'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key':
            'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1}, 'setup_updated_at':
            '2026-02-18T09:30:00Z', 'setup_updated_by_user_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'setup_verification': {'active_setup_run_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'fingerprint':
            'example', 'image': {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z',
            'computeId': 'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example',
            'imageId': 'example', 'runnerImage': 'example', 'setupRunId': 'example', 'sizeBytes': 1,
            'usable': True, 'warmup': 'example', 'warmupMessage': 'example'}, 'imageCapture': {'at':
            '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId':
            'example', 'status': 'failed'}, 'last_run': {'duration_ms': 1, 'exit_code': 1,
            'failed_command': 'example', 'failed_line': 1, 'hint': 'example', 'hint_code': 'example',
            'message': 'example', 'phase': 'example', 'setup_run_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example', 'stderr_tail': 'example'},
            'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True, 'status':
            'example', 'verified_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
            'setup_warnings': [{'code': 'example', 'line': 1, 'message': 'example'}],
            'stopped_delete_after_seconds': 1, 'updated_at': '2026-02-18T09:30:00Z'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment
     """


    return sync_detailed(
        environment_id=environment_id,
client=client,
body=body,
verify=verify,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]:
    """ Update environment

     Applies a partial update and returns the stored environment; omitted fields keep their current
    values. Changing from a non-Runs provider to Runs with an absent or {} stored policy requires an
    explicit network_policy: {"version":"v1","rules":[]} for deny-all or {} for unrestricted egress. A
    provider is validated only when the request actually names one. Sending setup with an empty script
    clears the script; omitting setup leaves it. Any change to provider, image, setup (script or
    timeout), resources, workspace disk size, provider config, variables, secret references, mounts,
    network policy, or effective Docker privilege marks the previous setup verification stale; name,
    description, metadata, and http_port do not. Pass ?verify=true to re-run setup in the same call;
    that half is authorized as createEnvironmentSetupRun is, in addition to the update itself. Sessions
    already running keep the spec they started with, so a change takes effect on the next session start.
    A Runs update that changes a nonempty network_policy or enables privileged Docker requires
    expected_access with the network_policy and privileged values from the last environment read. A
    missing access snapshot returns 428; a stale one returns 412. A concurrent placement edit may return
    409; reload and retry.

    Args:
        environment_id (UUID): Environment id (UUID) as returned by createEnvironment or
            listEnvironments.
        verify (bool | Unset): When true, a manual setup run is started as soon as the update is
            saved. Read setup_verification.active_setup_run_id from the response and poll
            getEnvironmentSetupRun; setup_verification.setup_run_id keeps naming an earlier verified
            run while it re-verifies. Ignored when the environment has no setup script. Starting the
            run is authorized exactly as createEnvironmentSetupRun is, so a caller who may update the
            environment but may not start a setup run is refused with 403 rather than saved without
            one.
        body (ManagedAgentsUpdateEnvironmentRequest): A sandbox environment a session executes in:
            its provider, resources, mounts, setup steps and idle/delete lifecycle. Created and
            started independently of any session. Example: {'computer_use': True, 'config': {'key':
            'example'}, 'created_at': '2026-02-18T09:30:00Z', 'description': 'example', 'env_vars':
            {'key': 'example'}, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'expected_access': {'network_policy': {'key': 'example'}, 'privileged': True},
            'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key':
            'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
            name', 'network_policy': {'key': 'example'}, 'organization_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'privileged': True, 'provider': 'example',
            'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name',
            'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
            'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
            'regions': ['example']}, 'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key':
            'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1}, 'setup_updated_at':
            '2026-02-18T09:30:00Z', 'setup_updated_by_user_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'setup_verification': {'active_setup_run_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'fingerprint':
            'example', 'image': {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z',
            'computeId': 'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example',
            'imageId': 'example', 'runnerImage': 'example', 'setupRunId': 'example', 'sizeBytes': 1,
            'usable': True, 'warmup': 'example', 'warmupMessage': 'example'}, 'imageCapture': {'at':
            '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId':
            'example', 'status': 'failed'}, 'last_run': {'duration_ms': 1, 'exit_code': 1,
            'failed_command': 'example', 'failed_line': 1, 'hint': 'example', 'hint_code': 'example',
            'message': 'example', 'phase': 'example', 'setup_run_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example', 'stderr_tail': 'example'},
            'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True, 'status':
            'example', 'verified_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
            'setup_warnings': [{'code': 'example', 'line': 1, 'message': 'example'}],
            'stopped_delete_after_seconds': 1, 'updated_at': '2026-02-18T09:30:00Z'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
body=body,
verify=verify,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateEnvironmentRequest,
    verify: bool | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment | None:
    """ Update environment

     Applies a partial update and returns the stored environment; omitted fields keep their current
    values. Changing from a non-Runs provider to Runs with an absent or {} stored policy requires an
    explicit network_policy: {"version":"v1","rules":[]} for deny-all or {} for unrestricted egress. A
    provider is validated only when the request actually names one. Sending setup with an empty script
    clears the script; omitting setup leaves it. Any change to provider, image, setup (script or
    timeout), resources, workspace disk size, provider config, variables, secret references, mounts,
    network policy, or effective Docker privilege marks the previous setup verification stale; name,
    description, metadata, and http_port do not. Pass ?verify=true to re-run setup in the same call;
    that half is authorized as createEnvironmentSetupRun is, in addition to the update itself. Sessions
    already running keep the spec they started with, so a change takes effect on the next session start.
    A Runs update that changes a nonempty network_policy or enables privileged Docker requires
    expected_access with the network_policy and privileged values from the last environment read. A
    missing access snapshot returns 428; a stale one returns 412. A concurrent placement edit may return
    409; reload and retry.

    Args:
        environment_id (UUID): Environment id (UUID) as returned by createEnvironment or
            listEnvironments.
        verify (bool | Unset): When true, a manual setup run is started as soon as the update is
            saved. Read setup_verification.active_setup_run_id from the response and poll
            getEnvironmentSetupRun; setup_verification.setup_run_id keeps naming an earlier verified
            run while it re-verifies. Ignored when the environment has no setup script. Starting the
            run is authorized exactly as createEnvironmentSetupRun is, so a caller who may update the
            environment but may not start a setup run is refused with 403 rather than saved without
            one.
        body (ManagedAgentsUpdateEnvironmentRequest): A sandbox environment a session executes in:
            its provider, resources, mounts, setup steps and idle/delete lifecycle. Created and
            started independently of any session. Example: {'computer_use': True, 'config': {'key':
            'example'}, 'created_at': '2026-02-18T09:30:00Z', 'description': 'example', 'env_vars':
            {'key': 'example'}, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'expected_access': {'network_policy': {'key': 'example'}, 'privileged': True},
            'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example', 'metadata': {'key':
            'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
            name', 'network_policy': {'key': 'example'}, 'organization_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'privileged': True, 'provider': 'example',
            'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name': 'example-name',
            'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
            'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'],
            'regions': ['example']}, 'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key':
            'example'}, 'setup': {'script': 'example', 'timeout_seconds': 1}, 'setup_updated_at':
            '2026-02-18T09:30:00Z', 'setup_updated_by_user_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'setup_verification': {'active_setup_run_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'fingerprint':
            'example', 'image': {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z',
            'computeId': 'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example',
            'imageId': 'example', 'runnerImage': 'example', 'setupRunId': 'example', 'sizeBytes': 1,
            'usable': True, 'warmup': 'example', 'warmupMessage': 'example'}, 'imageCapture': {'at':
            '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId':
            'example', 'status': 'failed'}, 'last_run': {'duration_ms': 1, 'exit_code': 1,
            'failed_command': 'example', 'failed_line': 1, 'hint': 'example', 'hint_code': 'example',
            'message': 'example', 'phase': 'example', 'setup_run_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example', 'stderr_tail': 'example'},
            'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True, 'status':
            'example', 'verified_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
            'setup_warnings': [{'code': 'example', 'line': 1, 'message': 'example'}],
            'stopped_delete_after_seconds': 1, 'updated_at': '2026-02-18T09:30:00Z'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEnvironment
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
client=client,
body=body,
verify=verify,

    )).parsed

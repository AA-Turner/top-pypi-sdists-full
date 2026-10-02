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
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_session_created_response import ManagedAgentsSessionCreatedResponse
from ...models.managed_agents_start_session_request import ManagedAgentsStartSessionRequest
from typing import cast



def _get_kwargs(
    *,
    body: ManagedAgentsStartSessionRequest,
    idempotency_key: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/sessions",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse | None:
    if response.status_code == 202:
        response_202 = ManagedAgentsSessionCreatedResponse.from_dict(response.json())



        return response_202

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
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



        return response_404

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsStartSessionRequest,
    idempotency_key: str,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse]:
    """ Start a managed session

     Starts a managed agent session and returns 202 with its session_id and status_path; the agent runs
    asynchronously, so poll getSession or subscribe with streamSessionEvents to follow it. Sandbox
    compute is provisioned here, which is where a session begins costing money. Requires an Idempotency-
    Key header: the same key with the same body returns the original session, and with a different body
    is rejected. A reasoning_effort incompatible with the selected model or its frozen output capacity
    returns 400 before provisioning; a temporarily unavailable model reference or catalog dependency
    returns 503. An environment on managed compute whose setup script has no verified, current run
    returns 422 environment_not_verified before provisioning; run createEnvironmentSetupRun first.

    Args:
        idempotency_key (str): Replay-protection key in an organization-wide namespace shared by
            keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent as exactly
            one header value. Request identity is the exact HTTP method, escaped path, raw query, and
            raw body bytes. The same request replays the original successful response; any different
            request returns 409 idempotency_conflict, and an active matching request returns 409
            idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsStartSessionRequest): Request body for starting a session: which agent
            to run, the environment to run it in, the vault grants it receives, and the opening
            message and/or outcome that gives it work. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'credential_refs': [{'credential_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluation': {'limit': 1, 'session_ids':
            ['example'], 'statuses': ['active']}, 'external_source_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'message':
            'example', 'metadata': {'key': 'example'}, 'outcome': {'description': 'Export the product
            catalog to /out/catalog.csv', 'rubric': '- /out/catalog.csv exists\\n- The CSV has a
            header row with sku, name, and price columns\\n- Every price value is a number'},
            'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'referenced_session_ids':
            ['example'], 'resources': [{'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'mount_path': 'example', 'relative_path': 'example', 'type': 'file'}],
            'skip_default_outcome': True, 'team': {'mode': 'auto'}, 'vault_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse]
     """


    kwargs = _get_kwargs(
        body=body,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsStartSessionRequest,
    idempotency_key: str,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse | None:
    """ Start a managed session

     Starts a managed agent session and returns 202 with its session_id and status_path; the agent runs
    asynchronously, so poll getSession or subscribe with streamSessionEvents to follow it. Sandbox
    compute is provisioned here, which is where a session begins costing money. Requires an Idempotency-
    Key header: the same key with the same body returns the original session, and with a different body
    is rejected. A reasoning_effort incompatible with the selected model or its frozen output capacity
    returns 400 before provisioning; a temporarily unavailable model reference or catalog dependency
    returns 503. An environment on managed compute whose setup script has no verified, current run
    returns 422 environment_not_verified before provisioning; run createEnvironmentSetupRun first.

    Args:
        idempotency_key (str): Replay-protection key in an organization-wide namespace shared by
            keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent as exactly
            one header value. Request identity is the exact HTTP method, escaped path, raw query, and
            raw body bytes. The same request replays the original successful response; any different
            request returns 409 idempotency_conflict, and an active matching request returns 409
            idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsStartSessionRequest): Request body for starting a session: which agent
            to run, the environment to run it in, the vault grants it receives, and the opening
            message and/or outcome that gives it work. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'credential_refs': [{'credential_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluation': {'limit': 1, 'session_ids':
            ['example'], 'statuses': ['active']}, 'external_source_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'message':
            'example', 'metadata': {'key': 'example'}, 'outcome': {'description': 'Export the product
            catalog to /out/catalog.csv', 'rubric': '- /out/catalog.csv exists\\n- The CSV has a
            header row with sku, name, and price columns\\n- Every price value is a number'},
            'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'referenced_session_ids':
            ['example'], 'resources': [{'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'mount_path': 'example', 'relative_path': 'example', 'type': 'file'}],
            'skip_default_outcome': True, 'team': {'mode': 'auto'}, 'vault_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse
     """


    return sync_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsStartSessionRequest,
    idempotency_key: str,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse]:
    """ Start a managed session

     Starts a managed agent session and returns 202 with its session_id and status_path; the agent runs
    asynchronously, so poll getSession or subscribe with streamSessionEvents to follow it. Sandbox
    compute is provisioned here, which is where a session begins costing money. Requires an Idempotency-
    Key header: the same key with the same body returns the original session, and with a different body
    is rejected. A reasoning_effort incompatible with the selected model or its frozen output capacity
    returns 400 before provisioning; a temporarily unavailable model reference or catalog dependency
    returns 503. An environment on managed compute whose setup script has no verified, current run
    returns 422 environment_not_verified before provisioning; run createEnvironmentSetupRun first.

    Args:
        idempotency_key (str): Replay-protection key in an organization-wide namespace shared by
            keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent as exactly
            one header value. Request identity is the exact HTTP method, escaped path, raw query, and
            raw body bytes. The same request replays the original successful response; any different
            request returns 409 idempotency_conflict, and an active matching request returns 409
            idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsStartSessionRequest): Request body for starting a session: which agent
            to run, the environment to run it in, the vault grants it receives, and the opening
            message and/or outcome that gives it work. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'credential_refs': [{'credential_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluation': {'limit': 1, 'session_ids':
            ['example'], 'statuses': ['active']}, 'external_source_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'message':
            'example', 'metadata': {'key': 'example'}, 'outcome': {'description': 'Export the product
            catalog to /out/catalog.csv', 'rubric': '- /out/catalog.csv exists\\n- The CSV has a
            header row with sku, name, and price columns\\n- Every price value is a number'},
            'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'referenced_session_ids':
            ['example'], 'resources': [{'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'mount_path': 'example', 'relative_path': 'example', 'type': 'file'}],
            'skip_default_outcome': True, 'team': {'mode': 'auto'}, 'vault_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse]
     """


    kwargs = _get_kwargs(
        body=body,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsStartSessionRequest,
    idempotency_key: str,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse | None:
    """ Start a managed session

     Starts a managed agent session and returns 202 with its session_id and status_path; the agent runs
    asynchronously, so poll getSession or subscribe with streamSessionEvents to follow it. Sandbox
    compute is provisioned here, which is where a session begins costing money. Requires an Idempotency-
    Key header: the same key with the same body returns the original session, and with a different body
    is rejected. A reasoning_effort incompatible with the selected model or its frozen output capacity
    returns 400 before provisioning; a temporarily unavailable model reference or catalog dependency
    returns 503. An environment on managed compute whose setup script has no verified, current run
    returns 422 environment_not_verified before provisioning; run createEnvironmentSetupRun first.

    Args:
        idempotency_key (str): Replay-protection key in an organization-wide namespace shared by
            keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent as exactly
            one header value. Request identity is the exact HTTP method, escaped path, raw query, and
            raw body bytes. The same request replays the original successful response; any different
            request returns 409 idempotency_conflict, and an active matching request returns 409
            idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsStartSessionRequest): Request body for starting a session: which agent
            to run, the environment to run it in, the vault grants it receives, and the opening
            message and/or outcome that gives it work. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'credential_refs': [{'credential_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluation': {'limit': 1, 'session_ids':
            ['example'], 'statuses': ['active']}, 'external_source_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'message':
            'example', 'metadata': {'key': 'example'}, 'outcome': {'description': 'Export the product
            catalog to /out/catalog.csv', 'rubric': '- /out/catalog.csv exists\\n- The CSV has a
            header row with sku, name, and price columns\\n- Every price value is a number'},
            'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'referenced_session_ids':
            ['example'], 'resources': [{'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'mount_path': 'example', 'relative_path': 'example', 'type': 'file'}],
            'skip_default_outcome': True, 'team': {'mode': 'auto'}, 'vault_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionCreatedResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed

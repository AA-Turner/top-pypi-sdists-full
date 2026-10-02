from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.agent_run_event_list_dto_item import AgentRunEventListDtoItem
from ...models.get_live_transcript_envelope import GetLiveTranscriptEnvelope
from ...models.live_transcript_envelope_dto import LiveTranscriptEnvelopeDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    run_config_probe_run_id: UUID,
    *,
    after: str | Unset = UNSET,
    envelope: GetLiveTranscriptEnvelope | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["after"] = after

    json_envelope: str | Unset = UNSET
    if not isinstance(envelope, Unset):
        json_envelope = envelope.value

    params["envelope"] = json_envelope


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/run-config-probe-runs/{run_config_probe_run_id}/transcript/live".format(run_config_probe_run_id=quote(str(run_config_probe_run_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto | None:
    if response.status_code == 200:
        def _parse_response_200(data: object) -> list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                response_200_type_0 = []
                _response_200_type_0 = data
                for componentsschemas_agent_run_event_list_dto_item_data in (_response_200_type_0):
                    componentsschemas_agent_run_event_list_dto_item = AgentRunEventListDtoItem.from_dict(componentsschemas_agent_run_event_list_dto_item_data)



                    response_200_type_0.append(componentsschemas_agent_run_event_list_dto_item)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = LiveTranscriptEnvelopeDto.from_dict(data)



            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = TargetApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = TargetApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = TargetApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = TargetApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = TargetApiErrorRateLimitExceeded.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        def _parse_response_500(data: object) -> TargetApiErrorInternalError | TargetApiErrorInvariantViolation:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_500_type_0 = TargetApiErrorInternalError.from_dict(data)



                return response_500_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_500_type_1 = TargetApiErrorInvariantViolation.from_dict(data)



            return response_500_type_1

        response_500 = _parse_response_500(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    run_config_probe_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after: str | Unset = UNSET,
    envelope: GetLiveTranscriptEnvelope | Unset = UNSET,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto]:
    """ Read the in-flight transcript of a probe-run

     Proxies agent-service transcript events while the probe-run is pending or running; with the after
    cursor only newer events are returned.

    Args:
        run_config_probe_run_id (UUID): Stable probe-run identifier (UUID). Probe runs validate a
            run-config version before locking.
        after (str | Unset): Return only events whose sequence is greater than this value. Omit to
            read the whole transcript.
        envelope (GetLiveTranscriptEnvelope | Unset): When true, wrap the events in an object that
            also carries the generation token of the run they came from. Omit for the bare event
            array.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto]
     """


    kwargs = _get_kwargs(
        run_config_probe_run_id=run_config_probe_run_id,
after=after,
envelope=envelope,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    run_config_probe_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after: str | Unset = UNSET,
    envelope: GetLiveTranscriptEnvelope | Unset = UNSET,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto | None:
    """ Read the in-flight transcript of a probe-run

     Proxies agent-service transcript events while the probe-run is pending or running; with the after
    cursor only newer events are returned.

    Args:
        run_config_probe_run_id (UUID): Stable probe-run identifier (UUID). Probe runs validate a
            run-config version before locking.
        after (str | Unset): Return only events whose sequence is greater than this value. Omit to
            read the whole transcript.
        envelope (GetLiveTranscriptEnvelope | Unset): When true, wrap the events in an object that
            also carries the generation token of the run they came from. Omit for the bare event
            array.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto
     """


    return sync_detailed(
        run_config_probe_run_id=run_config_probe_run_id,
client=client,
after=after,
envelope=envelope,

    ).parsed

async def asyncio_detailed(
    run_config_probe_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after: str | Unset = UNSET,
    envelope: GetLiveTranscriptEnvelope | Unset = UNSET,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto]:
    """ Read the in-flight transcript of a probe-run

     Proxies agent-service transcript events while the probe-run is pending or running; with the after
    cursor only newer events are returned.

    Args:
        run_config_probe_run_id (UUID): Stable probe-run identifier (UUID). Probe runs validate a
            run-config version before locking.
        after (str | Unset): Return only events whose sequence is greater than this value. Omit to
            read the whole transcript.
        envelope (GetLiveTranscriptEnvelope | Unset): When true, wrap the events in an object that
            also carries the generation token of the run they came from. Omit for the bare event
            array.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto]
     """


    kwargs = _get_kwargs(
        run_config_probe_run_id=run_config_probe_run_id,
after=after,
envelope=envelope,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    run_config_probe_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after: str | Unset = UNSET,
    envelope: GetLiveTranscriptEnvelope | Unset = UNSET,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto | None:
    """ Read the in-flight transcript of a probe-run

     Proxies agent-service transcript events while the probe-run is pending or running; with the after
    cursor only newer events are returned.

    Args:
        run_config_probe_run_id (UUID): Stable probe-run identifier (UUID). Probe runs validate a
            run-config version before locking.
        after (str | Unset): Return only events whose sequence is greater than this value. Omit to
            read the whole transcript.
        envelope (GetLiveTranscriptEnvelope | Unset): When true, wrap the events in an object that
            also carries the generation token of the run they came from. Omit for the bare event
            array.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[AgentRunEventListDtoItem] | LiveTranscriptEnvelopeDto
     """


    return (await asyncio_detailed(
        run_config_probe_run_id=run_config_probe_run_id,
client=client,
after=after,
envelope=envelope,

    )).parsed

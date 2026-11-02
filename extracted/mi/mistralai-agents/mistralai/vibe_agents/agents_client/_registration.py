"""Private Agent registration operation shared by authenticated clients."""

from http import HTTPMethod

from mistralai.vibe_agents._http import _InternalHTTPClient
from mistralai.vibe_agents.agents_client.api_models import (
    AgentConfigurationRequest,
    AgentResponse,
    RegisterAgentRequest,
)

# A registration without configuration is an idempotent upsert, so any gateway status or transport
# error is safe to send again. One with configuration stores a new snapshot each time it reaches the
# service. A 502, a 504, a client timeout, or a reset after the request was forwarded can follow a
# commit, so none of those is sent again. Only a 503, which the mesh returns for a reset upstream
# connection before the request reaches the service, is safe to send again, along with a transport
# error raised before the request is sent.
_REGISTER_RETRIES = 3
_REGISTER_RETRY_STATUS_CODES = frozenset({502, 503, 504})
_REGISTER_WITH_CONFIGURATION_RETRY_STATUS_CODES = frozenset({503})
_CONFIGURATION_FIELDS = tuple(AgentConfigurationRequest.model_fields)


async def _register_agent(client: _InternalHTTPClient, body: RegisterAgentRequest) -> AgentResponse:
    """Register one self-hosted Agent binding.

    The service returns the existing Agent with status 201 for an identical
    restart. A 409 means that the name has another Workflow or deployment
    binding and must remain an error. Without a deployment name, the service
    chooses one and returns it.
    """

    declares_configuration = any(getattr(body, field) for field in _CONFIGURATION_FIELDS)
    response = await client.make_request(
        HTTPMethod.POST,
        "/agents/register",
        json=body.model_dump(mode="json"),
        retries=_REGISTER_RETRIES,
        retries_codes=(
            _REGISTER_WITH_CONFIGURATION_RETRY_STATUS_CODES if declares_configuration else _REGISTER_RETRY_STATUS_CODES
        ),
        # make_request retries every TransportError while retries is non-zero, including a read timeout
        # after the service committed. A configuration register must not send that request again.
        only_retry_unsent_transport_errors=declares_configuration,
    )
    response.raise_for_status()
    return AgentResponse.model_validate(response.json())


__all__: list[str] = []

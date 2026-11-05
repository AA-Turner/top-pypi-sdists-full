"""Mistral connector adapters for local Harness Sessions."""

import asyncio
import difflib
import json
import random
import re
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from hashlib import sha256
from typing import Literal, Protocol

import structlog
from pydantic import BaseModel, ConfigDict, JsonValue, TypeAdapter, ValidationError

from mistralai.client import Mistral
from mistralai.client import errors as mistral_errors
from mistralai.client.httpclient import AsyncHttpClient
from mistralai.client.types.basemodel import Unset
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.capabilities import (
    McpHostSourceConfiguration,
    McpIntegrationMetadata,
    McpRemoteToolDefinition,
    McpSourceConfiguration,
    McpToolCallFailed,
    McpToolCallRequest,
    McpToolCallResult,
    McpToolCallSucceeded,
    McpToolCatalog,
    MistralConnectorConfiguration,
    MistralConnectorDescriptor,
)
from mistralai.vibe.harness.runtime.capabilities.plugins import mistral_connectors as harness_connectors
from mistralai.vibe.harness.runtime.capabilities.plugins.mcp import McpCapabilityHost
from mistralai.vibe.harness.runtime.capabilities.plugins.mistral_connectors import (
    MistralConnectorHost,
    MistralConnectorNotConnectedError,
)
from mistralai.vibe.harness.runtime.content import to_model_json_text
from mistralai.vibe.harness.runtime.hosts.mcp_http import McpHttpCapabilityHost
from mistralai.vibe_agents._http import _header_api_key
from mistralai.vibe_agents.sdk.assembly.local_mistral import local_mistral_client
from mistralai.vibe_agents.sdk.authoring import connector_selection
from mistralai.vibe_agents.sdk.authoring.errors import MistralConnectorNotFoundError
from mistralai.workflows.client import get_mistral_client as get_workflows_mistral_client
from mistralai.workflows.core.config.config import config as workflows_config
from mistralai.workflows.plugins.mistralai.connectors import decorator as connector_decorator

# Released plugins 3.15–3.16 only ship the old name; drop once the plugin floor includes RunAs.
try:
    from mistralai.workflows.plugins.mistralai.connectors.run_as import RunAs
except ImportError:
    from mistralai.workflows.plugins.mistralai.connectors.run_as import (
        ConnectorRunAs as RunAs,
    )

logger = structlog.get_logger(__name__)


# TODO: drop for the plugin's get_mistral_client once agents_controller pins a
# mistralai-workflows-plugins-mistralai release that passes executor_credentials_server_url.
def get_workflow_mistral_client(run_as: RunAs) -> Mistral:
    """The Mistral client for connector and Registry skill calls from a Workflow worker, as the given identity.

    These calls go to the worker's Mistral API URL. Executor tokens come from the Workflows API the
    worker is registered with: a worker inside the platform cluster reaches it on an internal URL, with
    its identity headers, which the Mistral API URL does not accept.
    """
    agent = workflows_config.worker.agent
    api_key = agent.mistral_client_api_key
    return get_workflows_mistral_client(
        api_key=_header_api_key(api_key.get_secret_value(), name="The worker's Mistral API key") if api_key else None,
        server=agent.mistral_client_server,
        server_url=agent.mistral_client_server_url,
        url_params=agent.mistral_client_url_params,
        timeout_ms=agent.mistral_client_timeout_ms,
        run_as=run_as,
        executor_credentials_server_url=workflows_config.worker.server_url,
    )


_JSON_VALUE_ADAPTER: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)
_SOURCE_PREFIX = "agents-sdk-connector:"
_DISCOVERED_REF = re.compile(r"(?P<digest>[0-9a-f]{16})@(?P<name>.+)", re.DOTALL)
_MISSING_CREDENTIAL_PREFIXES = (
    "No credentials found for connector ",
    "No credentials found with name ",
)
_MCP_NOT_SUPPORTED_DETAIL = "Connector does not support MCP."
_UNSUPPORTED_REASON = "it exposes no MCP-compatible tool interface."
_UNAVAILABLE_REASON = "the connectors API failed for it."
_NOT_FOUND_REASON = "no connector has this name."
# Ends every warning for a connector the Session starts without. Each of these has a notice too,
# which `agents chat` prints, so the chat leaves out the log lines that end with it.
SESSION_GOES_ON_WITHOUT_IT = "the Session goes on without it"
# Enough of an error message to diagnose it. An API error's message is not logged at all: it
# embeds the response body.
_LOGGED_ERROR_MAX_CHARS = 300
# How many connectors to probe at once. The connectors API limits MCP operations by rate, not by
# concurrency, so going faster does not finish sooner - it only converts requests into retries.
# Measured over a 129-connector catalog: at 8 at a time, 236 calls were rate-limited and 86
# connectors were described; at 3, 106 were rate-limited and 115 were described. Pacing the probe
# wastes fewer calls and answers for more connectors.
_PROBE_CONCURRENCY = 3
_RATE_LIMITED_STATUS = 429
_NOT_FOUND_STATUS = 404
_RATE_LIMIT_MAX_ATTEMPTS = 6
_RATE_LIMIT_BASE_DELAY_SECONDS = 0.5
_RATE_LIMIT_MAX_DELAY_SECONDS = 8.0
# The connectors SDK's own default when the client configures no timeout.
_CONNECTORS_API_TIMEOUT_MS = 300_000


async def _await_rate_limit(error: mistral_errors.SDKError, attempt: int) -> None:
    """Wait out one rate-limited connectors API call.

    The server's ``Retry-After`` is a floor: retrying before it only spends an attempt on a
    request the server has already said it will reject. Otherwise the delay doubles per
    attempt. Either way the delay gets jitter, because preparation probes many connectors
    at once and without it every one of them would come back at the same instant and be
    rejected together; jitter only ever lengthens a delay the server set.
    """

    spread = random.random()  # noqa: S311 - spreading retries, not a secret
    server_delay = _retry_after_seconds(error)
    if server_delay is not None:
        await asyncio.sleep(server_delay * (1 + 0.5 * spread))
        return
    delay = min(_RATE_LIMIT_BASE_DELAY_SECONDS * (2**attempt), _RATE_LIMIT_MAX_DELAY_SECONDS)
    await asyncio.sleep(delay * (0.5 + spread))


def _retry_after_seconds(error: mistral_errors.SDKError) -> float | None:
    retry_after = error.headers.get("retry-after")
    if retry_after is None:
        return None
    try:
        delay = float(retry_after)
    except ValueError:
        return None
    return delay if delay >= 0 else None


async def _retrying_rate_limits[T](operation: Callable[[], Awaitable[T]], *, what: str) -> T:
    """Run one connectors API call, waiting out the MCP rate limit rather than failing.

    A discovered connector set is as large as the organization's catalog, so a Session on a
    large one will be rate-limited during preparation as a matter of course. Treating that as
    a failure makes the mounted set depend on which probes won the race, which means the same
    Agent offers a different set of connectors on every Session.
    """

    for attempt in range(_RATE_LIMIT_MAX_ATTEMPTS):
        try:
            return await operation()
        except mistral_errors.SDKError as error:
            if error.status_code != _RATE_LIMITED_STATUS or attempt == _RATE_LIMIT_MAX_ATTEMPTS - 1:
                raise
            logger.debug(
                "agents_sdk waiting out the connectors API rate limit",
                operation=what,
                attempt=attempt + 1,
            )
            await _await_rate_limit(error, attempt)
    raise AssertionError("unreachable: the loop either returns or raises")


class ConnectorAuthenticationRequiredError(RuntimeError):
    """The selected connector has no usable credential for this executor."""


class ConnectorMcpNotSupportedError(RuntimeError):
    """The selected connector exposes no MCP-compatible tool interface."""


class _ConnectorApiError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detail: str


@dataclass(frozen=True, slots=True)
class ResolvedConnector:
    """One connector as the connectors API resolved it.

    ``instructions`` is the API's ``system_prompt``: the instructions the connector's MCP
    server returned at ``initialize``.
    """

    id: str
    name: str
    authenticated: bool | None = None
    instructions: str | None = None


@dataclass(frozen=True, slots=True)
class BootstrappedConnector:
    """One connector as the connectors API resolved it for this identity.

    ``is_ready`` is the API's own verdict on whether the Session user can call the
    connector, and ``tools`` is the tool list it already resolved. Both arrive without
    a per-connector request, which is the whole reason for preferring bootstrap over
    listing the catalog and probing it.

    ``needs_auth`` separates the two ways a connector can be unready: the user has not
    connected it, which they can fix, or the API failed to reach it, which they cannot.

    ``instructions`` is the API's ``system_prompt``, as on :class:`ResolvedConnector`.
    """

    id: str
    name: str
    is_ready: bool
    tools: tuple[McpRemoteToolDefinition, ...] = ()
    needs_auth: bool = False
    instructions: str | None = None

    @property
    def unreachable(self) -> bool:
        """Whether the API failed to reach the connector, which the user cannot fix."""

        return not self.is_ready and not self.needs_auth


@dataclass(frozen=True, slots=True)
class _ConnectorSourceBinding:
    connector_id: str
    credentials_name: str | None
    # Kept with the route because the connector tool listing does not return them.
    instructions: str | None = None


@dataclass(frozen=True, slots=True)
class _ConnectorSourceRef:
    """Opaque pointer from a Harness MCP source back to one connector slot.

    Deliberately carries no connector id. A source configuration is caller-authored, so anything
    read out of a ref is attacker-chosen; routing resolves the slot through the connectors API and
    takes the id from that answer instead. The digest covers the credential name so that rebinding
    a slot under different credentials mints a new source rather than reusing the old route.

    A discovered slot's ref also names its connector. Authored slots can be matched against the
    ref offline, but discovered ones exist only in a catalog, and routing restores a binding on
    every tool call: without the name, each call would have to fetch the whole catalog again to
    find the one slot it routes to. The name is caller-authored like the rest of the ref, so it
    is only accepted for a connector the selection admits.
    """

    digest: str
    retired_connector_id: str | None = None
    discovered_name: str | None = None

    @classmethod
    def for_slot(cls, authored_name: str, credentials_name: str | None) -> "_ConnectorSourceRef":
        return cls(digest=_slot_digest(authored_name, credentials_name))

    @classmethod
    def for_discovered_slot(cls, connector_name: str, credentials_name: str | None) -> "_ConnectorSourceRef":
        return cls(digest=_slot_digest(connector_name, credentials_name), discovered_name=connector_name)

    @classmethod
    def parse(cls, source_ref: str) -> "_ConnectorSourceRef | None":
        if not source_ref.startswith(_SOURCE_PREFIX):
            return None
        remainder = source_ref[len(_SOURCE_PREFIX) :]
        if not remainder:
            return None
        discovered = _DISCOVERED_REF.fullmatch(remainder)
        if discovered is not None:
            return cls(digest=discovered["digest"], discovered_name=discovered["name"])
        retired_connector_id, separator, digest = remainder.rpartition(":")
        if not separator:
            return cls(digest=remainder)
        # A ref minted while the id was still embedded. Sessions retain their materialized sources
        # and replay them on resume, so refs in the retired shape outlive the deploy that changed it.
        return cls(digest=digest, retired_connector_id=retired_connector_id) if digest else None

    def owned_by(self, authored_name: str, credentials_name: str | None) -> bool:
        """Whether this ref was minted for the given slot.

        A retired id is only ever a digest input here, never a routing target: matching still
        yields an authored slot, and the connector id still comes from resolving that slot.
        """

        if self.retired_connector_id is None:
            return self.digest == _slot_digest(authored_name, credentials_name)
        return self.digest == _retired_slot_digest(
            authored_name,
            self.retired_connector_id,
            credentials_name,
        )

    def encode(self) -> str:
        if self.discovered_name is not None:
            return f"{_SOURCE_PREFIX}{self.digest}@{self.discovered_name}"
        return f"{_SOURCE_PREFIX}{self.digest}"


def _slot_digest(authored_name: str, credentials_name: str | None) -> str:
    return sha256(f"{authored_name}\0{credentials_name or ''}".encode()).hexdigest()[:16]


def _retired_slot_digest(authored_name: str, connector_id: str, credentials_name: str | None) -> str:
    """Reproduce the digest of refs minted while the connector id was still part of it."""

    identity = f"{authored_name}\0{connector_id}\0{credentials_name or ''}"
    return sha256(identity.encode()).hexdigest()[:16]


def _classified_connector_error(error: mistral_errors.SDKError) -> Exception | None:
    """Map the connectors API's documented failures onto this adapter's own errors."""

    try:
        payload = _ConnectorApiError.model_validate_json(error.body)
    except ValidationError:
        return None
    if error.status_code == 401 and payload.detail.startswith(_MISSING_CREDENTIAL_PREFIXES):
        return ConnectorAuthenticationRequiredError(payload.detail)
    if error.status_code == 400 and payload.detail == _MCP_NOT_SUPPORTED_DETAIL:
        return ConnectorMcpNotSupportedError(payload.detail)
    return None


def _unsupported_descriptor(authored_name: str, resolved: ResolvedConnector) -> MistralConnectorDescriptor:
    """Report the slot as unsupported so the rest of the session keeps its connectors.

    The Harness turns this into a per-connector notice naming the connector, which is why an
    unusable slot no longer has to fail discovery for every other slot.
    """

    logger.warning(
        f"agents_sdk connector is not MCP-capable; {SESSION_GOES_ON_WITHOUT_IT}",
        connector_name=authored_name,
        connector_id=resolved.id,
    )
    return MistralConnectorDescriptor(
        id=authored_name,
        name=resolved.name,
        status="unsupported",
        unsupported_reason=_UNSUPPORTED_REASON,
    )


def _not_found_descriptor(error: MistralConnectorNotFoundError) -> MistralConnectorDescriptor:
    """Report an authored name the connectors API does not know, so the Session goes on without it.

    No later listing fixes a wrong name, so it is unsupported, which the Harness never retries.
    The reason carries the close names the error suggests, so the notice and the model's message
    both name them. It is logged at warning, like the other connector failures in this module.
    """

    logger.warning(
        f"agents_sdk found no connector with an authored name; {SESSION_GOES_ON_WITHOUT_IT}",
        connector_name=error.connector_name,
        error=str(error),
    )
    reason = _NOT_FOUND_REASON
    if error.close_matches:
        reason += f" Did you mean {' or '.join(repr(name) for name in error.close_matches)}?"
    return MistralConnectorDescriptor(
        id=error.connector_name,
        name=error.connector_name,
        status="unsupported",
        unsupported_reason=reason,
    )


def _unavailable_descriptor(authored_name: str, error: Exception) -> MistralConnectorDescriptor:
    """Report a slot the connectors API failed to describe, so the rest of the session keeps theirs.

    Without this, one connector's failed probe - a rate limit that outlasted the retries, a
    timeout - failed the whole listing, and the Harness started the Session with no connector at
    all. The Harness turns this descriptor into a notice naming the connector and lists it again
    at later Turn starts. No credential would fix it, so it is not offered for authentication.
    """

    if isinstance(error, mistral_errors.MistralError):
        status_code, message = error.status_code, None
    else:
        status_code, message = None, str(error)[:_LOGGED_ERROR_MAX_CHARS]
    logger.warning(
        f"agents_sdk could not describe a connector; {SESSION_GOES_ON_WITHOUT_IT}",
        connector_name=authored_name,
        error_type=type(error).__name__,
        status_code=status_code,
        error=message,
    )
    return MistralConnectorDescriptor(
        id=authored_name,
        name=authored_name,
        status="unavailable",
        unavailable_reason=_UNAVAILABLE_REASON,
    )


class ConnectorApi(Protocol):
    """Typed boundary over the public Mistral connector client."""

    async def bootstrap(self) -> list[BootstrappedConnector]: ...

    async def resolve(self, connector_id_or_name: str) -> ResolvedConnector: ...

    async def list_tools(
        self,
        connector_id_or_name: str,
        *,
        credentials_name: str | None,
    ) -> list[McpRemoteToolDefinition]: ...

    async def call_tool(
        self,
        connector_id_or_name: str,
        tool_name: str,
        arguments: dict[str, JsonValue],
        *,
        credentials_name: str | None,
    ) -> McpToolCallResult: ...

    async def close(self) -> None: ...


class MistralConnectorApi(ConnectorApi):
    """Own one isolated Mistral client and both of its HTTP transports.

    Workflow factories supply fresh transports to the public SDK, whose context
    manager deliberately leaves supplied clients open. This adapter owns those
    transports as well as clients constructed by the local factory.
    """

    def __init__(
        self,
        client: Mistral,
        *,
        http: AsyncHttpClient | None = None,
        api_key: str | None = None,
    ) -> None:
        self._client = client
        self._http = http
        self._api_key = api_key

    @classmethod
    def from_local_environment(
        cls,
        execution_identity: Literal["auto", "deployment"],
    ) -> "MistralConnectorApi":
        """Use the local process identity when no executor identity exists.

        A local Host has one credential context. Both ``auto`` and
        ``deployment`` therefore resolve to that explicit local credential;
        neither mode pretends that a managed executor token is available.
        """

        del execution_identity
        local = local_mistral_client("Mistral connectors")
        return cls(local.client, http=local.http, api_key=local.api_key)

    @classmethod
    def from_workflow_context(
        cls,
        execution_identity: Literal["auto", "deployment"],
    ) -> "MistralConnectorApi":
        """Build a client whose request hook enforces the authored identity."""

        return cls(get_workflow_mistral_client(RunAs(execution_identity)))

    async def bootstrap(self) -> list[BootstrappedConnector]:
        """Ask the connectors API to resolve this identity's connectors in one call.

        ``/v1/connectors/bootstrap`` answers what listing the catalog and probing every
        connector used to answer - which connectors are callable, and what tools they
        expose - but server-side and in a single request. On a 129-connector
        organization that is one request instead of roughly 250, and it is not subject
        to the per-connector MCP rate limit that made the probed answer vary between
        Sessions.

        The endpoint is public but absent from the generated client, so the request is
        issued by hand. It deliberately goes through the SDK's own transport: in a
        Workflow the executing identity is applied by a hook on that httpx client and
        the SDK holds no API key, so a request sent on any other client would silently
        lose the on-behalf-of identity and answer for the wrong user.
        """

        base_url, _ = self._client.sdk_configuration.get_server_details()
        transport = self._client.sdk_configuration.async_client
        if transport is None:
            raise RuntimeError("The Mistral client has no async transport to bootstrap connectors with")
        headers = {"Accept": "application/json"}
        if self._api_key is not None:
            # Local runs authenticate with an explicit key. A Workflow client carries no key
            # here at all: its hook adds the executing identity per request.
            headers["Authorization"] = f"Bearer {self._api_key}"
        # Built on the transport so it carries the same timeout the SDK's own connector calls
        # use; a bare request would fall back to httpx's 5-second default, which a large
        # catalog can outlast.
        timeout_ms = self._client.sdk_configuration.timeout_ms or _CONNECTORS_API_TIMEOUT_MS
        request = transport.build_request(
            "GET",
            f"{base_url}/v1/connectors/bootstrap",
            params={"supports_mcp": "true", "include_auth_actionable_connectors": "true"},
            headers=headers,
            timeout=timeout_ms / 1000,
        )
        response = await transport.send(request)
        response.raise_for_status()
        return _parse_bootstrap(response.json())

    async def resolve(self, connector_id_or_name: str) -> ResolvedConnector:
        try:
            connector = await _retrying_rate_limits(
                lambda: self._client.beta.connectors.get_async(connector_id_or_name=connector_id_or_name),
                what=f"resolve {connector_id_or_name}",
            )
        except mistral_errors.SDKError as error:
            # The connectors API answers 404 for a name or id this identity cannot see.
            if error.status_code == _NOT_FOUND_STATUS:
                raise MistralConnectorNotFoundError(connector_id_or_name) from error
            raise
        # mistralai 3.x types the response as an open union. Its UnknownConnector fallback keeps only the
        # raw payload, both for a protocol the client does not know and for a known one that fails
        # validation, e.g. a server older than the client that omits a field it now requires.
        # Reading the fields from that payload keeps older servers, such as MAIS 2026.08, working.
        raw = getattr(connector, "raw", None)
        if getattr(connector, "is_unknown", False) is True and isinstance(raw, dict):
            connector_id, name, authenticated = raw.get("id"), raw.get("name"), raw.get("is_authenticated")
            system_prompt = raw.get("system_prompt")
        else:
            connector_id = getattr(connector, "id", None)
            name = getattr(connector, "name", None)
            authenticated = getattr(connector, "is_authenticated", None)
            system_prompt = getattr(connector, "system_prompt", None)
        if not isinstance(connector_id, str) or not isinstance(name, str):
            raise ValueError(f"Mistral returned an unsupported connector for {connector_id_or_name}")
        if isinstance(authenticated, Unset) or authenticated is None:
            resolved_authenticated = None
        else:
            resolved_authenticated = bool(authenticated)
        return ResolvedConnector(
            id=connector_id,
            name=name,
            authenticated=resolved_authenticated,
            instructions=system_prompt if isinstance(system_prompt, str) else None,
        )

    async def list_tools(
        self,
        connector_id_or_name: str,
        *,
        credentials_name: str | None,
    ) -> list[McpRemoteToolDefinition]:
        if credentials_name is None:
            call = partial(
                self._client.beta.connectors.list_tools_async,
                connector_id_or_name=connector_id_or_name,
            )
        else:
            call = partial(
                self._client.beta.connectors.list_tools_async,
                connector_id_or_name=connector_id_or_name,
                credentials_name=credentials_name,
            )
        try:
            tools = await _retrying_rate_limits(call, what=f"list_tools {connector_id_or_name}")
        except mistral_errors.SDKError as error:
            classified = _classified_connector_error(error)
            if classified is None:
                raise
            raise classified from error
        return [_build_remote_tool(tool) for tool in tools]

    async def call_tool(
        self,
        connector_id_or_name: str,
        tool_name: str,
        arguments: dict[str, JsonValue],
        *,
        credentials_name: str | None,
    ) -> McpToolCallResult:
        if credentials_name is None:
            response = await self._client.beta.connectors.call_tool_async(
                connector_id_or_name=connector_id_or_name,
                tool_name=tool_name,
                arguments=arguments,
            )
        else:
            response = await self._client.beta.connectors.call_tool_async(
                connector_id_or_name=connector_id_or_name,
                tool_name=tool_name,
                arguments=arguments,
                credentials_name=credentials_name,
            )
        text = _connector_response_text(response.content)
        content = [core_protocol.TextContentBlock(text=text)] if text else []
        structured_content = _structured_content_from_text(text)
        metadata = response.metadata
        is_error = False
        if metadata is not None and not isinstance(metadata, Unset):
            mcp_metadata = metadata.mcp_meta
            if mcp_metadata is not None and not isinstance(mcp_metadata, Unset):
                is_error = bool(mcp_metadata.is_error)
        if is_error:
            return McpToolCallFailed(
                message=text or f"Connector tool {tool_name!r} returned an error",
                content=content,
                structured_content=structured_content,
            )
        return McpToolCallSucceeded(
            content=content,
            structured_content=structured_content,
        )

    async def close(self) -> None:
        configuration = self._client.sdk_configuration
        try:
            if configuration.async_client is not None:
                await configuration.async_client.aclose()
        finally:
            try:
                if configuration.client is not None:
                    configuration.client.close()
            finally:
                if self._http is not None and self._http is not configuration.async_client:
                    await self._http.aclose()


class AgentsSdkConnectorResource(McpCapabilityHost, MistralConnectorHost):
    """Bind authored connector slots to Harness connector and MCP ports."""

    def __init__(
        self,
        slots: Sequence[connector_decorator.ConnectorSlot],
        *,
        discovery: connector_selection.AllConnectors | None = None,
        api: ConnectorApi,
        http_mcp_host: McpCapabilityHost | None = None,
    ) -> None:
        self._authored_slots = {slot.connector_name: slot for slot in slots}
        if len(self._authored_slots) != len(slots):
            raise ValueError("Connector slots must have unique connector names")
        self._discovery = discovery
        self._api = api
        self._http_mcp_host = http_mcp_host or McpHttpCapabilityHost()
        self._source_bindings: dict[str, _ConnectorSourceBinding] = {}
        # Without discovery the authored slots are the whole set and need no resolution.
        self._slots: dict[str, connector_decorator.ConnectorSlot] | None = (
            None if discovery is not None else dict(self._authored_slots)
        )
        # What bootstrap already told us about each discovered connector: whether it is
        # callable, and its tools. Keyed by connector name, filled during discovery.
        self._bootstrapped: dict[str, BootstrappedConnector] = {}
        # Whether a listing already used bootstrap's answer. A later listing is a Turn-start
        # retry, which asks a connector bootstrap failed to reach directly: bootstrap's answer
        # for it is stale by then. Only an in-process Session gets here: a deployed worker opens
        # a fresh resource per listing, so its fresh bootstrap answer already says what changed.
        self._listed = False
        # Tools bootstrap resolved, keyed by the source they were mounted under, so routing
        # does not list them again per connector at Session start.
        self._source_tools: dict[str, tuple[McpRemoteToolDefinition, ...]] = {}
        self._discovery_lock = asyncio.Lock()
        # Connector names listed only to suggest a fix for a misspelled authored name. Slots are
        # described concurrently, so the lock makes every missing slot share one listing.
        self._suggestion_names: list[str] | None = None
        self._suggestion_names_lock = asyncio.Lock()

    @classmethod
    def from_local_environment(
        cls,
        slots: Sequence[connector_decorator.ConnectorSlot],
        *,
        discovery: connector_selection.AllConnectors | None = None,
        configuration: MistralConnectorConfiguration,
        http_mcp_host: McpCapabilityHost | None = None,
    ) -> "AgentsSdkConnectorResource":
        return cls(
            slots,
            discovery=discovery,
            api=MistralConnectorApi.from_local_environment(configuration.execution_identity),
            http_mcp_host=http_mcp_host,
        )

    @classmethod
    def from_workflow_context(
        cls,
        slots: Sequence[connector_decorator.ConnectorSlot],
        *,
        discovery: connector_selection.AllConnectors | None = None,
        configuration: MistralConnectorConfiguration,
        http_mcp_host: McpCapabilityHost | None = None,
    ) -> "AgentsSdkConnectorResource":
        return cls(
            slots,
            discovery=discovery,
            api=MistralConnectorApi.from_workflow_context(configuration.execution_identity),
            http_mcp_host=http_mcp_host,
        )

    async def _resolved_slots(self) -> dict[str, connector_decorator.ConnectorSlot]:
        """Return the connector slots this Session runs with, discovering them once.

        Discovery is memoized rather than repeated per call because routing asks for
        the slots on every connector tool call, and because a catalog that changed
        mid-Session would silently move tools out from under the Agent.
        """

        if self._slots is not None:
            return self._slots
        async with self._discovery_lock:
            if self._slots is None:
                self._slots = await self._discover_slots()
            return self._slots

    async def _discover_slots(self) -> dict[str, connector_decorator.ConnectorSlot]:
        discovery = self._discovery
        if discovery is None:
            return dict(self._authored_slots)
        available = await self._api.bootstrap()
        self._bootstrapped = {connector.name: connector for connector in available}
        # An explicitly authored connector keeps its own options, so it wins over the
        # discovered default for the same name.
        slots = dict(self._authored_slots)
        for name in discovery.candidates([connector.name for connector in available]):
            if name in slots:
                continue
            slots[name] = connector_decorator.connector(
                name,
                auto_auth=discovery.auto_auth,
                allow_mcp_ui=discovery.allow_mcp_ui,
            )
        logger.info(
            "agents_sdk discovered the Session user's connectors",
            available_count=len(available),
            selected_count=len(slots),
        )
        if (
            discovery.max_connectors is None
            and len(slots) > connector_selection.DEFAULT_CONNECTOR_COUNT_WARNING_THRESHOLD
        ):
            logger.warning(
                "agents_sdk mounted a large connector set; the Agent searches every connector's "
                "tools, so a tool from an unrelated connector can win. Narrow it with "
                "all_connectors(exclude=[...]) or name the connectors the Agent needs.",
                selected_count=len(slots),
            )
        return slots

    async def list_connectors(
        self,
        configuration: MistralConnectorConfiguration,
    ) -> list[MistralConnectorDescriptor]:
        # Slots are independent and each costs a resolve plus a capability probe, so run them
        # together: preparation then waits for the slowest connector instead of the sum of all of
        # them, and one slow slot no longer delays every slot authored after it. gather preserves
        # input order, so descriptors still come back in authored order.
        #
        # The concurrency is bounded because a discovered set is as large as the organization's
        # catalog - over a hundred connectors on a large one - and the connectors API rate-limits
        # MCP operations. Probing all of them at once trips that limit and starts the Session with
        # no connectors at all.
        slots = await self._resolved_slots()
        capped_out = self._capped_out(slots)
        retry = self._listed
        limit = asyncio.Semaphore(_PROBE_CONCURRENCY)

        async def describe(slot: connector_decorator.ConnectorSlot) -> MistralConnectorDescriptor | None:
            bootstrapped = self._bootstrapped.get(slot.connector_name)
            # Bootstrap already answered for a discovered connector. An authored one is still
            # probed: it may name a credential bootstrap did not resolve against, and the Agent
            # asked for it by name, so it deserves the direct answer. A discovered connector
            # bootstrap failed to reach is probed too on a later listing: the Harness is retrying
            # it, and bootstrap's answer is stale by then.
            if bootstrapped is not None and slot.connector_name not in self._authored_slots:
                if not (bootstrapped.unreachable and retry):
                    return self._descriptor_from_bootstrap(slot, bootstrapped, configuration)
            async with limit:
                try:
                    return await self._describe_slot(slot, configuration)
                except MistralConnectorNotFoundError as error:
                    return _not_found_descriptor(error)
                except ValidationError:
                    # A descriptor our own models reject is a bug here, not an outage: no later
                    # session fixes it, so it still fails preparation and names the problem.
                    raise
                except Exception as error:  # noqa: BLE001 - one connector's outage must not cost the others.
                    return _unavailable_descriptor(slot.connector_name, error)

        described = await asyncio.gather(*(describe(slot) for name, slot in slots.items() if name not in capped_out))
        self._listed = True
        return [descriptor for descriptor in described if descriptor is not None]

    def _descriptor_from_bootstrap(
        self,
        slot: connector_decorator.ConnectorSlot,
        bootstrapped: BootstrappedConnector,
        configuration: MistralConnectorConfiguration,
    ) -> MistralConnectorDescriptor | None:
        """Describe a discovered connector from what bootstrap already resolved.

        An unready connector is only offered when connecting it is what it lacks. One the API
        failed to reach is unavailable: offering it would start an authorization flow that
        cannot fix it, and the Harness lists it again at later Turn starts.
        """

        authored_name = slot.connector_name
        if bootstrapped.unreachable:
            logger.warning(
                f"agents_sdk could not describe a connector; {SESSION_GOES_ON_WITHOUT_IT}",
                connector_name=authored_name,
            )
            return MistralConnectorDescriptor(
                id=authored_name,
                name=bootstrapped.name,
                status="unavailable",
                unavailable_reason=_UNAVAILABLE_REASON,
            )
        if not bootstrapped.is_ready:
            return MistralConnectorDescriptor(
                id=authored_name,
                name=bootstrapped.name,
                status="unauthenticated",
            )
        resolved = ResolvedConnector(
            id=bootstrapped.id,
            name=bootstrapped.name,
            authenticated=True,
            instructions=bootstrapped.instructions,
        )
        source = self._build_source(
            slot,
            resolved,
            credentials_name=configuration.credential_names.get(authored_name),
        )
        self._source_tools[source.source_ref] = bootstrapped.tools
        return MistralConnectorDescriptor(
            id=authored_name,
            name=bootstrapped.name,
            status="authenticated",
            mcp_source=source,
        )

    def _capped_out(self, slots: dict[str, connector_decorator.ConnectorSlot]) -> set[str]:
        """The discovered connectors ``max_connectors`` leaves out of this Session.

        The cap counts the connectors that are possible, not the ones that loaded: every
        discovered connector the user has signed in to, including one the API failed to reach.
        Such a connector keeps its place and gets its notice, and its tools take that same place
        when it loads at a later Turn start. Nothing moves between places, and the answer only
        needs bootstrap, so a deployed worker, which opens a fresh resource for every listing,
        gets the same set, as long as the user has not signed in to or out of a connector
        since. A connector that loads at once does not take a failed one's place:
        the cap is a rarely used safety limit, and keeping it simple matters more than filling
        every place.

        An explicitly authored connector is never capped away - naming a connector is a
        stronger statement than the selection that happens to also cover it. A signed-in
        connector past the cap leaves the set altogether rather than becoming an offer:
        offering one the user has already connected would ask them to authorize what they
        have authorized.

        Discovered connectors the user has not connected are only offered while the cap has
        room. Connecting one once it is full would mount nothing: the refreshed set would cap
        it straight back out, after the Agent was told its tools are now available.
        """

        discovery = self._discovery
        if discovery is None or discovery.max_connectors is None:
            return set()
        discovered = {
            name: self._bootstrapped[name]
            for name in slots
            if name not in self._authored_slots and name in self._bootstrapped
        }
        # The cap is on the connectors that are possible, not the ones that loaded.
        signed_in = [name for name, connector in discovered.items() if not connector.needs_auth]
        kept = set(discovery.cap(signed_in))
        capped_out = {name for name in signed_in if name not in kept}
        if capped_out:
            logger.info(
                "agents_sdk held the discovered connector set to its cap",
                max_connectors=discovery.max_connectors,
                dropped=sorted(capped_out),
            )
        if len(kept) >= discovery.max_connectors:
            capped_out |= {name for name, connector in discovered.items() if connector.needs_auth}
        return capped_out

    async def _describe_slot(
        self,
        slot: connector_decorator.ConnectorSlot,
        configuration: MistralConnectorConfiguration,
    ) -> MistralConnectorDescriptor:
        authored_name = slot.connector_name
        try:
            resolved = await self._api.resolve(authored_name)
        except harness_connectors.MistralConnectorNotFoundError as error:
            raise MistralConnectorNotFoundError(
                authored_name, close_matches=await self._close_connector_names(authored_name)
            ) from error
        credentials_name = configuration.credential_names.get(authored_name)
        # Listing tools is the only trustworthy answer, so every slot is probed. The connectors
        # API reports is_authenticated=False for connectors whose tools are in fact reachable,
        # and it cannot report MCP capability at all. Deciding both here, once, is what keeps a
        # descriptor from claiming a connector is callable when tool listing will reject it.
        try:
            tools = await self._api.list_tools(resolved.id, credentials_name=credentials_name)
        except ConnectorAuthenticationRequiredError:
            tools = None
        except ConnectorMcpNotSupportedError:
            return _unsupported_descriptor(authored_name, resolved)
        authenticated = tools is not None
        source = (
            self._build_source(
                slot,
                resolved,
                credentials_name=credentials_name,
            )
            if authenticated
            else None
        )
        if source is not None and tools is not None:
            # The probe's answer is the tool list: serving it saves listing the tools again,
            # which on a Turn start would run outside the time the Harness gives the probe.
            self._source_tools[source.source_ref] = tuple(tools)
        return MistralConnectorDescriptor(
            id=authored_name,
            name=resolved.name,
            status="authenticated" if authenticated else "unauthenticated",
            mcp_source=source,
        )

    async def _close_connector_names(self, name: str) -> list[str]:
        """Name the connectors a misspelled name was likely meant to be, when they are cheap to list.

        Bootstrap lists this identity's connectors in one request, and a discovered set has already
        made it. The names only help the error message, so a failed listing gives none.
        """

        known = list(self._bootstrapped) or await self._names_for_suggestions()
        by_folded = {candidate.casefold(): candidate for candidate in known}
        matches = difflib.get_close_matches(name.casefold(), list(by_folded), n=3, cutoff=0.6)
        return [by_folded[match] for match in matches]

    async def _names_for_suggestions(self) -> list[str]:
        async with self._suggestion_names_lock:
            if self._suggestion_names is None:
                try:
                    self._suggestion_names = [connector.name for connector in await self._api.bootstrap()]
                except Exception:  # noqa: BLE001 - the suggestion is optional; the not-found error is not.
                    logger.debug("agents_sdk could not list connectors to suggest a name", exc_info=True)
                    self._suggestion_names = []
            return self._suggestion_names

    async def restore_source_binding(
        self,
        source: McpSourceConfiguration,
        configuration: MistralConnectorConfiguration,
    ) -> None:
        """Restore routing for one source, resolving only the slot that owns it.

        Runs on every connector tool listing and call, so it must not walk the catalog: that would
        cost one request per slot per call - a whole bootstrap when the set is discovered - and let
        an unrelated slot's resolution failure block the connector being routed. The ref identifies
        the slot offline; the connector id then comes from resolving that slot, never from the ref,
        which is caller-authored.
        """

        if not isinstance(source, McpHostSourceConfiguration):
            return
        ref = _ConnectorSourceRef.parse(source.source_ref)
        if ref is None:
            return
        if ref.discovered_name is None:
            authored_name = _slot_owning(ref, configuration, self._authored_slots)
        else:
            authored_name = self._discovered_slot_owning(ref, configuration)
        if authored_name is None:
            return
        credentials_name = configuration.credential_names.get(authored_name)
        # The id still comes from an answer the connectors API gave us, keyed by the slot the
        # ref matched - never from the ref itself, which is caller-authored. Bootstrap is such
        # an answer, so reusing it keeps that property and saves a request per source. Tools
        # are only reused when the slot adds no credential of its own, since a different
        # credential may see a different tool list.
        bootstrapped = self._bootstrapped.get(authored_name)
        if bootstrapped is not None:
            connector_id = bootstrapped.id
            instructions = bootstrapped.instructions
            if credentials_name is None:
                self._source_tools.setdefault(source.source_ref, bootstrapped.tools)
        else:
            resolved = await self._api.resolve(authored_name)
            connector_id = resolved.id
            instructions = resolved.instructions
        self._source_bindings[source.source_ref] = _ConnectorSourceBinding(
            connector_id=connector_id,
            credentials_name=credentials_name,
            instructions=instructions,
        )

    def _discovered_slot_owning(
        self,
        ref: _ConnectorSourceRef,
        configuration: MistralConnectorConfiguration,
    ) -> str | None:
        """Accept the connector a discovered ref names only if this selection could have mounted it."""

        name = ref.discovered_name
        discovery = self._discovery
        if name is None or discovery is None or name in self._authored_slots or not discovery.admits(name):
            return None
        if not ref.owned_by(name, configuration.credential_names.get(name)):
            return None
        return name

    async def apply_connected_connectors(self, connector_ids: list[str]) -> None:
        slots = await self._resolved_slots()
        unknown = set(connector_ids) - slots.keys()
        # Bootstrap answered for the whole catalog when the Session started, so a connector
        # the user just connected is stale there either way: missing from it, or listed as
        # not ready. Discovered descriptors are built from that answer, so refresh it.
        stale = bool(unknown) or any(
            not bootstrapped.is_ready
            for connector_id in connector_ids
            if (bootstrapped := self._bootstrapped.get(connector_id)) is not None
        )
        if stale and self._discovery is not None:
            async with self._discovery_lock:
                self._slots = await self._discover_slots()
                slots = self._slots
            unknown = set(connector_ids) - slots.keys()
        if unknown:
            raise ValueError(f"Unknown connector ids in callback result: {sorted(unknown)}")
        # The callback answer is the app's word, and an app can be wrong: the user closed the
        # sign-in page, or it answered before sign-in finished. Check each connector the way
        # Session start did, so the model is never told tools are available when none mount.
        connected = await asyncio.gather(*(self._is_connected(slots[connector_id]) for connector_id in connector_ids))
        unconnected = [connector_id for connector_id, ok in zip(connector_ids, connected, strict=True) if not ok]
        if unconnected:
            raise MistralConnectorNotConnectedError(unconnected)

    async def _is_connected(self, slot: connector_decorator.ConnectorSlot) -> bool:
        name = slot.connector_name
        bootstrapped = self._bootstrapped.get(name)
        if bootstrapped is not None and name not in self._authored_slots:
            return bootstrapped.is_ready
        resolved = await self._api.resolve(name)
        try:
            await self._api.list_tools(resolved.id, credentials_name=slot.credentials_name)
        except ConnectorAuthenticationRequiredError:
            return False
        return True

    async def list_tools(
        self,
        source: McpSourceConfiguration,
    ) -> McpToolCatalog:
        if not isinstance(source, McpHostSourceConfiguration):
            return await self._http_mcp_host.list_tools(source)
        binding = self._source_bindings.get(source.source_ref)
        instructions = binding.instructions if binding is not None else None
        # Bootstrap resolved these tools already. Serving them from that answer is what keeps
        # a Session with a dozen connectors from making a dozen more MCP calls to learn what
        # it has just been told, against the rate limit that makes those calls expensive.
        cached = self._source_tools.get(source.source_ref)
        if cached is not None:
            return McpToolCatalog(tools=list(cached), instructions=instructions)
        if binding is None:
            return await self._http_mcp_host.list_tools(source)
        tools = await self._api.list_tools(
            binding.connector_id,
            credentials_name=binding.credentials_name,
        )
        return McpToolCatalog(tools=tools, instructions=instructions)

    async def call_tool(self, request: McpToolCallRequest) -> McpToolCallResult:
        if not isinstance(request.source, McpHostSourceConfiguration):
            return await self._http_mcp_host.call_tool(request)
        binding = self._source_bindings.get(request.source.source_ref)
        if binding is None:
            return await self._http_mcp_host.call_tool(request)
        return await self._api.call_tool(
            binding.connector_id,
            request.remote_tool_name,
            dict(request.arguments),
            credentials_name=binding.credentials_name,
        )

    async def close(self) -> None:
        await self._api.close()

    def _build_source(
        self,
        slot: connector_decorator.ConnectorSlot,
        resolved: ResolvedConnector,
        *,
        credentials_name: str | None,
    ) -> McpHostSourceConfiguration:
        authored_name = slot.connector_name
        if authored_name in self._authored_slots:
            ref = _ConnectorSourceRef.for_slot(authored_name, credentials_name)
        else:
            ref = _ConnectorSourceRef.for_discovered_slot(authored_name, credentials_name)
        source_ref = ref.encode()
        binding = _ConnectorSourceBinding(
            connector_id=resolved.id,
            credentials_name=credentials_name,
            instructions=resolved.instructions,
        )
        self._source_bindings[source_ref] = binding
        return McpHostSourceConfiguration(
            id=source_ref,
            name=resolved.name,
            namespace=f"connector_{_safe_namespace(authored_name)}",
            source_ref=source_ref,
            mcp_app_connector_id=(resolved.id if slot.allow_mcp_ui else None),
            integration=McpIntegrationMetadata(id=resolved.id, name=resolved.name),
            model_access="direct",
        )


def _slot_owning(
    ref: _ConnectorSourceRef,
    configuration: MistralConnectorConfiguration,
    slots: Mapping[str, connector_decorator.ConnectorSlot],
) -> str | None:
    for authored_name in slots:
        credentials_name = configuration.credential_names.get(authored_name)
        if ref.owned_by(authored_name, credentials_name):
            return authored_name
    return None


def is_agents_sdk_connector_source(source: McpSourceConfiguration) -> bool:
    """Return whether this adapter minted the Host-routed MCP source."""

    return isinstance(source, McpHostSourceConfiguration) and source.source_ref.startswith(_SOURCE_PREFIX)


def _parse_bootstrap(payload: object) -> list[BootstrappedConnector]:
    """Read the bootstrap response, skipping any connector it could not describe.

    A connector the API failed on carries its own ``bootstrap_errors`` and no tools; it is
    reported as not ready rather than dropped, and ``auth_action`` then says whether
    connecting it is what it lacks.
    """

    if not isinstance(payload, dict):
        raise ValueError("The connectors bootstrap response is not an object")
    rows = payload.get("connectors")
    if not isinstance(rows, list):
        raise ValueError("The connectors bootstrap response carries no connector list")
    bootstrapped: list[BootstrappedConnector] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        identifier, name = row.get("id"), row.get("name")
        if not isinstance(identifier, str) or not isinstance(name, str):
            continue
        status = row.get("status")
        is_ready = bool(status.get("is_ready")) if isinstance(status, dict) else False
        needs_auth = isinstance(row.get("auth_action"), dict)
        raw_tools = row.get("tools")
        if not isinstance(raw_tools, list):
            raw_tools = []
        tools: list[McpRemoteToolDefinition] = []
        for raw_tool in raw_tools:
            try:
                tools.append(_build_remote_tool(raw_tool))
            except (KeyError, TypeError, ValidationError):
                logger.warning(
                    "agents_sdk skipped a bootstrap tool it could not read",
                    connector_name=name,
                )
        system_prompt = row.get("system_prompt")
        bootstrapped.append(
            BootstrappedConnector(
                id=identifier,
                name=name,
                is_ready=is_ready,
                tools=tuple(tools),
                needs_auth=needs_auth,
                instructions=system_prompt if isinstance(system_prompt, str) else None,
            )
        )
    return bootstrapped


def _build_remote_tool(tool: object) -> McpRemoteToolDefinition:
    if isinstance(tool, dict):
        payload = tool
    elif isinstance(tool, BaseModel):
        payload = tool.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True,
            exclude_unset=True,
            serialize_as_any=True,
        )
    else:
        raise TypeError(f"Unsupported connector tool response {type(tool).__name__}")
    return McpRemoteToolDefinition.model_validate(payload)


def _connector_response_text(content: Sequence[object]) -> str:
    values: list[str] = []
    for block in content:
        text = getattr(block, "text", None)
        if isinstance(text, str):
            values.append(text)
            continue
        if hasattr(block, "model_dump"):
            values.append(
                to_model_json_text(
                    block.model_dump(
                        mode="json",
                        by_alias=True,
                        exclude_none=True,
                        exclude_unset=True,
                    )
                )
            )
    return "\n".join(values)


def _structured_content_from_text(text: str) -> JsonValue:
    if not text:
        return None
    try:
        return _JSON_VALUE_ADAPTER.validate_python(json.loads(text))
    except json.JSONDecodeError:
        return text


def _safe_namespace(value: str) -> str:
    normalized = "".join(character if character.isalnum() else "_" for character in value)
    return normalized.strip("_") or "connector"


__all__ = [
    "AgentsSdkConnectorResource",
    "ConnectorApi",
    "ConnectorAuthenticationRequiredError",
    "ConnectorMcpNotSupportedError",
    "MistralConnectorApi",
    "ResolvedConnector",
    "is_agents_sdk_connector_source",
]

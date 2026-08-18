"""MCP server configs."""

import builtins
import hashlib
import os
import re
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from mistralai.vibe.sdk.capabilities.mcp.port import McpPort
from mistralai.vibe.sdk.utils.types import NonEmptyStr

if TYPE_CHECKING:
    from mcp import StdioServerParameters

__all__ = [
    "ConnectorMcpConfig",
    "ConnectorMcpDirectTransport",
    "ConnectorMcpSdkTransport",
    "ConnectorMcpTransport",
    "HttpMcpConfig",
    "McpConfigBase",
    "StdioMcpConfig",
]

DEFAULT_CONNECTOR_API_KEY_ENV_VAR = "MISTRAL_API_KEY"
DEFAULT_DIRECT_TIMEOUT_MS = 30_000
DEFAULT_STDIO_TIMEOUT_MS = 30_000
DEFAULT_CONNECTOR_MCP_PATH_TEMPLATE = "/connectors-gateway/{{connector_id}}/mcp"
TEMPLATED_VAR_EXPRESSION = re.compile(r"\{\{(\w+)\}\}")


def _resolve_scoped_headers(scoped_headers: dict[str, str]) -> dict[str, str]:
    """Resolve ``{{ENV_VAR}}`` placeholders from the host environment."""
    resolved: dict[str, str] = {}
    for header_name, value in scoped_headers.items():
        env_vars = {
            name: os.environ.get(name, "").strip()
            for name in TEMPLATED_VAR_EXPRESSION.findall(value)
        }
        resolved[header_name] = TEMPLATED_VAR_EXPRESSION.sub(
            lambda m, ev=env_vars: ev[m.group(1)], value
        )
    return resolved


class McpConfigBase(BaseModel):
    """Open base class for MCP server configs"""

    type: Any

    _registry: ClassVar[dict[str, builtins.type["McpConfigBase"]]] = {}

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        # Only register subclasses that pin ``type`` to a concrete default.
        if "type" not in cls.__annotations__:
            return
        type_field = cls.model_fields.get("type")
        if type_field is None or type_field.default is None:
            return
        type_name: str = type_field.default
        existing = cls._registry.get(type_name)
        if existing is not None and existing is not cls:
            msg = f"Duplicate MCP config type '{type_name}': {existing.__name__} and {cls.__name__}"
            raise TypeError(msg)
        cls._registry[type_name] = cls

    @model_validator(mode="wrap")
    @classmethod
    def _dispatch_config(cls, data: Any, handler: Any) -> "McpConfigBase":
        """Route dict data to the concrete config subclass."""
        if cls is not McpConfigBase:
            result: McpConfigBase = handler(data)
            return result
        if isinstance(data, McpConfigBase):
            return data
        if isinstance(data, dict):
            type_name = data.get("type")
            if type_name and type_name in cls._registry:
                concrete: McpConfigBase = cls._registry[type_name].model_validate(data)
                return concrete
            if type_name:
                msg = (
                    f"Unknown MCP config type '{type_name}'. "
                    f"Registered types: {sorted(cls._registry)}."
                )
                raise ValueError(msg)
        msg = (
            f"Cannot validate McpConfigBase from {type(data).__name__}: "
            f"expected dict or McpConfigBase instance"
        )
        raise ValueError(msg)

    def create_adapter(self) -> McpPort:
        """Create the runtime adapter for this MCP server config."""
        raise TypeError(f"Unsupported MCP config type: {type(self)}")

    @property
    def server_key(self) -> str:
        """Return the stable identifier derived from this MCP server config"""
        return hashlib.sha256(self.model_dump_json(exclude_none=False).encode()).hexdigest()


class StdioMcpConfig(McpConfigBase):
    """Config of a stdio MCP server (a local subprocess)."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["stdio"] = "stdio"
    command: str
    args: list[str] = Field(default_factory=list)
    cwd: str | Path | None = None
    encoding: str = "utf-8"
    encoding_error_handler: Literal["strict", "ignore", "replace"] = "strict"
    env: ClassVar[None] = None
    env_key_names: list[str] | None = Field(
        default=None,
        description=(
            "Names of host environment variables to project into the MCP "
            "subprocess. Values are read from the host at launch, so secrets "
            "are never stored in the serialized config."
        ),
    )
    timeout_ms: int = Field(
        default=DEFAULT_STDIO_TIMEOUT_MS,
        gt=0,
        description=(
            "Timeout in milliseconds applied to the MCP handshake and to each "
            "tools/list and tools/call request, so an unresponsive server "
            "cannot stall the agent turn indefinitely."
        ),
    )

    def to_stdio_parameters(self) -> "StdioServerParameters":
        from mcp import StdioServerParameters
        from mcp.client.stdio import get_default_environment

        env = None
        if self.env_key_names:
            env = get_default_environment()
            env.update(
                {name: os.environ[name] for name in self.env_key_names if name in os.environ}
            )
        return StdioServerParameters(
            command=self.command,
            args=self.args,
            env=env,
            cwd=self.cwd,
            encoding=self.encoding,
            encoding_error_handler=self.encoding_error_handler,
        )

    def create_adapter(self) -> McpPort:
        """Create the runtime adapter for this stdio MCP server."""
        from mistralai.vibe.sdk.capabilities.mcp.adapters.stdio_mcp import StdioMcpAdapter

        return StdioMcpAdapter(self)


DEFAULT_HTTP_TIMEOUT_MS = 30_000
DEFAULT_HTTP_SSE_READ_TIMEOUT_MS = 300_000


class HttpMcpConfig(McpConfigBase):
    """Config of an HTTP (Streamable HTTP) MCP server."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["http"] = "http"
    url: NonEmptyStr
    scoped_headers: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Headers sent on every request. A value is either a literal (sent "
            "verbatim) or a template with '{{ENV_VAR}}' placeholders (e.g. 'Bearer "
            "{{MISTRAL_API_KEY}}'). Placeholders are read from the host env at "
            "request time so secrets are never stored in the serialized config."
        ),
    )
    timeout_ms: int = Field(
        default=DEFAULT_HTTP_TIMEOUT_MS,
        gt=0,
        description="Timeout in milliseconds for the MCP handshake and each request.",
    )
    sse_read_timeout_ms: int = Field(
        default=DEFAULT_HTTP_SSE_READ_TIMEOUT_MS,
        gt=0,
        description="Timeout in milliseconds for reading SSE streams.",
    )

    @property
    def headers(self) -> dict[str, str]:
        """Resolve header values, substituting ``{{ENV_VAR}}`` placeholders from the host env."""
        return _resolve_scoped_headers(self.scoped_headers)

    def create_adapter(self) -> McpPort:
        from mistralai.vibe.sdk.capabilities.mcp.adapters.http_mcp import HttpMcpAdapter

        return HttpMcpAdapter(self)


class ConnectorMcpSdkTransport(BaseModel):
    """Reach a connector through the public Mistral SDK."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["sdk"] = "sdk"
    api_key_env_var: NonEmptyStr = Field(
        default=DEFAULT_CONNECTOR_API_KEY_ENV_VAR,
        description=(
            "Name of the host environment variable holding the Mistral API key. "
            "The value is read at runtime, so the secret is never stored in the "
            "serialized config."
        ),
    )
    server_url: NonEmptyStr | None = None
    timeout_ms: int | None = None

    @property
    def api_key(self) -> str:
        api_key = os.environ.get(self.api_key_env_var, "").strip()
        if not api_key:
            raise KeyError(f"Required environment variable is not set: {self.api_key_env_var}")

        return api_key

    def client_extra_params(self) -> dict[str, Any]:
        """Optional keyword params for the Mistral client."""
        params: dict[str, Any] = {}
        if self.server_url is not None:
            params["server_url"] = self.server_url
        if self.timeout_ms is not None:
            params["timeout_ms"] = self.timeout_ms

        return params


class ConnectorMcpDirectTransport(BaseModel):
    """Reach a connector directly through direct JSON-RPC http call."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["direct"] = "direct"
    base_url: NonEmptyStr
    origin_service: NonEmptyStr = Field(
        description=("Name of the calling service to identify caller."),
    )
    scoped_headers: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Headers sent on every request. A value is either a literal (sent "
            "verbatim) or a template with '{{ENV_VAR}}' placeholders (e.g. 'Bearer "
            "{{MISTRAL_API_KEY}}'). Placeholders are read from the host env at request time"
        ),
    )
    timeout_ms: int = Field(
        default=DEFAULT_DIRECT_TIMEOUT_MS,
        gt=0,
        description="Request timeout in milliseconds.",
    )
    mcp_path_template: NonEmptyStr = Field(
        default=DEFAULT_CONNECTOR_MCP_PATH_TEMPLATE,
        description=(
            "URL path of the direct endpoint, relative to the base url."
            "It may include a '{{connector_id}}' value that will replaced at runtime."
        ),
    )

    @property
    def headers(self) -> dict[str, str]:
        """Resolve header values, substituting ``{{ENV_VAR}}`` placeholders from the host env."""
        return _resolve_scoped_headers(self.scoped_headers)


ConnectorMcpTransport = Annotated[
    ConnectorMcpSdkTransport | ConnectorMcpDirectTransport,
    Field(discriminator="type"),
]


class ConnectorMcpConfig(McpConfigBase):
    """Config of a connector-backed MCP server."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["connector"] = "connector"
    connector_id_or_name: NonEmptyStr
    credentials_name: NonEmptyStr | None = Field(
        default=None,
        description=(
            "Selects which named credential set the connector uses to resolve, "
            "list, and call tools. Leave unset to use the connector's default "
            "credential resolution."
        ),
    )
    transport: ConnectorMcpTransport = Field(default_factory=ConnectorMcpSdkTransport)

    def create_adapter(self) -> McpPort:
        """Create the runtime adapter for this connector MCP server."""
        from mistralai.vibe.sdk.capabilities.mcp.adapters.connector_mcp import ConnectorMcpAdapter

        return ConnectorMcpAdapter(self)

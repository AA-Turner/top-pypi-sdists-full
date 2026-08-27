from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, model_validator

from xpander_sdk.models.shared import XPanderSharedModel


class MCPServerType(str, Enum):
    Local = "local"
    Remote = "remote"


class MCPServerAuthType(str, Enum):
    APIKey = "api_key"
    OAuth2 = "oauth2"
    CustomHeaders = "custom_headers"
    _None = "none"


class MCPServerTransport(str, Enum):
    STDIO = "stdio"
    SSE = "sse"
    HTTP_Transport = "streamable-http"


class MCPServerDetails(BaseModel):
    # the registry row this server came from; absent for a task-supplied or pre-registry server
    id: Optional[str] = None
    type: Optional[MCPServerType] = MCPServerType.Remote
    name: Optional[str] = None
    command: Optional[str] = None
    url: Optional[str] = None
    transport: Optional[MCPServerTransport] = MCPServerTransport.HTTP_Transport
    auth_type: Optional[MCPServerAuthType] = MCPServerAuthType._None
    api_key: Optional[str] = None
    use_secrets_manager: Optional[bool] = False
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    headers: Optional[Dict] = {}
    env_vars: Optional[Dict] = {}
    allowed_tools: Optional[List[str]] = []
    additional_scopes: Optional[List[str]] = []
    share_user_token_across_other_agents: Optional[bool] = True

    @model_validator(mode="after")
    def _coerce_transport_to_type(self) -> "MCPServerDetails":
        """Coerce type/transport coherent (local=>stdio, remote+stdio/null=>streamable-http); the runtime picks its client off `type`, so a mismatched pair is unsatisfiable. Mirror of xpander_dev_utils AIAgentGraphItemMCPSettings - keep in sync."""
        if self.type == MCPServerType.Local:
            if self.transport != MCPServerTransport.STDIO:
                self.transport = MCPServerTransport.STDIO
        elif self.transport in (MCPServerTransport.STDIO, None):
            self.transport = MCPServerTransport.HTTP_Transport
        return self


class MCPOAuthResponseType(str, Enum):
    NOT_SUPPORTED = "not_supported"
    LOGIN_REQUIRED = "login_required"
    TOKEN_ISSUE = "token_issue"
    TOKEN_READY = "token_ready"


class MCPOAuthGetTokenGenericResponse(XPanderSharedModel):
    message: str
    # Server identity so consumers (app auth cards) can correlate a token_issue
    # back to the specific MCP server when several are authenticating at once.
    server_url: Optional[str] = None
    server_name: Optional[str] = None


class MCPOAuthGetTokenLoginRequiredResponse(XPanderSharedModel):
    url: str
    server_url: str
    server_name: str


class MCPOAuthGetTokenTokenReadyResponse(XPanderSharedModel):
    access_token: str
    # Server identity so consumers can correlate a token_ready back to the
    # specific MCP server when several are authenticating concurrently.
    server_url: Optional[str] = None
    server_name: Optional[str] = None


class MCPOAuthGetTokenResponse(XPanderSharedModel):
    type: MCPOAuthResponseType
    data: Union[
        MCPOAuthGetTokenTokenReadyResponse,
        MCPOAuthGetTokenLoginRequiredResponse,
        MCPOAuthGetTokenGenericResponse,
    ]

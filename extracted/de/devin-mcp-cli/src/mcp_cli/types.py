from dataclasses import dataclass
from typing import List, TypedDict
from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel
from mcp.types import Tool, Resource, ResourceTemplate, Prompt


@dataclass
class ServerCapabilities:
    tools: List[Tool]
    resources: List[Resource | ResourceTemplate]
    prompts: List[Prompt]


class OAuthClientData(BaseModel):
    client_id: str

class OAuthTokens(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str | None
    scope: str | None
    obtained_at: datetime

class OAuthServerData(BaseModel):
    server_name: str
    tokens: OAuthTokens
    oauth_client_data: OAuthClientData
import typing as t
from enum import Enum

import pydantic

from connector.generated.models.credential_config import CredentialConfig
from connector.oai.capability import AuthRequest


class OAuthFlowType(str, Enum):
    CODE_FLOW = "CODE_FLOW"
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"


class ClientAuthenticationMethod(str, Enum):
    CLIENT_SECRET_POST = "CLIENT_SECRET_POST"
    CLIENT_SECRET_BASIC = "CLIENT_SECRET_BASIC"


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class RequestDataType(str, Enum):
    FORMDATA = "FORMDATA"
    JSON = "JSON"
    QUERY = "QUERY"


class OAuthRequest(pydantic.BaseModel):
    method: RequestMethod = RequestMethod.POST
    data: RequestDataType = RequestDataType.FORMDATA


class OAuthCapabilities(pydantic.BaseModel):
    get_authorization_url: bool = True
    handle_authorization_callback: bool = True
    handle_client_credentials_request: bool = True
    refresh_access_token: bool = True


class OAuthSettings(pydantic.BaseModel):
    authorization_url: str | t.Callable[[AuthRequest], str] | None = pydantic.Field(
        default=None,
        description="The URL to use to get the authorization code, if using the client credentials flow, this can be None. Can be a string, callable (method that accepts the request args and returns a string) or None.",
    )
    token_url: str | t.Callable[[AuthRequest], str] = pydantic.Field(
        description="The URL to use to get the access token, can be a string or callable (method that accepts the request args and returns a string).",
    )
    scopes: dict[str, str] | t.Callable[[AuthRequest], dict[str, str]] = pydantic.Field(
        default=None,
        description=(
            "A dictionary of scopes to request for the token, keyed by the name of each capability."
        ),
    )
    flow_type: OAuthFlowType = pydantic.Field(
        default=OAuthFlowType("CODE_FLOW"),
        description="The type of OAuth flow to use, defaults to CODE_FLOW.",
    )
    client_auth: ClientAuthenticationMethod | None = pydantic.Field(
        default=ClientAuthenticationMethod("CLIENT_SECRET_POST"),
        description="The client authentication method to use, defaults to CLIENT_SECRET_POST.",
    )
    request_type: OAuthRequest | None = pydantic.Field(
        default=OAuthRequest(method=RequestMethod("POST"), data=RequestDataType("FORMDATA")),
        description="The request type to use, defaults to POST with FORMDATA.",
    )
    capabilities: OAuthCapabilities = pydantic.Field(
        default=OAuthCapabilities(
            handle_authorization_callback=True,
            handle_client_credentials_request=True,
            get_authorization_url=True,
            refresh_access_token=True,
        ),
        description="The capabilities to use, defaults to all capabilities enabled.",
    )
    pkce: bool | None = pydantic.Field(
        default=False,
        description="Whether to use PKCE (code verifier and challenge), defaults to False.",
    )


class OAuthConfig(CredentialConfig):
    """
    OAuth config, this is a CredentialConfig, used when needing to configure OAuth for an apps credentials list.
    """

    oauth_settings: t.Annotated[
        OAuthSettings | None,
        pydantic.Field(
            default=None,
            description="The OAuth settings to use, defaults to all capabilities enabled.",
        ),
    ] = None

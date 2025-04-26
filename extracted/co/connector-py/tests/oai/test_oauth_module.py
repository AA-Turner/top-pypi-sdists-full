from unittest.mock import AsyncMock, patch
from urllib.parse import parse_qs, urlparse

import pytest
from connector.generated import (
    AuthModel,
    GetAuthorizationUrl,
    GetAuthorizationUrlRequest,
    HandleAuthorizationCallback,
    HandleAuthorizationCallbackRequest,
    HandleClientCredentials,
    HandleClientCredentialsRequest,
    OAuthClientCredential,
    OAuthCredential,
    RefreshAccessToken,
    RefreshAccessTokenRequest,
    StandardCapabilityName,
)
from connector.httpx_rewrite import AsyncClient
from connector.oai.capability import AuthRequest, get_settings
from connector.oai.errors import ConnectorError
from connector.oai.integration import DescriptionData, Integration
from connector.oai.modules.oauth_module import OAuthModule
from connector.oai.modules.oauth_module_types import (
    ClientAuthenticationMethod,
    OAuthConfig,
    OAuthFlowType,
    OAuthRequest,
    OAuthSettings,
    RequestDataType,
    RequestMethod,
)
from httpx import Request, Response
from pydantic import BaseModel, ValidationError


class Settings(BaseModel):
    subdomain: str


INTEGRATION_OAUTH_SETTINGS = OAuthSettings(
    authorization_url="https://example.com/auth",
    token_url="https://example.com/token",
    scopes={
        StandardCapabilityName.VALIDATE_CREDENTIALS: "test:scope another:scope",
        StandardCapabilityName.LIST_ACCOUNTS: "test:scope another:scope",
    },
)

INTEGRATION_OAUTH_SETTINGS_2 = OAuthSettings(
    authorization_url="https://example.com/auth2",
    token_url="https://example.com/token2",
    scopes={},
)

CLIENT_CREDENTIALS_INTEGRATION_OAUTH_SETTINGS = OAuthSettings(
    flow_type=OAuthFlowType.CLIENT_CREDENTIALS,
    token_url="https://example.com/token",
    scopes={
        StandardCapabilityName.VALIDATE_CREDENTIALS: "test:scope another:scope",
        StandardCapabilityName.LIST_ACCOUNTS: "test:scope another:scope",
    },
)


@pytest.fixture
def settings():
    return Settings(subdomain="test")


@pytest.fixture()
def integration():
    """
    FIXTURE: Create an integration with an OAuthModule
    """
    return Integration(
        app_id="test_app",
        auth=OAuthCredential,
        version="0.1.0",
        exception_handlers=[],
        settings_model=Settings,
        oauth_settings=INTEGRATION_OAUTH_SETTINGS,
        description_data=DescriptionData(user_friendly_name="test_oauth_module.py", categories=[]),
    )


@pytest.fixture()
def client_credentials_integration():
    """
    FIXTURE: Create an integration with an OAuthModule configured with a client credentials flow
    """
    return Integration(
        app_id="test_app",
        auth=OAuthClientCredential,
        version="0.1.0",
        exception_handlers=[],
        settings_model=Settings,
        oauth_settings=CLIENT_CREDENTIALS_INTEGRATION_OAUTH_SETTINGS,
        description_data=DescriptionData(user_friendly_name="test_oauth_module.py", categories=[]),
    )


@pytest.fixture()
def integration_with_credentials():
    """
    FIXTURE: Create an integration that uses OAuthModule through the credentials configs
    """
    return Integration(
        app_id="test_app",
        credentials=[
            OAuthConfig(
                id="test_credential",
                type=AuthModel.OAUTH,
                description="Test credential",
                oauth_settings=INTEGRATION_OAUTH_SETTINGS,
            ),
            OAuthConfig(
                id="test_credential_2",
                type=AuthModel.OAUTH,
                description="Test credential 2",
                oauth_settings=INTEGRATION_OAUTH_SETTINGS_2,
            ),
        ],
        version="0.1.0",
        exception_handlers=[],
        settings_model=Settings,
        description_data=DescriptionData(user_friendly_name="test_oauth_module.py", categories=[]),
    )


@pytest.fixture(autouse=True)
def cleanup_integration(integration, client_credentials_integration):
    """
    FIXTURE: Cleanup the integrations before each test is run
    """
    integration.oauth_settings = INTEGRATION_OAUTH_SETTINGS
    client_credentials_integration.oauth_settings = CLIENT_CREDENTIALS_INTEGRATION_OAUTH_SETTINGS

    integration.auth = OAuthCredential
    client_credentials_integration.auth = OAuthClientCredential
    integration_with_credentials.credentials = [
        OAuthConfig(
            id="test_credential",
            type=AuthModel.OAUTH,
            description="Test credential",
            oauth_settings=INTEGRATION_OAUTH_SETTINGS,
        ),
        OAuthConfig(
            id="test_credential_2",
            type=AuthModel.OAUTH,
            description="Test credential 2",
            oauth_settings=INTEGRATION_OAUTH_SETTINGS,
        ),
    ]

    yield


def get_oauth_module(integration: Integration) -> OAuthModule:
    """
    HELPER: Get the OAuthModule from the integration
    """
    for module in integration.modules:
        if isinstance(module, OAuthModule):
            return module
    raise ValueError("OAuthModule not found")


def test_get_scopes(integration):
    """
    Test if OAuthModule correctly returns the scopes defined in the integration settings
    """
    module = get_oauth_module(integration)

    request = GetAuthorizationUrlRequest(
        request=GetAuthorizationUrl(
            client_id="test_client_id",
            redirect_uri="https://example.com/callback",
            state="test_state",
            scopes=[],
        ),
        settings={"subdomain": "test"},
    )

    if isinstance(module.settings[0], OAuthSettings):
        scopes = module._get_scopes(module.settings[0], request)
        assert set(scopes.split()) == {"test:scope", "another:scope"}
    else:
        with pytest.raises(ConnectorError):
            module._get_scopes(module.settings[0], request)  # type: ignore


def test_get_scopes_with_scopes_callable(integration):
    """
    Test if OAuthModule correctly returns the scopes defined in the integration settings if its a callable
    """

    def get_scopes(args: AuthRequest) -> dict[str, str]:
        return {
            StandardCapabilityName.VALIDATE_CREDENTIALS: "test:scope another:scope",
            StandardCapabilityName.LIST_ACCOUNTS: "test:scope another:scope",
        }

    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].scopes = get_scopes

    request = GetAuthorizationUrlRequest(
        request=GetAuthorizationUrl(
            client_id="test_client_id",
            redirect_uri="https://example.com/callback",
            state="test_state",
            scopes=[],
        ),
        settings={"subdomain": "test"},
    )

    if isinstance(module.settings[0], OAuthSettings):
        scopes = module._get_scopes(module.settings[0], request)
        assert set(scopes.split()) == {"test:scope", "another:scope"}
    else:
        with pytest.raises(ConnectorError):
            module._get_scopes(module.settings[0], request)  # type: ignore


@pytest.mark.asyncio
async def test_dynamic_authorization_url(integration):
    """
    Test if OAuthModule correctly handles dynamic authorization URLs based on settings
    """

    def get_auth_url(args: AuthRequest) -> str:
        settings = get_settings(args, integration.settings_model)
        return f"https://{settings.subdomain}.example.com/auth"

    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].authorization_url = get_auth_url

    request = GetAuthorizationUrlRequest(
        request=GetAuthorizationUrl(
            client_id="test_client_id",
            redirect_uri="https://test.example.com/callback",
            state="test_state",
            scopes=["scope1"],
        ),
        settings={"subdomain": "test"},
    )

    response = await integration.capabilities[StandardCapabilityName.GET_AUTHORIZATION_URL](request)

    parsed_url = urlparse(response.response.authorization_url)
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "test.example.com"
    assert parsed_url.path == "/auth"


@pytest.mark.asyncio
async def test_dynamic_token_url(integration):
    """
    Test if OAuthModule correctly handles dynamic token URLs based on settings
    """

    def get_token_url(args: AuthRequest) -> str:
        settings = get_settings(args, integration.settings_model)
        return f"https://{settings.subdomain}.example.com/token"

    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].token_url = get_token_url

    request = HandleAuthorizationCallbackRequest(
        request=HandleAuthorizationCallback(
            client_id="test_client_id",
            client_secret="test_secret",
            redirect_uri_with_code="https://test.example.com/callback?code=test_code",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={"access_token": "test_token", "token_type": "bearer"},
        request=Request("POST", "https://test.example.com/token"),
    )

    with patch.object(AsyncClient, "request", return_value=mock_response) as mock_request:
        await integration.capabilities[StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK](
            request
        )

        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs["url"] == "https://test.example.com/token"


@pytest.mark.asyncio
async def test_get_authorization_url(integration):
    """
    Test if OAuthModule correctly constructs the authorization URL
    """
    request = GetAuthorizationUrlRequest(
        request=GetAuthorizationUrl(
            client_id="test_client_id",
            redirect_uri="https://test.example.com/callback",
            state="test_state",
            scopes=["scope1", "scope2", "scope3"],
        ),
        settings={"subdomain": "test"},
    )

    response = await integration.capabilities[StandardCapabilityName.GET_AUTHORIZATION_URL](request)

    parsed_url = urlparse(response.response.authorization_url)

    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "test.example.com"
    assert parsed_url.path == "/auth"

    assert "client_id=test_client_id" in parsed_url.query
    assert "redirect_uri=https%3A%2F%2Ftest.example.com%2Fcallback" in parsed_url.query
    assert "state=test_state" in parsed_url.query
    assert "scope=scope1+scope2+scope3" in parsed_url.query


@pytest.mark.asyncio
async def test_get_authorization_url_no_input_scopes(integration):
    """
    Test if OAuthModule falls back to the scopes defined in the integration settings
    if no scopes are provided in the request to the connector
    """
    request = GetAuthorizationUrlRequest(
        request=GetAuthorizationUrl(
            client_id="test_client_id",
            redirect_uri="https://test.example.com/callback",
            state="test_state",
            scopes=[],
        ),
        settings={"subdomain": "test"},
    )

    response = await integration.capabilities[StandardCapabilityName.GET_AUTHORIZATION_URL](request)

    parsed_url = urlparse(response.response.authorization_url)
    scopes = parse_qs(parsed_url.query).get("scope", [""])[0].split()
    assert set(scopes) == {"another:scope", "test:scope"}


@pytest.mark.asyncio
async def test_handle_authorization_callback(integration):
    """
    Test if OAuthModule correctly handles the authorization callback
    """
    request = HandleAuthorizationCallbackRequest(
        request=HandleAuthorizationCallback(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri_with_code="https://test.example.com/callback?code=test_code",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "refresh_token": "test_refresh_token",
        },
        request=Request("POST", "https://test.example.com/token"),
    )

    with patch.object(AsyncClient, "request", return_value=mock_response):
        response = await integration.capabilities[
            StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK
        ](request)

    assert response.response.access_token == "test_access_token"
    assert response.response.token_type == "bearer"
    assert response.response.refresh_token == "test_refresh_token"


@pytest.mark.asyncio
async def test_handle_client_credentials_request(client_credentials_integration):
    """
    Test if OAuthModule correctly handles the client credentials request
    """
    request = HandleClientCredentialsRequest(
        request=HandleClientCredentials(
            client_id="test_client_id",
            client_secret="test_client_secret",
            scopes=["scope1", "scope2", "scope3"],
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            "access_token": "test_access_token",
            "token_type": "Bearer",
        },
        request=Request("POST", "https://test.example.com/token"),
    )

    with patch.object(AsyncClient, "request", return_value=mock_response):
        response = await client_credentials_integration.capabilities[
            StandardCapabilityName.HANDLE_CLIENT_CREDENTIALS_REQUEST
        ](request)

    assert response.response.access_token == "test_access_token"
    assert response.response.token_type == "bearer"


@pytest.mark.asyncio
async def test_refresh_access_token(integration):
    """
    Test if OAuthModule correctly refreshes the access token
    """
    request = RefreshAccessTokenRequest(
        request=RefreshAccessToken(
            client_id="test_client_id",
            client_secret="test_client_secret",
            refresh_token="test_refresh_token",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            "access_token": "new_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "new_refresh_token",
        },
        request=Request("POST", "https://test.example.com/token"),
    )

    with patch.object(AsyncClient, "request", return_value=mock_response):
        response = await integration.capabilities[StandardCapabilityName.REFRESH_ACCESS_TOKEN](
            request
        )

    assert response.response.access_token == "new_access_token"
    assert response.response.token_type == "bearer"
    assert response.response.refresh_token == "new_refresh_token"


@pytest.mark.asyncio
async def test_send_authorized_request_client_secret_basic(integration):
    """
    Test if OAuthModule correctly constructs the request for the token endpoint
    when using client secret basic authentication (header auth)
    """
    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].client_auth = ClientAuthenticationMethod.CLIENT_SECRET_BASIC

    request = HandleAuthorizationCallbackRequest(
        request=HandleAuthorizationCallback(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri_with_code="https://test.example.com/callback?code=test_code",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "refresh_token": "test_refresh_token",
        },
        request=Request("POST", "https://test.example.com/token"),
    )

    mock_client = AsyncMock(spec=AsyncClient)
    mock_client.request.return_value = mock_response

    await module._send_authorized_request(
        "https://test.example.com/token", "authorization_code", mock_client, request
    )

    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args.kwargs["auth"] is not None
    assert "client_id" not in call_args.kwargs["data"]
    assert "client_secret" not in call_args.kwargs["data"]


@pytest.mark.asyncio
async def test_send_authorized_request_query_request_type(integration):
    """
    Test if OAuthModule correctly constructs the request for the token endpoint
    when using a request type with QUERY as the data parameter
    """
    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].request_type = OAuthRequest(
            method=RequestMethod.GET, data=RequestDataType.QUERY
        )

    request = RefreshAccessTokenRequest(
        request=RefreshAccessToken(
            client_id="test_client_id",
            client_secret="test_client_secret",
            refresh_token="test_refresh_token",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "refresh_token": "test_refresh_token",
        },
        request=Request("POST", "https://test.example.com/token"),
    )

    mock_client = AsyncMock(spec=AsyncClient)
    mock_client.request.return_value = mock_response

    await module._send_authorized_request(
        "https://test.example.com/token", "refresh_token", mock_client, request
    )

    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args.kwargs["method"] == "GET"
    assert call_args.kwargs["params"] is not None
    assert call_args.kwargs["data"] is None
    assert call_args.kwargs["json"] is None


@pytest.mark.asyncio
async def test_send_authorized_request_json_request_type(integration):
    """
    Test if OAuthModule correctly constructs the request for the token endpoint
    when using a request type with JSON as the data parameter
    """
    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].request_type = OAuthRequest(
            method=RequestMethod.GET, data=RequestDataType.JSON
        )

    request = RefreshAccessTokenRequest(
        request=RefreshAccessToken(
            client_id="test_client_id",
            client_secret="test_client_secret",
            refresh_token="test_refresh_token",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "refresh_token": "test_refresh_token",
        },
        request=Request("GET", "https://test.example.com/token"),
    )

    mock_client = AsyncMock(spec=AsyncClient)
    mock_client.request.return_value = mock_response

    await module._send_authorized_request(
        "https://test.example.com/token", "refresh_token", mock_client, request
    )

    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args.kwargs["method"] == "GET"
    assert call_args.kwargs["params"] is None
    assert call_args.kwargs["data"] is None
    assert call_args.kwargs["json"] is not None


@pytest.mark.asyncio
async def test_send_authorized_request_formdata_request_type(integration):
    """
    Test if OAuthModule correctly constructs the request for the token endpoint
    when using a request type with FORMDATA as the data parameter
    """
    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].request_type = OAuthRequest(
            method=RequestMethod.GET, data=RequestDataType.FORMDATA
        )

    request = RefreshAccessTokenRequest(
        request=RefreshAccessToken(
            client_id="test_client_id",
            client_secret="test_client_secret",
            refresh_token="test_refresh_token",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "refresh_token": "test_refresh_token",
        },
        request=Request("POST", "https://test.example.com/token"),
    )

    mock_client = AsyncMock(spec=AsyncClient)
    mock_client.request.return_value = mock_response

    await module._send_authorized_request(
        "https://test.example.com/token", "refresh_token", mock_client, request
    )

    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args.kwargs["method"] == "GET"
    assert call_args.kwargs["params"] is None
    assert call_args.kwargs["data"] is not None
    assert call_args.kwargs["json"] is None


@pytest.mark.asyncio
async def test_handle_authorization_callback_error(integration):
    """
    Test if OAuthModule correctly handles errors during authorization callback
    """
    request = HandleAuthorizationCallbackRequest(
        request=HandleAuthorizationCallback(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri_with_code="https://test.example.com/callback?code=test_code",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        400,
        json={"error": "invalid_grant", "error_description": "Invalid authorization code"},
        request=Request("POST", "https://test.example.com/token"),
    )

    with patch.object(AsyncClient, "request", return_value=mock_response):
        with pytest.raises(ConnectorError):
            await integration.capabilities[StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK](
                request
            )


@pytest.mark.asyncio
async def test_invalid_grant_type(integration):
    """
    Test if OAuthModule correctly handles an invalid grant type
    """
    module = get_oauth_module(integration)
    request = RefreshAccessTokenRequest(
        request=RefreshAccessToken(
            client_id="test_client_id",
            client_secret="test_client_secret",
            refresh_token="test_refresh_token",
        ),
        settings={"subdomain": "test"},
    )

    mock_client = AsyncMock(spec=AsyncClient)
    with pytest.raises(ValueError, match="Unsupported grant_type"):
        await module._send_authorized_request(
            "https://test.example.com/token", "invalid_grant_type", mock_client, request
        )


@pytest.mark.asyncio
async def test_oauth_credentials_conversion_error(integration):
    """
    Test if OAuthModule correctly handles errors when converting raw JSON to OAuthCredentials
    """
    request = HandleAuthorizationCallbackRequest(
        request=HandleAuthorizationCallback(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri_with_code="https://test.example.com/callback?code=test_code",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            # Missing required fields
            "some_other_field": "value",
        },
        request=Request("POST", "https://test.example.com/token"),
    )

    with patch.object(AsyncClient, "request", return_value=mock_response):
        with pytest.raises(ValidationError, match="1 validation error for OauthCredentials"):
            await integration.capabilities[StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK](
                request
            )


@pytest.mark.asyncio
async def test_handle_authorization_callback_pkce(integration):
    """
    Test if OAuthModule correctly handles the authorization callback with PKCE
    """
    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].client_auth = ClientAuthenticationMethod.CLIENT_SECRET_POST
        module.settings[0].pkce = True

    request = HandleAuthorizationCallbackRequest(
        request=HandleAuthorizationCallback(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri_with_code="https://test.example.com/callback?code=test_code",
            code_verifier="test_code_verifier",
        ),
        settings={"subdomain": "test"},
    )

    mock_response = Response(
        200,
        json={
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "refresh_token": "test_refresh_token",
        },
        request=Request("POST", "https://test.example.com/token"),
    )

    mock_client = AsyncMock(spec=AsyncClient)
    mock_client.request.return_value = mock_response

    await module._send_authorized_request(
        "https://test.example.com/token", "authorization_code", mock_client, request
    )

    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args.kwargs["data"] == {
        "grant_type": "authorization_code",
        "code": "test_code",
        "redirect_uri": "https://test.example.com/callback",
        "code_verifier": "test_code_verifier",  # must be included
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
    }


@pytest.mark.asyncio
async def test_get_authorization_url_pkce(integration):
    """
    Test if OAuthModule correctly handles the authorization URL with PKCE
    """
    module = get_oauth_module(integration)
    if isinstance(module.settings[0], OAuthSettings):
        module.settings[0].pkce = True

    request = GetAuthorizationUrlRequest(
        request=GetAuthorizationUrl(
            client_id="test_client_id",
            redirect_uri="https://test.example.com/callback",
            state="test_state",
            scopes=["scope1"],
        ),
        settings={"subdomain": "test"},
    )

    response = await integration.capabilities[StandardCapabilityName.GET_AUTHORIZATION_URL](request)

    parsed_url = urlparse(response.response.authorization_url)
    query_params = parse_qs(parsed_url.query)
    assert "code_challenge" in query_params
    assert "code_challenge_method" in query_params


@pytest.mark.asyncio
async def test_check_oauth_module_settings_when_using_credentials(integration_with_credentials):
    """
    Test if OAuthModule correctly collects the settings from the credentials configs
    """
    module = get_oauth_module(integration_with_credentials)

    assert isinstance(module.settings[0], OAuthConfig)
    assert isinstance(module.settings[1], OAuthConfig)

    assert module.settings[0].id == "test_credential"
    assert module.settings[1].id == "test_credential_2"


@pytest.mark.asyncio
async def test_get_authorization_url_with_credentials(integration_with_credentials):
    """
    Test if OAuthModule correctly handles the authorization URL when configured with credentials
    """
    module = get_oauth_module(integration_with_credentials)
    assert not isinstance(module.settings[0], OAuthSettings)
    assert len(module.settings) == 2

    request = GetAuthorizationUrlRequest(
        request=GetAuthorizationUrl(
            credential_id="test_credential",  # match
            client_id="test_client_id",
            redirect_uri="https://test.example.com/callback",
            state="test_state",
            scopes=["scope1", "scope2", "scope3"],
        ),
        settings={"subdomain": "test"},
    )

    response = await integration_with_credentials.capabilities[
        StandardCapabilityName.GET_AUTHORIZATION_URL
    ](request)

    parsed_url = urlparse(response.response.authorization_url)
    assert parsed_url.path == "/auth"

    assert "client_id=test_client_id" in parsed_url.query
    assert "redirect_uri=https%3A%2F%2Ftest.example.com%2Fcallback" in parsed_url.query
    assert "state=test_state" in parsed_url.query
    assert "scope=scope1+scope2+scope3" in parsed_url.query


@pytest.mark.asyncio
async def test_get_authorization_url_with_credentials_2(integration_with_credentials):
    """
    Test if OAuthModule correctly handles the authorization URL when configured with credentials
    """
    request = GetAuthorizationUrlRequest(
        request=GetAuthorizationUrl(
            credential_id="test_credential_2",  # match
            client_id="test_client_id",
            redirect_uri="https://test.example.com/callback",
            state="test_state",
            scopes=["scope1", "scope2", "scope3"],
        ),
        settings={"subdomain": "test"},
    )

    response = await integration_with_credentials.capabilities[
        StandardCapabilityName.GET_AUTHORIZATION_URL
    ](request)

    parsed_url = urlparse(response.response.authorization_url)
    assert parsed_url.path == "/auth2"  # parent credential settings are changed

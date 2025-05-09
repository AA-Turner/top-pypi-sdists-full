import time

import pytest
import respx
from httpx import HTTPError, Response

from httpx_oauth.oauth2 import (
    GetAccessTokenError,
    MissingRevokeTokenAuthMethodError,
    NotSupportedAuthMethodError,
    OAuth2,
    OAuth2Token,
    RefreshTokenError,
    RefreshTokenNotSupportedError,
    RevokeTokenError,
    RevokeTokenNotSupportedError,
)

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
AUTHORIZE_ENDPOINT = "https://www.camelot.bt/authorize"
ACCESS_TOKEN_ENDPOINT = "https://www.camelot.bt/access-token"
REDIRECT_URI = "https://www.tintagel.bt/oauth-callback"
REFRESH_TOKEN_ENDPOINT = "https://www.camelot.bt/refresh"
REVOKE_TOKEN_ENDPOINT = "https://www.camelot.bt/revoke"


@pytest.fixture(scope="module", params=["client_secret_basic", "client_secret_post"])
def client(request: pytest.FixtureRequest) -> OAuth2:
    return OAuth2(
        CLIENT_ID,
        CLIENT_SECRET,
        AUTHORIZE_ENDPOINT,
        ACCESS_TOKEN_ENDPOINT,
        token_endpoint_auth_method=request.param,
    )


@pytest.fixture(scope="module", params=["client_secret_basic", "client_secret_post"])
def client_refresh(request: pytest.FixtureRequest) -> OAuth2:
    return OAuth2(
        CLIENT_ID,
        CLIENT_SECRET,
        AUTHORIZE_ENDPOINT,
        ACCESS_TOKEN_ENDPOINT,
        refresh_token_endpoint=REFRESH_TOKEN_ENDPOINT,
        token_endpoint_auth_method=request.param,
    )


@pytest.fixture(scope="module", params=["client_secret_basic", "client_secret_post"])
def client_revoke(request: pytest.FixtureRequest) -> OAuth2:
    return OAuth2(
        CLIENT_ID,
        CLIENT_SECRET,
        AUTHORIZE_ENDPOINT,
        ACCESS_TOKEN_ENDPOINT,
        revoke_token_endpoint=REVOKE_TOKEN_ENDPOINT,
        token_endpoint_auth_method=request.param,
        revocation_endpoint_auth_method=request.param,
    )


def test_not_supported_auth_method() -> None:
    with pytest.raises(NotSupportedAuthMethodError):
        OAuth2(
            CLIENT_ID,
            CLIENT_SECRET,
            AUTHORIZE_ENDPOINT,
            ACCESS_TOKEN_ENDPOINT,
            token_endpoint_auth_method="invalid",  # type: ignore
        )


def test_missing_revoke_token_auth_method() -> None:
    with pytest.raises(MissingRevokeTokenAuthMethodError):
        OAuth2(
            CLIENT_ID,
            CLIENT_SECRET,
            AUTHORIZE_ENDPOINT,
            ACCESS_TOKEN_ENDPOINT,
            revoke_token_endpoint=REVOKE_TOKEN_ENDPOINT,
        )


class TestOAuth2Token:
    @pytest.mark.parametrize(
        "expires_at,expired", [(0, True), (time.time() + 3600, False)]
    )
    def test_expires_at(self, expires_at, expired):
        token = OAuth2Token({"access_token": "ACCESS_TOKEN", "expires_at": expires_at})

        assert token["access_token"] == "ACCESS_TOKEN"
        assert token.is_expired() is expired

    def test_expires_in(self):
        token = OAuth2Token({"access_token": "ACCESS_TOKEN", "expires_in": 3600})

        assert token["access_token"] == "ACCESS_TOKEN"
        assert "expires_at" in token
        assert token.is_expired() is False

    def test_no_expire(self):
        token = OAuth2Token({"access_token": "ACCESS_TOKEN"})

        assert token["access_token"] == "ACCESS_TOKEN"
        assert token.is_expired() is False


@pytest.mark.asyncio
class TestGetAuthorizationURL:
    async def test_get_authorization_url(self, client: OAuth2):
        authorization_url = await client.get_authorization_url(REDIRECT_URI)
        assert authorization_url.startswith("https://www.camelot.bt/authorize")
        assert "response_type=code" in authorization_url
        assert f"client_id={CLIENT_ID}" in authorization_url
        assert (
            "redirect_uri=https%3A%2F%2Fwww.tintagel.bt%2Foauth-callback"
            in authorization_url
        )

    async def test_get_authorization_url_with_state(self, client: OAuth2):
        authorization_url = await client.get_authorization_url(
            REDIRECT_URI,
            state="STATE",
        )
        assert "state=STATE" in authorization_url

    async def test_get_authorization_url_with_scopes(self, client: OAuth2):
        authorization_url = await client.get_authorization_url(
            REDIRECT_URI,
            scope=["SCOPE1", "SCOPE2", "SCOPE3"],
        )
        assert "scope=SCOPE1+SCOPE2+SCOPE3" in authorization_url

    async def test_get_authorization_url_with_plain_code_challenge(
        self, client: OAuth2
    ):
        authorization_url = await client.get_authorization_url(
            REDIRECT_URI,
            code_challenge="CODE_CHALLENGE",
            code_challenge_method="plain",
        )
        assert "code_challenge=CODE_CHALLENGE" in authorization_url
        assert "code_challenge_method=plain" in authorization_url

    @pytest.mark.asyncio
    async def test_get_authorization_url_with_extras_params(self, client: OAuth2):
        authorization_url = await client.get_authorization_url(
            REDIRECT_URI,
            extras_params={"PARAM1": "VALUE1", "PARAM2": "VALUE2"},
        )
        assert "PARAM1=VALUE1" in authorization_url
        assert "PARAM2=VALUE2" in authorization_url


@pytest.mark.asyncio
class TestGetAccessToken:
    @respx.mock
    async def test_get_access_token(
        self, load_mock, get_respx_call_args, client: OAuth2
    ):
        request = respx.post(client.access_token_endpoint).mock(
            return_value=Response(200, json=load_mock("google_success_access_token"))
        )
        access_token = await client.get_access_token(
            "CODE", REDIRECT_URI, "CODE_VERIFIER"
        )

        url, headers, content = await get_respx_call_args(request)
        assert headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert headers["Accept"] == "application/json"
        assert "grant_type=authorization_code" in content
        assert "code=CODE" in content
        assert "code_verifier=CODE_VERIFIER" in content
        assert "redirect_uri=https%3A%2F%2Fwww.tintagel.bt%2Foauth-callback" in content

        if client.token_endpoint_auth_method == "client_secret_basic":
            assert "Authorization" in headers
            assert headers["Authorization"].startswith("Basic ")
        elif client.token_endpoint_auth_method == "client_secret_post":
            assert f"client_id={CLIENT_ID}" in content
            assert f"client_secret={CLIENT_SECRET}" in content

        assert type(access_token) is OAuth2Token
        assert "access_token" in access_token
        assert "token_type" in access_token
        assert access_token.is_expired() is False

    @respx.mock
    async def test_get_access_token_error(self, load_mock, client: OAuth2):
        respx.post(client.access_token_endpoint).mock(
            return_value=Response(400, json=load_mock("error"))
        )

        with pytest.raises(GetAccessTokenError) as excinfo:
            await client.get_access_token("CODE", REDIRECT_URI)
        assert isinstance(excinfo.value.response, Response)

    @respx.mock
    async def test_get_access_token_http_error(self, client: OAuth2):
        respx.post(client.access_token_endpoint).mock(side_effect=HTTPError("ERROR"))

        with pytest.raises(GetAccessTokenError) as excinfo:
            await client.get_access_token("CODE", REDIRECT_URI)
        assert excinfo.value.response is None

    @respx.mock
    async def test_get_access_token_json_error(self, client: OAuth2):
        respx.post(client.access_token_endpoint).mock(
            return_value=Response(200, text="NOT JSON")
        )

        with pytest.raises(GetAccessTokenError) as excinfo:
            await client.get_access_token("CODE", REDIRECT_URI)
        assert isinstance(excinfo.value.response, Response)


@pytest.mark.asyncio
class TestRefreshToken:
    @respx.mock
    async def test_unsupported_refresh_token(self, client: OAuth2):
        with pytest.raises(RefreshTokenNotSupportedError):
            await client.refresh_token("REFRESH_TOKEN")

    @respx.mock
    async def test_refresh_token(
        self, load_mock, get_respx_call_args, client_refresh: OAuth2
    ):
        request = respx.post(client_refresh.refresh_token_endpoint).mock(
            return_value=Response(200, json=load_mock("google_success_refresh_token"))
        )
        access_token = await client_refresh.refresh_token("REFRESH_TOKEN")

        url, headers, content = await get_respx_call_args(request)
        assert headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert headers["Accept"] == "application/json"
        assert "grant_type=refresh_token" in content
        assert "refresh_token=REFRESH_TOKEN" in content

        if client_refresh.token_endpoint_auth_method == "client_secret_basic":
            assert "Authorization" in headers
            assert headers["Authorization"].startswith("Basic ")
        elif client_refresh.token_endpoint_auth_method == "client_secret_post":
            assert f"client_id={CLIENT_ID}" in content
            assert f"client_secret={CLIENT_SECRET}" in content

        assert type(access_token) is OAuth2Token
        assert "access_token" in access_token
        assert "token_type" in access_token
        assert access_token.is_expired() is False

    @respx.mock
    async def test_refresh_token_error(self, load_mock, client_refresh: OAuth2):
        respx.post(client_refresh.refresh_token_endpoint).mock(
            return_value=Response(400, json=load_mock("error"))
        )

        with pytest.raises(RefreshTokenError) as excinfo:
            await client_refresh.refresh_token("REFRESH_TOKEN")
        assert isinstance(excinfo.value.response, Response)

    @respx.mock
    async def test_refresh_token_http_error(self, client_refresh: OAuth2):
        respx.post(client_refresh.refresh_token_endpoint).mock(
            side_effect=HTTPError("ERROR")
        )

        with pytest.raises(RefreshTokenError) as excinfo:
            await client_refresh.refresh_token("REFRESH_TOKEN")
        assert excinfo.value.response is None

    @respx.mock
    async def test_refresh_token_json_error(self, client_refresh: OAuth2):
        respx.post(client_refresh.refresh_token_endpoint).mock(
            return_value=Response(200, text="NOT JSON")
        )

        with pytest.raises(RefreshTokenError) as excinfo:
            await client_refresh.refresh_token("REFRESH_TOKEN")
        assert isinstance(excinfo.value.response, Response)


@pytest.mark.asyncio
class TestRevokeToken:
    @respx.mock
    async def test_unsupported_revoke_token(self, client: OAuth2):
        with pytest.raises(RevokeTokenNotSupportedError):
            await client.revoke_token("TOKEN")

    @respx.mock
    async def test_revoke_token(
        self, load_mock, get_respx_call_args, client_revoke: OAuth2
    ):
        request = respx.post(client_revoke.revoke_token_endpoint).mock(
            return_value=Response(200)
        )
        await client_revoke.revoke_token("TOKEN", "TOKEN_TYPE_HINT")

        url, headers, content = await get_respx_call_args(request)
        assert headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert headers["Accept"] == "application/json"
        assert "token=TOKEN" in content
        assert "token_type_hint=TOKEN_TYPE_HINT" in content

        if client_revoke.revocation_endpoint_auth_method == "client_secret_basic":
            assert "Authorization" in headers
            assert headers["Authorization"].startswith("Basic ")
        elif client_revoke.revocation_endpoint_auth_method == "client_secret_post":
            assert f"client_id={CLIENT_ID}" in content
            assert f"client_secret={CLIENT_SECRET}" in content

    @respx.mock
    async def test_revoke_token_error(self, load_mock, client_revoke: OAuth2):
        respx.post(client_revoke.revoke_token_endpoint).mock(
            return_value=Response(400, json=load_mock("error"))
        )

        with pytest.raises(RevokeTokenError) as excinfo:
            await client_revoke.revoke_token("TOKEN", "TOKEN_TYPE_HINT")
        assert isinstance(excinfo.value.response, Response)

    @respx.mock
    async def test_revoke_token_http_error(self, client_revoke: OAuth2):
        respx.post(client_revoke.revoke_token_endpoint).mock(
            side_effect=HTTPError("ERROR")
        )

        with pytest.raises(RevokeTokenError) as excinfo:
            await client_revoke.revoke_token("TOKEN", "TOKEN_TYPE_HINT")
        assert excinfo.value.response is None


@pytest.mark.asyncio
class TestGetProfile:
    async def test_not_implemented(self, client: OAuth2):
        with pytest.raises(NotImplementedError):
            await client.get_profile("TOKEN")


@pytest.mark.asyncio
class TestGetIdEmail:
    async def test_not_implemented(self, client: OAuth2):
        with pytest.raises(NotImplementedError):
            await client.get_id_email("TOKEN")

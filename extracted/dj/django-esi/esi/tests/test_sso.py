import base64
import pickle
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import httpx2
from jose import jwt

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import SimpleTestCase, TestCase

from esi import __url__, __version__, sso
from esi.errors import IncompleteResponseError, SSOOAuthError, SSOUnavailableError
from esi.models import Token

from . import _generate_token, _store_as_Token
from .jwt_factory import _RSA_PRIVATE_KEY, generate_jwk, generate_token

TOKEN_URL = "https://login.example.com/v2/oauth/token"
JWKS_URL = "https://login.example.com/oauth/jwks"


class MockSSO:
    """Serves queued responses (or raises queued exceptions) and records requests."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests: list[httpx2.Request] = []

    def __call__(self, request: httpx2.Request) -> httpx2.Response:
        self.requests.append(request)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response

    def client(self) -> httpx2.Client:
        return sso._build_client(transport=httpx2.MockTransport(self))


def token_response(**extra):
    return httpx2.Response(200, json={"access_token": "new_access", "refresh_token": "new_refresh", **extra})


def form(request: httpx2.Request) -> dict:
    return {k: v[0] for k, v in parse_qs(request.content.decode()).items()}


class SSOTestCase(TestCase):
    """Base for tests driving the real SSO client through a mock transport."""

    def setUp(self):
        super().setUp()
        for name, value in {
            "ESI_SSO_CLIENT_ID": "abc",
            "ESI_SSO_CLIENT_SECRET": "xyz",
            "ESI_SSO_CALLBACK_URL": "https://auth.example.com/sso/callback",
            "ESI_TOKEN_URL": TOKEN_URL,
            "ESI_TOKEN_JWK_SET_URL": JWKS_URL,
            "ESI_SSO_MAX_RETRIES": 3,
            "ESI_SSO_MAX_RETRY_AFTER": 60,
        }.items():
            self._start_patch(patch(f"esi.app_settings.{name}", value))
        self.mock_sleep = self._start_patch(patch("esi.sso.time.sleep"))
        cache.delete_many([sso.JWKS_CACHE_KEY, sso.JWKS_FORCE_REFRESH_LOCK_KEY])
        self.addCleanup(cache.delete_many, [sso.JWKS_CACHE_KEY, sso.JWKS_FORCE_REFRESH_LOCK_KEY])

    def _start_patch(self, patcher):
        mocked = patcher.start()
        self.addCleanup(patcher.stop)
        return mocked

    def patch_sso(self, *responses) -> MockSSO:
        mock_sso = MockSSO(*responses)
        self._start_patch(patch("esi.sso.sso_client", return_value=mock_sso.client()))
        return mock_sso


class TestUserAgent(SSOTestCase):
    @patch("esi.app_settings.ESI_USER_CONTACT_EMAIL", "admin@example.com")
    @patch("esi.app_settings.ESI_SSO_USER_AGENT", None)
    def test_default_user_agent(self):
        self.assertEqual(
            sso.sso_user_agent(),
            f"DjangoEsi/{__version__} (admin@example.com; +{__url__})"
        )

    @patch("esi.app_settings.ESI_SSO_USER_AGENT", "MyAuth/1.0")
    def test_user_agent_override(self):
        self.assertEqual(sso.sso_user_agent(), "MyAuth/1.0")

    @patch("esi.app_settings.ESI_SSO_USER_AGENT", "MyAuth/1.0")
    def test_user_agent_sent(self):
        mock_sso = self.patch_sso(token_response(), token_response(), httpx2.Response(200, json={"keys": []}))

        sso.refresh_token("old_refresh")
        sso.exchange_code("code")
        sso.get_jwks()

        self.assertEqual(len(mock_sso.requests), 3)
        for request in mock_sso.requests:
            self.assertEqual(request.headers["User-Agent"], "MyAuth/1.0")


class TestSSOClient(TestCase):
    def tearDown(self):
        sso._client = None
        sso._client_pid = None

    def test_client_is_reused(self):
        self.assertIs(sso.sso_client(), sso.sso_client())

    def test_client_is_rebuilt_after_fork(self):
        with patch("esi.sso.os.getpid", return_value=1):
            client = sso.sso_client()
        with patch("esi.sso.os.getpid", return_value=2):
            self.assertIsNot(sso.sso_client(), client)


class TestRefreshToken(SSOTestCase):
    def test_success(self):
        mock_sso = self.patch_sso(token_response())

        token = sso.refresh_token("old_refresh")

        self.assertEqual(token["access_token"], "new_access")
        self.assertEqual(token["refresh_token"], "new_refresh")
        request = mock_sso.requests[0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(str(request.url), TOKEN_URL)
        self.assertEqual(form(request), {"grant_type": "refresh_token", "refresh_token": "old_refresh"})
        self.assertEqual(
            request.headers["Authorization"],
            "Basic " + base64.b64encode(b"abc:xyz").decode()
        )
        self.mock_sleep.assert_not_called()

    def test_keeps_refresh_token_when_not_rotated(self):
        self.patch_sso(httpx2.Response(200, json={"access_token": "new_access"}))

        token = sso.refresh_token("old_refresh")

        self.assertEqual(token["refresh_token"], "old_refresh")

    def test_retries_server_error(self):
        mock_sso = self.patch_sso(httpx2.Response(503), token_response())

        token = sso.refresh_token("old_refresh")

        self.assertEqual(token["access_token"], "new_access")
        self.assertEqual(len(mock_sso.requests), 2)
        self.assertEqual(self.mock_sleep.call_count, 1)

    def test_gives_up_after_max_retries(self):
        mock_sso = self.patch_sso(httpx2.Response(502), httpx2.Response(503), httpx2.Response(504))

        with self.assertRaises(SSOUnavailableError):
            sso.refresh_token("old_refresh")

        self.assertEqual(len(mock_sso.requests), 3)

    def test_honours_retry_after_seconds(self):
        self.patch_sso(httpx2.Response(429, headers={"Retry-After": "7"}), token_response())

        sso.refresh_token("old_refresh")

        self.mock_sleep.assert_called_once_with(7.0)

    def test_honours_retry_after_date(self):
        retry_at = datetime.now(timezone.utc) + timedelta(seconds=30)
        self.patch_sso(
            httpx2.Response(503, headers={"Retry-After": format_datetime(retry_at, usegmt=True)}),
            token_response()
        )

        sso.refresh_token("old_refresh")

        waited = self.mock_sleep.call_args[0][0]
        self.assertTrue(25 <= waited <= 30, waited)

    def test_retry_after_over_max_not_retried(self):
        mock_sso = self.patch_sso(httpx2.Response(429, headers={"Retry-After": "120"}))

        with self.assertRaises(SSOUnavailableError):
            sso.refresh_token("old_refresh")

        self.assertEqual(len(mock_sso.requests), 1)
        self.mock_sleep.assert_not_called()

    def test_retries_connect_error(self):
        mock_sso = self.patch_sso(httpx2.ConnectError("refused"), token_response())

        sso.refresh_token("old_refresh")

        self.assertEqual(len(mock_sso.requests), 2)

    def test_retries_read_timeout(self):
        mock_sso = self.patch_sso(httpx2.ReadTimeout("slow"), token_response())

        sso.refresh_token("old_refresh")

        self.assertEqual(len(mock_sso.requests), 2)

    def test_oauth_error_not_retried(self):
        mock_sso = self.patch_sso(
            httpx2.Response(400, json={"error": "invalid_grant", "error_description": "Invalid refresh token."})
        )

        with self.assertRaises(SSOOAuthError) as cm:
            sso.refresh_token("old_refresh")

        self.assertEqual(cm.exception.error, "invalid_grant")
        self.assertEqual(cm.exception.description, "Invalid refresh token.")
        self.assertEqual(len(mock_sso.requests), 1)

    def test_unexpected_error_response(self):
        mock_sso = self.patch_sso(httpx2.Response(500, text="<html>oops</html>"))

        with self.assertRaises(SSOUnavailableError):
            sso.refresh_token("old_refresh")

        self.assertEqual(len(mock_sso.requests), 1)

    def test_success_without_access_token(self):
        self.patch_sso(httpx2.Response(200, json={"refresh_token": "new_refresh"}))

        with self.assertRaises(IncompleteResponseError) as cm:
            sso.refresh_token("old_refresh")

        self.assertNotIsInstance(cm.exception, SSOUnavailableError)


class TestSSOOAuthError(SimpleTestCase):
    def test_str(self):
        self.assertEqual(
            str(SSOOAuthError("invalid_grant", "Invalid refresh token.")), "invalid_grant: Invalid refresh token."
        )
        self.assertEqual(str(SSOOAuthError("invalid_grant")), "invalid_grant")

    def test_pickle_round_trip(self):
        e = pickle.loads(pickle.dumps(SSOOAuthError("invalid_grant", "Invalid refresh token.")))

        self.assertEqual(e.error, "invalid_grant")
        self.assertEqual(e.description, "Invalid refresh token.")
        self.assertEqual(str(e), "invalid_grant: Invalid refresh token.")


class TestExchangeCode(SSOTestCase):
    def test_success(self):
        mock_sso = self.patch_sso(token_response())

        token = sso.exchange_code("the_code")

        self.assertEqual(token["access_token"], "new_access")
        self.assertEqual(
            form(mock_sso.requests[0]),
            {
                "grant_type": "authorization_code",
                "code": "the_code",
                "redirect_uri": "https://auth.example.com/sso/callback",
            }
        )

    def test_retries_connect_error(self):
        mock_sso = self.patch_sso(httpx2.ConnectError("refused"), token_response())

        sso.exchange_code("the_code")

        self.assertEqual(len(mock_sso.requests), 2)

    def test_retries_server_error(self):
        mock_sso = self.patch_sso(httpx2.Response(503), token_response())

        sso.exchange_code("the_code")

        self.assertEqual(len(mock_sso.requests), 2)

    def test_read_timeout_not_retried(self):
        """The SSO may have already used the single use code"""
        mock_sso = self.patch_sso(httpx2.ReadTimeout("slow"))

        with self.assertRaises(SSOUnavailableError):
            sso.exchange_code("the_code")

        self.assertEqual(len(mock_sso.requests), 1)


class TestGetJwks(SSOTestCase):
    def test_success(self):
        mock_sso = self.patch_sso(httpx2.Response(200, json={"keys": [{"alg": "RS256"}]}))

        self.assertEqual(sso.get_jwks(), {"keys": [{"alg": "RS256"}]})
        self.assertEqual(mock_sso.requests[0].method, "GET")
        self.assertEqual(str(mock_sso.requests[0].url), JWKS_URL)

    def test_retries_server_error(self):
        mock_sso = self.patch_sso(httpx2.Response(503), httpx2.Response(200, json={"keys": []}))

        sso.get_jwks()

        self.assertEqual(len(mock_sso.requests), 2)

    def test_error_response(self):
        self.patch_sso(httpx2.Response(404))

        with self.assertRaises(SSOUnavailableError):
            sso.get_jwks()

    def test_invalid_json(self):
        self.patch_sso(httpx2.Response(200, text="not json"))

        with self.assertRaises(SSOUnavailableError):
            sso.get_jwks()

    def test_cached_for_max_age_less_age(self):
        mock_sso = self.patch_sso(
            httpx2.Response(
                200, json={"keys": [{"kid": "a"}]}, headers={"Cache-Control": "public, max-age=14400", "Age": "400"}
            )
        )

        with patch("esi.sso.cache.set") as mock_set:
            sso.get_jwks()

        mock_set.assert_called_once_with(sso.JWKS_CACHE_KEY, {"keys": [{"kid": "a"}]}, 14000)
        self.assertEqual(len(mock_sso.requests), 1)

    def test_served_from_cache(self):
        mock_sso = self.patch_sso(
            httpx2.Response(200, json={"keys": [{"kid": "a"}]}, headers={"Cache-Control": "max-age=600"})
        )

        sso.get_jwks()
        self.assertEqual(sso.get_jwks(), {"keys": [{"kid": "a"}]})

        self.assertEqual(len(mock_sso.requests), 1)

    def test_default_cache_time_without_headers(self):
        self.patch_sso(httpx2.Response(200, json={"keys": []}))

        with patch("esi.sso.cache.set") as mock_set:
            sso.get_jwks()

        mock_set.assert_called_once_with(sso.JWKS_CACHE_KEY, {"keys": []}, sso.JWKS_DEFAULT_CACHE_TIME)

    def test_not_cached_when_stale(self):
        mock_sso = self.patch_sso(
            httpx2.Response(200, json={"keys": []}, headers={"Cache-Control": "max-age=600", "Age": "600"}),
            httpx2.Response(200, json={"keys": []}, headers={"Cache-Control": "max-age=600"}),
        )

        sso.get_jwks()
        sso.get_jwks()

        self.assertEqual(len(mock_sso.requests), 2)

    def test_invalid_payload_not_cached(self):
        mock_sso = self.patch_sso(
            httpx2.Response(200, json={}, headers={"Cache-Control": "max-age=600"}),
            httpx2.Response(200, json={"keys": []}, headers={"Cache-Control": "max-age=600"}),
        )

        self.assertEqual(sso.get_jwks(), {})
        self.assertEqual(sso.get_jwks(), {"keys": []})

        self.assertEqual(len(mock_sso.requests), 2)

    def test_force_refresh_skips_cache(self):
        mock_sso = self.patch_sso(
            httpx2.Response(200, json={"keys": [{"kid": "a"}]}, headers={"Cache-Control": "max-age=600"}),
            httpx2.Response(200, json={"keys": [{"kid": "b"}]}, headers={"Cache-Control": "max-age=600"}),
        )

        sso.get_jwks()
        self.assertEqual(sso.get_jwks(force_refresh=True), {"keys": [{"kid": "b"}]})
        self.assertEqual(sso.get_jwks(), {"keys": [{"kid": "b"}]})

        self.assertEqual(len(mock_sso.requests), 2)

    def test_force_refresh_has_cooldown(self):
        mock_sso = self.patch_sso(
            httpx2.Response(200, json={"keys": [{"kid": "a"}]}, headers={"Cache-Control": "max-age=600"}),
            httpx2.Response(200, json={"keys": [{"kid": "b"}]}, headers={"Cache-Control": "max-age=600"}),
        )

        sso.get_jwks()
        sso.get_jwks(force_refresh=True)
        self.assertEqual(sso.get_jwks(force_refresh=True), {"keys": [{"kid": "b"}]})

        self.assertEqual(len(mock_sso.requests), 2)

    def test_cached_until_expires_without_cache_control(self):
        expires = datetime.now(timezone.utc) + timedelta(seconds=600)
        self.patch_sso(
            httpx2.Response(200, json={"keys": []}, headers={"Expires": format_datetime(expires, usegmt=True)})
        )

        with patch("esi.sso.cache.set") as mock_set:
            sso.get_jwks()

        ttl = mock_set.call_args[0][2]
        self.assertTrue(590 <= ttl <= 600, ttl)

    def test_invalid_age_ignored(self):
        self.patch_sso(
            httpx2.Response(200, json={"keys": []}, headers={"Cache-Control": "max-age=600", "Age": "soon"})
        )

        with patch("esi.sso.cache.set") as mock_set:
            sso.get_jwks()

        mock_set.assert_called_once_with(sso.JWKS_CACHE_KEY, {"keys": []}, 600)


class TestValidateAccessTokenWithJwksCache(SSOTestCase):
    """validate_access_token against the real cache, with signed tokens"""

    ES256_JWK = {"alg": "ES256", "kid": "8878a23f-2489-4045-989e-4d2f3ec1ae1a", "kty": "EC", "use": "sig"}

    @staticmethod
    def jwks_response(*keys):
        return httpx2.Response(200, json={"keys": list(keys)}, headers={"Cache-Control": "max-age=600"})

    def test_keys_cached_between_validations(self):
        mock_sso = self.patch_sso(self.jwks_response(generate_jwk()))
        access_token, _ = generate_token(1001, "Bruce Wayne")

        self.assertEqual(Token.objects.validate_access_token(access_token)["character_id"], 1001)
        self.assertEqual(Token.objects.validate_access_token(access_token)["character_id"], 1001)

        self.assertEqual(len(mock_sso.requests), 1)

    def test_rotated_keys_refetched(self):
        mock_sso = self.patch_sso(
            self.jwks_response({**generate_jwk(), "kid": "old-key"}),
            self.jwks_response(generate_jwk()),
        )
        access_token, _ = generate_token(1001, "Bruce Wayne")

        self.assertEqual(Token.objects.validate_access_token(access_token)["character_id"], 1001)
        self.assertEqual(len(mock_sso.requests), 2)

        # the new keys replaced the old ones in the cache
        self.assertEqual(Token.objects.validate_access_token(access_token)["character_id"], 1001)
        self.assertEqual(len(mock_sso.requests), 2)

    def test_unknown_kid_refetch_has_cooldown(self):
        mock_sso = self.patch_sso(
            self.jwks_response({**generate_jwk(), "kid": "other-key"}),
            self.jwks_response({**generate_jwk(), "kid": "other-key"}),
        )
        access_token, _ = generate_token(1001, "Bruce Wayne")

        self.assertIsNone(Token.objects.validate_access_token(access_token))
        self.assertEqual(len(mock_sso.requests), 2)

        self.assertIsNone(Token.objects.validate_access_token(access_token))
        self.assertEqual(len(mock_sso.requests), 2)

    def test_token_without_kid_uses_rs256_key(self):
        """The live SSO also publishes an ES256 key"""
        self.patch_sso(self.jwks_response(self.ES256_JWK, generate_jwk()))
        _, claims = generate_token(1001, "Bruce Wayne")
        access_token = jwt.encode(claims, _RSA_PRIVATE_KEY, algorithm="RS256", headers={"typ": "JWT"})
        self.assertNotIn("kid", jwt.get_unverified_header(access_token))

        self.assertEqual(Token.objects.validate_access_token(access_token)["character_id"], 1001)

    def test_token_selects_key_by_kid(self):
        self.patch_sso(self.jwks_response(self.ES256_JWK, generate_jwk()))
        access_token, _ = generate_token(1001, "Bruce Wayne")

        self.assertEqual(Token.objects.validate_access_token(access_token)["character_id"], 1001)


@patch("esi.app_settings.ESI_SSO_CLIENT_ID", "abc")
@patch("esi.app_settings.ESI_SSO_CALLBACK_URL", "https://auth.example.com/sso/callback")
@patch("esi.app_settings.ESI_OAUTH_LOGIN_URL", "https://login.example.com/v2/oauth/authorize/")
class TestAuthorizationUrl(TestCase):
    def test_with_scopes(self):
        url, state = sso.authorization_url(["esi-a.v1", "esi-b.v1"])

        parts = urlsplit(url)
        self.assertEqual(
            f"{parts.scheme}://{parts.netloc}{parts.path}", "https://login.example.com/v2/oauth/authorize/"
        )
        self.assertEqual(
            {k: v[0] for k, v in parse_qs(parts.query).items()},
            {
                "response_type": "code",
                "client_id": "abc",
                "redirect_uri": "https://auth.example.com/sso/callback",
                "scope": "esi-a.v1 esi-b.v1",
                "state": state,
            }
        )

    def test_without_scopes(self):
        url, _ = sso.authorization_url([])

        self.assertNotIn("scope", parse_qs(urlsplit(url).query))

    def test_state_is_unique(self):
        _, state_1 = sso.authorization_url()
        _, state_2 = sso.authorization_url()

        self.assertNotEqual(state_1, state_2)
        self.assertLessEqual(len(state_1), 128)  # CallbackRedirect.state max_length


class TestTokenRefreshWithSSO(SSOTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.create_user("Bruce Wayne", "abc@example.com", "password")
        self.token = _store_as_Token(_generate_token(99, "Bruce Wayne"), user)

    def test_sso_down_keeps_token(self):
        self.patch_sso(httpx2.Response(503), httpx2.Response(503), httpx2.Response(503))

        with self.assertRaises(SSOUnavailableError):
            self.token.refresh_or_delete()

        self.assertTrue(Token.objects.filter(pk=self.token.pk).exists())

    def test_invalid_grant_deletes_token(self):
        self.patch_sso(httpx2.Response(400, json={"error": "invalid_grant"}))

        self.token.refresh_or_delete()

        self.assertFalse(Token.objects.filter(pk=self.token.pk).exists())


class TestNoNestedRetries(TestCase):
    def test_esi_client_does_not_retry_sso_errors(self):
        """Token refreshes during an ESI request run inside the ESI client's retries"""
        from esi.openapi_clients import _httpx_exceptions

        self.assertFalse(_httpx_exceptions(SSOUnavailableError()))

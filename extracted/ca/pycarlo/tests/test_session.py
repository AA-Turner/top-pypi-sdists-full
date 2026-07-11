from configparser import NoSectionError
from typing import Any
from unittest import TestCase
from unittest.mock import Mock, call, patch
from urllib.parse import parse_qs

import responses

from pycarlo.common.errors import InvalidSessionError
from pycarlo.core import Session


class SessionTest(TestCase):
    @patch.object(Session, "_read_config")
    def test_session_with_params(self, mock_read: Mock):
        mcd_id, mcd_token = "foo", "bar"
        session = Session(mcd_id=mcd_id, mcd_token=mcd_token)

        self.assertEqual(session.id, mcd_id)
        self.assertEqual(session.token, mcd_token)
        mock_read.assert_not_called()

    @patch("pycarlo.core.session.MCD_DEFAULT_API_ID", "foo")
    @patch("pycarlo.core.session.MCD_DEFAULT_API_TOKEN", "bar")
    @patch.object(Session, "_read_config")
    def test_session_with_env(self, mock_read: Mock):
        session = Session()

        self.assertEqual(session.id, "foo")
        self.assertEqual(session.token, "bar")
        mock_read.assert_not_called()

    @patch("pycarlo.core.session.MCD_DEFAULT_API_TOKEN", "bar")
    @patch.object(Session, "_read_config")
    def test_session_with_mixed(self, mock_read: Mock):
        mcd_id = "foo"
        session = Session(mcd_id=mcd_id)

        self.assertEqual(session.id, mcd_id)
        self.assertEqual(session.token, "bar")
        mock_read.assert_not_called()

    @patch("pycarlo.core.session.MCD_DEFAULT_API_TOKEN", "qux")
    @patch.object(Session, "_read_config")
    def test_session_with_precedence(self, mock_read: Mock):
        mcd_id, mcd_token = "foo", "bar"
        session = Session(mcd_id=mcd_id, mcd_token=mcd_token)

        self.assertEqual(session.id, mcd_id)
        self.assertEqual(session.token, mcd_token)
        mock_read.assert_not_called()

    @patch.object(Session, "_read_config")
    def test_session_with_partial(self, mock_read: Mock):
        with self.assertRaises(InvalidSessionError):
            Session(mcd_id="foo")
        mock_read.assert_not_called()

    @patch("pycarlo.core.session.configparser")
    def test_read_config(self, mock_parser: Mock):
        mcd_id, mcd_token, mcd_api_endpoint, mcd_config_path = "foo", "bar", "endpoint", "path/"
        _unset = object()
        values = {
            "mcd_id": mcd_id,
            "mcd_token": mcd_token,
            "mcd_api_endpoint": mcd_api_endpoint,
        }

        def fake_get(section: str, option: str, fallback: Any = _unset) -> Any:
            if option in values:
                return values[option]
            if fallback is not _unset:
                return fallback
            raise AssertionError(f"unexpected option without fallback: {option}")

        parser = mock_parser.ConfigParser()
        parser.has_section.return_value = True
        parser.get.side_effect = fake_get

        session = Session(mcd_config_path=mcd_config_path)
        mock_parser.assert_has_calls = [
            call.ConfigParser(),
            call.ConfigParser().read("path/profiles.ini"),
            call.ConfigParser().get("default", "mcd_id"),
            call.ConfigParser().get("default", "mcd_token"),
            call.ConfigParser().get("default", "mcd_api_endpoint"),
        ]  # type: ignore
        self.assertEqual(session.id, mcd_id)
        self.assertEqual(session.token, mcd_token)
        self.assertEqual(session.endpoint, mcd_api_endpoint)

    @patch.object(Session, "_get_config_parser")
    def test_read_config_with_bad_section(self, mock_parser: Mock):
        class InvalidParser:
            def read(self, *args: Any, **kwargs: Any):
                pass

            def has_section(self, *args: Any, **kwargs: Any):
                return True

            def get(self, *args: Any, **kwargs: Any):
                raise NoSectionError("")

        mock_parser.return_value = InvalidParser()

        with self.assertRaises(InvalidSessionError):
            Session()

    @patch("pycarlo.core.session.get_version")
    @patch("pycarlo.core.session.uuid")
    def test_set_session_name(self, mock_uuid: Mock, mock_get_version: Mock):
        mcd_id, mcd_token = "foo", "bar"
        mock_uuid_val, mock_pkg_val = "42", "99"

        mock_uuid.uuid4.return_value = mock_uuid_val
        mock_get_version.return_value = mock_pkg_val
        session = Session(mcd_id=mcd_id, mcd_token=mcd_token)

        self.assertEqual(session.id, mcd_id)
        self.assertEqual(session.token, mcd_token)
        self.assertEqual(session.session_name, f"python-sdk-{mock_pkg_val}-{mock_uuid_val}")

    def test_set_session_endpoint(self):
        mcd_id, mcd_token, endpoint = "foo", "bar", "test.com"
        self.assertEqual(
            Session(mcd_id=mcd_id, mcd_token=mcd_token, endpoint=endpoint).endpoint, endpoint
        )
        self.assertEqual(
            Session(mcd_id=mcd_id, mcd_token=mcd_token).endpoint,
            "https://api.getmontecarlo.com/graphql",
        )


class OAuthSessionTest(TestCase):
    _PROD_TOKEN = "https://api.getmontecarlo.com/oauth2/token"
    _PROD_OAUTH_API = "https://api.getmontecarlo.com/graphql"

    @staticmethod
    def _oauth_session(**kwargs: Any) -> Session:
        # OAuth requires an instance id; default it so individual tests stay concise.
        kwargs.setdefault("mcd_instance_id", "us1")
        return Session(mcd_oauth_client_id="cid", mcd_oauth_client_secret="sec", **kwargs)

    @patch.object(Session, "_read_config")
    def test_oauth_with_params(self, mock_read: Mock):
        session = self._oauth_session()
        self.assertTrue(session.is_oauth)
        self.assertEqual(session.id, "cid")
        self.assertEqual(session.oauth_token_endpoint, self._PROD_TOKEN)
        self.assertEqual(session.endpoint, self._PROD_OAUTH_API)
        mock_read.assert_not_called()

    @patch.object(Session, "_read_config")
    def test_oauth_preferred_over_api_key(self, mock_read: Mock):
        session = Session(
            mcd_id="foo",
            mcd_token="bar",
            mcd_oauth_client_id="cid",
            mcd_oauth_client_secret="sec",
            mcd_instance_id="us1",
        )
        self.assertTrue(session.is_oauth)
        self.assertEqual(session.id, "cid")

    @patch.object(Session, "_read_config")
    def test_oauth_partial_raises(self, _mock_read: Mock):
        with self.assertRaises(InvalidSessionError):
            Session(mcd_oauth_client_id="cid")

    @patch.object(Session, "_read_config")
    def test_oauth_explicit_endpoint_overrides(self, _mock_read: Mock):
        session = self._oauth_session(
            token_endpoint="https://custom/token",
            oauth_api_endpoint="https://custom/oauth/graphql",
        )
        self.assertEqual(session.oauth_token_endpoint, "https://custom/token")
        self.assertEqual(session.endpoint, "https://custom/oauth/graphql")

    @patch("pycarlo.core.session.MCD_API_ENDPOINT", "https://api.dev.getmontecarlo.com/graphql")
    @patch.object(Session, "_read_config")
    def test_oauth_derives_from_env_api_endpoint(self, _mock_read: Mock):
        session = self._oauth_session()
        self.assertEqual(
            session.oauth_token_endpoint, "https://api.dev.getmontecarlo.com/oauth2/token"
        )
        # The OAuth API endpoint is the API endpoint unchanged; the gateway routes it.
        self.assertEqual(session.endpoint, "https://api.dev.getmontecarlo.com/graphql")

    @patch.object(Session, "_read_config")
    def test_oauth_with_gateway_scope_raises(self, _mock_read: Mock):
        # OAuth + a gateway (IGW) scope is unsupported and must fail at construction, not on the
        # first token fetch.
        with self.assertRaises(InvalidSessionError):
            self._oauth_session(scope="agents:read")

    @patch("pycarlo.core.session.MCD_API_ENDPOINT", "https://custom.example.com/api")
    @patch.object(Session, "_read_config")
    def test_oauth_non_graphql_endpoint_raises(self, _mock_read: Mock):
        # An API endpoint without /graphql can't derive a token endpoint — fail loudly rather
        # than posting credentials to the wrong URL.
        with self.assertRaises(InvalidSessionError):
            self._oauth_session()

    @patch.object(Session, "_read_config")
    def test_oauth_instance_id_sets_scope(self, _mock_read: Mock):
        session = Session(
            mcd_oauth_client_id="cid",
            mcd_oauth_client_secret="sec",
            mcd_instance_id="eu1",
        )
        self.assertEqual(session.oauth_instance_scope, "https://instance.getmontecarlo.com/eu1")

    @patch("pycarlo.core.session.MCD_DEFAULT_INSTANCE_ID", None)
    @patch.object(Session, "_read_config")
    def test_oauth_without_instance_id_raises(self, _mock_read: Mock):
        with self.assertRaises(InvalidSessionError):
            Session(mcd_oauth_client_id="cid", mcd_oauth_client_secret="sec")

    @patch("pycarlo.core.session.MCD_DEFAULT_INSTANCE_ID", None)
    @patch.object(Session, "_read_config")
    def test_oauth_invalid_instance_id_raises(self, _mock_read: Mock):
        with self.assertRaises(InvalidSessionError):
            Session(
                mcd_oauth_client_id="cid",
                mcd_oauth_client_secret="sec",
                mcd_instance_id="bad id!",
            )

    def test_validate_instance_id_static(self):
        # Trims + accepts valid ids (alphanumerics + hyphens), rejects the rest with ValueError.
        self.assertEqual(Session.validate_instance_id("  us1  "), "us1")
        self.assertEqual(Session.validate_instance_id("eu1-a"), "eu1-a")
        # Rejects empties, bad chars, and anything over 63 chars (matches the gateway's bound).
        for bad in ["", "bad id", "us1/x", "us1.eu1", "a" * 64]:
            with self.assertRaises(ValueError):
                Session.validate_instance_id(bad)

    @responses.activate
    @patch.object(Session, "_read_config")
    def test_get_access_token_requests_instance_scope(self, _mock_read: Mock):
        responses.add(
            responses.POST,
            self._PROD_TOKEN,
            json={"access_token": "tok", "expires_in": 3600},
            status=200,
        )
        session = self._oauth_session(mcd_instance_id="eu1")
        session.get_access_token()
        body = responses.calls[0].request.body
        assert isinstance(body, str)
        requested_scopes = parse_qs(body)["scope"][0]
        self.assertIn("https://api.getmontecarlo.com/access", requested_scopes)
        self.assertIn("https://instance.getmontecarlo.com/eu1", requested_scopes)

    @patch.object(Session, "_read_config")
    def test_get_access_token_non_oauth_raises(self, _mock_read: Mock):
        session = Session(mcd_id="foo", mcd_token="bar")
        with self.assertRaises(InvalidSessionError):
            session.get_access_token()

    @responses.activate
    @patch.object(Session, "_read_config")
    def test_get_access_token_grant_and_cache(self, _mock_read: Mock):
        responses.add(
            responses.POST,
            self._PROD_TOKEN,
            json={"access_token": "tok-1", "expires_in": 3600},
            status=200,
        )
        session = self._oauth_session()
        self.assertEqual(session.get_access_token(), "tok-1")
        # cached: second call does not hit the token endpoint again
        self.assertEqual(session.get_access_token(), "tok-1")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    @patch.object(Session, "_read_config")
    def test_get_access_token_non_integer_expires_in_defaults(self, _mock_read: Mock):
        # A non-integer expires_in must not escape as a ValueError — fall back to the 1h default.
        responses.add(
            responses.POST,
            self._PROD_TOKEN,
            json={"access_token": "tok", "expires_in": "soon"},
            status=200,
        )
        session = self._oauth_session()
        self.assertEqual(session.get_access_token(), "tok")

    @responses.activate
    @patch.object(Session, "_read_config")
    def test_get_access_token_refreshes_when_expired(self, _mock_read: Mock):
        responses.add(
            responses.POST,
            self._PROD_TOKEN,
            json={"access_token": "tok-old", "expires_in": 3600},
            status=200,
        )
        responses.add(
            responses.POST,
            self._PROD_TOKEN,
            json={"access_token": "tok-new", "expires_in": 3600},
            status=200,
        )
        session = self._oauth_session()
        self.assertEqual(session.get_access_token(), "tok-old")
        session._token_expiry = 0.0  # force expiry
        self.assertEqual(session.get_access_token(), "tok-new")
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    @patch.object(Session, "_read_config")
    def test_get_access_token_failure_raises(self, _mock_read: Mock):
        responses.add(
            responses.POST, self._PROD_TOKEN, json={"error": "invalid_client"}, status=401
        )
        session = self._oauth_session()
        with self.assertRaises(InvalidSessionError):
            session.get_access_token()
        # 4xx is not retried — a bad credential won't succeed on retry.
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    @patch.object(Session, "_read_config")
    def test_get_access_token_retries_transient_5xx(self, _mock_read: Mock):
        # A transient 5xx is retried; the subsequent 200 succeeds.
        responses.add(responses.POST, self._PROD_TOKEN, json={"error": "boom"}, status=503)
        responses.add(
            responses.POST,
            self._PROD_TOKEN,
            json={"access_token": "tok", "expires_in": 3600},
            status=200,
        )
        session = self._oauth_session()
        self.assertEqual(session.get_access_token(), "tok")
        self.assertEqual(len(responses.calls), 2)

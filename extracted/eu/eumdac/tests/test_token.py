import unittest
import time
from datetime import datetime

from responses import RequestsMock, _ensure_url_default_path

from eumdac.token import AccessToken
from .base import DataServiceTestCase, INTEGRATION_TESTING

import requests


class TestAccessToken(DataServiceTestCase):
    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)

    def test_str_representation(self):
        self.assertEqual(str(self.token), self.token.access_token)

    @unittest.skipIf(INTEGRATION_TESTING, "Avoid revoking tokens on integration")
    def test_revoke_not_expired(self):
        token_url = self.token.urls.get("token", "token")
        revoke_url = self.token.urls.get("token", "revoke")
        self.token = AccessToken(self.credentials)
        str(self.token)
        # token cached, only 1 request
        str(self.token)
        # revoke token
        self.token._revoke()
        str(self.token)
        str(self.token)
        str(self.token)
        # 1 revoke, 1 token request, then cached
        self.requests_mock.assert_call_count(token_url, 2)
        self.requests_mock.assert_call_count(revoke_url, 1)

    def test_expired_token(self):
        token_url = self.token.urls.get("token", "token")
        revoke_url = self.token.urls.get("token", "revoke")
        self.token = AccessToken(self.credentials, validity=15)
        str(self.token)
        time.sleep(30)
        str(self.token)
        # new token requested at least once
        # (can't know how many times it'll be called, depends on server)
        self._assert_was_called(self.requests_mock, token_url)
        # no revoking
        self.requests_mock.assert_call_count(revoke_url, 0)

    def test_properties(self):
        now = datetime.now()
        access_token = self.token.access_token
        expiration = self.token.expiration
        self.assertIsInstance(access_token, str)
        self.assertIsInstance(expiration, datetime)
        self.assertLessEqual(now, self.token.expiration)

    @unittest.skipIf(INTEGRATION_TESTING, "Check against changing value!")
    def test_auth(self):
        mock_token = "1f29ecb3-5973-35d5-a7e6-ec3348c9c49a"
        self.token._access_token = mock_token
        self.token._expiration = time.time() + 1000
        request = requests.Request("GET", "some-url")
        self.token.auth(request)
        auth_header = request.headers.get("authorization")
        self.assertEqual(auth_header, f"Bearer {mock_token}")

    def _assert_was_called(self, requests_mock: RequestsMock, url: str):
        call_count = len(
            [1 for call in requests_mock.calls if call.request.url == _ensure_url_default_path(url)]
        )
        assert call_count > 0

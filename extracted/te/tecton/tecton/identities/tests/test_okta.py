import tempfile
import time
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import pytest
import requests

from tecton.identities import okta
from tecton_core import conf


def fake_get_tokens_helper(endpoint, params):
    msg = "simulating refresh token expired"
    raise requests.RequestException(msg)


class OktaTest(TestCase):
    def test_refresh_token_success(self):
        class FakeRefreshFlow:
            def get_tokens(*args):
                return "NEW_ACCESS_TOKEN", 0, 0, 0

        # Test local Tecton config file
        with tempfile.NamedTemporaryFile() as f:
            f.write(
                (
                    '{"OAUTH_ACCESS_TOKEN": "dummy", "OAUTH_REFRESH_TOKEN": "dummy", "OAUTH_ACCESS_TOKEN_EXPIRATION": "%s"}'
                    % (str(time.time() - 60))
                ).encode()
            )
            f.flush()
            with patch("tecton.conf._LOCAL_TECTON_TOKENS_FILE", Path(f.name)):
                conf._init_configs()
                with patch("tecton.identities.okta.RefreshFlow", FakeRefreshFlow):
                    assert okta.get_token_refresh_if_needed() == "NEW_ACCESS_TOKEN"

    def test_refresh_token_failure(self):
        conf.set_okta_tokens(access_token="dummy", access_token_expiration=time.time() - 60, refresh_token="dummy")
        with patch("tecton.identities.okta.get_tokens_helper", fake_get_tokens_helper):
            with pytest.raises(PermissionError, match="Authorization token expired"):
                okta.get_token_refresh_if_needed()

    def test_get_user_profile_refresh_token_expired(self):
        conf.set_okta_tokens(access_token="dummy", access_token_expiration=time.time() - 60, refresh_token="dummy")
        with patch("tecton.identities.okta.get_tokens_helper", fake_get_tokens_helper):
            with pytest.raises(PermissionError, match="Authorization token expired"):
                okta.get_user_profile()

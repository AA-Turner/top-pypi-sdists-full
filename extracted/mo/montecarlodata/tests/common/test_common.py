from unittest import TestCase
from unittest.mock import patch

from montecarlodata.common.common import ConditionalDictionary, create_session
from montecarlodata.config import Config

_API_ENDPOINT = "https://api.getmontecarlo.com/graphql"


class CreateSessionTest(TestCase):
    @patch("montecarlodata.common.common.Session")
    def test_create_session_legacy(self, session_mock):
        config = Config(mcd_id="id", mcd_token="token", mcd_api_endpoint=_API_ENDPOINT)
        create_session(config)
        session_mock.assert_called_once_with(endpoint=_API_ENDPOINT, mcd_id="id", mcd_token="token")

    @patch("montecarlodata.common.common.Session")
    def test_create_session_oauth(self, session_mock):
        config = Config(
            mcd_id=None,
            mcd_token=None,
            mcd_api_endpoint=_API_ENDPOINT,
            mcd_oauth_client_id="cid",
            mcd_oauth_client_secret="sec",
            mcd_instance_id="us1",
            mcd_token_endpoint="https://api.getmontecarlo.com/oauth2/token",
            mcd_oauth_api_endpoint=None,
        )
        create_session(config)
        session_mock.assert_called_once_with(
            mcd_oauth_client_id="cid",
            mcd_oauth_client_secret="sec",
            mcd_instance_id="us1",
            endpoint=_API_ENDPOINT,
            token_endpoint="https://api.getmontecarlo.com/oauth2/token",
            oauth_api_endpoint=None,
        )


class MyTestCase(TestCase):
    def test_no_nones_set(self):
        dictionary = ConditionalDictionary(lambda x: x is not None)
        dictionary["a"] = 0
        dictionary["b"] = True
        dictionary["c"] = None
        dictionary["d"] = False
        self.assertEqual({"a": 0, "b": True, "d": False}, dictionary)

    def test_no_nones_update(self):
        dictionary = ConditionalDictionary(lambda x: x is not None)
        dictionary.update({"a": 0, "b": True, "c": None, "d": False})
        self.assertEqual({"a": 0, "b": True, "d": False}, dictionary)

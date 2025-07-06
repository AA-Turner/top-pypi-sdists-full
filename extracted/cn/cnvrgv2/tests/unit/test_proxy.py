import requests

from cnvrgv2.config.config import SSO_VERSION
from cnvrgv2.context import Context
from cnvrgv2.proxy import HTTP, Proxy


class MockResponse:
    def __init__(self, status, json):
        self.status_code = status
        self._json = json

    def json(self, *args, **kwargs):
        return self._json


class TestProxy:
    def test_call_api(self, mocker):
        def mock_requests_post(*args, **kwargs):
            assert args[0] == "http://localhost:3000/api/sample/url"
            assert kwargs["headers"]["Authorization"] == "CAPI sampletoken"
            assert kwargs["headers"]["test"] == "test"
            assert kwargs["json"]["test"] == "test"

            return MockResponse(status=200, json={})

        def mock_credentials_init(obj):
            obj.domain = "http://localhost:3000"
            obj.token = "sampletoken"
            obj.organization = "test"
            obj.sso_version = SSO_VERSION.CAPI

        mocker.patch.object(Context, "__init__", mock_credentials_init)
        mocker.patch.object(requests, "post", mock_requests_post)

        creds = Context()
        proxy = Proxy(creds)
        proxy.call_api("sample/url", HTTP.POST, payload={"test": "test"}, headers={"test": "test"})

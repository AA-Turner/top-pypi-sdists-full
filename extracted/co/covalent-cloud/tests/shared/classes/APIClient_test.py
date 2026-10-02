# Copyright 2023 Agnostiq Inc.

from unittest.mock import MagicMock

from covalent_cloud.shared.classes.api import APIClient
from covalent_cloud.shared.classes.settings import AuthSettings, Settings

MOCK_CC_API_KEY = "mock-cc-api-key"  # pragma: allowlist secret
MOCK_DR_API_TOKEN = "mock-dr-api-token"  # pragma: allowlist secret

MOCK_SETTINGS = Settings(
    auth=AuthSettings(
        dr_api_token=MOCK_DR_API_TOKEN,
    )
)

MOCK_LEGACY_SETTINGS = Settings(
    auth=AuthSettings(
        api_key=MOCK_CC_API_KEY,
    )
)

MOCK_GLOBAL_HEADERS = {
    "Authorization": f"Bearer {MOCK_DR_API_TOKEN}",
    "x-dr-region": "",
}

MOCK_LEGACY_GLOBAL_HEADERS = {
    "x-api-key": MOCK_CC_API_KEY,
}
MOCK_REQUEST_OPTIONS = {
    "params": {"a": 1},
}


class TestAPIClient:

    MOCK_URI = "https://www.example.com"

    def test_get_global_headers(self):
        # substituting token avoids fetching/creating from config file
        api = APIClient(host_uri=self.MOCK_URI, headers={"CLIENT": "TEST"}, settings=MOCK_SETTINGS)
        assert api.get_global_headers() == {"CLIENT": "TEST", **MOCK_GLOBAL_HEADERS}

    def test_get_legacy_global_headers(self):
        # substituting token avoids fetching/creating from config file
        api = APIClient(
            host_uri=self.MOCK_URI, headers={"CLIENT": "TEST"}, settings=MOCK_LEGACY_SETTINGS
        )
        assert api.get_global_headers() == {"CLIENT": "TEST", **MOCK_LEGACY_GLOBAL_HEADERS}

    def test_prepare_request(self):
        # substituting token avoids fetching/creating from config file
        api = APIClient(host_uri="http://some.site/", headers={}, settings=MOCK_SETTINGS)
        uri, options = api.prepare_request("/test", {"data": 123})
        print("OPTIONS:", options)
        assert uri == "http://some.site/test"
        assert options == {"headers": MOCK_GLOBAL_HEADERS, "data": 123}

    def test_prepare_request_with_legacy_headers(self):
        # substituting token avoids fetching/creating from config file
        api = APIClient(host_uri="http://some.site/", headers={}, settings=MOCK_LEGACY_SETTINGS)
        uri, options = api.prepare_request("/test", {"data": 123})
        print("OPTIONS:", options)
        assert uri == "http://some.site/test"
        assert options == {"headers": MOCK_LEGACY_GLOBAL_HEADERS, "data": 123}

    def test_get_request_options(self):
        # substituting token avoids fetching/creating from config file
        api = APIClient(host_uri=self.MOCK_URI, headers={}, settings=MOCK_SETTINGS)
        options = api.get_request_options({"body": {"a": 1}})
        assert options["body"] == {"a": 1}

    def test_post(self, mocker):

        api_mock = APIClient(host_uri=self.MOCK_URI)
        requests_mock = MagicMock()
        mocker.patch(
            "covalent_cloud.shared.classes.api.requests.Session.__enter__",
            return_value=requests_mock,
        )

        mock_request_options = {"json": {"a": 1}, "data": b"ef8"}

        mocker.patch.object(api_mock, "get_request_options", return_value=mock_request_options)
        api_mock.post("/api/v0/resource", mock_request_options)
        requests_mock.post.assert_called_with(
            f"{self.MOCK_URI}/api/v0/resource", **mock_request_options
        )

    def test_get(self, mocker):

        api_mock = APIClient(host_uri=self.MOCK_URI)
        requests_mock = MagicMock()
        mocker.patch(
            "covalent_cloud.shared.classes.api.requests.Session.__enter__",
            return_value=requests_mock,
        )
        mocker.patch.object(api_mock, "get_request_options", return_value=MOCK_REQUEST_OPTIONS)
        api_mock.get("/api/v0/resource", MOCK_REQUEST_OPTIONS)
        requests_mock.get.assert_called_with(
            f"{self.MOCK_URI}/api/v0/resource", **MOCK_REQUEST_OPTIONS
        )

    def test_delete(self, mocker):

        api_mock = APIClient(host_uri=self.MOCK_URI)
        requests_mock = MagicMock()
        mocker.patch(
            "covalent_cloud.shared.classes.api.requests.Session.__enter__",
            return_value=requests_mock,
        )
        mocker.patch.object(api_mock, "get_request_options")
        api_mock.delete("/api/v0/resource")
        requests_mock.delete.assert_called_with(f"{self.MOCK_URI}/api/v0/resource")

    def test_put(self, mocker):

        api_mock = APIClient(host_uri=self.MOCK_URI)
        requests_mock = MagicMock()
        mocker.patch(
            "covalent_cloud.shared.classes.api.requests.Session.__enter__",
            return_value=requests_mock,
        )
        mocker.patch.object(api_mock, "get_request_options", return_value=MOCK_REQUEST_OPTIONS)
        api_mock.put("/api/v0/resource", MOCK_REQUEST_OPTIONS)
        requests_mock.put.assert_called_with(
            f"{self.MOCK_URI}/api/v0/resource", **MOCK_REQUEST_OPTIONS
        )

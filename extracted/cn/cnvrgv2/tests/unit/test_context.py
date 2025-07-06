import os

import pytest
import requests

from cnvrgv2.config import error_messages
from cnvrgv2.config.config import SSO_VERSION
from cnvrgv2.context import Context
from cnvrgv2.errors import CnvrgError, CnvrgLoginError
from cnvrgv2.modules.users.users_client import UsersClient


class MockResponse:
    def __init__(self, status, json):
        self.status_code = status
        self._json = json

    def json(self, *args, **kwargs):
        return self._json


class FakeContext:
    def __init__(self):
        # Set the credentials variables:
        self.token = "fake"
        self.domain = "fake"
        self.user = "fake"

        # Set context variables:
        self.project = "fake"
        self.experiment = "fake"
        self.organization = "fake"
        self.sso_version = None
        self.digest = None


# TODO: add organization auth test
class TestContext:
    def test_init(self, mocker):
        # Test that the constructor raises errors on bad params:
        with pytest.raises(CnvrgError):
            Context(domain="test", user="test")
        with pytest.raises(CnvrgError):
            Context(user="test", password="test", organization="test")

        # Test that the load_credentials function was called on empty input
        def mock_load_credentials(obj):
            obj.domain = "test-success"

        def mock_organization_exists(obj, name):
            return True

        mocker.patch.object(Context, "_load_credentials", mock_load_credentials)
        mocker.patch.object(Context, "ensure_organization_exist", mock_organization_exists)
        context = Context()
        assert context.domain == "test-success"

    def test_init_from_context(self):
        fake_context = FakeContext()
        copied_context = Context(context=fake_context)

        assert copied_context.token == fake_context.token
        assert copied_context.domain == fake_context.domain
        assert copied_context.user == fake_context.user

        assert copied_context.project == fake_context.project
        assert copied_context.experiment == fake_context.experiment
        assert copied_context.organization == fake_context.organization

        copied_context.token = "new-token"
        assert copied_context.token != fake_context.token

    def test_authenticate_success(self, mocker, empty_context):
        # Test that the load_credentials function runs correctly with valid response
        def mock_requests_post(*args, **kwargs):
            resp = {
                "meta": {
                    "jwt": "fake-token",
                    "organization": "org1"
                }
            }
            return MockResponse(status=200, json=resp)

        def mock_get_sso_version(*args, **kwargs):
            return SSO_VERSION.CAPI

        mocker.patch.object(requests, "post", mock_requests_post)
        mocker.patch.object(UsersClient, "_get_sso_version", side_effect=mock_get_sso_version)

        # Test call
        empty_context._authenticate("http://fake-url.com", "fake-user", "fake-pass")
        assert empty_context.token == "fake-token"
        assert empty_context.organization == "org1"

    def test_authenticate_fail(self, mocker, empty_context):
        # Test that the load_credentials function runs correctly with invalid response
        def mock_requests_post(*args, **kwargs):
            resp = {
                "message": "An exception has occurred"
            }
            return MockResponse(status=401, json=resp)

        def mock_get_sso_version(*args, **kwargs):
            return SSO_VERSION.CAPI

        mocker.patch.object(requests, "post", mock_requests_post)
        mocker.patch.object(UsersClient, "_get_sso_version", side_effect=mock_get_sso_version)

        # Test call
        with pytest.raises(CnvrgLoginError) as exception_info:
            empty_context._authenticate("http://fake-url.com", "fake-user", "fake-pass")
        assert error_messages.INVALID_CREDENTIALS in str(exception_info.value)

    def test_load_from_env(self, monkeypatch, empty_context):
        monkeypatch.setenv("CNVRG_URL", "fake-domain")
        monkeypatch.setenv("CNVRG_JWT_TOKEN", '')
        monkeypatch.setenv("CNVRG_ORGANIZATION", '')

        assert not empty_context._load_from_env()

        monkeypatch.setenv("CNVRG_URL", "fake-domain")
        monkeypatch.setenv("CNVRG_EMAIL", "fake-email")
        monkeypatch.setenv("CNVRG_JWT_TOKEN", "fake-token")
        monkeypatch.setenv("CNVRG_ORGANIZATION", "fake-organization")

        assert empty_context._load_from_env()
        assert empty_context.token == "fake-token"
        assert empty_context.domain == "fake-domain"
        assert empty_context.user == "fake-email"
        assert empty_context.organization == "fake-organization"

    def test_load_from_pod_env(self, monkeypatch, empty_context):
        monkeypatch.setenv("CNVRG_URL", "fake-domain")
        monkeypatch.setenv("CNVRG_JWT_TOKEN", '')
        monkeypatch.setenv("CNVRG_ORGANIZATION", '')

        assert not empty_context._load_from_env()

        monkeypatch.setenv("CNVRG_URL", "fake-domain")
        monkeypatch.setenv("CNVRG_EMAIL", "fake-email")
        monkeypatch.setenv("CNVRG_JWT_TOKEN", "fake-token")
        monkeypatch.setenv("CNVRG_ORGANIZATION", "fake-organization")

        # Pod env vars
        monkeypatch.setenv("CNVRG_PROJECT", "fake-project")
        monkeypatch.setenv("CNVRG_JOB_ID", "fake-job-slug")
        monkeypatch.setenv("CNVRG_JOB_TYPE", "Experiment")

        assert empty_context._load_from_env()
        assert empty_context.project == "fake-project"
        assert empty_context.experiment == "fake-job-slug"

    def test_load_from_config_file_doesnt_exist(self, mocker, empty_context):
        def mock_path_exists(*args, **kwargs):
            return False

        mocker.patch.object(os.path, "exists", mock_path_exists)

        assert not empty_context._load_from_config()

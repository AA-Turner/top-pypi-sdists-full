import pytest

from cnvrgv2.config.config import SSO_VERSION
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.users.user import User
from cnvrgv2.modules.users.users_client import UsersClient
from cnvrgv2.proxy import Proxy
from cnvrgv2.utils.json_api_format import JAF


class TestUsersClient:
    def test_user_client_invalid_domain(self):
        domain = "bad_domain"
        with pytest.raises(CnvrgArgumentsError) as exception_info:
            UsersClient(domain=domain)

        assert "URL" in str(exception_info.value)

    def test_user_client_valid_domain(self, mocker):
        def mock_get_sso_version(*args, **kwargs):
            return SSO_VERSION.CAPI

        mocker.patch.object(UsersClient, "_get_sso_version", side_effect=mock_get_sso_version)

        domain = "http://localhost:3000"
        UsersClient(domain=domain)

        domain = "http://0.0.0.0:3000"
        UsersClient(domain=domain)

        domain = "https://example.com"
        UsersClient(domain=domain)

        assert True

    def test_user_register_bad_email(self, mocker):
        def mock_call_api(*args, **kwargs):
            return

        def mock_get_sso_version(*args, **kwargs):
            return SSO_VERSION.CAPI

        mock_response = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        mocker.patch.object(UsersClient, "_get_sso_version", side_effect=mock_get_sso_version)

        domain = "http://localhost:3000"
        uc = UsersClient(domain=domain)

        with pytest.raises(CnvrgArgumentsError) as exception_info:
            uc.register(username="valid_user", email="invalid email", password="password")

        assert "email" in str(exception_info.value)
        assert mock_response.call_count == 0

    def test_user_register_invalid_character_in_domain(self, mocker):
        def mock_call_api(*args, **kwargs):
            return

        def mock_get_sso_version(*args, **kwargs):
            return SSO_VERSION.CAPI

        # Mock the call_api and _get_sso_version methods
        mock_response = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        mocker.patch.object(UsersClient, "_get_sso_version", side_effect=mock_get_sso_version)

        domain = "http://localhost:3000"
        uc = UsersClient(domain=domain)

        # Test with invalid email containing forbidden character
        with pytest.raises(CnvrgArgumentsError):
            uc.register(username="invalid_user", email="nonexistent@-example.com", password="password")

        assert mock_response.call_count == 0

    def test_user_register_bad_username(self, mocker):
        def mock_call_api(*args, **kwargs):
            return

        def mock_get_sso_version(*args, **kwargs):
            return SSO_VERSION.CAPI

        mock_response = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        mocker.patch.object(UsersClient, "_get_sso_version", side_effect=mock_get_sso_version)

        domain = "http://localhost:3000"
        uc = UsersClient(domain=domain)

        with pytest.raises(CnvrgArgumentsError) as exception_info:
            uc.register(username="invalid user", email="valid@email.com", password="password")

        assert "user" in str(exception_info.value)
        assert mock_response.call_count == 0

    def test_user_register_valid_inputs(self, mocker):
        def mock_call_api(*args, **kwargs):
            return JAF(response={
                "data": {
                    "id": "1",
                    "type": "user",
                    "attributes": {
                        "email": "valid@email.com",
                        "username": "valid_user",
                    }
                },
                "meta": {
                    "jwt": "asdasd"
                }

            })

        def mock_get_sso_version(*args, **kwargs):
            return SSO_VERSION.CAPI

        mock_response = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        mocker.patch.object(UsersClient, "_get_sso_version", side_effect=mock_get_sso_version)

        domain = "http://localhost:3000"
        uc = UsersClient(domain=domain)

        user = uc.register(username="validuser", email="val.ID@email.com", password="password")
        assert isinstance(user, User)
        assert mock_response.call_count == 1

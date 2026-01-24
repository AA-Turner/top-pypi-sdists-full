from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import UUID

from pycarlo.core import Client, Session

from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.fields import ORACLE_DB_TYPE
from montecarlodata.integrations.onboarding.transactional.transactional_db import (
    TransactionalOnboardingService,
)
from montecarlodata.utils import GqlWrapper
from tests.test_base_onboarding import _SAMPLE_BASE_OPTIONS
from tests.test_common_user import _SAMPLE_CONFIG


class TransactionalOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._mc_client = Client(
            session=Session(
                endpoint=_SAMPLE_CONFIG.mcd_api_endpoint,
                mcd_id=_SAMPLE_CONFIG.mcd_id,
                mcd_token=_SAMPLE_CONFIG.mcd_token,
            )
        )
        self._service = TransactionalOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            mc_client=self._mc_client,
            user_service=self._user_service_mock,
        )

    @patch.object(TransactionalOnboardingService, "test_new_credentials")
    def test_generic_transactional_db_flow(self, test_new_credentials_mock):
        expected_options = {
            **{
                "connection_type": "transactional-db",
                "warehouse_type": "transactional-db",
            },
            **_SAMPLE_BASE_OPTIONS,
        }

        test_new_credentials_mock.return_value = "tmp-string"

        self._service.onboard_transactional_db(**_SAMPLE_BASE_OPTIONS)
        test_new_credentials_mock.assert_called_once_with(**expected_options)

    @patch("montecarlodata.integrations.onboarding.base.Path")
    @patch.object(TransactionalOnboardingService, "test_new_credentials")
    @patch.object(TransactionalOnboardingService, "add_connection")
    def test_oracle_ssl_options_flow(
        self, add_connection_mock, test_new_credentials_mock, path_mock
    ):
        """Test that SSL options are properly loaded and passed through for Oracle connections."""
        # Mock certificate file contents
        ca_cert_content = "-----BEGIN CERTIFICATE-----\nCA_CERT_CONTENT\n-----END CERTIFICATE-----"
        client_cert_content = (
            "-----BEGIN CERTIFICATE-----\nCLIENT_CERT_CONTENT\n-----END CERTIFICATE-----"
        )
        client_key_content = (
            "-----BEGIN PRIVATE KEY-----\nCLIENT_KEY_CONTENT\n-----END PRIVATE KEY-----"
        )

        # Setup Path mock: Path(path_string) returns a mock with read_text() method
        def path_side_effect(path_string):
            mock_path = Mock()
            if path_string == "/path/to/ca.pem":
                mock_path.read_text.return_value = ca_cert_content
            elif path_string == "/path/to/cert.pem":
                mock_path.read_text.return_value = client_cert_content
            elif path_string == "/path/to/key.pem":
                mock_path.read_text.return_value = client_key_content
            return mock_path

        path_mock.side_effect = path_side_effect
        test_new_credentials_mock.return_value = "tmp-string"

        options = {
            **_SAMPLE_BASE_OPTIONS,
            "dbType": ORACLE_DB_TYPE,
            "dbName": "test_db",
            "ssl_ca": "/path/to/ca.pem",
            "ssl_cert": "/path/to/cert.pem",
            "ssl_key": "/path/to/key.pem",
        }

        self._service.onboard_transactional_db(**options)

        # Verify SSL options were loaded correctly
        expected_ssl_options = {
            "ca_data": ca_cert_content,
            "cert_data": client_cert_content,
            "key_data": client_key_content,
        }

        # Verify test_new_credentials was called with SSL options in connection_settings
        call_args = test_new_credentials_mock.call_args[1]
        self.assertIn("connection_settings", call_args)
        self.assertEqual(call_args["connection_settings"]["ssl_options"], expected_ssl_options)
        self.assertEqual(call_args["connection_type"], ORACLE_DB_TYPE)
        self.assertEqual(call_args["warehouse_type"], ORACLE_DB_TYPE)
        self.assertEqual(call_args["dbType"], ORACLE_DB_TYPE)

    @patch.object(TransactionalOnboardingService, "create_update_credentials")
    @patch.object(TransactionalOnboardingService, "test_new_credentials_on_existing_connection")
    @patch.object(TransactionalOnboardingService, "update_existing_connection")
    def test_update_transactional_db_basic_flow(
        self,
        update_existing_connection_mock,
        test_new_credentials_on_existing_connection_mock,
        create_update_credentials_mock,
    ):
        """Test basic update flow for transactional DB connections."""
        connection_id = UUID("12345678-1234-1234-1234-123456789012")
        create_update_credentials_mock.return_value = "tmp-key"

        self._service.update_transactional_db(
            connection_id=connection_id,
            connection_type=ORACLE_DB_TYPE,
            skip_validation=False,
            validate_only=False,
            auto_yes=True,
            host="new-host",
            port=1521,
        )

        # Verify create_update_credentials was called with correct changes
        create_update_credentials_mock.assert_called_once()
        call_kwargs = create_update_credentials_mock.call_args[1]
        self.assertEqual(call_kwargs["connection_id"], connection_id)
        self.assertEqual(call_kwargs["connection_type"], ORACLE_DB_TYPE)
        self.assertEqual(call_kwargs["changes"]["host"], "new-host")
        self.assertEqual(call_kwargs["changes"]["port"], 1521)
        self.assertNotIn("ssl_options", call_kwargs["changes"])

        # Verify validation was called
        test_new_credentials_on_existing_connection_mock.assert_called_once_with(
            temp_key="tmp-key",
            connection_id=connection_id,
            connection_type=ORACLE_DB_TYPE,
        )

        # Verify update was called
        update_existing_connection_mock.assert_called_once_with(
            connection_id=connection_id, temp_key="tmp-key"
        )

    @patch("montecarlodata.integrations.onboarding.base.Path")
    @patch.object(TransactionalOnboardingService, "create_update_credentials")
    @patch.object(TransactionalOnboardingService, "test_new_credentials_on_existing_connection")
    @patch.object(TransactionalOnboardingService, "update_existing_connection")
    def test_update_oracle_ssl_options_flow(
        self,
        update_existing_connection_mock,
        test_new_credentials_on_existing_connection_mock,
        create_update_credentials_mock,
        path_mock,
    ):
        """Test that SSL options are properly loaded and passed through
        when updating Oracle connections."""
        connection_id = UUID("12345678-1234-1234-1234-123456789012")

        # Mock certificate file contents
        ca_cert_content = "-----BEGIN CERTIFICATE-----\nCA_CERT_CONTENT\n-----END CERTIFICATE-----"
        client_cert_content = (
            "-----BEGIN CERTIFICATE-----\nCLIENT_CERT_CONTENT\n-----END CERTIFICATE-----"
        )
        client_key_content = (
            "-----BEGIN PRIVATE KEY-----\nCLIENT_KEY_CONTENT\n-----END PRIVATE KEY-----"
        )

        # Setup Path mock: Path(path_string) returns a mock with read_text() method
        def path_side_effect(path_string):
            mock_path = Mock()
            if path_string == "/path/to/ca.pem":
                mock_path.read_text.return_value = ca_cert_content
            elif path_string == "/path/to/cert.pem":
                mock_path.read_text.return_value = client_cert_content
            elif path_string == "/path/to/key.pem":
                mock_path.read_text.return_value = client_key_content
            return mock_path

        path_mock.side_effect = path_side_effect
        create_update_credentials_mock.return_value = "tmp-key"

        self._service.update_transactional_db(
            connection_id=connection_id,
            connection_type=ORACLE_DB_TYPE,
            skip_validation=False,
            validate_only=False,
            auto_yes=True,
            ssl_ca="/path/to/ca.pem",
            ssl_cert="/path/to/cert.pem",
            ssl_key="/path/to/key.pem",
        )

        # Verify SSL options were loaded correctly and passed to create_update_credentials
        expected_ssl_options = {
            "ca_data": ca_cert_content,
            "cert_data": client_cert_content,
            "key_data": client_key_content,
        }

        call_kwargs = create_update_credentials_mock.call_args[1]
        self.assertIn("ssl_options", call_kwargs["changes"])
        self.assertEqual(call_kwargs["changes"]["ssl_options"], expected_ssl_options)
        self.assertEqual(call_kwargs["connection_id"], connection_id)
        self.assertEqual(call_kwargs["connection_type"], ORACLE_DB_TYPE)

        # Verify skip_cert_verification is NOT in top-level changes (should be excluded)
        self.assertNotIn("skip_cert_verification", call_kwargs["changes"])
        # Verify skip_verification is NOT in ssl_options (not supported in update mutations)
        self.assertNotIn("skip_verification", call_kwargs["changes"]["ssl_options"])

    @patch.object(TransactionalOnboardingService, "create_update_credentials")
    @patch.object(TransactionalOnboardingService, "test_new_credentials_on_existing_connection")
    @patch.object(TransactionalOnboardingService, "update_existing_connection")
    def test_update_oracle_ssl_disabled_flow(
        self,
        update_existing_connection_mock,
        test_new_credentials_on_existing_connection_mock,
        create_update_credentials_mock,
    ):
        """Test that SSL disabled option is properly handled when updating Oracle connections."""
        connection_id = UUID("12345678-1234-1234-1234-123456789012")
        create_update_credentials_mock.return_value = "tmp-key"

        self._service.update_transactional_db(
            connection_id=connection_id,
            connection_type=ORACLE_DB_TYPE,
            skip_validation=False,
            validate_only=False,
            auto_yes=True,
            ssl_disabled=True,
        )

        # Verify ssl_disabled is converted to ssl_options with disabled=True
        call_kwargs = create_update_credentials_mock.call_args[1]
        self.assertIn("ssl_options", call_kwargs["changes"])
        self.assertEqual(call_kwargs["changes"]["ssl_options"]["disabled"], True)
        self.assertEqual(call_kwargs["connection_type"], ORACLE_DB_TYPE)

    @patch.object(TransactionalOnboardingService, "create_update_credentials")
    def test_update_oracle_skip_validation(
        self,
        create_update_credentials_mock,
    ):
        """Test that skip_validation bypasses validation when updating Oracle connections."""
        connection_id = UUID("12345678-1234-1234-1234-123456789012")
        create_update_credentials_mock.return_value = "tmp-key"

        # fmt: off
        with patch.object(
            self._service, "test_new_credentials_on_existing_connection"
        ) as test_mock, patch.object(
            self._service, "update_existing_connection"
        ) as update_mock:
            self._service.update_transactional_db(
                connection_id=connection_id,
                connection_type=ORACLE_DB_TYPE,
                skip_validation=True,
                validate_only=False,
                auto_yes=True,
                host="new-host",
            )
        # fmt: on

            # Verify validation was skipped
            test_mock.assert_not_called()

            # Verify update was still called
            update_mock.assert_called_once_with(connection_id=connection_id, temp_key="tmp-key")

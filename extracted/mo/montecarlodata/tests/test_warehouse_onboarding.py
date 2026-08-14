import base64
from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner

from montecarlodata.common.user import UserService
from montecarlodata.integrations.commands import add_redshift
from montecarlodata.integrations.onboarding.warehouse.warehouses import (
    WarehouseOnboardingService,
)
from montecarlodata.queries.onboarding import (
    TEST_BQ_CRED_MUTATION,
    TEST_DATABASE_CRED_MUTATION,
    TEST_SNOWFLAKE_CRED_MUTATION,
)
from montecarlodata.utils import AwsClientWrapper, GqlWrapper
from tests.test_base_onboarding import _SAMPLE_BASE_OPTIONS
from tests.test_common_user import _SAMPLE_CONFIG


class WarehouseOnBoardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = WarehouseOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )

    @patch.object(WarehouseOnboardingService, "onboard")
    def test_redshift_flow(self, onboard_mock):
        expected_options = {
            **{"connectionType": "redshift", "warehouseType": "redshift"},
            **_SAMPLE_BASE_OPTIONS,
        }

        self._service.onboard_redshift(**_SAMPLE_BASE_OPTIONS)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_DATABASE_CRED_MUTATION,
            validation_response="testDatabaseCredentials",
            connection_type="redshift",
            **expected_options,
        )

    @patch("montecarlodata.integrations.onboarding.base.Path")
    @patch.object(WarehouseOnboardingService, "onboard")
    def test_redshift_ssl_ca_flow(self, onboard_mock, path_mock):
        """--ssl-ca is loaded into ssl_options as inline CA cert data (CA-only SSL)."""
        ca_cert_content = "-----BEGIN CERTIFICATE-----\nCA_CERT\n-----END CERTIFICATE-----"
        path_mock.return_value.read_text.return_value = ca_cert_content

        self._service.onboard_redshift(ssl_ca="/path/to/ca.pem", **_SAMPLE_BASE_OPTIONS)

        call_kwargs = onboard_mock.call_args[1]
        self.assertEqual(call_kwargs["ssl_options"], {"ca_data": ca_cert_content})
        self.assertEqual(call_kwargs["connectionType"], "redshift")
        self.assertEqual(call_kwargs["warehouseType"], "redshift")
        self.assertEqual(call_kwargs["validation_query"], TEST_DATABASE_CRED_MUTATION)
        self.assertEqual(call_kwargs["validation_response"], "testDatabaseCredentials")
        self.assertEqual(call_kwargs["connection_type"], "redshift")

    @patch.object(WarehouseOnboardingService, "onboard")
    def test_redshift_ssl_disabled_flow(self, onboard_mock):
        """--ssl-disabled is forwarded as ssl_options.disabled=True."""
        self._service.onboard_redshift(ssl_disabled=True, **_SAMPLE_BASE_OPTIONS)

        call_kwargs = onboard_mock.call_args[1]
        self.assertEqual(call_kwargs["ssl_options"], {"disabled": True})

    @patch("montecarlodata.integrations.commands.WarehouseOnboardingService")
    def test_add_redshift_command_forwards_ssl_ca(self, service_mock):
        """The add_redshift CLI command exposes --ssl-ca and forwards it to the service."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("ca.pem", "w") as ca_file:
                ca_file.write("-----BEGIN CERTIFICATE-----\nCA\n-----END CERTIFICATE-----")
            result = runner.invoke(
                add_redshift,
                [
                    "--host",
                    "redshift.example.com",
                    "--user",
                    "admin",
                    "--password",
                    "secret",
                    "--database",
                    "dev",
                    "--ssl-ca",
                    "ca.pem",
                ],
                obj={"config": _SAMPLE_CONFIG},
            )

        self.assertEqual(result.exit_code, 0, result.output)
        service_mock.return_value.onboard_redshift.assert_called_once()
        call_kwargs = service_mock.return_value.onboard_redshift.call_args[1]
        self.assertEqual(call_kwargs["ssl_ca"], "ca.pem")
        self.assertIsNone(call_kwargs["ssl_disabled"])
        self.assertEqual(call_kwargs["dbName"], "dev")

    @patch.object(WarehouseOnboardingService, "onboard")
    def test_snowflake_flow(self, onboard_mock):
        expected_options = {**{"warehouseType": "snowflake"}, **_SAMPLE_BASE_OPTIONS}

        self._service.onboard_snowflake(**_SAMPLE_BASE_OPTIONS)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_SNOWFLAKE_CRED_MUTATION,
            validation_response="testSnowflakeCredentials",
            connection_type="snowflake",
            **expected_options,
        )

    @patch.object(WarehouseOnboardingService, "onboard")
    @patch("montecarlodata.integrations.onboarding.warehouse.warehouses.read_as_base64")
    def test_snowflake_flow_with_private_key(self, read_as_base64_mock, onboard_mock):
        file_path = "/tmp/my_private_key"
        private_key = "private_key"
        base64_private_key = base64.b64encode(private_key.encode("utf-8"))
        input_options = {"private_key": file_path, **_SAMPLE_BASE_OPTIONS}

        expected_options = {
            **{
                "warehouseType": "snowflake",
                "private_key": base64_private_key.decode(),
            },
            **_SAMPLE_BASE_OPTIONS,
        }

        read_as_base64_mock.return_value = base64_private_key

        self._service.onboard_snowflake(**input_options)
        read_as_base64_mock.assert_called_once_with(file_path)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_SNOWFLAKE_CRED_MUTATION,
            validation_response="testSnowflakeCredentials",
            connection_type="snowflake",
            **expected_options,
        )

    @patch.object(WarehouseOnboardingService, "onboard")
    @patch("montecarlodata.integrations.onboarding.warehouse.warehouses.read_as_base64")
    def test_snowflake_flow_with_private_key_and_passphrase(
        self, read_as_base64_mock, onboard_mock
    ):
        file_path = "/tmp/my_private_key"
        private_key = "private_key"
        passphrase = "foobar123"
        base64_private_key = base64.b64encode(private_key.encode("utf-8"))
        input_options = {
            "private_key": file_path,
            "private_key_passphrase": passphrase,
            **_SAMPLE_BASE_OPTIONS,
        }

        expected_options = {
            **{
                "warehouseType": "snowflake",
                "private_key": base64_private_key.decode(),
                "private_key_passphrase": passphrase,
            },
            **_SAMPLE_BASE_OPTIONS,
        }

        read_as_base64_mock.return_value = base64_private_key

        self._service.onboard_snowflake(**input_options)
        read_as_base64_mock.assert_called_once_with(file_path)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_SNOWFLAKE_CRED_MUTATION,
            validation_response="testSnowflakeCredentials",
            connection_type="snowflake",
            **expected_options,
        )

    @patch.object(WarehouseOnboardingService, "onboard")
    @patch("montecarlodata.integrations.onboarding.warehouse.warehouses.read_as_base64")
    def test_bq_flow(self, read_as_base64_mock, onboard_mock):
        file_path, service_json = "foo", "bar"
        base64_service_json = base64.b64encode(service_json.encode("utf-8"))

        input_options = {"ServiceFile": file_path, **_SAMPLE_BASE_OPTIONS}
        expected_options = {
            **{
                "warehouseType": "bigquery",
                "serviceJson": base64_service_json.decode(),
            },
            **_SAMPLE_BASE_OPTIONS,
        }

        read_as_base64_mock.return_value = base64_service_json

        self._service.onboard_bq(**input_options)
        read_as_base64_mock.assert_called_once_with(file_path)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_BQ_CRED_MUTATION,
            validation_response="testBqCredentials",
            connection_type="bigquery",
            **expected_options,
        )

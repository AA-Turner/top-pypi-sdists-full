import os
import tempfile
from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner

from montecarlodata.common.user import UserService
from montecarlodata.integrations.commands import add_presto
from montecarlodata.integrations.onboarding.data_lake.presto import (
    PrestoOnboardingService,
)
from montecarlodata.queries.onboarding import (
    TEST_PRESTO_CRED_MUTATION,
)
from montecarlodata.utils import AwsClientWrapper, GqlWrapper
from tests.test_base_onboarding import _SAMPLE_BASE_OPTIONS
from tests.test_common_user import _SAMPLE_CONFIG


class PrestoOnBoardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = PrestoOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )

    @patch.object(PrestoOnboardingService, "onboard")
    def test_presto_sql_flow(self, onboard_mock):
        s3_key = "testing/test"
        expected_options = {
            "ssl_options": {
                "mechanism": "dc-s3",
                "cert": "testing/test",
                "skip_verification": False,
            },
            **_SAMPLE_BASE_OPTIONS,
        }

        self._service.onboard_presto_sql(
            **{
                "cert_s3": s3_key,
                "skip_cert_verification": False,
                **_SAMPLE_BASE_OPTIONS,
            }
        )
        onboard_mock.assert_called_once_with(
            validation_query=TEST_PRESTO_CRED_MUTATION,
            validation_response="testPrestoCredentials",
            connection_type="presto",
            **expected_options,
        )

    @patch.object(PrestoOnboardingService, "onboard")
    def test_presto_sql_flow_passes_metadata_catalog_id(self, onboard_mock):
        # The Glue-side catalog name must flow through to the API payload so
        # the monolith can persist the metadata-catalog mapping.
        self._service.onboard_presto_sql(
            **{
                "catalog": "bronze",
                "metadata_catalog_id": "s3tablescatalog/lakehouse-bronze-prd",
                **_SAMPLE_BASE_OPTIONS,
            }
        )
        onboard_mock.assert_called_once_with(
            validation_query=TEST_PRESTO_CRED_MUTATION,
            validation_response="testPrestoCredentials",
            connection_type="presto",
            catalog="bronze",
            metadata_catalog_id="s3tablescatalog/lakehouse-bronze-prd",
            **_SAMPLE_BASE_OPTIONS,
        )
        # The mutation must declare and forward the variable under the exact
        # name convert_snakes_to_camels produces for metadata_catalog_id.
        self.assertIn("$metadataCatalogId:String", TEST_PRESTO_CRED_MUTATION)
        self.assertIn("metadataCatalogId:$metadataCatalogId", TEST_PRESTO_CRED_MUTATION)


class PrestoCommandWiringTest(TestCase):
    """CLI-command-level tests for `integrations add-presto`."""

    _ARGS = [
        "--host",
        "trino.example.com",
        "--http-scheme",
        "https",
        "--name",
        "my-warehouse",
    ]

    @patch("montecarlodata.integrations.commands.PrestoOnboardingService")
    def test_add_presto_cli_command_passes_metadata_catalog_id(self, service_class_mock):
        onboard_mock = service_class_mock.return_value.onboard_presto_sql

        result = CliRunner().invoke(
            add_presto,
            obj={"config": _SAMPLE_CONFIG},
            args=self._ARGS
            + [
                "--catalog",
                "bronze",
                "--metadata-catalog-id",
                "s3tablescatalog/lakehouse-bronze-prd",
            ],
        )

        self.assertEqual(result.exit_code, 0, result.output)
        call_kwargs = onboard_mock.call_args.kwargs
        self.assertEqual(call_kwargs["catalog"], "bronze")
        self.assertEqual(call_kwargs["metadata_catalog_id"], "s3tablescatalog/lakehouse-bronze-prd")

    @patch("montecarlodata.integrations.commands.PrestoOnboardingService")
    def test_add_presto_cli_command_rejects_metadata_catalog_id_without_catalog(
        self, service_class_mock
    ):
        result = CliRunner().invoke(
            add_presto,
            obj={"config": _SAMPLE_CONFIG},
            args=self._ARGS + ["--metadata-catalog-id", "s3tablescatalog/lakehouse-bronze-prd"],
        )

        # Assert the reason, not just the failure: an unknown option also
        # exits 2 without constructing the service.
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Cannot use 'metadata-catalog-id' without 'catalog'", result.output)
        service_class_mock.assert_not_called()

    @patch("montecarlodata.integrations.commands.PrestoOnboardingService")
    def test_add_presto_cli_command_accepts_catalog_without_metadata_catalog_id(
        self, service_class_mock
    ):
        # The pairing rule is one-directional: --catalog predates this option
        # and must keep working alone for existing users.
        onboard_mock = service_class_mock.return_value.onboard_presto_sql

        result = CliRunner().invoke(
            add_presto,
            obj={"config": _SAMPLE_CONFIG},
            args=self._ARGS + ["--catalog", "bronze"],
        )

        self.assertEqual(result.exit_code, 0, result.output)
        call_kwargs = onboard_mock.call_args.kwargs
        self.assertEqual(call_kwargs["catalog"], "bronze")
        self.assertIsNone(call_kwargs["metadata_catalog_id"])

    @patch("montecarlodata.integrations.commands.PrestoOnboardingService")
    def test_add_presto_cli_command_pairing_check_ignores_option_file_values(
        self, service_class_mock
    ):
        # Documents a known limitation: AdvancedOptions' required_with_options
        # only sees command-line flags. Values from --option-file merge into the
        # default map after the check runs, so catalog supplied there does not
        # satisfy the pairing and the invocation is falsely rejected. The server
        # is the authority for option-file-supplied pairs; flip this expectation
        # if the shared mechanism is ever fixed to consult ctx.lookup_default.
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as option_file:
            option_file.write("catalog = 'bronze'\n")
            option_file_path = option_file.name

        try:
            result = CliRunner().invoke(
                add_presto,
                obj={"config": _SAMPLE_CONFIG},
                args=[
                    "--option-file",
                    option_file_path,
                    "--host",
                    "trino.example.com",
                    "--http-scheme",
                    "https",
                    "--name",
                    "my-warehouse",
                    "--metadata-catalog-id",
                    "s3tablescatalog/lakehouse-bronze-prd",
                ],
            )
        finally:
            os.unlink(option_file_path)

        self.assertEqual(result.exit_code, 2)
        self.assertIn("Cannot use 'metadata-catalog-id' without 'catalog'", result.output)
        service_class_mock.assert_not_called()

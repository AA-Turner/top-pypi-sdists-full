from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner
from pycarlo.core import Client

from montecarlodata.collector.validation import CollectorValidationService
from montecarlodata.common.user import UserService
from montecarlodata.integrations.commands import (
    add_databricks_metastore_sql_warehouse,
    add_databricks_sql_warehouse,
    create_databricks_webhook_key,
)
from montecarlodata.integrations.onboarding.data_lake.databricks import (
    DatabricksOnboardingService,
)
from montecarlodata.integrations.onboarding.fields import (
    DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
    DATABRICKS_SQL_WAREHOUSE_CONNECTION_TYPE,
    EXPECTED_TEST_DATABRICKS_METASTORE_SQL_WAREHOUSE_V2_RESPONSE_FIELD,
    EXPECTED_TEST_DATABRICKS_SQL_WAREHOUSE_V2_RESPONSE_FIELD,
)
from montecarlodata.queries.onboarding import (
    TEST_DATABRICKS_METASTORE_SQL_WAREHOUSE_CRED_V2_MUTATION,
    TEST_DATABRICKS_SQL_WAREHOUSE_CRED_V2_MUTATION,
)
from montecarlodata.utils import GqlWrapper
from tests.test_common_user import _SAMPLE_CONFIG


class DatabricksOnboardingTest(TestCase):
    _TEMP_KEY = "tmp/databricks-key"

    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._mc_client_mock = Mock(autospec=Client)

        self._service = DatabricksOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            mc_client=self._mc_client_mock,
            request_wrapper=self._request_wrapper_mock,
            user_service=self._user_service_mock,
        )

    @patch.object(DatabricksOnboardingService, "add_connection")
    @patch.object(DatabricksOnboardingService, "test_new_credentials")
    def test_onboard_databricks_sql_warehouse(
        self,
        test_new_credentials_mock,
        add_connection_mock,
    ):
        test_new_credentials_mock.return_value = self._TEMP_KEY
        options = {
            "databricks_workspace_url": "databricks_workspace_url",
            "databricks_warehouse_id": "databricks_warehouse_id",
            "databricks_token": "databricks_token",
        }

        self._service.onboard_databricks_sql_warehouse(
            connection_type=DATABRICKS_SQL_WAREHOUSE_CONNECTION_TYPE,
            warehouseName="test",
            **options,
        )

        # Validates via the modern v2 flow for the plain SQL warehouse connection type...
        test_new_credentials_mock.assert_called_once_with(
            connection_type=DATABRICKS_SQL_WAREHOUSE_CONNECTION_TYPE,
            warehouseName="test",
            **options,
        )
        # ...then adds the connection using the returned temp credentials key.
        add_connection_mock.assert_called_once_with(
            self._TEMP_KEY,
            connection_type=DATABRICKS_SQL_WAREHOUSE_CONNECTION_TYPE,
            warehouseName="test",
            **options,
        )

    @patch.object(DatabricksOnboardingService, "add_connection")
    @patch.object(DatabricksOnboardingService, "test_new_credentials")
    def test_onboard_databricks_metastore_sql_warehouse(
        self,
        test_new_credentials_mock,
        add_connection_mock,
    ):
        test_new_credentials_mock.return_value = self._TEMP_KEY
        options = {
            "databricks_workspace_url": "databricks_workspace_url",
            "databricks_warehouse_id": "databricks_warehouse_id",
            "databricks_workspace_id": "databricks_workspace_id",
            "databricks_token": "databricks_token",
        }

        self._service.onboard_databricks_sql_warehouse(
            connection_type=DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
            warehouseName="test",
            **options,
        )

        test_new_credentials_mock.assert_called_once_with(
            connection_type=DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
            warehouseName="test",
            **options,
        )
        add_connection_mock.assert_called_once_with(
            self._TEMP_KEY,
            connection_type=DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
            warehouseName="test",
            **options,
        )

    @patch.object(DatabricksOnboardingService, "add_connection")
    @patch.object(DatabricksOnboardingService, "test_new_credentials")
    def test_onboard_skips_add_connection_when_no_key(
        self,
        test_new_credentials_mock,
        add_connection_mock,
    ):
        # --validate-only (and any path that does not return a key) must not add a connection.
        test_new_credentials_mock.return_value = None

        self._service.onboard_databricks_sql_warehouse(
            connection_type=DATABRICKS_SQL_WAREHOUSE_CONNECTION_TYPE,
            warehouseName="test",
            databricks_workspace_url="databricks_workspace_url",
            databricks_warehouse_id="databricks_warehouse_id",
            databricks_token="databricks_token",
        )

        test_new_credentials_mock.assert_called_once()
        add_connection_mock.assert_not_called()

    def test_databricks_connection_types_wired_to_v2_mutations(self):
        # Guardrail: each Databricks command validates via its own v2 mutation/validator.
        # In particular the metastore command must use the metastore v2 mutation (historically
        # it reused the plain SQL-warehouse path).
        creds = CollectorValidationService._CONNECTION_TYPES_TO_CREDS_MUTATIONS_MAPPING
        operations = CollectorValidationService._CONNECTION_TYPES_TO_OPERATION_TYPE

        self.assertEqual(
            creds[DATABRICKS_SQL_WAREHOUSE_CONNECTION_TYPE],
            TEST_DATABRICKS_SQL_WAREHOUSE_CRED_V2_MUTATION,
        )
        self.assertEqual(
            creds[DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE],
            TEST_DATABRICKS_METASTORE_SQL_WAREHOUSE_CRED_V2_MUTATION,
        )
        self.assertEqual(
            operations[DATABRICKS_SQL_WAREHOUSE_CONNECTION_TYPE],
            EXPECTED_TEST_DATABRICKS_SQL_WAREHOUSE_V2_RESPONSE_FIELD,
        )
        self.assertEqual(
            operations[DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE],
            EXPECTED_TEST_DATABRICKS_METASTORE_SQL_WAREHOUSE_V2_RESPONSE_FIELD,
        )


class DatabricksCommandWiringTest(TestCase):
    """CLI-command-level tests: each Databricks command must construct the service with the
    now-required mc_client and forward the correct connection type / args."""

    _PLAIN_ARGS = [
        "--databricks-workspace-url",
        "https://dbc-test.cloud.databricks.com",
        "--databricks-warehouse-id",
        "warehouse-123",
        "--databricks-token",
        "dummy-token",
        "--name",
        "my-warehouse",
    ]

    @patch("montecarlodata.integrations.commands.DatabricksOnboardingService")
    @patch("montecarlodata.integrations.commands.create_mc_client")
    def test_add_databricks_sql_warehouse_cli_command(
        self, create_mc_client_mock, service_class_mock
    ):
        onboard_mock = service_class_mock.return_value.onboard_databricks_sql_warehouse

        result = CliRunner().invoke(
            add_databricks_sql_warehouse,
            obj={"config": _SAMPLE_CONFIG},
            args=self._PLAIN_ARGS,
        )

        self.assertEqual(result.exit_code, 0, result.output)
        create_mc_client_mock.assert_called_once()
        self.assertEqual(
            service_class_mock.call_args.kwargs["mc_client"],
            create_mc_client_mock.return_value,
        )
        onboard_mock.assert_called_once()
        call_kwargs = onboard_mock.call_args.kwargs
        self.assertEqual(call_kwargs["connection_type"], DATABRICKS_SQL_WAREHOUSE_CONNECTION_TYPE)
        self.assertEqual(call_kwargs["warehouseName"], "my-warehouse")

    @patch("montecarlodata.integrations.commands.DatabricksOnboardingService")
    @patch("montecarlodata.integrations.commands.create_mc_client")
    def test_add_databricks_metastore_sql_warehouse_cli_command(
        self, create_mc_client_mock, service_class_mock
    ):
        onboard_mock = service_class_mock.return_value.onboard_databricks_sql_warehouse

        result = CliRunner().invoke(
            add_databricks_metastore_sql_warehouse,
            obj={"config": _SAMPLE_CONFIG},
            args=self._PLAIN_ARGS + ["--databricks-workspace-id", "workspace-1"],
        )

        self.assertEqual(result.exit_code, 0, result.output)
        create_mc_client_mock.assert_called_once()
        self.assertEqual(
            service_class_mock.call_args.kwargs["mc_client"],
            create_mc_client_mock.return_value,
        )
        onboard_mock.assert_called_once()
        self.assertEqual(
            onboard_mock.call_args.kwargs["connection_type"],
            DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
        )

    @patch("montecarlodata.integrations.commands.DatabricksOnboardingService")
    @patch("montecarlodata.integrations.commands.create_mc_client")
    def test_create_databricks_webhook_key_cli_command_wires_mc_client(
        self, create_mc_client_mock, service_class_mock
    ):
        # Regression for SUP-496 review F1: this command also constructs the service and must
        # pass the now-required mc_client (previously it did not, raising TypeError at runtime).
        webhook_mock = service_class_mock.return_value.create_webhook_key

        result = CliRunner().invoke(
            create_databricks_webhook_key,
            obj={"config": _SAMPLE_CONFIG},
            args=["--integration-name", "my-metastore"],
        )

        self.assertEqual(result.exit_code, 0, result.output)
        create_mc_client_mock.assert_called_once()
        self.assertEqual(
            service_class_mock.call_args.kwargs["mc_client"],
            create_mc_client_mock.return_value,
        )
        webhook_mock.assert_called_once_with(warehouse_name="my-metastore")

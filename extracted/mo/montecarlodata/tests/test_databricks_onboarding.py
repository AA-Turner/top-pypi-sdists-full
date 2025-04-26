from unittest import TestCase
from unittest.mock import Mock, call, patch

from box import Box
from parameterized import parameterized
from pycarlo.core import Client, Mutation, Query

from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.data_lake.databricks import (
    DEFAULT_GATEWAY_URL,
    DEFAULT_SECRET_NAME,
    DEFAULT_SECRET_SCOPE,
    DatabricksOnboardingService,
)
from montecarlodata.integrations.onboarding.fields import (
    DATA_LAKE_WAREHOUSE_TYPE,
    DATABRICKS_DELTA_CONNECTION_TYPE,
    DATABRICKS_METASTORE_CONNECTION_TYPE,
    DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
)
from montecarlodata.queries.onboarding import (
    TEST_DATABRICKS_CRED_MUTATION,
    DatabricksSqlWarehouseOnboardingQueries,
)
from montecarlodata.utils import AwsClientWrapper
from tests.test_base_onboarding import _SAMPLE_BASE_OPTIONS
from tests.test_common_user import _SAMPLE_CONFIG


class DatabricksMetastoreOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._mc_client_mock = Mock(autospec=Client)
        self._user_service_mock = Mock(autospec=UserService)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = DatabricksOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            mc_client=self._mc_client_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )

    @parameterized.expand(
        [
            (DATABRICKS_METASTORE_CONNECTION_TYPE, [], {}, 3),
            (DATABRICKS_DELTA_CONNECTION_TYPE, ["hive"], {"project_id": "hive"}, 4),
            (
                DATABRICKS_DELTA_CONNECTION_TYPE,
                ["awsdatacatalog"],
                {"project_id": "awsdatacatalog"},
                4,
            ),
        ]
    )
    @patch.object(DatabricksOnboardingService, "onboard")
    def test_databricks_flow(
        self,
        connection_type,
        projects,
        expected_projects,
        expected_call_count,
        onboard_mock,
    ):
        options = {
            "databricks_workspace_url": "databricks_workspace_url",
            "databricks_workspace_id": "databricks_workspace_id",
            "databricks_cluster_id": "databricks_cluster_id",
            "databricks_token": "databricks_token",
            "databricks_secret_key": DEFAULT_SECRET_NAME,
            "databricks_secret_scope": DEFAULT_SECRET_SCOPE,
        }
        job_info = dict(
            databricks_job_id="databricks_job_id",
            databricks_job_name="databricks_job_name",
            databricks_notebook_path="databricks_notebook_path",
            databricks_notebook_source="databricks_notebook_path",
            databricks_notebook_version="123",
        )

        self._mc_client_mock.side_effect = [
            Mock(),
            Mock(),
            Box(
                dict(
                    create_databricks_notebook_job=dict(
                        databricks=dict(
                            workspace_job_id=job_info["databricks_job_id"],
                            workspace_job_name=job_info["databricks_job_name"],
                            workspace_notebook_path=job_info["databricks_notebook_path"],
                            notebook_source=job_info["databricks_notebook_source"],
                            notebook_version=job_info["databricks_notebook_version"],
                        ),
                    )
                )
            ),
            Box(dict(get_projects=dict(projects=projects))),
        ]

        self._service.onboard_databricks_metastore(
            connection_type=connection_type, **options, **_SAMPLE_BASE_OPTIONS
        )

        expected_options = {**options, **_SAMPLE_BASE_OPTIONS}
        expected_job_limits = {
            **job_info,
            "integration_gateway": {
                "gateway_url": DEFAULT_GATEWAY_URL,
                "databricks_secret_key": DEFAULT_SECRET_NAME,
                "databricks_secret_scope": DEFAULT_SECRET_SCOPE,
            },
            **expected_projects,
        }

        onboard_mock.assert_called_once_with(
            validation_query=TEST_DATABRICKS_CRED_MUTATION,
            validation_response="testDatabricksCredentials",
            connection_type=connection_type,
            job_limits=expected_job_limits,
            **expected_options,
        )
        self.assertEqual(self._mc_client_mock.call_count, expected_call_count)

    @patch.object(DatabricksOnboardingService, "onboard")
    def test_databricks_gql_api_calls(self, onboard_mock):
        options = {
            "databricks_workspace_url": "databricks_workspace_url",
            "databricks_workspace_id": "databricks_workspace_id",
            "databricks_cluster_id": "databricks_cluster_id",
            "databricks_token": "databricks_token",
            "databricks_secret_key": DEFAULT_SECRET_NAME,
            "databricks_secret_scope": DEFAULT_SECRET_SCOPE,
            "dc_id": "data collector id",
        }
        job_info = dict(
            databricks_job_id="databricks_job_id",
            databricks_job_name="databricks_job_name",
            databricks_notebook_path="databricks_notebook_path",
            databricks_notebook_source="databricks_notebook_path",
            databricks_notebook_version="123",
        )

        databricks_config = {
            "databricks_workspace_url": "databricks_workspace_url",
            "databricks_workspace_id": "databricks_workspace_id",
            "databricks_cluster_id": "databricks_cluster_id",
            "databricks_token": "databricks_token",
        }

        self._mc_client_mock.side_effect = [
            Mock(),
            Mock(),
            Box(
                dict(
                    create_databricks_notebook_job=dict(
                        databricks=dict(
                            workspace_job_id=job_info["databricks_job_id"],
                            workspace_job_name=job_info["databricks_job_name"],
                            workspace_notebook_path=job_info["databricks_notebook_path"],
                            notebook_source=job_info["databricks_notebook_source"],
                            notebook_version=job_info["databricks_notebook_version"],
                        )
                    )
                )
            ),
            Box(dict(get_projects=dict(projects=[]))),
        ]

        self._service.onboard_databricks_metastore(
            connection_type=DATABRICKS_METASTORE_CONNECTION_TYPE,
            **options,
            **_SAMPLE_BASE_OPTIONS,
        )

        expected_validation_call = Query()
        expected_validation_call.validate_connection_type(
            warehouse_type=DATA_LAKE_WAREHOUSE_TYPE,
            connection_type=DATABRICKS_METASTORE_CONNECTION_TYPE,
        )

        expected_secret_call = Mutation()
        expected_secret_call.create_databricks_secret(
            databricks_config=databricks_config,
            secret_name=DEFAULT_SECRET_NAME,
            scope_name=DEFAULT_SECRET_SCOPE,
            connection_options={"dc_id": "data collector id"},
        )

        expected_notebook_job_call = Mutation()
        expected_notebook_job_call.create_databricks_notebook_job(
            databricks_config=databricks_config,
            connection_options={"dc_id": "data collector id"},
        )

        expected_calls = [
            call(
                expected_validation_call,
                additional_headers={
                    "x-mcd-telemetry-reason": "cli",
                    "x-mcd-telemetry-service": "databricks_onboarding_service",
                    "x-mcd-telemetry-command": "test",
                },
            ),
            call(
                expected_secret_call,
                additional_headers={
                    "x-mcd-telemetry-reason": "cli",
                    "x-mcd-telemetry-service": "databricks_onboarding_service",
                    "x-mcd-telemetry-command": "test",
                },
            ),
            call(
                expected_notebook_job_call,
                additional_headers={
                    "x-mcd-telemetry-reason": "cli",
                    "x-mcd-telemetry-service": "databricks_onboarding_service",
                    "x-mcd-telemetry-command": "test",
                },
            ),
        ]
        self.assertEqual(len(self._mc_client_mock.call_args_list), len(expected_calls))

        for i, expected_call in enumerate(expected_calls):
            # This is the same way that the SDK tests that two calls are the same
            # https://github.com/monte-carlo-data/python-sdk/blob/62f1ab7a8404119da4621b224e77bbbdd5dc938c/tests/test_operations.py#L21
            self.assertEqual(
                str(self._mc_client_mock.call_args_list[i]).strip(),
                str(expected_call).strip(),
            )

    def test_update_databricks_notebook_gql_calls(self):
        options = {"connection_id": "123456789"}
        self._service.update_databricks_notebook(**options)
        expected_mutation = Mutation()
        expected_mutation.update_databricks_notebook(**options)
        expected_call = call(
            expected_mutation,
            additional_headers={
                "x-mcd-telemetry-reason": "cli",
                "x-mcd-telemetry-service": "databricks_onboarding_service",
                "x-mcd-telemetry-command": "test",
            },
        )
        self.assertEqual(
            str(self._mc_client_mock.call_args_list[0]).strip(),
            str(expected_call).strip(),
        )

    def test_get_databricks_job_info_gql_calls(self):
        options = {"connection_id": "123456789"}
        self._mc_client_mock.return_value = Mock(
            get_databricks_metadata_job_info=[
                Mock(
                    workspace_job_id="123456",
                    workspace_job_name="test_job_name",
                    workspace_notebook_path="/some/path",
                    notebook_source="test_source",
                    notebook_version="123",
                )
            ]
        )
        self._service.get_databricks_job_info(**options)
        expected_query = Query()
        expected_query.get_databricks_metadata_job_info(**options)
        expected_call = call(
            expected_query,
            additional_headers={
                "x-mcd-telemetry-reason": "cli",
                "x-mcd-telemetry-service": "databricks_onboarding_service",
                "x-mcd-telemetry-command": "test",
            },
        )
        self.assertEqual(
            str(self._mc_client_mock.call_args_list[0]).strip(),
            str(expected_call).strip(),
        )

    def test_get_current_databricks_notebook_version_gql_calls(self):
        self._service.get_current_databricks_notebook_version()
        expected_query = Query()
        expected_query.get_current_databricks_notebook_version()
        expected_call = call(
            expected_query,
            additional_headers={
                "x-mcd-telemetry-reason": "cli",
                "x-mcd-telemetry-service": "databricks_onboarding_service",
                "x-mcd-telemetry-command": "test",
            },
        )
        self.assertEqual(
            str(self._mc_client_mock.call_args_list[0]).strip(),
            str(expected_call).strip(),
        )

    @patch.object(DatabricksOnboardingService, "onboard")
    def test_onboard_databricks_metastore_sql_warehouse(
        self,
        onboard_mock,
    ):
        options = {
            "databricks_workspace_url": "databricks_workspace_url",
            "databricks_warehouse_id": "databricks_warehouse_id",
            "databricks_workspace_id": "databricks_workspace_id",
            "databricks_token": "databricks_token",
        }

        self._service.onboard_databricks_sql_warehouse(
            connection_type=DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
            **options,
        )

        onboard_mock.assert_called_once_with(
            validation_query=DatabricksSqlWarehouseOnboardingQueries.test_credentials.query,
            validation_response="testDatabricksSqlWarehouseCredentials",
            connection_type=DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
            **options,
        )

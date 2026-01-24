from unittest import TestCase
from unittest.mock import Mock, patch

from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.data_lake.databricks import (
    DatabricksOnboardingService,
)
from montecarlodata.integrations.onboarding.fields import (
    DATABRICKS_METASTORE_SQL_WAREHOUSE_CONNECTION_TYPE,
)
from montecarlodata.queries.onboarding import (
    DatabricksSqlWarehouseOnboardingQueries,
)
from montecarlodata.utils import AwsClientWrapper
from tests.test_common_user import _SAMPLE_CONFIG


class DatabricksMetastoreOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = DatabricksOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
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

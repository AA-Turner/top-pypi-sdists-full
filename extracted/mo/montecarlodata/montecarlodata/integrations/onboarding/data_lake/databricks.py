from typing import Optional

from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort, manage_errors
from montecarlodata.integrations.keys import IntegrationKeyService
from montecarlodata.integrations.onboarding.base import BaseOnboardingService
from montecarlodata.integrations.onboarding.fields import (
    EXPECTED_DATABRICKS_SQL_WAREHOUSE_GQL_RESPONSE_FIELD,
)
from montecarlodata.queries.onboarding import (
    DatabricksSqlWarehouseOnboardingQueries,
)


class DatabricksOnboardingService(BaseOnboardingService):
    def __init__(
        self,
        config: Config,
        command_name: str,
        integration_key_service: Optional[IntegrationKeyService] = None,
        **kwargs,
    ):
        super().__init__(config, command_name=command_name, **kwargs)
        self._integration_key_service = integration_key_service or IntegrationKeyService(
            config=config,
            command_name=command_name,
            user_service=self._user_service,
        )

    @manage_errors
    def create_webhook_key(self, warehouse_name: Optional[str] = None):
        # find Databricks metastore integration in current account
        warehouses = self._user_service.get_warehouses_with_connection_type(
            connection_type="DATABRICKS_METASTORE_SQL_WAREHOUSE",
            warehouse_name=warehouse_name,
        )
        if len(warehouses) == 0:
            message = "No Databricks metastore integrations found"
            if warehouse_name:
                message += f" with name '{warehouse_name}'"
            complain_and_abort(message)
        if len(warehouses) > 1:
            message = "Multiple Databricks metastore integrations found"
            if warehouse_name:
                # technically, we should never have two warehouses with the same name
                message += f" with name '{warehouse_name}'"
            else:
                message += ", please provide an integration name"
            complain_and_abort(message)

        self._integration_key_service.create(
            scope="DatabricksWebhook",
            description="Databricks webhook integration",
            warehouse_ids=[warehouses[0].uuid],
        )

    @manage_errors
    def onboard_databricks_sql_warehouse(self, **kwargs):
        # Onboard
        self.onboard(
            validation_query=DatabricksSqlWarehouseOnboardingQueries.test_credentials.query,
            validation_response=EXPECTED_DATABRICKS_SQL_WAREHOUSE_GQL_RESPONSE_FIELD,
            **kwargs,
        )

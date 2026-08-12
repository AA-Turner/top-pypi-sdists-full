from typing import Optional

from montecarlodata.collector.validation import CollectorValidationService
from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort, manage_errors
from montecarlodata.integrations.keys import IntegrationKeyService
from montecarlodata.integrations.onboarding.base import BaseOnboardingService


class DatabricksOnboardingService(CollectorValidationService, BaseOnboardingService):
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
        """
        Onboard a Databricks SQL warehouse connection by validating and adding a connection.

        Runs all supported v2 validations for the connection type and, if they all pass,
        stores a temp credentials key and adds the connection. If the --skip-validation flag
        is used no validations are run and just a temp key is returned; --validate-only runs
        the validations without adding the connection.
        """
        key = self.test_new_credentials(**kwargs)
        if key:
            self.add_connection(key, **kwargs)

from logging import Logger
from retrying import retry

from azure.mgmt.resource.managedapplications.models import ProvisioningState

from sidecar.apps_configuration_end_tracker import AppsConfigurationEndTracker
from sidecar.azure_clp.azure_clients import AzureClientsManager
from sidecar.azure_clp.azure_status_maintainer import AzureStatusMaintainer
from sidecar.azure_clp.retrying_helpers import retry_if_connection_error
from sidecar.const import DateTimeProvider
from sidecar.health_check.app_health_check_state import AppHealthCheckState
from sidecar.sandbox_start_time_updater import ISandboxStartTimeUpdater
from sidecar.utils import Utils


class AzureSandboxStartTimeUpdater(ISandboxStartTimeUpdater):
    def __init__(self, date_time_provider: DateTimeProvider, logger: Logger,
                 apps_configuration_end_tracker: AppsConfigurationEndTracker,
                 status_maintainer: AzureStatusMaintainer,
                 app_health_check_state: AppHealthCheckState,
                 sandbox_id: str,
                 clients_manager: AzureClientsManager):
        super(AzureSandboxStartTimeUpdater, self).__init__(
            app_health_check_state=app_health_check_state,
            date_time_provider=date_time_provider,
            logger=logger,
            apps_configuration_end_tracker=apps_configuration_end_tracker)
        self._clients_manager = clients_manager
        self._sandbox_id = sandbox_id
        self._status_maintainer = status_maintainer

    def _on_deployment_complete(self):
        self._logger.info('waiting for deployment to succeed')
        
        Utils.retry_on_exception(func=lambda: self._throw_if_not_succeeded(),
                                 timeout_in_sec=20*1000, interval_in_sec=15,
                                 logger=self._logger, log_every_n_attempts=4,
                                 logger_msg="waiting for deployment to succeed")

        self._logger.info('deployment succeeded!')

        self._status_maintainer.update_sandbox_start_status(self._date_time_provider.get_current_time_utc())

    @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_exception=retry_if_connection_error)
    def _throw_if_not_succeeded(self):
        deployments = list(
            self._clients_manager.resource_client.deployments.list_by_resource_group(
                resource_group_name=self._sandbox_id,
                timeout=20))
        deployment = next((x for x in deployments if x.name.startswith('qs_')), None)

        if not deployment or deployment.properties.provisioning_state != ProvisioningState.succeeded.value:
            raise Exception('not succeeded yet')

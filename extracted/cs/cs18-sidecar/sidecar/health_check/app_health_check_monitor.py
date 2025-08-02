from logging import Logger

import threading
from typing import List

from sidecar.app_instance_identifier import AppInstanceIdentifier
from sidecar.app_services.app_service import AppService
from sidecar.apps_configuration_end_tracker import AppsConfigurationEndTracker, AppConfigurationEndStatus
from sidecar.const import AppNetworkStatus, Const
from sidecar.health_check.app_health_check_configuration import AppHealthCheckConfiguration
from sidecar.health_check.app_health_check_state import AppHealthCheckState
from sidecar.health_check.health_check_executor import HealthCheckExecutor
from sidecar.health_check.health_check_preparer import HealthCheckPreparer
from sidecar.model.objects import SidecarApplication
from sidecar.sandbox_error import SandboxError
from sidecar.utils import CallsLogger


class AppHealthCheckMonitor:
    def __init__(self,
                 apps: List[SidecarApplication],
                 executor: HealthCheckExecutor,
                 preparer: HealthCheckPreparer,
                 app_health_check_state: AppHealthCheckState,
                 app_service: AppService,
                 health_check_configuration: AppHealthCheckConfiguration,
                 apps_configuration_end_tracker: AppsConfigurationEndTracker,
                 logger: Logger,
                 internet_facing: bool = True):
        self._apps = apps
        self._health_check_configuration = health_check_configuration
        self._apps_configuration_end_tracker = apps_configuration_end_tracker
        self._app_health_check_state = app_health_check_state
        self._preparer = preparer
        self._executor = executor
        self._app_service = app_service
        self._logger = logger
        self.internet_facing = internet_facing
        self._lock = threading.RLock()

    @CallsLogger.wrap
    def start(self, identifier: AppInstanceIdentifier):
        try:
            app_configuration_status = self._get_app_configuration_status(identifier)

            if app_configuration_status \
                    and app_configuration_status.is_ended_with_status(AppConfigurationEndStatus.ERROR):
                self._update_status(app_name=identifier.name, status=AppNetworkStatus.ERROR)

            if app_configuration_status \
                    and app_configuration_status.is_ended_with_status(AppConfigurationEndStatus.COMPLETED):
                self._start(identifier=identifier)
            else:
                self._logger.info("skipping network health-check. identifier: '{}', status: '{}'".format(
                    identifier,
                    str(app_configuration_status)))
        except Exception as ex:
            self._logger.exception("error - identifier: '{}'. {}".format(identifier, str(ex)))
            raise

    def _get_app_configuration_status(self, identifier: AppInstanceIdentifier):
        app_configuration_statuses = self._apps_configuration_end_tracker \
            .get_app_configuration_statuses(identifier.name)
        if len(app_configuration_statuses) != 1:
            raise Exception("Status for app '{}' was no found".format(identifier.name))
        return app_configuration_statuses[identifier.name]

    def _start(self, identifier: AppInstanceIdentifier):
        succeed = self._test_private_network(identifier=identifier)

        if succeed:
            check_public = self._app_service.can_access_from_public_address(identifier=identifier) and \
                           any([app for app in self._apps if app.name == identifier.name and app.has_public_access])
            if check_public:
                self._logger.info(f"Starting public health check on {identifier.name}")
                self._test_public_network(identifier=identifier)
            else:
                self._update_status(app_name=identifier.name, status=AppNetworkStatus.COMPLETED)
        else:
            self._update_status(app_name=identifier.name, status=AppNetworkStatus.ERROR)
            self._add_private_healthcheck_error(app_name=identifier.name)

    def _test_public_network(self, identifier: AppInstanceIdentifier):
        timeout = self._health_check_configuration.get_configuration(identifier.name).timeout_sec

        self._update_status(app_name=identifier.name, status=AppNetworkStatus.TESTING_PUBLIC_NETWORK)

        try:
            address = self._app_service.get_sandbox_gateway_address(app_name=identifier.name,
                                                                    infra_id=identifier.infra_id,
                                                                    address_read_timeout=timeout,
                                                                    internet_facing=self.internet_facing)

            self._logger.info(f"Start _test_sandbox_gateway_network with dns_name = {address}")

            dns_check = self._health_check_dns_names(identifier=identifier,
                                                     dns_name=address)
            if dns_check:
                status = AppNetworkStatus.COMPLETED
            else:
                status = AppNetworkStatus.ERROR
                self._add_public_healthcheck_error(app_name=identifier.name)

            self._update_status(app_name=identifier.name, status=status)
        except Exception as ex:
            self._logger.exception(ex)

    def _test_private_network(self, identifier: AppInstanceIdentifier) -> bool:
        private_dns_name = self._app_service.get_private_dns_name_by_app_name(app_name=identifier.name,
                                                                              infra_id=identifier.infra_id)

        # app may not be accessible via private dns (no internal ports)
        if not private_dns_name:
            return True

        self._update_status(app_name=identifier.name, status=AppNetworkStatus.TESTING_PRIVATE_NETWORK)
        return self._health_check_dns_names(identifier=identifier,
                                            dns_name=private_dns_name)

    def _update_status(self, app_name: str, status: str):
        with self._lock:
            self._app_service.update_network_status(app_name=app_name, status=status)
            self._app_health_check_state.set_app_state(app_name=app_name, status=status)

    def _add_private_healthcheck_error(self, app_name: str):
        self._app_service.add_error(
            app_name=app_name,
            error=SandboxError.PrivateHealthcheckFailed(app_name=app_name))

    def _add_public_healthcheck_error(self, app_name: str):
        self._app_service.add_error(
            app_name=app_name,
            error=SandboxError.PublicHealthcheckFailed(app_name=app_name))

    def _health_check_dns_names(self,
                                identifier: AppInstanceIdentifier,
                                dns_name: str) -> bool:
        cmd = self._preparer.prepare(app_name=identifier.name,
                                     address=dns_name)

        if not cmd:
            return True

        return self._executor.start(identifier=identifier, cmd=cmd, address=dns_name)

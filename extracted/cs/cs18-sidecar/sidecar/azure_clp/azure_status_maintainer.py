import threading
from contextlib import contextmanager
from datetime import datetime
from typing import List

from retrying import retry

from sidecar.azure_clp.data_store_service import DataStoreService
from sidecar.azure_clp.retrying_helpers import retry_if_connection_error, retry_if_result_none_or_empty
from sidecar.const import Const
from sidecar.status_maintainer import StatusMaintainer, IngressRouteRequest
from logging import Logger
from sidecar.sandbox_error import SandboxError


class AzureStatusMaintainer(StatusMaintainer):
    ROOT_SPEC_KEY = "spec"
    EXPECTED_APPS_KEY = "expected_apps"
    ROOT_APPS_KEY = "apps"
    INSTANCES_KEY = "instances"
    ROOT_SERVICES_KEY = "services"
    ROOT_LOGICAL_APPS_KEY = "logical-apps"
    ROOT_INGRESS_ROUTES_KEY = "ingress_routes"

    def __init__(self, data_store_service: DataStoreService, sandbox_id: str, logger: Logger):
        super().__init__(logger)
        self._data_store_service = data_store_service
        self._sandbox_id = sandbox_id
        self._apps_lock = threading.RLock()
        self._logical_apps_lock = threading.RLock()

        self._cached_realtime_apps = None
        self._cached_realtime_services = None
        self._cached_spec = None
        self._cached_logical_apps = None
        self._cached_sandbox_errors = None

        self._cache_sandbox_data()

    def _cache_sandbox_data(self):
        sandbox_document = self._get_sandbox_document_with_retries()
        if not sandbox_document:
            raise Exception("Failed to get sandbox data from cosmos_db after 5 retries")

        self._cached_realtime_apps = sandbox_document[self.ROOT_APPS_KEY]
        self._cached_realtime_services = sandbox_document[self.ROOT_SERVICES_KEY]
        self._cached_spec = sandbox_document[self.ROOT_SPEC_KEY]
        self._cached_logical_apps = sandbox_document.get(self.ROOT_LOGICAL_APPS_KEY, {})
        self._cached_sandbox_errors = sandbox_document.get(Const.SANDBOX_ERRORS)
        self._cached_ingress_routes = sandbox_document.get(self.ROOT_INGRESS_ROUTES_KEY, {})

    @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_result=retry_if_result_none_or_empty,
           retry_on_exception=retry_if_connection_error)
    def _get_sandbox_document_with_retries(self):
        return self._data_store_service.find_data_by_id(data_id=self._sandbox_id)

    def _construct_instances_key_path(self, instance_logical_id):
        return '{apps_key}.{instance_logical_id}.{instances_key}'.format(apps_key=self.ROOT_APPS_KEY,
                                                                         instance_logical_id=instance_logical_id,
                                                                         instances_key=self.INSTANCES_KEY)

    def update_qualiy_status(self, status: str):
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=status,
                                             column_name=Const.QUALIY_STATUS)

    def update_logical_app_artifacts_status(self, app_name: str, status: str):
        with self._modify_logical_apps():
            self._cached_logical_apps[app_name][Const.ARTIFACTS_INTO_SIDECAR_STATUS] = status

    def update_logical_app_healthcheck_status(self, app_name: str, status: str):
        with self._modify_logical_apps():
            self._cached_logical_apps[app_name][Const.HEALTH_CHECK_STATUS] = status

    def add_logical_app_error(self, app_name: str, error: SandboxError):
        with self._modify_logical_apps():
            self._cached_logical_apps[app_name][Const.APP_ERRORS].append(error.to_dict())

    def update_app_instance_healthcheck_status(self, instance_logical_id, instance_id, app_name, status):
        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details[Const.APP_STATUS_TAG] = status

    def update_app_instance_configuration_status(self, instance_logical_id, instance_id, app_name, status):
        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details[Const.CONFIGURATION_STATUS] = status

    def update_app_instance_artifacts_status(self, instance_logical_id, instance_id, app_name, status):
        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details[Const.ARTIFACTS_INTO_INSTANCE_STATUS] = status

    def update_app_instance_outputs(self, instance_logical_id, instance_id, app_name, outputs: {}):
        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details["outputs"] = outputs

    def add_app_instance_error(self, instance_logical_id, instance_id, app_name, error: SandboxError):
        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details[Const.APP_INSTANCE_ERRORS].append(error.to_dict())

    @contextmanager
    def _modify_logical_apps(self):
        with self._logical_apps_lock:
            yield  # executes the code inside the "with self._modify_logical_apps():"
            self._data_store_service.update_data(data_id=self._sandbox_id,
                                                 data=self._cached_logical_apps,
                                                 column_name=self.ROOT_LOGICAL_APPS_KEY)

    @contextmanager
    def _modify_apps(self):
        with self._apps_lock:
            yield  # executes the code inside the "with self._modify_apps():"
            self._data_store_service.update_data(data_id=self._sandbox_id,
                                                 data=self._cached_realtime_apps,
                                                 column_name=self.ROOT_APPS_KEY)

    def get_or_add_instance_under_logical_id(self, instance_id: str, instance_logical_id: str) -> dict:
        instances = self._cached_realtime_apps[instance_logical_id][self.INSTANCES_KEY]
        return instances.setdefault(instance_id, {"apps": {}})

    def get_or_add_app_under_instance(self, instance: dict, app_name: str) -> dict:
        return instance['apps'].setdefault(
            app_name,
            {
                Const.ARTIFACTS_INTO_INSTANCE_STATUS: None,
                Const.CONFIGURATION_STATUS: None,
                Const.APP_STATUS_TAG: None,
                Const.APP_INSTANCE_ERRORS: []
            })

    def get_app_names_on_instance(self, instance_logical_id: str) -> List[str]:
        return self._cached_spec[self.EXPECTED_APPS_KEY][instance_logical_id]["apps"]

    def update_sandbox_end_status(self, sandbox_deployment_end_status: str):
        # assume that DB-level lock is good enough here
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=sandbox_deployment_end_status,
                                             column_name=Const.SANDBOX_DEPLOYMENT_END_STATUS)

        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=sandbox_deployment_end_status,
                                             column_name=Const.SANDBOX_DEPLOYMENT_END_STATUS_v2)

    def update_sandbox_start_status(self, sandbox_start_time: datetime):
        # assume that DB-level lock is good enough here

        # todo gil:add update data bulk
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=str(sandbox_start_time),
                                             column_name=Const.SANDBOX_START_TIME)

        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=str(sandbox_start_time),
                                             column_name=Const.SANDBOX_START_TIME_v2)

    def update_service_status(self, name: str, status: str):
        self._cached_realtime_services[name]["status"] = status
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=self._cached_realtime_services,
                                             column_name=self.ROOT_SERVICES_KEY)

    def add_sandbox_error(self, error: SandboxError):
        self._cached_sandbox_errors.append(error.to_dict())
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=self._cached_sandbox_errors,
                                             column_name=Const.SANDBOX_ERRORS)

    def update_service_outputs(self, name: str, outputs: {}):
        self._cached_realtime_services[name]["outputs"] = outputs
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=self._cached_realtime_services,
                                             column_name=self.ROOT_SERVICES_KEY)

    def get_service_deployment_outputs(self, service_name: str) -> {}:
        service = self._cached_realtime_services.get(service_name, None)
        if service:
            return service.get("outputs", {})
        raise Exception(f"could not find service with name '{service_name}'")

    def get_app_deployment_outputs(self, app_name: str) -> {}:
        app_details = self._get_first_application(app_name)
        if app_details:
            return app_details.get('outputs', {})
        raise Exception(f"could not find application with name '{app_name}'")

    def _get_first_application(self, app_name: str):
        for logical_id, logical_details in self._cached_realtime_apps.items():
            for instance_id, instance_json in logical_details[self.INSTANCES_KEY].items():
                for name, app_details in instance_json['apps'].items():
                    if name == app_name:
                        return app_details
        return None

    def get_internal_ports_for_app(self, app_name: str) -> List[str]:
        # find app's internal ports don't care on which instance logical id
        for logical_id, logical_details in self._cached_spec[self.EXPECTED_APPS_KEY].items():
            if app_name in logical_details[Const.INTERNAL_PORTS]:
                return logical_details[Const.INTERNAL_PORTS][app_name]
        return []

    def get_ingress_routes(self) -> List[IngressRouteRequest]:
        items = []
        for ingress_route in self._cached_ingress_routes:
            items.append(IngressRouteRequest(
                listener_port=ingress_route['listener_port'],
                path=ingress_route['path'],
                host=ingress_route['host'],
                app_name=ingress_route['app_name'],
                app_port=ingress_route['app_port'],
                color=ingress_route['color']))
        return items

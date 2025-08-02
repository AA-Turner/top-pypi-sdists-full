import threading
from contextlib import contextmanager
from typing import List, Callable

from sidecar.app_instance_service import StaleAppInstanceException
from sidecar.const import Const, get_app_selector
from sidecar.kub_api_pod_reader import KubApiPodReader
from sidecar.status_maintainer import StatusMaintainer
from sidecar.kub_api_service import IKubApiService
from sidecar.sandbox_error import SandboxError
from logging import Logger
import json


class KubStatusMaintainer(StatusMaintainer):

    def __init__(self, logger: Logger, kub_api_service: IKubApiService):
        super().__init__(logger)
        self._apps_lock = threading.RLock()
        self._services_lock = threading.RLock()
        self.kub_api_service = kub_api_service

    # annotation is like an item in a dynamoDB
    def update_annotation_in_namespace(self, key: str, value: str):
        annotation = {key: value}
        self.kub_api_service.update_namespace(annotation)

    def update_qualiy_status(self, status: str):
        self.update_annotation_in_namespace(Const.QUALIY_STATUS, status)

    def add_sandbox_error(self, error: SandboxError):
        try:
            errors_as_json_str = self.kub_api_service.get_annotation(Const.SANDBOX_ERRORS)
            errors = self._json_str_to_errors(errors_as_json_str)
            errors.append(error)
            errors_as_json_str = self._errors_to_json_str(errors)
            self.update_annotation_in_namespace(Const.SANDBOX_ERRORS, errors_as_json_str)

        except:
            self._logger.exception('Failed to update sandbox errors')

    def update_app_instance_healthcheck_status(self, app_name: str, container_id: str, status: str):
        with self._modify_apps(app_name=app_name, container_id=container_id) as data:
            data['status'] = status

    def update_app_instance_configuration_status(self, app_name: str, container_id: str, status: str):
        with self._modify_apps(app_name=app_name, container_id=container_id) as data:
            data['configuration-status'] = status

    def update_app_instance_artifacts_status(self, app_name: str, container_id: str, status: str):
        with self._modify_apps(app_name=app_name, container_id=container_id) as data:
            data['artifacts-status'] = status

    def update_app_instance_outputs(self, app_name: str, container_id: str, outputs: dict):
        with self._modify_apps(app_name=app_name, container_id=container_id) as data:
            data['outputs'] = outputs

    def add_app_instance_error(self, app_name: str, container_id: str, error: SandboxError):
        with self._modify_apps(app_name=app_name, container_id=container_id) as data:
            data.setdefault('errors', []).append(error.to_dict())

    @contextmanager
    def _modify_apps(self, app_name: str, container_id: str,):
        with self._apps_lock:
            pod_json = self.kub_api_service.try_get_pod_json_by_container_id(container_id=container_id)
            # should update status only for a "live" instance
            if not self._is_pod_live_in_sandbox(pod_json):
                raise StaleAppInstanceException(f"cannot update '{app_name}' since the app "
                                                f"instance is no longer a part of the sandbox. infra id: {container_id}")
            apps_info_json = KubApiPodReader.get_apps_info_json(pod_json)

            yield apps_info_json[app_name]  # executes the code inside the "with self._modify_apps():"

            annotations = {Const.APPS: json.dumps(apps_info_json)}
            self.kub_api_service.update_pod(KubApiPodReader.get_pod_name(pod_json), annotations)

    def update_logical_app_healthcheck_status(self, app_name: str, status: str):
        def healthcheck_status_updater(annotations: dict):
            annotations[Const.HEALTH_CHECK_STATUS] = status

        self._modify_logical_apps(app_name=app_name,
                                  modifier=healthcheck_status_updater)

    def update_logical_app_artifacts_status(self, app_name: str, status: str):
        def artifacts_status_updater(annotations: dict):
            annotations[Const.ARTIFACTS_INTO_SIDECAR_STATUS] = status

        self._modify_logical_apps(app_name=app_name,
                                  modifier=artifacts_status_updater)

    def add_logical_app_error(self, app_name: str, error: SandboxError):
        def add_error_modifier(annotations: dict):
            errors = self._json_str_to_errors(annotations[Const.APP_ERRORS])
            errors.append(error)
            annotations[Const.APP_ERRORS] = self._errors_to_json_str(errors)

        self._modify_logical_apps(app_name=app_name,
                                  modifier=add_error_modifier)

    def _modify_logical_apps(self, app_name: str, modifier: Callable[[dict], None]):
        with self._services_lock:
            # TODO: rethink it !!! not so good to mark both services when only one got checked
            app_services = [service for service in self.kub_api_service.get_all_services()
                            if service['spec']['selector'] == {**{get_app_selector(app_name): app_name}}]

            for app_service in app_services:
                annotations = app_service['metadata']['annotations']

                modifier(annotations)

                self.kub_api_service.update_service(
                    name=app_service['metadata']['name'],
                    data={'metadata': {'annotations': annotations}}
                )

    @staticmethod
    def _is_pod_live_in_sandbox(pod_json) -> bool:
        return True if pod_json and \
                       not KubApiPodReader.is_pod_ended(pod_json) and \
                       not KubApiPodReader.is_pod_terminating(pod_json) else False

    @staticmethod
    def _json_str_to_errors(errors_as_json_str: str) -> List[SandboxError]:
        errors_as_json = json.loads(errors_as_json_str)
        errors = [SandboxError.from_dict(d) for d in errors_as_json or []]
        return errors

    @staticmethod
    def _errors_to_json_str(errors: List[SandboxError]) -> str:
        errors_as_json = [error.to_dict() for error in errors]
        errors_as_json_str = json.dumps(errors_as_json)
        return errors_as_json_str

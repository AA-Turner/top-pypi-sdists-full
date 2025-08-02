import json
import threading
from logging import Logger
from typing import List

from sidecar.app_instance_identifier import AppInstanceIdentifier
from sidecar.const import Const
from sidecar.kub_api_pod_reader import KubApiPodReader
from sidecar.kub_api_service import IKubApiService
from sidecar.app_instance_service import IAppInstanceService
from sidecar.kub_status_maintainer import KubStatusMaintainer
from sidecar.sandbox_error import SandboxError


class KubAppInstanceService(IAppInstanceService):

    def __init__(self, logger: Logger, kub_api_service: IKubApiService, k8s_status_maintainer: KubStatusMaintainer):
        super().__init__(logger)
        self.k8s_status_maintainer = k8s_status_maintainer
        self.kub_api_service = kub_api_service

    def get_public_address(self, app_instance_identifier: AppInstanceIdentifier) -> str:
        return ''

    def update_status_if_not_stale(self, app_instance_identifier: AppInstanceIdentifier, status: str):
        self.k8s_status_maintainer.update_app_instance_healthcheck_status(
            app_name=app_instance_identifier.name,
            container_id=app_instance_identifier.infra_id,
            status=status)

    def update_artifacts_status(self, app_instance_identifier: AppInstanceIdentifier, status: str):
        self.k8s_status_maintainer.update_app_instance_artifacts_status(
            app_name=app_instance_identifier.name,
            container_id=app_instance_identifier.infra_id,
            status=status)

    def update_configuration_status(self, app_instance_identifier: AppInstanceIdentifier, status: str):
        self.k8s_status_maintainer.update_app_instance_configuration_status(
            app_name=app_instance_identifier.name,
            container_id=app_instance_identifier.infra_id,
            status=status)

    def update_deployment_outputs(self, app_instance_identifier: AppInstanceIdentifier, outputs: {}):
        self.k8s_status_maintainer.update_app_instance_outputs(
            app_name=app_instance_identifier.name,
            container_id=app_instance_identifier.infra_id,
            outputs=outputs)

    def add_error(self, app_instance_identifier: AppInstanceIdentifier, error: SandboxError):
        self.k8s_status_maintainer.add_app_instance_error(
            app_name=app_instance_identifier.name,
            container_id=app_instance_identifier.infra_id,
            error=error)

    def check_which_exist(self, identifiers: List[AppInstanceIdentifier]) -> List[AppInstanceIdentifier]:
        # infra_id is container id and there is no way to query kub api by container ids, so getting all pods
        all_pods = self._get_all_live_app_pods_in_sandbox()
        existing_identifiers = [app_instance_identifier
                                for pod_json in all_pods
                                for app_instance_identifier in self._create_app_instance_identifiers(pod_json)
                                if app_instance_identifier in identifiers]
        return existing_identifiers

    def get_deployment_outputs(self, app_name: str) -> {}:
        all_pods = self._get_all_live_app_pods_in_sandbox()
        for pod_json in all_pods:
            apps_info_json = KubApiPodReader.get_apps_info_json(pod_json)
            if app_name in apps_info_json:
                return apps_info_json[app_name].get('outputs', {})

        raise Exception(f"could not find application with name '{app_name}'")

    def is_qualiy_off(self) -> bool:
        return True

    def _get_all_live_app_pods_in_sandbox(self):
        pods = self.kub_api_service.get_all_pods_list(include_infra=False, include_ended=False,
                                                      include_terminating=False)
        # only applications pods
        return [p for p in pods if not KubApiPodReader.is_services_related_pod(p)]

    def _create_app_instance_identifiers(self, pod_json: dict()) -> List[AppInstanceIdentifier]:
        apps_info_json = KubApiPodReader.get_apps_info_json(pod_json)
        return self._create_identifiers_from_pod_apps_info(pod_json, apps_info_json)

    @staticmethod
    def _create_identifiers_from_pod_apps_info(pod_json: dict(), apps_info_json: dict()) \
            -> List[AppInstanceIdentifier]:
        identifiers = []
        for app_name in apps_info_json:
            container_id = KubApiPodReader.safely_get_container_id_for_app(app_name, pod_json)
            # handling the possibility that container id is not available in the pod (maybe when pod in pending phase)
            if container_id:
                identifiers.append(AppInstanceIdentifier(name=app_name, infra_id=container_id))
        return identifiers
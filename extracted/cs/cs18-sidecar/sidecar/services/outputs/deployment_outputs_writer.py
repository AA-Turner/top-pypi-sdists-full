import json
import threading
from logging import Logger
from typing import List

from sidecar.app_instance_identifier import AppInstanceIdentifier
from sidecar.app_instance_service import IAppInstanceService
from sidecar.model.objects import ISidecarConfiguration
from sidecar.services.deployment_outputs_converter import DeploymentOutputsConverter
from sidecar.services.service_updater import IServiceUpdater


class DeploymentOutputsWriter:

    def __init__(self, logger: Logger,
                 app_instance_service: IAppInstanceService,
                 service_updater: IServiceUpdater,
                 config: ISidecarConfiguration):
        self._service_updater = service_updater
        self._app_instance_service = app_instance_service
        self._config = config
        self._logger = logger
        self._lock = threading.RLock()

    def save_application_outputs(self, app_identifier: AppInstanceIdentifier, outputs: str):
        app_name = app_identifier.name
        app_instance_id = app_identifier.infra_id
        try:
            deployment_output = DeploymentOutputsConverter.convert_from_configuration_script(outputs)
        except Exception as exc:
            self._logger.exception(f"application '{app_instance_id}/{app_name}' "
                                   f"deployment output is not valid:\n{outputs}")
            raise exc

        declared_outputs = self._get_application_declared_outputs(app_name)
        self._filter_redundant_deployment_outputs(deployment_output, declared_outputs)

        with self._lock:
            self._app_instance_service.update_deployment_outputs(app_identifier,
                                                                 deployment_output)

    def save_service_outputs(self, service_name: str, output_json: {}):
        try:
            deployment_output = DeploymentOutputsConverter.convert_from_terraform_outputs(output_json)
        except Exception:
            output_str = json.dumps(output_json)
            err = f"service '{service_name}' deployment output is not valid:\n{output_str}"
            self._logger.exception(err)
            raise Exception(err)

        declared_outputs = self._get_service_declared_outputs(service_name)
        self._filter_redundant_deployment_outputs(deployment_output, declared_outputs)
        with self._lock:
            self._service_updater.update_deployment_outputs(service_name, deployment_output)

    @staticmethod
    def _filter_redundant_deployment_outputs(deployment_output: dict, declared_outputs: List[str]):
        deployment_output_names = list(deployment_output.keys())
        for deployment_output_name in deployment_output_names:
            if deployment_output_name not in declared_outputs:
                deployment_output.pop(deployment_output_name, None)

    def _get_service_declared_outputs(self, service_name: str) -> List[str]:
        outputs = next((s.outputs for s in self._config.services if s.name == service_name))
        if outputs:
            return outputs
        return []

    def _get_application_declared_outputs(self, application_name: str) -> List[str]:
        outputs = next((a.outputs for a in self._config.apps if a.name == application_name))
        if outputs:
            return outputs
        return []

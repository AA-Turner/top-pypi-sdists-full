from logging import Logger
from typing import List, Dict

from sidecar.app_instance_service import IAppInstanceService
from sidecar.model.objects import ISidecarConfiguration
from sidecar.services.deployment_outputs_converter import OutputValueToStringConverterFactory
from sidecar.services.input_value_resolver import InputValueResolver
from sidecar.services.service_updater import IServiceUpdater


class DeploymentOutputsResolver(InputValueResolver):
    prefix = 'outputs.'

    def __init__(self, logger: Logger,
                 config: ISidecarConfiguration,
                 app_instance_service: IAppInstanceService,
                 service_updater: IServiceUpdater):
        self._config = config
        self._logger = logger
        self._output_value_to_str_factory = OutputValueToStringConverterFactory()
        self._service_updater = service_updater
        self._app_instance_service = app_instance_service

    def resolve(self, value: str):
        dic = self._get_deployment_outputs_dic([value])
        return dic[value]

    def can_resolve(self, value: str) -> bool:
        return value.lower().startswith(self.prefix)

    def _get_deployment_outputs_dic(self, outputs: List[str]) -> Dict[str, str]:
        entity_name_outputs_map = {}
        res = {}
        for output in outputs:
            try:
                entity_name, output_name = self._parse_output_name(output)
                entity_outputs = entity_name_outputs_map.get(entity_name, None)
                if entity_outputs is None:
                    entity_outputs = self._get_outputs(entity_name)
                    entity_name_outputs_map[entity_name] = entity_outputs

                if output_name in entity_outputs:
                    value_json = entity_outputs.get(output_name)
                    res[output] = self._output_value_to_str_factory.convert_to_str(value_json['type'],
                                                                                   value_json['value'])
                else:
                    res[output] = 'Output value not found'
            except Exception as ex:
                self._logger.exception("failed to resolve output: {output}\n{exc}".format(output=output, exc=ex))
                raise ex
        return res

    def _get_outputs(self, entity_name: str) -> {}:
        if next((service for service in self._config.services if service.name == entity_name), None):
            return self._service_updater.get_deployment_outputs(entity_name)

        if next((app for app in self._config.apps if app.name == entity_name), None):
            return self._app_instance_service.get_deployment_outputs(entity_name)
        else:
            raise Exception(f"could not find application/service with name '{entity_name}'")

    @staticmethod
    def _parse_output_name(output: str):
        try:
            split = output.split('.')
            entity_name = split[1]
            output_name = split[2]
            return entity_name, output_name
        except IndexError:
            raise Exception(f"output '{output}' cannot be resolved")

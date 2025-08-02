import json
from logging import Logger

from sidecar.app_instance_identifier import AppInstanceIdentifier
from sidecar.app_instance_identifier_creator import IAppInstanceIdentifierCreator
from sidecar.kub_api_pod_reader import KubApiPodReader
from sidecar.kub_api_service import IKubApiService
from sidecar.utils import Utils


class KubAppInstanceIdentifierCreator(IAppInstanceIdentifierCreator):
    def __init__(self, kub_api_service: IKubApiService, logger: Logger) -> None:
        super().__init__(logger=logger)
        self._kub_api_service = kub_api_service

    def create(self, app_name: str, instance_id: str) -> AppInstanceIdentifier:

        container_id = Utils.retry_on_exception(
            func=lambda: self._try_get_container_id(app_name=app_name, instance_id=instance_id),
            logger=self._logger,
            logger_msg=f"getting container id for app '{app_name}' in pod '{instance_id}'",
            timeout_in_sec=10,
            interval_in_sec=1)
        return AppInstanceIdentifier(name=app_name, infra_id=container_id)

    def _try_get_container_id(self, app_name: str, instance_id: str) -> str:
        # using pod name as instance id and not uid because it can easily be sent from the pod ($HOSTNAME) and
        # because it is more efficient to query by.
        # the advantage of uid is that it is unique over time whereas the pod name isn't, but it should be ok since we
        # only use the pod name to find the pod momentarily and then proceed to identify the instance by container id
        pod_json = self._kub_api_service.try_get_pod_json_by_pod_name(pod_name=instance_id)
        if not pod_json:
            raise Exception("pod with name '{NAME}' not found".format(NAME=instance_id))

        # container id is enough as infra identifier because it is supposed to be unique (across space and time),
        # meaning that even if there are multiple instances of the same app on different pods -
        # they should have different container ids
        container_id = KubApiPodReader.safely_get_container_id_for_app(app_name=app_name, pod=pod_json)
        if not container_id:
            raise Exception("container id for app '{APP}' not found on pod '{NAME}':\nPod Json: {POD_JSON}"
                            .format(APP=app_name,
                                    NAME=KubApiPodReader.get_pod_name(pod_json),
                                    POD_JSON=json.dumps(pod_json, indent=4)))
        return container_id

from time import sleep
from typing import Dict, List, Set

from _qwak_proto.qwak.audience.v1.audience_pb2 import AudienceRoutesEntry
from _qwak_proto.qwak.deployment.deployment_pb2 import (
    DeploymentHostingServiceType,
    EnvironmentDeploymentDetailsMessage,
    EnvironmentUndeploymentMessage,
    ModelDeploymentStatus,
    TrafficConfig,
)
from _qwak_proto.qwak.ecosystem.v0.ecosystem_pb2 import EnvironmentDetails
from qwak.clients.administration.eco_system.client import EcosystemClient
from qwak.clients.deployment.client import DeploymentManagementClient
from qwak.exceptions import QwakException
from qwak.tools.logger.logger import get_qwak_logger

from qwak_sdk.commands.models.deployments.deploy._logic.deploy_config import (
    DeployConfig,
)
from qwak_sdk.tools.utils import qwak_spinner

NO_DEPLOYED_VARIATIONS_ERROR_MSG = (
    "There are currently no deployed variations for model {model_id} in {env_name}"
)
UNDEPLOY_ERROR_MSG = "Environment {environment_id} failed with status: {status}"
logger = get_qwak_logger()

FAILED_UNDEPLOYMENT_STATUS = ["FAILED_UNDEPLOYMENT"]
SUCCESSFUL_UNDEPLOYMENT_STATUS = ["SUCCESSFUL_UNDEPLOYMENT"]
END_UNDEPLOYMENT_STATUSES = SUCCESSFUL_UNDEPLOYMENT_STATUS + FAILED_UNDEPLOYMENT_STATUS
TIME_TO_WAIT_FOR_UNDEPLOYMENT_POLLING = 5


def get_deployed_variation_name(existing_variations_names: Set[str]) -> str:
    return list(existing_variations_names)[0]


def get_environment_undeploy_message(
    audiences: List[AudienceRoutesEntry],
    existing_variations_names: Set[str],
    fallback_variation: str,
    model_id: str,
    model_uuid: str,
    variation_name: str,
):
    if not variation_name and len(existing_variations_names) == 1:
        variation_name = get_deployed_variation_name(
            existing_variations_names=existing_variations_names
        )

    return EnvironmentUndeploymentMessage(
        model_id=model_id,
        model_uuid=model_uuid,
        hosting_service_type=DeploymentHostingServiceType.KUBE_DEPLOYMENT,
        traffic_config=TrafficConfig(
            selected_variation_name=variation_name,
            audience_routes_entries=audiences,
            fallback_variation=fallback_variation,
        ),
    )


def get_env_to_undeploy_message(
    audiences: List[AudienceRoutesEntry],
    model_uuid: str,
    env_id_to_deployment_details: Dict[str, EnvironmentDeploymentDetailsMessage],
    env_name_to_env_details: Dict[str, EnvironmentDetails],
    model_id: str,
    variation_name: str,
    fallback_variation: str,
) -> Dict[str, EnvironmentUndeploymentMessage]:
    env_undeployment_requests = dict()
    errors = []
    for env_name, env_details in env_name_to_env_details.items():
        env_deployments_details_message = env_id_to_deployment_details.get(
            env_details.id
        )
        if not env_deployments_details_message:
            errors.append(
                NO_DEPLOYED_VARIATIONS_ERROR_MSG.format(
                    model_id=model_id, env_name=env_name
                )
            )
            continue

        env_deployments_details = env_deployments_details_message.deployments_details
        existing_variations_names = {
            deployment.variation.name for deployment in env_deployments_details
        }
        try:
            env_undeployment_requests[
                env_details.id
            ] = get_environment_undeploy_message(
                audiences,
                existing_variations_names,
                fallback_variation,
                model_id,
                model_uuid,
                variation_name,
            )
        except QwakException as e:
            errors.append(e.message)
    if errors:
        raise QwakException("\n".join(errors))
    return env_undeployment_requests


def undeploy(
    model_id: str,
    config: DeployConfig,
    model_uuid: str = "",
    sync: bool = False,
):
    deployment_client = DeploymentManagementClient()
    ecosystem_client = EcosystemClient()
    audiences: List[AudienceRoutesEntry] = [
        audience.to_audience_route_entry(index)
        for index, audience in enumerate(config.realtime.audiences)
    ]

    if not model_uuid:
        raise QwakException("missing argument model uuid")

    environments_names = config.realtime.environments if config.realtime else []

    deployment_details = deployment_client.get_deployment_details(model_id, model_uuid)
    env_id_to_deployment_details = dict(
        deployment_details.environment_to_deployment_details
    )
    env_name_to_env_details = ecosystem_client.get_environments_names_to_details(
        environments_names
    )

    env_undeployment_requests = get_env_to_undeploy_message(
        audiences,
        model_uuid,
        env_id_to_deployment_details,
        env_name_to_env_details,
        model_id,
        config.realtime.variation_name,
        config.realtime.fallback_variation,
    )

    environment_to_deployment_id = {}
    if sync:
        environment_to_deployment_id = __get_environment_to_deployment_id(
            deployment_client, model_id, model_uuid, env_undeployment_requests
        )

    undeployment_response = deployment_client.undeploy_model(
        model_id=model_id,
        model_uuid=model_uuid,
        env_undeployment_requests=env_undeployment_requests,
    )

    if sync:
        __sync_undeploy(
            environment_to_deployment_id=environment_to_deployment_id,
            model_id=model_id,
            deployment_client=deployment_client,
        )
    logger.info(
        f"Current status is {ModelDeploymentStatus.Name(undeployment_response.status)}."
    )

    return undeployment_response


def __get_environment_to_deployment_id(
    deployment_client: DeploymentManagementClient,
    model_id: str,
    model_uuid: str,
    env_undeployment_requests: Dict,
) -> Dict:
    deployment_details = deployment_client.get_deployment_details(
        model_id, model_uuid
    ).environment_to_deployment_details
    result = {}
    for env_id, env_deployment_details in env_undeployment_requests.items():
        deployment_detail_by_env = deployment_details.get(env_id)
        if deployment_detail_by_env:
            for deployment_detail in deployment_detail_by_env.deployments_details:
                if (
                    env_id == deployment_detail.environment_id
                    and deployment_detail.variation.name
                    == env_deployment_details.traffic_config.selected_variation_name
                ):
                    result[env_id] = deployment_detail.deployment_id
    return result


def __sync_undeploy(
    environment_to_deployment_id: Dict,
    model_id: str,
    deployment_client: DeploymentManagementClient,
):
    with qwak_spinner(
        begin_text=f"Undeploy - model: {model_id}",
        end_text="Successful undeployment",
        print_callback=print,
    ):
        for environment_id, deployment_id in environment_to_deployment_id.items():
            status_result = _poll_undeployment_status(
                deployment_id=deployment_id,
                deployment_client=deployment_client,
                check_every_n_seconds=TIME_TO_WAIT_FOR_UNDEPLOYMENT_POLLING,
            )
            failed_to_undeployment = []
            for _, status in status_result.items():
                if status in FAILED_UNDEPLOYMENT_STATUS:
                    failed_to_undeployment.append(
                        UNDEPLOY_ERROR_MSG.format(
                            environment_id=environment_id, status=status
                        )
                    )
            if failed_to_undeployment:
                raise QwakException("\n".join(failed_to_undeployment))


def _poll_undeployment_status(
    deployment_id: str,
    deployment_client: DeploymentManagementClient,
    check_every_n_seconds: int,
) -> Dict:
    deployment_status = ""

    while deployment_status not in END_UNDEPLOYMENT_STATUSES:
        sleep(check_every_n_seconds)
        deployment_status = __get_deployment_status(
            deployment_id=deployment_id, deployment_client=deployment_client
        )
    return {deployment_id: deployment_status}


def __get_deployment_status(
    deployment_id: str, deployment_client: DeploymentManagementClient
):
    try:
        return ModelDeploymentStatus.Name(
            deployment_client.get_deployment_status(
                deployment_named_id=deployment_id,
            ).status
        )
    except QwakException as e:
        logger.error(
            f"Got error while trying to get deployment id: {deployment_id} status. Error is: {e.message}"
        )
        return ""

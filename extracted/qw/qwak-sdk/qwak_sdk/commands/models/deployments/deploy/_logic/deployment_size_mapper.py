from __future__ import annotations

from _qwak_proto.qwak.deployment.deployment_pb2 import DeploymentSize, MemoryUnit
from _qwak_proto.qwak.user_application.common.v0.resources_pb2 import (
    ClientPodComputeResources,
    CpuResources,
    GpuResources,
    PodComputeResourceTemplateSpec,
)
from qwak.clients.administration.eco_system.client import EcosystemClient
from qwak.clients.instance_template.client import InstanceTemplateManagementClient
from qwak.exceptions import QwakException
from qwak.inner.instance_template.verify_template_id import verify_template_id
from qwak.inner.provider import Provider

from qwak_sdk.commands.models.deployments.deploy._logic.deploy_config import (
    DeployConfig,
)


def deployment_size_from_deploy_config(
    deploy_config: DeployConfig,
    instance_template_client: InstanceTemplateManagementClient,
    ecosystem_client: EcosystemClient,
) -> DeploymentSize:
    if deploy_config.resources.instance_size:
        deploy_config.resources.instance_size = (
            deploy_config.resources.instance_size.lower()
        )
        account_details = ecosystem_client.get_account_details()
        if deploy_config.environments:
            environments_config = list(
                ecosystem_client.get_environments_names_to_details(
                    deploy_config.environments
                ).values()
            )
        else:
            environments_config = [
                account_details.environment_by_id[
                    account_details.default_environment_id
                ]
            ]
        for environment_config in environments_config:
            provider = __get_provider(environment_config)
            try:
                verify_template_id(
                    deploy_config.resources.instance_size,
                    instance_template_client,
                    provider=provider,
                )
            except QwakException as e:
                raise QwakException(
                    f"Error with template {deploy_config.resources.instance_size} for environment {environment_config.name}: {e.message}"
                )

        return DeploymentSize(
            number_of_pods=deploy_config.resources.pods,
            client_pod_compute_resources=ClientPodComputeResources(
                template_spec=PodComputeResourceTemplateSpec(
                    template_id=deploy_config.resources.instance_size
                )
            ),
        )
    elif deploy_config.resources.gpu_type:
        return DeploymentSize(
            number_of_pods=deploy_config.resources.pods,
            client_pod_compute_resources=ClientPodComputeResources(
                gpu_resources=GpuResources(
                    gpu_type=deploy_config.resources.gpu_type,
                    gpu_amount=deploy_config.resources.gpu_amount,
                )
            ),
        )
    else:
        return DeploymentSize(
            number_of_pods=deploy_config.resources.pods,
            client_pod_compute_resources=ClientPodComputeResources(
                cpu_resources=CpuResources(
                    cpu=deploy_config.resources.cpus,
                    memory_amount=deploy_config.resources.memory,
                    memory_units=MemoryUnit.MIB,
                )
            ),
        )


def __get_provider(environment_config):
    provider = None
    cloud_type = environment_config.configuration.cloud_configuration.WhichOneof(
        "configuration"
    )
    if cloud_type == "aws_cloud_configuration":
        provider = Provider.AWS
    elif cloud_type == "gcp_cloud_configuration":
        provider = Provider.GCP
    return provider

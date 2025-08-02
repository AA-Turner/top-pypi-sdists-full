"""GKE policy
Users must use the following `~/.sky/config.yaml`

admin_policy: trainy.policy.GKEPolicy

kubernetes:
  autoscaler: gke
  provision_timeout: 600 # should be at least 10 min
  remote_identity: SERVICE_ACCOUNT

"""

import sky

from trainy.config import load_config
from trainy.logging import get_logger

logger = get_logger(__file__)

ALLOWED_GPUS = ["H100"]


def set_efa_config(user_request: sky.UserRequest) -> sky.MutatedUserRequest:
    """Sets pod specs for running TCPXO"""
    task = user_request.task
    config = user_request.skypilot_config
    for resource in task.resources:
        for accelerator, count in resource.accelerators.items():
            if accelerator == "H100":
                k8s_override_config = load_config("eks.yaml")
                config = user_request.skypilot_config
                new_config = sky.skypilot_config._recursive_update(
                    config, k8s_override_config
                )
                return sky.MutatedUserRequest(
                    task=user_request.task, skypilot_config=new_config
                )
    return sky.MutatedUserRequest(task=task, skypilot_config=config)


def validate_request(
    user_request: sky.MutatedUserRequest,
) -> sky.MutatedUserRequest:
    """Checks for valid Kueue user-queue and priority queue values
    populates the required labels and annotations for Kueue
    """
    task = user_request.task
    config = user_request.skypilot_config
    for resource in task.resources:
        if resource.cloud is None or str(resource.cloud) != "Kubernetes":
            raise ValueError("Only `kubernetes` is permitted as a cloud on Trainy")

    return sky.MutatedUserRequest(task=task, skypilot_config=config)


class EKSPolicy(sky.AdminPolicy):
    """EKS specific configurations."""

    @classmethod
    def validate_and_mutate(
        cls, user_request: sky.UserRequest
    ) -> sky.MutatedUserRequest:
        """Updates the kubernetes context to use
        and kueue labels and sets GKE autoscaler
        """
        if not user_request.task.is_controller_task():
            new_request: sky.MutatedUserRequest = set_efa_config(user_request)
            new_request = validate_request(user_request)
            return sky.MutatedUserRequest(
                task=new_request.task, skypilot_config=new_request.skypilot_config
            )
        return sky.MutatedUserRequest(
            task=user_request.task, skypilot_config=user_request.skypilot_config
        )

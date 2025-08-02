import uuid

import sky

from trainy.config import load_config
from trainy.logging import get_logger

logger = get_logger(__file__)

ALLOWED_GPUS = ["H100"]


def set_nebius_config(user_request: sky.UserRequest) -> sky.MutatedUserRequest:
    task = user_request.task
    config = user_request.skypilot_config
    for resource in task.resources:
        for accelerator, count in resource.accelerators.items():
            if accelerator == "H100":
                k8s_override_config = load_config("nebius.yaml")
                config = user_request.skypilot_config
                config.set_nested(
                    (
                        "kubernetes",
                        "pod_config",
                        "metadata",
                        "labels",
                        "kueue.x-k8s.io/pod-group-name",
                    ),
                    f"{task.name[:8]}-{uuid.uuid4().hex[:4]}",
                )
                config.set_nested(
                    (
                        "kubernetes",
                        "pod_config",
                        "metadata",
                        "annotations",
                        "kueue.x-k8s.io/pod-group-total-count",
                    ),
                    str(task.num_nodes),
                )
                config.set_nested(
                    (
                        "kubernetes",
                        "pod_config",
                        "metadata",
                        "annotations",
                        "kueue.x-k8s.io/retriable-in-group",
                    ),
                    "false",
                )
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
    task = user_request.task
    config = user_request.skypilot_config
    for resource in task.resources:
        if resource.cloud is None or str(resource.cloud) != "Kubernetes":
            raise ValueError("Only `kubernetes` is permitted as a cloud on Trainy")

    return sky.MutatedUserRequest(task=task, skypilot_config=config)


class NebiusPolicy(sky.AdminPolicy):
    """Nebius specific configurations."""

    @classmethod
    def validate_and_mutate(
        cls, user_request: sky.UserRequest
    ) -> sky.MutatedUserRequest:
        if not user_request.task.is_controller_task():
            new_request: sky.MutatedUserRequest = set_nebius_config(user_request)
            new_request = validate_request(user_request)
            return sky.MutatedUserRequest(
                task=new_request.task, skypilot_config=new_request.skypilot_config
            )
        return sky.MutatedUserRequest(
            task=user_request.task, skypilot_config=user_request.skypilot_config
        )

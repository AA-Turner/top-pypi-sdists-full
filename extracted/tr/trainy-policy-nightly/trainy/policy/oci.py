import uuid

import sky

from trainy.config import load_config
from trainy.logging import get_logger

logger = get_logger(__file__)

ALLOWED_GPUS = ["H100"]


def set_oci_config(user_request: sky.UserRequest) -> sky.MutatedUserRequest:
    """Sets pod specs for Oracle Cloud H100 NCCL configuration."""
    task = user_request.task
    config = user_request.skypilot_config

    # Set kueue pod-group labels/annotations for all jobs
    if task.name is None:
        raise ValueError("no sky.Task name defined. You must set a task name")
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

    # Apply H100-specific NCCL configuration only when H100 is requested
    for resource in task.resources:
        if not resource.accelerators:
            continue
        for accelerator, count in resource.accelerators.items():
            if accelerator == "H100":
                k8s_override_config = load_config("oci.yaml")
                new_config = sky.skypilot_config._recursive_update(
                    config, k8s_override_config
                )
                return sky.MutatedUserRequest(task=task, skypilot_config=new_config)

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


class OCIPolicy(sky.AdminPolicy):
    """Oracle Cloud Infrastructure H100 specific configurations."""

    @classmethod
    def validate_and_mutate(
        cls, user_request: sky.UserRequest
    ) -> sky.MutatedUserRequest:
        if not user_request.task.is_controller_task():
            new_request: sky.MutatedUserRequest = set_oci_config(user_request)
            new_request = validate_request(new_request)
            return sky.MutatedUserRequest(
                task=new_request.task, skypilot_config=new_request.skypilot_config
            )
        return sky.MutatedUserRequest(
            task=user_request.task, skypilot_config=user_request.skypilot_config
        )

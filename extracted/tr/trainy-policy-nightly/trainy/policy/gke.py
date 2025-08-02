"""GKE policy
Users must use the following `~/.sky/config.yaml`

admin_policy: trainy.policy.GKEPolicy

kubernetes:
  autoscaler: gke
  provision_timeout: 600 # should be at least 10 min
  remote_identity: SERVICE_ACCOUNT

"""

import sky
import uuid

from trainy.config import load_config
from trainy.logging import get_logger

logger = get_logger(__file__)

DEFAULT_QUEUE = "user-queue"
PRIORITY_CLASSES = ["low-priority", "high-priority"]
ALLOWED_GPUS = ["H100-MEGA-80GB", "A100-80GB", "A100"]


def set_tcpxo_config(user_request: sky.UserRequest) -> sky.MutatedUserRequest:
    """Sets pod specs for running TCPXO"""
    task = user_request.task
    config = user_request.skypilot_config
    for resource in task.resources:
        for accelerator, count in resource.accelerators.items():
            if accelerator == "H100-MEGA-80GB":
                k8s_override_config = load_config("gke.yaml")
                config = user_request.skypilot_config
                new_config = sky.skypilot_config._recursive_update(
                    config, k8s_override_config
                )
                return sky.MutatedUserRequest(
                    task=user_request.task, skypilot_config=new_config
                )
    return sky.MutatedUserRequest(task=task, skypilot_config=config)


def validate_set_kueue_dws_labels_annotations(
    user_request: sky.MutatedUserRequest,
) -> sky.MutatedUserRequest:
    """Checks for valid Kueue user-queue and priority queue values
    populates the required labels and annotations for Kueue
    """
    task = user_request.task
    config = user_request.skypilot_config
    new_resources = []
    for resource in task.resources:
        if resource.cloud is None or str(resource.cloud) != "Kubernetes":
            raise ValueError("Only `kubernetes` is permitted as a cloud on Trainy")
        if not resource.accelerators:
            raise ValueError(
                "You must request a GPU instance. Set `accelerators: "
                "H100-MEGA-80GB:8` under resources for example"
            )
        for accelerator, count in resource.accelerators.items():
            if accelerator not in ALLOWED_GPUS:
                raise ValueError(
                    f"{resource.accelerators} requested,"
                    f"only `{ALLOWED_GPUS}` allowed"
                )
            nodepool = (
                "kubernetes",
                "pod_config",
                "spec",
                "nodeSelector",
                "cloud.google.com/gke-nodepool",
            )
            if config.get_nested(nodepool, None) is None:
                logger.info(
                    "`cloud.google.com/gke-nodepool` not set, "
                    f"setting to default nodepool `{accelerator.lower()}-pool`"
                )
                config.set_nested(nodepool, f"{accelerator.lower()}-pool")

        labels = resource.labels
        if labels is None:
            labels = {}
        queue_name: str = labels.get("kueue.x-k8s.io/queue-name", DEFAULT_QUEUE)
        priority: str = labels.get("kueue.x-k8s.io/priority-class", "low-priority")
        run_duration: str = labels.get("max-run-duration-seconds", None)
        if queue_name != DEFAULT_QUEUE:
            raise ValueError(
                f"{queue_name} queue was selected, "
                f"only {DEFAULT_QUEUE} queue is permitted for hosted Trainy clusters"
            )
        if priority not in PRIORITY_CLASSES:
            raise ValueError(
                f"priority `{priority}` was selected, "
                f"only {PRIORITY_CLASSES} are available"
            )
        if task.name is None:
            raise ValueError("no sky.Task name defined. You must set a task name")
        if len(task.name) > 59:
            raise ValueError(f"sky.Task name is {len(task.name)} long. Expected 58 characters or less.")
        labels.update(
            {
                "kueue.x-k8s.io/queue-name": queue_name,
                "kueue.x-k8s.io/priority-class": priority,
                "kueue.x-k8s.io/pod-group-name": f"{task.name}-"
                f"{uuid.uuid4().hex[:4]}",
            }
        )
        if resource.labels is not None:
            resource.labels.update(labels)
        new_resources.append(resource)
    task.set_resources(type(task.resources)(new_resources))

    # pod annotations
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

    maxRunDurationSeconds = (
        "kubernetes",
        "pod_config",
        "metadata",
        "annotations",
        "provreq.kueue.x-k8s.io/maxRunDurationSeconds",
    )
    if config.get_nested(maxRunDurationSeconds, None) is None:
        if run_duration is None:
            raise ValueError("You must specify a label for `max-run-duration-seconds`")
        # maximum runtime on gke dws is 7 days
        config.set_nested(maxRunDurationSeconds, str(run_duration))

    run_duration = config.get_nested(maxRunDurationSeconds, None)
    assert run_duration is not None
    if not (0 < int(run_duration) <= 3600 * 24 * 7):
        raise ValueError(
            f"largest allowed run duration is 7 days "
            f" = {3600 * 24 * 7} seconds {int(run_duration)} requested "
            "from either `max-run-duration-seconds` or "
            "`provreq.kueue.x-k8s.io/maxRunDurationSeconds`"
        )

    safe_to_evict = (
        "kubernetes",
        "pod_config",
        "metadata",
        "annotations",
        "cluster-autoscaler.kubernetes.io/safe-to-evict",
    )
    if config.get_nested(safe_to_evict, None) is None:
        config.set_nested(safe_to_evict, "false")

    return sky.MutatedUserRequest(task=task, skypilot_config=config)


class GKEPolicy(sky.AdminPolicy):
    """GKE specific configurations."""

    @classmethod
    def validate_and_mutate(
        cls, user_request: sky.UserRequest
    ) -> sky.MutatedUserRequest:
        """Updates the kubernetes context to use
        and kueue labels and sets GKE autoscaler
        """
        if not user_request.task.is_controller_task():
            new_request: sky.MutatedUserRequest = set_tcpxo_config(user_request)
            new_request = validate_set_kueue_dws_labels_annotations(user_request)
            return sky.MutatedUserRequest(
                task=new_request.task, skypilot_config=new_request.skypilot_config
            )
        return sky.MutatedUserRequest(
            task=user_request.task, skypilot_config=user_request.skypilot_config
        )


def configure_and_get_allowed_contexts():
    """Mock implementation of getting allowed kubernetes contexts."""
    from sky.provision.kubernetes import utils

    contexts = utils.get_all_kube_config_context_names()
    return contexts[:2]


class TailscaleGKEPolicy(GKEPolicy):
    @classmethod
    def validate_and_mutate(
        cls, user_request: sky.UserRequest
    ) -> sky.MutatedUserRequest:
        """Updates the kubernetes context to use
        and kueue labels and sets GKE autoscaler
        """

        super().validate_and_mutate(user_request=user_request)

        # Append any new kubernetes clusters in local kubeconfig. An example
        # implementation of this method can be:
        #  1. Query tailscale for k8s clusters.
        #  2. Append the new credentials to the local kubeconfig.
        #  3. Set the allow contexts for the cluster.

        # Get the allowed contexts for the user. Similarly, it can retrieve
        # the latest allowed contexts from an organization's internal API.
        # allowed_contexts = configure_and_get_allowed_contexts()

        # # Update the kubernetes allowed contexts in skypilot config.
        # config = user_request.skypilot_config
        # config.set_nested(("kubernetes", "allowed_contexts"), allowed_contexts)

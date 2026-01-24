"""GKE policy
Users must use the following `~/.sky/config.yaml`

admin_policy: trainy.policy.GKEPolicy

kubernetes:
  autoscaler: gke
  provision_timeout: 600 # should be at least 10 min
  remote_identity: SERVICE_ACCOUNT

"""

from copy import deepcopy
from typing import Any, Dict, List, Optional, Sequence, Tuple

import sky
import uuid

from trainy.config import load_config
from trainy.logging import get_logger

logger = get_logger(__file__)

DEFAULT_QUEUE = "user-queue"
PRIORITY_CLASSES = ["low-priority", "high-priority"]
ALLOWED_GPUS = ["H100", "H100-MEGA-80GB", "A100-80GB", "A100"]

_POD_SPEC_PATH: Tuple[str, ...] = ("kubernetes", "pod_config", "spec")


def _get_dict_path(
    data: Dict[str, Any], path: Sequence[str]
) -> Optional[Dict[str, Any]]:
    """Returns the nested dict at path, creating dicts along the way."""
    cursor: Dict[str, Any] = data
    for key in path:
        if key not in cursor or not isinstance(cursor[key], dict):
            cursor[key] = {}
        cursor = cursor[key]
    return cursor


def _merge_named_items(
    base_list: Optional[List[Dict[str, Any]]],
    override_list: Optional[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Merges two lists of dicts keyed by `name` while preserving order."""
    merged: List[Dict[str, Any]] = []
    index_by_name: Dict[str, int] = {}

    def _append(item: Dict[str, Any]) -> None:
        index_by_name[item.get("name", f"__idx_{len(merged)}")] = len(merged)
        merged.append(item)

    for entry in base_list or []:
        if isinstance(entry, dict):
            _append(deepcopy(entry))

    for entry in override_list or []:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        replacement = deepcopy(entry)
        if name is not None and name in index_by_name:
            merged[index_by_name[name]] = replacement
        else:
            _append(replacement)

    return merged


def _merge_container_sections(
    base_containers: Optional[List[Dict[str, Any]]],
    override_containers: Optional[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Merges env/volumeMounts between lists of containers."""
    base_containers = base_containers or []
    override_containers = override_containers or []
    merged_containers: List[Dict[str, Any]] = []
    max_len = max(len(base_containers), len(override_containers))

    for idx in range(max_len):
        base_container = base_containers[idx] if idx < len(base_containers) else None
        override_container = (
            deepcopy(override_containers[idx]) if idx < len(override_containers) else None
        )

        if override_container is None:
            if base_container is not None:
                merged_containers.append(deepcopy(base_container))
            continue

        merged_env = _merge_named_items(
            base_container.get("env") if base_container else None,
            override_container.get("env"),
        )
        if merged_env:
            override_container["env"] = merged_env
        elif "env" in override_container:
            del override_container["env"]

        merged_volume_mounts = _merge_named_items(
            base_container.get("volumeMounts") if base_container else None,
            override_container.get("volumeMounts"),
        )
        if merged_volume_mounts:
            override_container["volumeMounts"] = merged_volume_mounts
        elif "volumeMounts" in override_container:
            del override_container["volumeMounts"]

        merged_containers.append(override_container)

    return merged_containers


def _merge_pod_spec_sections(
    config: sky.skypilot_config.Config, override_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Returns override_config with volumes/env/volumeMounts merged from config."""
    merged_override = deepcopy(override_config)
    spec = _get_dict_path(merged_override, _POD_SPEC_PATH)

    base_volumes = config.get_nested(_POD_SPEC_PATH + ("volumes",), None)
    override_volumes = spec.get("volumes")
    merged_volumes = _merge_named_items(base_volumes, override_volumes)
    if merged_volumes:
        spec["volumes"] = merged_volumes
    elif "volumes" in spec:
        del spec["volumes"]

    merged_containers = _merge_container_sections(
        config.get_nested(_POD_SPEC_PATH + ("containers",), None),
        spec.get("containers"),
    )
    if merged_containers:
        spec["containers"] = merged_containers
    elif "containers" in spec:
        del spec["containers"]

    merged_init_containers = _merge_container_sections(
        config.get_nested(_POD_SPEC_PATH + ("initContainers",), None),
        spec.get("initContainers"),
    )
    if merged_init_containers:
        spec["initContainers"] = merged_init_containers
    elif "initContainers" in spec:
        del spec["initContainers"]

    return merged_override

_POD_SPEC_PATH: Tuple[str, ...] = ("kubernetes", "pod_config", "spec")


def _get_dict_path(
    data: Dict[str, Any], path: Sequence[str]
) -> Optional[Dict[str, Any]]:
    """Returns the nested dict at path, creating dicts along the way."""
    cursor: Dict[str, Any] = data
    for key in path:
        if key not in cursor or not isinstance(cursor[key], dict):
            cursor[key] = {}
        cursor = cursor[key]
    return cursor


def _merge_named_items(
    base_list: Optional[List[Dict[str, Any]]],
    override_list: Optional[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Merges two lists of dicts keyed by `name` while preserving order."""
    merged: List[Dict[str, Any]] = []
    index_by_name: Dict[str, int] = {}

    def _append(item: Dict[str, Any]) -> None:
        index_by_name[item.get("name", f"__idx_{len(merged)}")] = len(merged)
        merged.append(item)

    for entry in base_list or []:
        if isinstance(entry, dict):
            _append(deepcopy(entry))

    for entry in override_list or []:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        replacement = deepcopy(entry)
        if name is not None and name in index_by_name:
            merged[index_by_name[name]] = replacement
        else:
            _append(replacement)

    return merged


def _merge_container_sections(
    base_containers: Optional[List[Dict[str, Any]]],
    override_containers: Optional[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Merges env/volumeMounts between lists of containers."""
    base_containers = base_containers or []
    override_containers = override_containers or []
    merged_containers: List[Dict[str, Any]] = []
    max_len = max(len(base_containers), len(override_containers))

    for idx in range(max_len):
        base_container = base_containers[idx] if idx < len(base_containers) else None
        override_container = (
            deepcopy(override_containers[idx]) if idx < len(override_containers) else None
        )

        if override_container is None:
            if base_container is not None:
                merged_containers.append(deepcopy(base_container))
            continue

        merged_env = _merge_named_items(
            base_container.get("env") if base_container else None,
            override_container.get("env"),
        )
        if merged_env:
            override_container["env"] = merged_env
        elif "env" in override_container:
            del override_container["env"]

        merged_volume_mounts = _merge_named_items(
            base_container.get("volumeMounts") if base_container else None,
            override_container.get("volumeMounts"),
        )
        if merged_volume_mounts:
            override_container["volumeMounts"] = merged_volume_mounts
        elif "volumeMounts" in override_container:
            del override_container["volumeMounts"]

        merged_containers.append(override_container)

    return merged_containers


def _merge_pod_spec_sections(
    config: sky.skypilot_config.Config, override_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Returns override_config with volumes/env/volumeMounts merged from config."""
    merged_override = deepcopy(override_config)
    spec = _get_dict_path(merged_override, _POD_SPEC_PATH)

    base_volumes = config.get_nested(_POD_SPEC_PATH + ("volumes",), None)
    override_volumes = spec.get("volumes")
    merged_volumes = _merge_named_items(base_volumes, override_volumes)
    if merged_volumes:
        spec["volumes"] = merged_volumes
    elif "volumes" in spec:
        del spec["volumes"]

    merged_containers = _merge_container_sections(
        config.get_nested(_POD_SPEC_PATH + ("containers",), None),
        spec.get("containers"),
    )
    if merged_containers:
        spec["containers"] = merged_containers
    elif "containers" in spec:
        del spec["containers"]

    merged_init_containers = _merge_container_sections(
        config.get_nested(_POD_SPEC_PATH + ("initContainers",), None),
        spec.get("initContainers"),
    )
    if merged_init_containers:
        spec["initContainers"] = merged_init_containers
    elif "initContainers" in spec:
        del spec["initContainers"]

    return merged_override


def set_tcpxo_config(user_request: sky.UserRequest) -> sky.MutatedUserRequest:
    """Sets pod specs for running TCPXO"""
    task = user_request.task
    config = user_request.skypilot_config
    for resource in task.resources:
        for accelerator, count in resource.accelerators.items():
            if accelerator == "H100-MEGA-80GB":
                k8s_override_config = load_config("gke.yaml")
                config = user_request.skypilot_config
                merged_override = _merge_pod_spec_sections(
                    config, k8s_override_config
                )
                new_config = sky.skypilot_config._recursive_update(
                    config, merged_override
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
        # if queue_name != DEFAULT_QUEUE:
        #     raise ValueError(
        #         f"{queue_name} queue was selected, "
        #         f"only {DEFAULT_QUEUE} queue is permitted for hosted Trainy clusters"
        #     )
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

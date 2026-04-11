"""Helpers for merging Kubernetes pod-spec sections in admin policies.

`sky.skypilot_config._recursive_update` overrides lists wholesale, which
causes user-supplied entries (e.g. extra environment variables, volumes,
volumeMounts) to be wiped out when an admin policy applies its own pod
config overrides. The helpers in this module merge the relevant sections
by `name` so user-supplied entries are preserved alongside the policy
overrides.
"""

from copy import deepcopy
from typing import Any, Dict, List, Optional, Sequence, Tuple

import sky

POD_SPEC_PATH: Tuple[str, ...] = ("kubernetes", "pod_config", "spec")


def _get_dict_path(data: Dict[str, Any], path: Sequence[str]) -> Dict[str, Any]:
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
            deepcopy(override_containers[idx])
            if idx < len(override_containers)
            else None
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


def merge_pod_spec_sections(
    config: sky.skypilot_config.Config, override_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Returns override_config with volumes/env/volumeMounts merged from config."""
    merged_override = deepcopy(override_config)
    spec = _get_dict_path(merged_override, POD_SPEC_PATH)

    base_volumes = config.get_nested(POD_SPEC_PATH + ("volumes",), None)
    override_volumes = spec.get("volumes")
    merged_volumes = _merge_named_items(base_volumes, override_volumes)
    if merged_volumes:
        spec["volumes"] = merged_volumes
    elif "volumes" in spec:
        del spec["volumes"]

    merged_containers = _merge_container_sections(
        config.get_nested(POD_SPEC_PATH + ("containers",), None),
        spec.get("containers"),
    )
    if merged_containers:
        spec["containers"] = merged_containers
    elif "containers" in spec:
        del spec["containers"]

    merged_init_containers = _merge_container_sections(
        config.get_nested(POD_SPEC_PATH + ("initContainers",), None),
        spec.get("initContainers"),
    )
    if merged_init_containers:
        spec["initContainers"] = merged_init_containers
    elif "initContainers" in spec:
        del spec["initContainers"]

    return merged_override

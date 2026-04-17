"""Helpers for merging admin-policy pod-config overrides into a user config.

`sky.skypilot_config._recursive_update` clobbers scalar values and replaces
lists wholesale, so any field the user has set (extra env vars, volumes,
a custom `hostNetwork`, etc.) is wiped out when an admin policy applies
its own pod-config overrides. `apply_pod_override` performs a recursive
merge with user-wins semantics: any key the user has already set keeps
its value, and the policy only contributes keys that are absent. Named
lists (`env`, `volumes`, `volumeMounts`) are merged by `name` with the
user entry winning on collision; container lists (`containers`,
`initContainers`) are merged index-wise with the same rules applied to
their env/volumeMounts.
"""

from copy import deepcopy
from typing import Any, Dict, List, Optional

import sky

NAMED_LIST_KEYS = frozenset(("env", "volumes", "volumeMounts"))
CONTAINER_LIST_KEYS = frozenset(("containers", "initContainers"))


def _merge_named_items(
    base_list: Optional[List[Dict[str, Any]]],
    override_list: Optional[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Merges two lists of dicts keyed by `name` while preserving order.

    On name collision the base entry wins: override entries only contribute
    when the name is not already present in the base list.
    """
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
        if name is not None and name in index_by_name:
            continue
        _append(deepcopy(entry))

    return merged


def _merge_container_sections(
    base_containers: Optional[List[Dict[str, Any]]],
    override_containers: Optional[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Merges containers index-wise with user-wins semantics."""
    base_containers = base_containers or []
    override_containers = override_containers or []
    merged_containers: List[Dict[str, Any]] = []
    max_len = max(len(base_containers), len(override_containers))

    for idx in range(max_len):
        base_container = base_containers[idx] if idx < len(base_containers) else None
        override_container = (
            override_containers[idx] if idx < len(override_containers) else None
        )

        if override_container is None:
            merged_containers.append(deepcopy(base_container) if base_container else {})
            continue
        if base_container is None:
            merged_containers.append(deepcopy(override_container))
            continue

        merged = deepcopy(base_container)
        _merge_user_wins(merged, override_container)
        merged_containers.append(merged)

    return merged_containers


def _merge_user_wins(base: Any, override: Dict[str, Any]) -> None:
    """Recursively merges override into base in-place with user-wins semantics."""
    for key, override_val in override.items():
        has_key = key in base
        base_val = base[key] if has_key else None

        if key in NAMED_LIST_KEYS and isinstance(override_val, list):
            base[key] = _merge_named_items(
                base_val if isinstance(base_val, list) else None,
                override_val,
            )
            continue
        if key in CONTAINER_LIST_KEYS and isinstance(override_val, list):
            base[key] = _merge_container_sections(
                base_val if isinstance(base_val, list) else None,
                override_val,
            )
            continue
        if isinstance(override_val, dict) and isinstance(base_val, dict):
            _merge_user_wins(base_val, override_val)
            continue
        if not has_key or base_val is None:
            base[key] = deepcopy(override_val)
        # else: user has set a concrete value, preserve it.


def apply_pod_override(
    config: sky.skypilot_config.Config, override_config: Dict[str, Any]
) -> sky.skypilot_config.Config:
    """Applies override_config into config with user-wins semantics.

    Any field the user has already set in `config` is preserved. Named
    lists (env/volumes/volumeMounts) are merged by `name`; container
    lists are merged index-wise.
    """
    _merge_user_wins(config, override_config)
    return config

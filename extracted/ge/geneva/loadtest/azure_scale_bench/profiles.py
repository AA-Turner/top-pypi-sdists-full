# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Named dataset × compute-scale profiles loaded from ``profiles.yaml``.

A profile is a small bundle of ``BenchConfig`` field overrides selected by name
(`--dataset 50b --scale 100n`), so a run is one or two flags instead of a dozen.
Keys are exactly ``BenchConfig`` field names (1:1 ``setattr``, no aliases); the
loader rejects unknown keys, an ``account_key`` key (no secrets in a checked-in
file), and unknown profile names.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import attrs

if TYPE_CHECKING:
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

DEFAULT_PROFILES_PATH = Path(__file__).with_name("profiles.yaml")


def load_profiles(path: str | Path | None = None) -> dict[str, Any]:
    """Load the profiles YAML (defaults to the checked-in ``profiles.yaml``)."""
    import yaml

    resolved = Path(path) if path else DEFAULT_PROFILES_PATH
    with resolved.open() as handle:
        return yaml.safe_load(handle) or {}


def apply_profile(
    cfg: BenchConfig,
    profiles: dict[str, Any],
    *,
    dataset: str | None = None,
    scale: str | None = None,
) -> None:
    """Overlay the named ``datasets[dataset]`` then ``scales[scale]`` onto ``cfg``.

    Mutates ``cfg`` in place. Raises ``ValueError`` on an unknown profile name, an
    unknown key (typo guard), or an ``account_key`` key (secret).
    """
    field_names = {field.name for field in attrs.fields(type(cfg))}
    for group_key, name in (("datasets", dataset), ("scales", scale)):
        if name is None:
            continue
        group = profiles.get(group_key) or {}
        if name not in group:
            raise ValueError(
                f"unknown {group_key[:-1]} {name!r}; available: {sorted(group)}"
            )
        entry = group[name] or {}
        if "account_key" in entry:
            raise ValueError(
                "do not put account_key in profiles (it is a secret); set the "
                "AZURE_STORAGE_ACCOUNT_KEY env var instead"
            )
        for key, value in entry.items():
            if key not in field_names:
                raise ValueError(
                    f"unknown profile key {key!r} in {group_key}.{name} — not a "
                    "BenchConfig field"
                )
            setattr(cfg, key, value)

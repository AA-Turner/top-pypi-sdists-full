"""A policy's model family and a benchmark's physics engine: what the declaration names (`@seq.policy(family="pi")`,
`@seq.benchmark(engine="mujoco")`), a benchmark's engine else the one its replay names (benchmark_registry.
_declared_engine) - neither ever guessed from the packages an image installs or the weights it names. The console draws
the entity's icon from it (π for pi, NVIDIA for gr00t and isaac, a lettered tile otherwise). A benchmark's engine also
picks the platform's adapter for its 3D replay when seq.Replay names none (benchmark_registry.REPLAY_ADAPTERS).


"""
from __future__ import annotations

import re
from typing import Any

from sequence_base.contract.policy import KIND_NAME

_NAME = re.compile(KIND_NAME)


def declared(value: Any, what: str, error: type[Exception]) -> str | None:
    """`family=` / `engine=` as written: a short name, lower-cased (MuJoCo → mujoco); None when not given."""
    if value is None:
        return None
    name = value.strip().lower() if isinstance(value, str) else value
    if not isinstance(name, str) or not _NAME.fullmatch(name):
        raise error(f"{what}= must be a short name like {'pi' if what == 'family' else 'mujoco'!r} (a letter or digit, "
                    f"then up to 31 letters, digits, '.', '_' or '-'), got {value!r}")
    return name

"""One definition of the launchers' rank environment variables and how to read them."""

from __future__ import annotations

import os
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

_INTEGER = re.compile(r"[0-9]+")


@dataclass(frozen=True)
class LaunchScheme:
    """The three variables one launcher exports for each process it starts."""

    name: str
    rank_var: str
    size_var: str
    local_rank_var: str


TORCH = LaunchScheme("torch", "RANK", "WORLD_SIZE", "LOCAL_RANK")
SLURM = LaunchScheme("slurm", "SLURM_PROCID", "SLURM_NTASKS", "SLURM_LOCALID")
OPENMPI = LaunchScheme(
    "openmpi", "OMPI_COMM_WORLD_RANK", "OMPI_COMM_WORLD_SIZE", "OMPI_COMM_WORLD_LOCAL_RANK"
)
PMI = LaunchScheme("pmi", "PMI_RANK", "PMI_SIZE", "PMI_LOCAL_RANK")

#: Most specific first: under `srun` + `torchrun`, SLURM_PROCID numbers the node and RANK numbers
#: the worker. The one precedence order every reader uses unless it passes its own subset.
LAUNCH_SCHEMES = (TORCH, SLURM, OPENMPI, PMI)


@dataclass(frozen=True)
class ProcessRank:
    """This process's place in a launch; ``size`` and ``local_rank`` are None when not advertised."""

    rank: int
    size: int | None
    local_rank: int | None
    scheme: LaunchScheme


def read_env_text(environ: Mapping[str, str] | None, name: str) -> str:
    """The stripped value of ``name``, "" when unset."""
    env = os.environ if environ is None else environ
    return (env.get(name) or "").strip()


def read_env_int(environ: Mapping[str, str] | None, name: str) -> int | None:
    """``name`` as a non-negative integer, None when unset, signed or not ASCII digits."""
    text = read_env_text(environ, name)
    return int(text) if _INTEGER.fullmatch(text) else None


def read_process_ranks(environ: Mapping[str, str] | None = None) -> tuple[ProcessRank, ...]:
    """Every scheme that names a rank (a non-negative integer), in `LAUNCH_SCHEMES` order."""
    found = []
    for scheme in LAUNCH_SCHEMES:
        rank = read_env_int(environ, scheme.rank_var)
        if rank is None or rank < 0:
            continue
        found.append(
            ProcessRank(
                rank=rank,
                size=read_env_int(environ, scheme.size_var),
                local_rank=read_env_int(environ, scheme.local_rank_var),
                scheme=scheme,
            )
        )
    return tuple(found)


def read_process_rank(environ: Mapping[str, str] | None = None) -> ProcessRank | None:
    """The first scheme that names a rank, or None outside a distributed launch."""
    ranks = read_process_ranks(environ)
    return ranks[0] if ranks else None


def read_world_size(environ: Mapping[str, str] | None = None) -> int | None:
    """The first world size any scheme advertises, in `LAUNCH_SCHEMES` order."""
    for scheme in LAUNCH_SCHEMES:
        size = read_env_int(environ, scheme.size_var)
        if size is not None:
            return size
    return None


def read_rank_text(
    environ: Mapping[str, str] | None, schemes: Iterable[LaunchScheme]
) -> tuple[LaunchScheme, str] | None:
    """The first of ``schemes`` whose rank variable is non-empty, with its raw stripped text.
    For callers that name files after the value and must not reinterpret it."""
    for scheme in schemes:
        text = read_env_text(environ, scheme.rank_var)
        if text:
            return scheme, text
    return None

from __future__ import annotations

import hashlib
import secrets
from os import PathLike
from pathlib import Path

from ._errors import ExperimentError

DEFAULT_ROOT_DIR = Path("boltz-experiments")
METADATA_FILE_NAME = ".boltz-run.json"

_ADJECTIVES = (
    "amber",
    "brisk",
    "calm",
    "clear",
    "keen",
    "lively",
    "lucid",
    "quiet",
    "rapid",
    "steady",
)
_NOUNS = (
    "atom",
    "binder",
    "cluster",
    "enzyme",
    "helix",
    "ligand",
    "motif",
    "pocket",
    "sample",
    "target",
)
_VERBS = (
    "aligns",
    "builds",
    "checks",
    "drifts",
    "folds",
    "guides",
    "mixes",
    "screens",
    "shifts",
    "tracks",
)
_AUTO_NAME_SUFFIX_NBYTES = 3


def resolve_root_dir(root_dir: str | PathLike[str] | None = None) -> Path:
    path = Path(root_dir) if root_dir is not None else DEFAULT_ROOT_DIR
    return _resolve_path(path)


def resolve_existing_run_dir(
    *,
    run_dir: str | PathLike[str] | None,
    name: str | None,
    root_dir: str | PathLike[str] | None,
) -> Path:
    if (run_dir is None) == (name is None):
        raise ValueError("Exactly one of `run_dir` or `name` must be provided")

    if run_dir is not None:
        if root_dir is not None:
            raise ValueError("`root_dir` cannot be provided when `run_dir` is used")
        path = _resolve_path(Path(run_dir))
    else:
        assert name is not None
        path = resolve_root_dir(root_dir) / validate_name(name)

    if not path.exists():
        raise ExperimentError(f"Run directory does not exist: {path}")
    if not path.is_dir():
        raise ExperimentError(f"Run path is not a directory: {path}")
    return path


def resolve_create_run_dir(root_dir: str | PathLike[str], name: str | None, *, run_id: str | None = None) -> Path:
    root_path = resolve_root_dir(root_dir)
    root_path.mkdir(parents=True, exist_ok=True)

    if name is not None:
        return root_path / validate_name(name)

    if run_id is not None:
        return root_path / deterministic_name(run_id)

    for _ in range(256):
        candidate = root_path / generate_name()
        if not candidate.exists():
            return candidate

    raise ExperimentError(f"Unable to generate a unique run directory under {root_path}")


def metadata_path(run_dir: Path) -> Path:
    return run_dir / METADATA_FILE_NAME


def validate_name(name: str) -> str:
    stripped = name.strip()
    if not stripped:
        raise ValueError("`name` must not be empty")
    if stripped in {".", ".."}:
        raise ValueError("`name` must not be '.' or '..'")
    if Path(stripped).name != stripped:
        raise ValueError("`name` must be a single directory name, not a path")
    return stripped


def generate_name() -> str:
    return "-".join(
        (
            secrets.choice(_ADJECTIVES),
            secrets.choice(_NOUNS),
            secrets.choice(_VERBS),
            secrets.token_hex(_AUTO_NAME_SUFFIX_NBYTES),
        )
    )


def deterministic_name(run_id: str) -> str:
    digest = hashlib.sha256(run_id.strip().encode("utf-8")).digest()
    return "-".join(
        (
            _deterministic_word(_ADJECTIVES, digest[0]),
            _deterministic_word(_NOUNS, digest[1]),
            _deterministic_word(_VERBS, digest[2]),
            digest[3:6].hex(),
        )
    )


def _deterministic_word(values: tuple[str, ...], seed: int) -> str:
    if not values:
        return "run"
    return values[seed % len(values)]


def _resolve_path(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_absolute():
        return expanded
    return (Path.cwd() / expanded).resolve()

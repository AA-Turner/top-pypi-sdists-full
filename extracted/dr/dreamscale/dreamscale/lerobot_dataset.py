"""A local LeRobot dataset (v2.0, v2.1 or v3.0), read for `dreamscale datasets upload ./folder`.

The summary comes from ``meta/info.json`` read through the run's data mapping (the columns it
trains on); the hardware check reads each episode's state, action (each its mapped columns
joined in order), timestamps and frame indices from the Parquet tables under ``data/`` (no
video is decoded). Every layout carries an ``episode_index`` column, so one reader serves all:
v2.x ``data/chunk-000/episode_000000.parquet``, v3.0 ``data/chunk-000/file-000.parquet``.
Reading Parquet needs pyarrow (the ``train`` extra).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from dreamscale_transport.training_data import (
    CheckReport,
    DatasetError,
    DatasetSummary,
    check_dataset,
    column_values,
    diagnose_layout,
    needs_stats,
    repair_info,
    summarize_folders,
    valid_upload_path,
)

from dreamscale import errors

# What an upload of a dataset sends: LeRobot's own folders, nothing hidden (.git, .cache).
UPLOAD_DIRS = ("meta", "data", "videos")
MAX_FILES = 20_000
MAX_BYTES = 500 * 10**9
_INDEX = ("episode_index", "frame_index", "timestamp")


@dataclass(frozen=True)
class LocalDataset:
    root: Path
    # meta/info.json by folder: {"": info} for one dataset; one per folder of recording
    # sessions (the summary says which combine).
    infos: dict[str, Any]
    summary: DatasetSummary
    files: tuple[tuple[str, int], ...]  # (path relative to root, size), sorted

    @property
    def folders(self) -> tuple[str, ...]:
        """The dataset folders trained on ("" for the root's one dataset)."""
        return self.summary.folders or ("",)

    @property
    def bytes(self) -> int:
        return sum(size for _, size in self.files)


def dataset_error(error: DatasetError, where: str) -> errors.DreamscaleError:
    return errors.DreamscaleError(
        errors.ErrorInfo(code=error.code, problem=error.message, cause=where, fix=error.fix)
    )


def _invalid(problem: str, fix: str, where: str) -> errors.DreamscaleError:
    return errors.DreamscaleError(
        errors.ErrorInfo(code="not_lerobot", problem=problem, cause=where, fix=fix)
    )


def _info(path: Path) -> Any:
    """A meta/info.json; one whose totals LeRobot never wrote reads them (and the cameras it
    recorded) from meta/stats.json beside it."""
    try:
        info = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    if needs_stats(info):
        try:
            info = repair_info(info, json.loads((path.parent / "stats.json").read_text()))
        except (OSError, ValueError):
            pass
    return info


def open_dataset(root: str | Path, mapping: dict | None = None) -> LocalDataset:
    """Summarize a dataset folder (through ``mapping``: any columns chosen), or a folder of
    datasets (recording sessions) combined, and list the files an upload would send."""
    root = Path(root).expanduser()
    where = f"read from {root}"
    if (root / "meta" / "info.json").is_file():
        infos = {"": _info(root / "meta" / "info.json")}
    else:
        layout = _layout(root)
        folders = sorted(
            p.removesuffix("/meta/info.json") for p in layout if p.endswith("/meta/info.json")
        )
        if not folders:
            raise dataset_error(diagnose_layout(layout, str(root)), where)
        infos = {f: _info(root / f / "meta" / "info.json") for f in folders}
    # Each folder's files (to see a recording LeRobot never finished) when combining.
    files_of = None if list(infos) == [""] else {
        f: [
            p.relative_to(root / f).as_posix()
            for d in UPLOAD_DIRS
            for p in (root / f / d).rglob("*")
            if p.is_file()
        ]
        for f in infos
    }
    # Before a base is chosen: what some family trains (the server reads the run's family's).
    from dreamscale_transport.training_families import widest_envelope

    try:
        summary = summarize_folders(infos, mapping, str(root), files_of,
                                    envelope=widest_envelope())
    except DatasetError as error:
        raise dataset_error(error, where) from None
    files = []
    bases = [root / f if f else root for f in summary.folders or ("",)]
    for path in sorted(p for base in bases for d in UPLOAD_DIRS for p in (base / d).rglob("*")):
        rel = path.relative_to(root)
        if not any(part.startswith(".") for part in rel.parts) and path.is_file():
            files.append((rel.as_posix(), path.stat().st_size))
    unsupported = next((name for name, _ in files if not valid_upload_path(name)), None)
    if unsupported is not None:
        raise _invalid(
            f"{unsupported} has a name an upload can't carry",
            "rename it with letters, digits and ._-+=@,() only, or push the dataset to "
            "Hugging Face and train from hf://owner/name",
            where,
        )
    if len(files) > MAX_FILES or sum(size for _, size in files) > MAX_BYTES:
        raise _invalid(
            f"{root} is too large to upload ({len(files):,} files)",
            f"upload at most {MAX_FILES:,} files and {MAX_BYTES // 10**9} GB: push it to "
            "Hugging Face and train from hf://owner/name",
            where,
        )
    return LocalDataset(root, infos, summary, tuple(files))


@dataclass(frozen=True)
class UploadFolder:
    """What an upload sends. ``summary`` is None when the folder's columns need picking: it
    stores and lists all the same, and the run names its columns."""

    root: Path
    infos: dict[str, Any]
    summary: DatasetSummary | None
    files: tuple[tuple[str, int], ...]
    local: LocalDataset | None

    @property
    def bytes(self) -> int:
        return sum(size for _, size in self.files)


def open_upload(root: str | Path) -> UploadFolder:
    """A folder to upload: every LeRobot dataset in it, whatever its columns."""
    root = Path(root).expanduser()
    where = f"read from {root}"
    if not root.is_dir():
        raise _invalid(f"{root} is not a folder", "point at the LeRobot dataset's root folder",
                       where)
    try:
        local = open_dataset(root)
        return UploadFolder(root, local.infos, local.summary, local.files, local)
    except errors.DreamscaleError as error:
        layout = _layout(root)
        folders = [""] if (root / "meta" / "info.json").is_file() else sorted(
            p.removesuffix("/meta/info.json") for p in layout if p.endswith("/meta/info.json")
        )
        readable = error.code in ("mapping_required", "ambiguous_columns") or bool(folders)
        if not folders or not readable or error.code in ("invalid_dataset", "too_large"):
            raise
        infos = {f: _info(root / f / "meta" / "info.json") for f in folders}
    files = []
    for base in (root / f if f else root for f in folders):
        for path in sorted(p for d in UPLOAD_DIRS for p in (base / d).rglob("*")):
            rel = path.relative_to(root)
            if not any(part.startswith(".") for part in rel.parts) and path.is_file():
                files.append((rel.as_posix(), path.stat().st_size))
    return UploadFolder(root, infos, None, tuple(files), None)


def _layout(root: Path, depth: int = 4, limit: int = 5000) -> list[str]:
    """What a folder holds, for ``diagnose_layout``: its paths to ``depth`` levels (folders end
    in "/"; hidden ones skipped) and the dataset folders below it (``<folder>/meta/info.json``)."""
    paths: list[str] = []
    queue = [root]
    while queue and len(paths) < limit:
        folder = queue.pop(0)
        try:
            children = sorted(folder.iterdir())
        except OSError:
            continue
        for child in children:
            if child.name.startswith("."):
                continue
            rel = child.relative_to(root).as_posix()
            if child.is_dir():
                paths.append(rel + "/")
                if (child / "meta" / "info.json").is_file():
                    paths.append(f"{rel}/meta/info.json")
                elif rel.count("/") < depth - 1:
                    queue.append(child)
            else:
                paths.append(rel)
    return paths


def _matrix(column, name: str, where: str) -> np.ndarray:
    import pyarrow as pa

    array = column.combine_chunks()
    if pa.types.is_list(array.type) or pa.types.is_large_list(array.type) or (
        pa.types.is_fixed_size_list(array.type)
    ):
        values = np.asarray(array.flatten().to_numpy(zero_copy_only=False), np.float64)
    else:
        values = np.asarray(array.to_numpy(zero_copy_only=False), np.float64)
    if array.null_count or not len(array) or values.size % len(array):
        raise _invalid(
            f"{name} isn't one vector per frame",
            f"record {name} as a float vector of the same width in every frame",
            where,
        )
    return values.reshape(len(array), -1)


def _joined(table, entries: tuple[str, ...], info: Any, where: str) -> np.ndarray:
    """The mapped columns side by side, each cut to the values its entry keeps."""
    parts = []
    for entry in entries:
        column, kept = column_values(info, entry)
        values = _matrix(table.column(column), column, where)
        parts.append(values if kept is None else values[:, kept])
    return np.ascontiguousarray(np.concatenate(parts, axis=1))


def read_episodes(dataset: LocalDataset) -> dict[int, dict[str, np.ndarray]]:
    """Every episode's timestamps, frame indices, state and action, in frame order; datasets
    combined from folders are numbered across them."""
    try:
        import pyarrow.parquet as pq  # noqa: F401
    except ImportError:
        raise errors.catalog("train_not_installed") from None
    episodes: dict[int, dict[str, np.ndarray]] = {}
    offset = 0
    for folder in dataset.folders:
        found = _read_folder(
            dataset.root / folder if folder else dataset.root, dataset, dataset.infos[folder]
        )
        episodes.update({offset + e: data for e, data in found.items()})
        offset += max(found, default=-1) + 1
    return episodes


def _read_folder(
    root: Path, dataset: LocalDataset, info: Any
) -> dict[int, dict[str, np.ndarray]]:
    import pyarrow.parquet as pq

    tables = sorted((root / "data").rglob("*.parquet"))
    where = f"read from {root / 'data'}"
    if not tables:
        raise _invalid(
            "the dataset has no data/*.parquet tables",
            "point at the LeRobot dataset's root folder (it holds meta/ and data/)",
            where,
        )
    mapping = dataset.summary.mapping
    wanted = list(
        dict.fromkeys(
            [*_INDEX, *(column_values(info, e)[0] for e in (*mapping.state, *mapping.action))]
        )
    )
    parts: dict[int, list[dict[str, np.ndarray]]] = {}
    for path in tables:
        try:
            table = pq.read_table(path, columns=wanted)
        except (OSError, ValueError, KeyError) as error:
            raise _invalid(
                f"{path.relative_to(root)} isn't a LeRobot data table ({error})",
                "record with LeRobot (v2.x or v3.0), or convert the dataset with its converter",
                where,
            ) from None
        if not table.num_rows:
            continue
        columns = {
            "episode": np.asarray(table.column("episode_index").to_numpy(), np.int64),
            "frame_index": np.asarray(table.column("frame_index").to_numpy(), np.int64),
            "timestamp": np.asarray(table.column("timestamp").to_numpy(), np.float64),
            "state": _joined(table, mapping.state, info, where),
            "action": _joined(table, mapping.action, info, where),
        }
        starts = np.flatnonzero(np.diff(columns["episode"])) + 1
        for chunk in np.split(np.arange(table.num_rows), starts):
            episode = int(columns["episode"][chunk[0]])
            parts.setdefault(episode, []).append(
                {key: value[chunk] for key, value in columns.items() if key != "episode"}
            )
    episodes = {}
    for episode, chunks in parts.items():
        merged = {key: np.concatenate([c[key] for c in chunks]) for key in chunks[0]}
        order = np.argsort(merged["frame_index"], kind="stable")
        episodes[episode] = {key: value[order] for key, value in merged.items()}
    return episodes


def hardware_check(dataset: LocalDataset, *, trim_idle: bool = True) -> CheckReport:
    """The hardware check, here, before anything is uploaded (the server runs it again)."""
    return check_dataset(
        read_episodes(dataset), fps=dataset.summary.fps, trim_idle=trim_idle
    )

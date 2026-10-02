from __future__ import annotations

import json
from typing import Any, cast
from pathlib import Path
from datetime import date, datetime
from collections.abc import Mapping, Sequence

from ._errors import ExperimentError
from ._materialize import SUPPORTED_ARCHIVE_SUFFIXES, preferred_structure_artifact_paths


def write_run_metadata(*, run_dir: Path, response: Any) -> None:
    data = _jsonable(response)
    if not isinstance(data, dict):
        raise ExperimentError("Unable to serialize run metadata")

    _write_json(run_dir / "run.json", _strip_presigned_urls(cast(dict[str, Any], data)))


def write_pipeline_result_metadata(
    *,
    run_dir: Path,
    result: Any,
) -> None:
    result_id = _result_id(result)
    result_dir = run_dir / "results" / result_id
    metadata = _result_metadata(result)

    _write_json(result_dir / "metadata.json", metadata)
    _append_index_entry(
        run_dir=run_dir,
        entry=_manifest_entry(run_dir=run_dir, result_dir=result_dir, metadata=metadata, fallback_id=result_id),
        fallback_id=result_id,
    )


def append_pipeline_result_metadata(
    *,
    run_dir: Path,
    result: Any,
) -> None:
    result_id = _result_id(result)
    _append_index_entry(run_dir=run_dir, entry=_result_metadata(result), fallback_id=result_id)


def _result_metadata(result: Any) -> dict[str, Any]:
    data = _jsonable(result)
    if not isinstance(data, dict):
        raise ExperimentError(f"Unable to serialize metadata for result {_result_id(result)}")

    metadata = cast(dict[str, Any], data)
    metadata.pop("artifacts", None)
    metadata.setdefault("id", _result_id(result))
    return metadata


def _result_id(result: Any) -> str:
    result_id = getattr(result, "id", None)
    if not isinstance(result_id, str):
        raise ExperimentError("Result is missing an ID")
    return result_id


def _local_paths(*, run_dir: Path, result_dir: Path) -> dict[str, str]:
    paths: dict[str, str] = {}

    archive_path = _find_archive(result_dir)
    if archive_path is not None:
        paths["archive"] = _relative_path(run_dir, archive_path)

    extracted_dir = result_dir / "files"
    if not extracted_dir.is_dir():
        return paths

    paths["files"] = _relative_path(run_dir, extracted_dir)

    metrics_path = _find_extracted_file(extracted_dir, "metrics.json", ("result/metrics.json", "metrics.json"))
    if metrics_path is not None:
        paths["metrics"] = _relative_path(run_dir, metrics_path)

    structure_path = _find_extracted_file(
        extracted_dir,
        "predicted_structure.cif",
        preferred_structure_artifact_paths(result_dir.name),
    )
    if structure_path is not None:
        paths["structure"] = _relative_path(run_dir, structure_path)

    pae_path = _find_extracted_file(extracted_dir, "pae.npz", ("result/pae.npz", "pae.npz"))
    if pae_path is not None:
        paths["pae"] = _relative_path(run_dir, pae_path)

    return paths


def _find_archive(result_dir: Path) -> Path | None:
    for suffix in SUPPORTED_ARCHIVE_SUFFIXES:
        candidate = result_dir / f"archive{suffix}"
        if candidate.is_file():
            return candidate
    return None


def _find_extracted_file(extracted_dir: Path, name: str, preferred_paths: tuple[str, ...]) -> Path | None:
    for preferred_path in preferred_paths:
        candidate = extracted_dir / preferred_path
        if candidate.is_file():
            return candidate

    matches = sorted(path for path in extracted_dir.rglob("*") if path.is_file() and _matches_artifact(path, name))
    return matches[0] if matches else None


def _matches_artifact(path: Path, name: str) -> bool:
    basename = path.name.lower()
    if name == "predicted_structure.cif":
        return basename == "predicted_structure.cif" or basename.endswith(".cif") or basename.endswith(".pdb")
    return basename == name


def _relative_path(run_dir: Path, path: Path) -> str:
    return path.relative_to(run_dir).as_posix()


def _manifest_entry(
    *,
    run_dir: Path,
    result_dir: Path,
    metadata: dict[str, Any],
    fallback_id: str,
) -> dict[str, Any]:
    entry = dict(metadata)
    entry.setdefault("id", fallback_id)
    paths = _local_paths(run_dir=run_dir, result_dir=result_dir)
    if paths:
        entry["paths"] = paths
    return entry


def _append_index_entry(*, run_dir: Path, entry: dict[str, Any], fallback_id: str) -> None:
    index_path = run_dir / "results" / "index.jsonl"
    result_id = str(entry.get("id", fallback_id))
    if result_id in _read_index_ids(index_path):
        return

    index_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_entry = dict(entry)
    manifest_entry.setdefault("id", fallback_id)
    with index_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(manifest_entry, separators=(",", ":")) + "\n")


def _read_index_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()

    ids: set[str] = set()
    with path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            loaded = json.loads(line)
            if isinstance(loaded, dict) and "id" in loaded:
                entry = cast(dict[str, Any], loaded)
                ids.add(str(entry["id"]))
    return ids


def _write_json(path: Path, data: dict[str, Any]) -> None:
    _write_text(path, json.dumps(data, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(f"{path.suffix}.tmp")
    tmp_path.write_text(text, encoding="utf-8")
    tmp_path.replace(path)


def _strip_presigned_urls(value: Any) -> Any:
    if isinstance(value, Mapping):
        data: dict[str, Any] = {}
        mapping = cast(Mapping[object, Any], value)
        for key, item in mapping.items():
            if key in {"url", "url_expires_at"}:
                continue
            stripped = _strip_presigned_urls(item)
            if isinstance(stripped, dict) and not stripped:
                continue
            data[str(key)] = stripped
        return data
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_strip_presigned_urls(item) for item in cast(Sequence[Any], value)]
    return value


def _jsonable(value: Any) -> Any:
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        try:
            return _jsonable(to_dict(mode="json", use_api_names=True, exclude_unset=True))
        except TypeError:
            pass

    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Mapping):
        mapping = cast(Mapping[object, Any], value)
        return {str(key): _jsonable(item) for key, item in mapping.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_jsonable(item) for item in cast(Sequence[Any], value)]
    if hasattr(value, "__dict__"):
        attrs = vars(value)
        return {key: _jsonable(item) for key, item in attrs.items() if not key.startswith("_")}
    return value
